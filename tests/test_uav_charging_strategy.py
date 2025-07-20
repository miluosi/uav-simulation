#!/usr/bin/env python3
# test_uav_charging_strategy.py
# 测试修改后的UAV类充电策略

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

import simpy
from models.uav_classes import UAV, calculate_distance
from models.charging_station import ChargingStation

def test_uav_charging_strategy():
    """测试UAV类的新充电策略"""
    print("=== UAV充电策略测试 ===")
    
    env = simpy.Environment()
    
    # 创建UAV，设置最大不充电距离为30km
    uav = UAV(env, "test_uav", 39.9042, 116.4074, max_no_charge_distance=30.0)
    print(f"创建UAV: {uav.uav_id}")
    print(f"基地坐标: ({uav.base_latitude:.3f}, {uav.base_longitude:.3f})")
    print(f"最大不充电距离: {uav.max_no_charge_distance} km")
    print(f"初始电池: {uav.current_battery}%")
    
    # 创建几个充电站
    charging_stations = [
        ChargingStation(env, "cs1", 39.9200, 116.4200, battery_type='unlimited'),
        ChargingStation(env, "cs2", 39.9300, 116.4300, battery_type='unlimited'),
        ChargingStation(env, "cs3", 39.8800, 116.3800, battery_type='unlimited')
    ]
    
    print(f"\n创建了 {len(charging_stations)} 个充电站")
    for i, cs in enumerate(charging_stations):
        distance = calculate_distance(uav.current_latitude, uav.current_longitude,
                                     cs.latitude, cs.longitude)
        print(f"  充电站{i+1}: ({cs.latitude:.3f}, {cs.longitude:.3f}), 距离: {distance:.2f}km")
    
    print("\n=== 测试1: 近距离目标点（不需要充电）===")
    # 测试近距离目标点
    near_target_lat, near_target_lon = 39.9100, 116.4100
    uav.set_destination(near_target_lat, near_target_lon)
    
    distance_to_near = calculate_distance(uav.current_latitude, uav.current_longitude,
                                         near_target_lat, near_target_lon)
    print(f"目标点坐标: ({near_target_lat:.3f}, {near_target_lon:.3f})")
    print(f"距离目标点: {distance_to_near:.2f}km")
    print(f"可以不充电到达: {uav.can_reach_destination_without_charging()}")
    print(f"需要充电: {uav.requires_charging_for_destination()}")
    
    print("\n=== 测试2: 远距离目标点（需要充电）===")
    # 测试远距离目标点
    far_target_lat, far_target_lon = 40.0500, 116.6000
    uav.set_destination(far_target_lat, far_target_lon)
    
    distance_to_far = calculate_distance(uav.current_latitude, uav.current_longitude,
                                        far_target_lat, far_target_lon)
    print(f"目标点坐标: ({far_target_lat:.3f}, {far_target_lon:.3f})")
    print(f"距离目标点: {distance_to_far:.2f}km")
    print(f"可以不充电到达: {uav.can_reach_destination_without_charging()}")
    print(f"需要充电: {uav.requires_charging_for_destination()}")
    
    # 测试充电策略
    optimal_station = uav.find_optimal_charging_strategy(charging_stations)
    if optimal_station:
        distance_to_station = calculate_distance(uav.current_latitude, uav.current_longitude,
                                                optimal_station.latitude, optimal_station.longitude)
        distance_station_to_target = calculate_distance(optimal_station.latitude, optimal_station.longitude,
                                                       far_target_lat, far_target_lon)
        print(f"最优充电站: {optimal_station.station_id}")
        print(f"  - 到充电站距离: {distance_to_station:.2f}km")
        print(f"  - 充电站到目标距离: {distance_station_to_target:.2f}km")
        print(f"  - 总距离: {distance_to_station + distance_station_to_target:.2f}km")
    
    print("\n=== 测试3: 低电量情况 ===")
    # 模拟低电量情况
    uav.current_battery = 30  # 设置低电量
    print(f"当前电池: {uav.current_battery}%")
    
    # 测试中等距离目标点
    medium_target_lat, medium_target_lon = 39.9300, 116.4400
    uav.set_destination(medium_target_lat, medium_target_lon)
    
    distance_to_medium = calculate_distance(uav.current_latitude, uav.current_longitude,
                                           medium_target_lat, medium_target_lon)
    print(f"目标点坐标: ({medium_target_lat:.3f}, {medium_target_lon:.3f})")
    print(f"距离目标点: {distance_to_medium:.2f}km")
    print(f"需要充电: {uav.requires_charging_for_destination()}")
    
    # 测试0-1矩阵判断（max/2规则）
    effective_max = uav.max_no_charge_distance / 2
    print(f"有效最大距离 (max/2): {effective_max:.1f}km")
    print(f"距离是否超过有效最大距离: {distance_to_medium > effective_max}")
    
    print("\n=== 测试4: 最短路径规划with新策略 ===")
    # 重置UAV状态
    uav.current_battery = 100
    uav.current_latitude = 39.9042
    uav.current_longitude = 116.4074
    
    # 测试航点
    waypoints = [
        {'id': 'wp1', 'latitude': 39.9200, 'longitude': 116.4200},
        {'id': 'wp2', 'latitude': 39.9400, 'longitude': 116.4400}
    ]
    
    print("计算包含充电约束的最短路径...")
    enhanced_path, total_distance = uav.plan_shortest_route_with_constraints(
        39.9042, 116.4074, 40.0000, 116.5000, waypoints, charging_stations
    )
    
    print(f"增强路径包含 {len(enhanced_path)} 个节点:")
    for i, node in enumerate(enhanced_path):
        node_type = node.get('type', 'waypoint')
        print(f"  {i+1}. {node_type}: ({node['latitude']:.3f}, {node['longitude']:.3f})")
    
    print(f"总距离: {total_distance:.2f}km")
    
    print("\n=== 测试完成 ===")
    return True

if __name__ == "__main__":
    success = test_uav_charging_strategy()
    if success:
        print("✓ UAV充电策略测试通过")
    else:
        print("✗ UAV充电策略测试失败")
