# simple_test.py
# 简单测试最短路径算法

import sys
import os

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

def test_shortest_path():
    try:
        # 导入必要的模块
        import simpy
        from models.uav_classes import UAV, calculate_distance
        from models.charging_station import ChargingStation
        
        print("=== UAV最短路径算法测试 ===")
        
        # 创建仿真环境
        env = simpy.Environment()
        
        # 创建UAV
        uav = UAV(env, "test_uav", 39.9042, 116.4074)
        print(f"✓ 创建UAV: {uav.uav_id}")
        
        # 测试1: 基本最短路径计算
        print("\n--- 测试1: 基本Dijkstra算法 ---")
        start_lat, start_lon = 39.9042, 116.4074  # 天安门
        end_lat, end_lon = 39.9500, 116.4500     # 目标点
        
        waypoints = [
            {'id': 'wp1', 'latitude': 39.9200, 'longitude': 116.4200},
            {'id': 'wp2', 'latitude': 39.9300, 'longitude': 116.4300},
        ]
        
        # 计算最短路径
        path, distance = uav.calculate_shortest_path_dijkstra(
            start_lat, start_lon, end_lat, end_lon, waypoints
        )
        
        print(f"起点: ({start_lat:.4f}, {start_lon:.4f})")
        print(f"终点: ({end_lat:.4f}, {end_lon:.4f})")
        print(f"计算出的路径包含 {len(path)} 个航点:")
        for i, point in enumerate(path):
            print(f"  {i+1}. {point['id']}: ({point['latitude']:.4f}, {point['longitude']:.4f})")
        print(f"总距离: {distance:.2f} km")
        
        # 测试2: 带充电站约束的路径
        print("\n--- 测试2: 带充电站约束的路径 ---")
        uav2 = UAV(env, "test_uav2", 39.9042, 116.4074, battery_capacity=50)
        uav2.current_battery = 30  # 低电量
        
        # 创建充电站
        charging_stations = [
            ChargingStation(env, "cs1", 39.9250, 116.4250, battery_type='unlimited'),
        ]
        
        enhanced_path, enhanced_distance = uav2.plan_shortest_route_with_constraints(
            start_lat, start_lon, end_lat, end_lon, waypoints, charging_stations
        )
        
        print(f"增强路径包含 {len(enhanced_path)} 个航点:")
        for i, point in enumerate(enhanced_path):
            point_type = point.get('type', 'waypoint')
            print(f"  {i+1}. {point['id']} ({point_type}): ({point['latitude']:.4f}, {point['longitude']:.4f})")
        print(f"增强路径总距离: {enhanced_distance:.2f} km")
        
        print("\n✓ 所有测试完成成功!")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_shortest_path()
    if success:
        print("\n🎉 最短路径算法工作正常!")
    else:
        print("\n❌ 最短路径算法测试失败")
