# distribution_center.py
# 配送中心功能实现

import simpy
import numpy as np
from .uav_classes import calculate_distance

class Truck:
    """卡车类"""
    
    def __init__(self, env, truck_id, base_latitude, base_longitude, 
                 speed=50, capacity=5):
        self.env = env
        self.truck_id = truck_id
        self.base_latitude = base_latitude
        self.base_longitude = base_longitude
        self.current_latitude = base_latitude
        self.current_longitude = base_longitude
        self.speed = speed
        self.capacity = capacity
        self.busy = False
        
        # 统计信息
        self.total_trips = 0
        self.total_distance = 0
        self.total_goods_delivered = 0

    def scheduled_delivery_trip(self, service_points, goods_to_deliver, schedule_interval):
        """按固定时间表执行配送"""
        while True:
            # 等待调度时间
            yield self.env.timeout(schedule_interval)
            
            if len(goods_to_deliver) > 0:
                self.busy = True
                print(f"卡车 {self.truck_id} 开始配送任务 在 {self.env.now:.2f}")
                
                # 装载货物（最多装载容量限制）
                current_load = []
                destinations = set()
                
                for _ in range(min(self.capacity, len(goods_to_deliver))):
                    if len(goods_to_deliver) > 0:
                        goods = goods_to_deliver.pop(0)
                        current_load.append(goods)
                        destinations.add(goods.destination_id)
                
                if current_load:
                    # 执行配送
                    yield self.env.process(self.deliver_goods(current_load, service_points))
                
                self.busy = False

    def deliver_goods(self, goods_list, service_points):
        """执行货物配送"""
        if not goods_list:
            return
        
        print(f"卡车 {self.truck_id} 开始配送 {len(goods_list)} 件货物")
        
        # 获取所有目的地
        destinations = list(set(goods.destination_id for goods in goods_list))
        
        total_distance = 0
        
        for dest_id in destinations:
            # 找到目的地服务点
            service_point = next((sp for sp in service_points if sp['id'] == dest_id), None)
            if service_point:
                dest_lat = service_point['latitude']
                dest_lon = service_point['longitude']
                
                # 计算行驶距离和时间
                distance = calculate_distance(self.current_latitude, self.current_longitude,
                                            dest_lat, dest_lon)
                travel_time = distance / self.speed
                
                # 行驶到目的地
                yield self.env.timeout(travel_time)
                
                # 更新位置
                self.current_latitude = dest_lat
                self.current_longitude = dest_lon
                total_distance += distance
                
                # 卸货时间
                goods_for_this_dest = [g for g in goods_list if g.destination_id == dest_id]
                unload_time = len(goods_for_this_dest) * 0.1  # 每件货物0.1时间单位
                yield self.env.timeout(unload_time)
                
                self.total_goods_delivered += len(goods_for_this_dest)
                
                print(f"卡车 {self.truck_id} 在服务点 {dest_id} 卸货 {len(goods_for_this_dest)} 件")
        
        # 返回配送中心
        return_distance = calculate_distance(self.current_latitude, self.current_longitude,
                                           self.base_latitude, self.base_longitude)
        return_time = return_distance / self.speed
        yield self.env.timeout(return_time)
        
        # 重置位置
        self.current_latitude = self.base_latitude
        self.current_longitude = self.base_longitude
        total_distance += return_distance
        
        # 更新统计
        self.total_distance += total_distance
        self.total_trips += 1
        
        print(f"卡车 {self.truck_id} 返回配送中心，总行程: {total_distance:.2f}")

    def get_statistics(self):
        """获取卡车统计信息"""
        return {
            'truck_id': self.truck_id,
            'total_trips': self.total_trips,
            'total_distance': self.total_distance,
            'total_goods_delivered': self.total_goods_delivered,
            'avg_distance_per_trip': self.total_distance / max(1, self.total_trips),
            'busy': self.busy
        }


class DistributionCenter:
    """
    配送中心类
    不提供无人机充电服务
    部署卡车按固定时间往返服务点
    无人机投放货物后等待卡车返回
    """
    
    def __init__(self, env, center_id, latitude, longitude, 
                 truck_count=2, truck_capacity=5, truck_speed=50,
                 schedule_interval=4.0, processing_time=0.5):
        self.env = env
        self.center_id = center_id
        self.latitude = latitude
        self.longitude = longitude
        self.truck_count = truck_count
        self.schedule_interval = schedule_interval  # 卡车固定往返时间间隔
        self.processing_time = processing_time
        
        # 创建卡车队列
        self.trucks = []
        for i in range(truck_count):
            truck = Truck(env, f"{center_id}_truck_{i}", latitude, longitude,
                         speed=truck_speed, capacity=truck_capacity)
            self.trucks.append(truck)
        
        # 货物管理
        self.received_goods = []  # 收到的货物
        self.processed_goods = []  # 处理好的货物，等待配送
        self.waiting_uavs = []   # 等待货物返回的无人机
        
        # 统计信息
        self.total_goods_received = 0
        self.total_goods_processed = 0
        self.total_uavs_served = 0
        
        # 启动处理进程
        self.env.process(self.goods_processing())
        
        # 启动卡车调度进程
        for truck in self.trucks:
            self.env.process(truck.scheduled_delivery_trip([], self.processed_goods, self.schedule_interval))

    def receive_goods_from_uav(self, uav, goods):
        """接收无人机投放的货物"""
        print(f"配送中心 {self.center_id} 接收来自 UAV {uav.uav_id} 的货物 在 {self.env.now:.2f}")
        
        # 设置货物目的地
        if hasattr(uav, 'current_order') and uav.current_order:
            goods.destination_id = uav.current_order.service_point_id
        else:
            goods.destination_id = np.random.randint(0, 10)  # 随机目的地
        
        goods.arrival_time = self.env.now
        self.received_goods.append(goods)
        self.total_goods_received += 1
        
        # 无人机等待货物返回
        uav.waiting_for_return = True
        self.waiting_uavs.append(uav)
        self.total_uavs_served += 1
        
        return True

    def goods_processing(self):
        """货物处理进程"""
        while True:
            if len(self.received_goods) > 0:
                goods = self.received_goods.pop(0)
                
                # 处理时间
                processing_time = np.random.exponential(scale=self.processing_time)
                yield self.env.timeout(processing_time)
                
                # 处理完成，加入配送队列
                self.processed_goods.append(goods)
                self.total_goods_processed += 1
                
                print(f"配送中心 {self.center_id} 处理完货物，加入配送队列")
                
                # 模拟卡车往返后货物返回给无人机
                # 简化处理：等待一个调度周期后货物返回
                self.env.process(self.return_goods_to_uav(goods))
                
            else:
                yield self.env.timeout(0.5)  # 等待新货物

    def return_goods_to_uav(self, goods):
        """模拟货物通过卡车配送并返回给无人机"""
        # 等待卡车往返时间（简化模型）
        return_time = self.schedule_interval * 2  # 往返时间
        yield self.env.timeout(return_time)
        
        # 货物返回，通知等待的无人机
        if len(self.waiting_uavs) > 0:
            uav = self.waiting_uavs.pop(0)
            uav.waiting_for_return = False
            print(f"配送中心 {self.center_id} 货物配送完成，UAV {uav.uav_id} 可以返回")

    def start_truck_schedules(self, service_points):
        """启动卡车调度（需要服务点信息）"""
        for truck in self.trucks:
            self.env.process(truck.scheduled_delivery_trip(
                service_points, self.processed_goods, self.schedule_interval))

    def get_statistics(self):
        """获取配送中心统计信息"""
        truck_stats = [truck.get_statistics() for truck in self.trucks]
        
        return {
            'center_id': self.center_id,
            'total_goods_received': self.total_goods_received,
            'total_goods_processed': self.total_goods_processed,
            'total_uavs_served': self.total_uavs_served,
            'current_received_goods': len(self.received_goods),
            'current_processed_goods': len(self.processed_goods),
            'current_waiting_uavs': len(self.waiting_uavs),
            'truck_count': self.truck_count,
            'truck_statistics': truck_stats,
            'schedule_interval': self.schedule_interval
        }


def test_distribution_center():
    """测试配送中心功能"""
    print("=== 配送中心功能测试 ===")
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 创建配送中心
    dc = DistributionCenter(
        env, 0, 30, 30,
        truck_count=2,
        truck_capacity=4,
        truck_speed=50,
        schedule_interval=3.0,
        processing_time=0.4
    )
    
    # 创建测试服务点
    service_points = [
        {'id': 0, 'latitude': 10, 'longitude': 10},
        {'id': 1, 'latitude': 50, 'longitude': 10},
        {'id': 2, 'latitude': 10, 'longitude': 50},
        {'id': 3, 'latitude': 50, 'longitude': 50}
    ]
    
    # 启动卡车调度
    dc.start_truck_schedules(service_points)
    
    # 创建测试无人机和货物投放
    from .uav_classes import UAV, Goods
    
    def goods_delivery_process():
        for i in range(10):
            yield env.timeout(i * 1.2)  # 每1.2时间单位一个货物
            
            # 创建无人机和货物
            uav = UAV(env, f"delivery_uav_{i}", 30, 30)
            goods = Goods(env, f"goods_{i}", weight=1.0)
            
            # 模拟订单
            class MockOrder:
                def __init__(self, service_point_id):
                    self.service_point_id = service_point_id
            
            uav.current_order = MockOrder(i % len(service_points))
            
            # 无人机投放货物
            dc.receive_goods_from_uav(uav, goods)
    
    env.process(goods_delivery_process())
    
    # 运行测试
    print("开始仿真...")
    env.run(until=25)
    
    # 输出结果
    print("\n=== 配送中心统计结果 ===")
    stats = dc.get_statistics()
    
    print(f"配送中心ID: {stats['center_id']}")
    print(f"接收货物总数: {stats['total_goods_received']}")
    print(f"处理货物总数: {stats['total_goods_processed']}")
    print(f"服务无人机总数: {stats['total_uavs_served']}")
    print(f"当前待处理货物: {stats['current_received_goods']}")
    print(f"当前待配送货物: {stats['current_processed_goods']}")
    print(f"当前等待无人机: {stats['current_waiting_uavs']}")
    print(f"调度间隔: {stats['schedule_interval']}")
    
    print(f"\n=== 卡车统计 ===")
    for truck_stat in stats['truck_statistics']:
        print(f"卡车 {truck_stat['truck_id']}:")
        print(f"  总行程数: {truck_stat['total_trips']}")
        print(f"  总距离: {truck_stat['total_distance']:.2f}")
        print(f"  配送货物总数: {truck_stat['total_goods_delivered']}")
        print(f"  平均每次行程距离: {truck_stat['avg_distance_per_trip']:.2f}")
    
    print("\n配送中心测试完成！")


if __name__ == "__main__":
    test_distribution_center()
