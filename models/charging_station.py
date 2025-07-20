# charging_station.py
# 充电站功能实现

import simpy
import numpy as np
from .uav_classes import calculate_distance

class ChargingStation:
    """
    充电站类
    支持有限和无限电池容量
    多个服务窗口(N)
    固定服务时间
    """
    
    def __init__(self, env, station_id, latitude, longitude, 
                 battery_type='limited', battery_capacity=50, 
                 service_windows=3, service_time=0.5, charge_time=2.0):
        self.env = env
        self.station_id = station_id
        self.latitude = latitude
        self.longitude = longitude
        self.battery_type = battery_type  # 'limited' or 'unlimited'
        self.service_time = service_time  # 固定服务时间
        self.charge_time = charge_time    # 电池充电时间
        
        # 电池管理
        if battery_type == 'limited':
            self.battery_capacity = battery_capacity
            self.available_batteries = battery_capacity
            self.charging_batteries = 0
            self.used_batteries = []  # 用过的电池队列
        else:
            self.battery_capacity = float('inf')
            self.available_batteries = float('inf')
        
        # 服务窗口管理
        self.service_windows = service_windows
        self.window_busy = [False] * service_windows
        self.queues = [[] for _ in range(service_windows)]  # 每个窗口一个队列
        
        # 统计信息
        self.total_served = 0
        self.total_waiting_time = 0
        self.queue_lengths_history = []
        
        # 启动充电进程（仅限有限电池类型）
        if battery_type == 'limited':
            self.env.process(self.battery_charging_process())
        
        # 启动服务进程
        for i in range(service_windows):
            self.env.process(self.service_window_process(i))
        
        # 启动统计收集进程
        self.env.process(self.statistics_collection_process())

    def battery_charging_process(self):
        """Battery charging process (for limited battery type only)"""
        while True:
            # Check if charging is needed and possible
            should_charge = (
                len(self.used_batteries) > 0 and 
                self.charging_batteries < min(5, self.battery_capacity // 4) and 
                self.available_batteries < self.battery_capacity
            )
            
            if should_charge:
                # Start charging a used battery
                battery = self.used_batteries.pop(0)
                self.charging_batteries += 1
                
                print(f"Charging Station {self.station_id}: Starting battery charge, charging batteries: {self.charging_batteries}")
                
                # Charging time with reasonable bounds
                charge_time = max(0.5, min(5.0, np.random.exponential(scale=self.charge_time)))
                yield self.env.timeout(charge_time)
                
                # Charging completed
                self.charging_batteries -= 1
                self.available_batteries += 1
                
                print(f"Charging Station {self.station_id}: Battery charging completed, available batteries: {self.available_batteries}")
                
            else:
                # No batteries to charge or charging slots full, wait appropriately
                if len(self.used_batteries) == 0:
                    # No used batteries, wait longer
                    yield self.env.timeout(10.0)
                elif self.available_batteries >= self.battery_capacity:
                    # At capacity, wait for batteries to be used
                    yield self.env.timeout(5.0)
                else:
                    # Charging slots full, wait shorter time
                    yield self.env.timeout(2.0)

    def service_window_process(self, window_id):
        """服务窗口进程"""
        while True:
            if len(self.queues[window_id]) > 0 and not self.window_busy[window_id]:
                # 检查是否有可用电池
                if self.available_batteries > 0:
                    # 开始服务
                    self.window_busy[window_id] = True
                    uav = self.queues[window_id].pop(0)
                    
                    # 记录等待时间
                    waiting_time = self.env.now - uav.arrival_time
                    self.total_waiting_time += waiting_time
                    self.total_served += 1
                    
                    print(f"Charging Station {self.station_id} Window {window_id} starting battery replacement for UAV {uav.uav_id} "
                          f"at {self.env.now:.2f}, waiting time: {waiting_time:.2f}")
                    
                    # 固定服务时间
                    yield self.env.timeout(self.service_time)
                    
                    # 换电池
                    if self.battery_type == 'limited':
                        # 有限电池：换下用过的电池，给新电池
                        # 只有在不超过总容量时才添加用过的电池
                        total_batteries = self.available_batteries + self.charging_batteries + len(self.used_batteries)
                        if total_batteries < self.battery_capacity:
                            self.used_batteries.append('used_battery')
                        self.available_batteries -= 1
                    
                    # 无人机电池充满
                    uav.current_battery = uav.battery_capacity
                    uav.ifcharge = False
                    uav.charging_complete_time = self.env.now
                    
                    print(f"Charging Station {self.station_id} Window {window_id} completed battery replacement for UAV {uav.uav_id}")
                    
                    self.window_busy[window_id] = False
                else:
                    # 没有可用电池，等待
                    yield self.env.timeout(0.1)
            else:
                yield self.env.timeout(0.1)

    def add_to_queue(self, uav):
        """将无人机加入最短队列"""
        # 找到最短的队列
        min_queue_length = min(len(queue) for queue in self.queues)
        for i, queue in enumerate(self.queues):
            if len(queue) == min_queue_length:
                uav.arrival_time = self.env.now
                uav.ifcharge = True
                queue.append(uav)
                print(f"UAV {uav.uav_id} joined Charging Station {self.station_id} Window {i} queue")
                return True
        return False

    def serve_uav(self, uav):
        """为无人机提供换电服务"""
        self.add_to_queue(uav)
        
        # 等待充电完成
        while uav.ifcharge:
            yield self.env.timeout(0.1)
        
        print(f"UAV {uav.uav_id} completed battery replacement at Charging Station {self.station_id}")

    def statistics_collection_process(self):
        """统计信息收集进程"""
        while True:
            # 记录当前队列长度
            total_queue_length = sum(len(queue) for queue in self.queues)
            self.queue_lengths_history.append(total_queue_length)
            
            yield self.env.timeout(1.0)  # 每时间单位收集一次

    def get_statistics(self):
        """获取充电站统计信息"""
        avg_waiting_time = self.total_waiting_time / max(1, self.total_served)
        avg_queue_length = np.mean(self.queue_lengths_history) if self.queue_lengths_history else 0
        current_queue_length = sum(len(queue) for queue in self.queues)
        
        return {
            'station_id': self.station_id,
            'battery_type': self.battery_type,
            'total_served': self.total_served,
            'avg_waiting_time': avg_waiting_time,
            'avg_queue_length': avg_queue_length,
            'current_queue_length': current_queue_length,
            'available_batteries': self.available_batteries if self.battery_type == 'limited' else 'unlimited',
            'charging_batteries': self.charging_batteries if self.battery_type == 'limited' else 0,
            'service_windows': self.service_windows,
            'window_utilization': [not busy for busy in self.window_busy].count(False) / self.service_windows
        }


def test_charging_station():
    """Test charging station functionality"""
    print("=== Charging Station Functionality Test ===")
    
    # Create simulation environment
    env = simpy.Environment()
    
    # Test limited battery charging station
    limited_station = ChargingStation(
        env, 0, 50, 50, 
        battery_type='limited', 
        battery_capacity=10,
        service_windows=3,
        service_time=0.5,
        charge_time=2.0
    )
    
    # Test unlimited battery charging station
    unlimited_station = ChargingStation(
        env, 1, 60, 60,
        battery_type='unlimited',
        service_windows=2,
        service_time=0.3
    )
    
    # Create test UAVs
    from .uav_classes import UAV
    
    test_uavs = []
    for i in range(8):
        uav = UAV(env, f"test_uav_{i}", 50, 50, speed=30)
        uav.current_battery = 20  # Set low battery level
        test_uavs.append(uav)
    
    # UAV arrival process
    def uav_arrival_process():
        for i, uav in enumerate(test_uavs):
            yield env.timeout(i * 0.8)  # One UAV arrives every 0.8 time units
            
            # First 4 go to limited battery station, last 4 go to unlimited battery station
            if i < 4:
                env.process(limited_station.serve_uav(uav))
            else:
                env.process(unlimited_station.serve_uav(uav))
    
    env.process(uav_arrival_process())
    
    # Run test
    print("Starting simulation...")
    env.run(until=20)
    
    # Output results
    print("\n=== Limited Battery Charging Station Results ===")
    limited_stats = limited_station.get_statistics()
    for key, value in limited_stats.items():
        print(f"{key}: {value}")
    
    print("\n=== Unlimited Battery Charging Station Results ===")
    unlimited_stats = unlimited_station.get_statistics()
    for key, value in unlimited_stats.items():
        print(f"{key}: {value}")
    
    print("\nCharging station test completed!")


if __name__ == "__main__":
    test_charging_station()
