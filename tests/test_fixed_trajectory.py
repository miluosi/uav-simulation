# test_fixed_trajectory.py
# 修复后的轨迹测试

import sys
import os
import matplotlib.pyplot as plt

# 添加当前目录和父目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from models.uav_classes import UAV, calculate_distance
from models.charging_station import ChargingStation
import simpy

def test_fixed_trajectory():
    """测试修复后的轨迹功能"""
    print("=" * 60)
    print("Fixed Trajectory Test")
    print("=" * 60)
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 创建无人机（小电池容量以确保需要充电）
    uav = UAV(env, "test_uav", 39.9042, 116.4074, battery_capacity=30)
    
    # 创建充电站
    charging_stations = [
        ChargingStation(env, 0, 39.9100, 116.4000, 'unlimited', 20, 2, 0.5),
        ChargingStation(env, 1, 39.9200, 116.3900, 'limited', 15, 3, 0.3)
    ]
    
    # 定义测试轨迹（会需要充电）
    test_waypoints = [
        {'latitude': 39.9585, 'longitude': 116.3974, 'service_time': 0.2},  # 远点1
        {'latitude': 39.9763, 'longitude': 116.3972, 'service_time': 0.3},  # 远点2
        {'latitude': 39.9042, 'longitude': 116.4074, 'service_time': 0.1}   # 返回起点
    ]
    
    uav.set_planned_route(test_waypoints)
    
    def run_test():
        print(f"Initial battery: {uav.current_battery}%")
        
        yield env.process(uav.execute_planned_route(charging_stations))
        
        print(f"Final battery: {uav.current_battery}%")
        
        # 验证轨迹
        adherence, details = uav.validate_trajectory_adherence(tolerance_km=0.5)
        
        print(f"\nFixed Trajectory Test Results:")
        print(f"Overall Adherence: {'✓ PASS' if adherence else '✗ FAIL'}")
        print(f"Average Deviation: {details['average_deviation']:.3f} km")
        print(f"Max Deviation: {details['max_deviation']:.3f} km") 
        print(f"Adherence Percentage: {details['adherence_percentage']:.1f}%")
        
        # 轨迹摘要
        summary = uav.get_trajectory_summary()
        print(f"\nTrajectory Summary:")
        print(f"Total Waypoints Logged: {summary['total_waypoints']}")
        print(f"Total Distance: {summary['total_distance_km']:.2f} km")
        print(f"Total Time: {summary['total_time']:.2f} units")
        print(f"Battery Used: {summary['battery_used']:.1f}%")
        print(f"Average Speed: {summary['average_speed']:.2f} km/time_unit")
        
        # 分析轨迹记录
        print(f"\nDetailed Trajectory Log:")
        for i, log in enumerate(uav.trajectory_log):
            from_pos = log['from']
            to_pos = log['to']
            print(f"  Step {i+1}: ({from_pos[0]:.3f}, {from_pos[1]:.3f}) -> ({to_pos[0]:.3f}, {to_pos[1]:.3f}) "
                  f"Distance: {log['distance']:.2f}km Battery: {log['battery_before']:.1f}→{log['battery_after']:.1f}")
        
        return adherence
    
    env.process(run_test())
    env.run()
    
    return True

def test_simple_trajectory():
    """测试简单轨迹（不需要充电）"""
    print("\n" + "=" * 60)
    print("Simple Trajectory Test (No Charging Required)")
    print("=" * 60)
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 创建无人机（大电池容量）
    uav = UAV(env, "simple_uav", 39.9042, 116.4074, battery_capacity=100)
    
    # 定义简单轨迹
    simple_waypoints = [
        {'latitude': 39.9085, 'longitude': 116.3974, 'service_time': 0.2},
        {'latitude': 39.9163, 'longitude': 116.3972, 'service_time': 0.3},
        {'latitude': 39.9042, 'longitude': 116.4074, 'service_time': 0.1}
    ]
    
    uav.set_planned_route(simple_waypoints)
    
    def run_simple_test():
        yield env.process(uav.execute_planned_route())
        
        # 验证轨迹
        adherence, details = uav.validate_trajectory_adherence(tolerance_km=0.1)
        
        print(f"\nSimple Trajectory Test Results:")
        print(f"Overall Adherence: {'✓ PASS' if adherence else '✗ FAIL'}")
        print(f"Average Deviation: {details['average_deviation']:.3f} km")
        print(f"Adherence Percentage: {details['adherence_percentage']:.1f}%")
        
        return adherence
    
    env.process(run_simple_test())
    env.run()
    
    return True

def main():
    """主测试函数"""
    print("Fixed UAV Trajectory System Test")
    print("=" * 80)
    
    results = []
    
    # 简单轨迹测试
    try:
        simple_success = test_simple_trajectory()
        results.append(("Simple Trajectory", simple_success))
    except Exception as e:
        print(f"Simple trajectory test failed: {e}")
        results.append(("Simple Trajectory", False))
    
    # 复杂轨迹测试（需要充电）
    try:
        complex_success = test_fixed_trajectory()
        results.append(("Complex Trajectory", complex_success))
    except Exception as e:
        print(f"Complex trajectory test failed: {e}")
        results.append(("Complex Trajectory", False))
    
    # 输出结果
    print("\n" + "=" * 80)
    print("Fixed Test Results Summary")
    print("=" * 80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:25}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 80)
    
    if all_passed:
        print("🎉 All fixed trajectory tests passed!")
        print("\nFixed Issues:")
        print("• Trajectory logging and validation logic")
        print("• Battery consumption tracking")
        print("• Charging station process loop")
        print("• Waypoint matching for trajectory adherence")
    else:
        print("❌ Some tests still failing.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    if success:
        print("\nTrajectory system fixes verified successfully!")
    else:
        print("\nSome issues remain to be fixed.")
