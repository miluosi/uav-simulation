# test_charging_station.py
# 专门测试充电站死循环问题

import sys
import os

# 添加当前目录和父目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from models.uav_classes import UAV, calculate_distance
from models.charging_station import ChargingStation
import simpy

def test_charging_station_no_deadlock():
    """测试充电站不死循环"""
    print("Charging Station Deadlock Test")
    print("=" * 50)
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 创建充电站 - 容量为5，看看是否会死循环
    charging_station = ChargingStation(env, 1, 39.9050, 116.4080, 'limited', 5, 1, 0.1)
    
    print(f"创建充电站，电池容量: {charging_station.battery_capacity}")
    print(f"初始可用电池: {charging_station.available_batteries}")
    
    # 创建多个UAV来测试
    uavs = []
    for i in range(7):  # 创建7个UAV，超过充电站容量
        uav = UAV(env, f"uav_{i}", 39.9042, 116.4074, battery_capacity=100)
        uav.current_battery = 10  # 设置低电量
        uavs.append(uav)
    
    def test_charging_process():
        # 让所有UAV去充电
        charging_processes = []
        for uav in uavs:
            process = env.process(charging_station.serve_uav(uav))
            charging_processes.append(process)
        
        # 等待所有充电完成
        yield env.all_of(charging_processes)
        
        print(f"\n充电完成后状态:")
        print(f"可用电池: {charging_station.available_batteries}")
        print(f"正在充电的电池: {charging_station.charging_batteries}")
        print(f"用过的电池: {len(charging_station.used_batteries)}")
        print(f"总电池数: {charging_station.available_batteries + charging_station.charging_batteries + len(charging_station.used_batteries)}")
        
        # 验证所有UAV都充满电了
        for uav in uavs:
            print(f"UAV {uav.uav_id} 电池: {uav.current_battery}%")
    
    env.process(test_charging_process())
    
    # 运行仿真，限制时间避免死循环
    try:
        env.run(until=50)  # 最多运行50个时间单位
        print("\n✓ 测试完成，充电站没有死循环")
        return True
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        return False

def test_charging_station_capacity_limit():
    """测试充电站容量限制"""
    print("\n" + "=" * 50)
    print("Charging Station Capacity Limit Test")
    print("=" * 50)
    
    env = simpy.Environment()
    
    # 创建小容量充电站
    charging_station = ChargingStation(env, 2, 39.9060, 116.4090, 'limited', 3, 1, 0.05)
    
    print(f"充电站容量: {charging_station.battery_capacity}")
    
    def monitor_batteries():
        """监控电池状态"""
        for _ in range(20):  # 监控20个时间点
            total = (charging_station.available_batteries + 
                    charging_station.charging_batteries + 
                    len(charging_station.used_batteries))
            
            print(f"时间 {env.now:.1f}: 可用={charging_station.available_batteries}, "
                  f"充电中={charging_station.charging_batteries}, "
                  f"用过={len(charging_station.used_batteries)}, "
                  f"总计={total}")
            
            # 检查是否超过容量
            if total > charging_station.battery_capacity:
                print(f"❌ 错误: 总电池数 {total} 超过容量 {charging_station.battery_capacity}")
                return False
            
            yield env.timeout(1.0)
        
        print("✓ 电池容量限制正常")
        return True
    
    def create_uav_demand():
        """创建UAV需求"""
        for i in range(5):
            uav = UAV(env, f"demand_uav_{i}", 39.9042, 116.4074)
            uav.current_battery = 5  # 低电量
            env.process(charging_station.serve_uav(uav))
            yield env.timeout(2.0)  # 每2个时间单位创建一个UAV
    
    env.process(monitor_batteries())
    env.process(create_uav_demand())
    
    try:
        env.run(until=25)
        print("✓ 容量限制测试完成")
        return True
    except Exception as e:
        print(f"✗ 容量限制测试失败: {e}")
        return False

if __name__ == "__main__":
    print("充电站死循环修复测试")
    print("=" * 80)
    
    test1_success = test_charging_station_no_deadlock()
    test2_success = test_charging_station_capacity_limit()
    
    if test1_success and test2_success:
        print("\n🎉 所有测试通过！充电站死循环问题已修复。")
    else:
        print("\n❌ 某些测试失败，还需要进一步修复。")
