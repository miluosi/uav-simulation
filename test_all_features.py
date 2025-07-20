# test_all_features.py
# 测试所有功能包括最短路径算法

import sys
import os

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_all_features():
    print("=== UAV物流仿真系统完整功能测试 ===")
    
    try:
        # 导入所有模块
        import simpy
        from models.uav_classes import UAV, calculate_distance
        from models.charging_station import ChargingStation
        from models.distribution_center import DistributionCenter
        from models.coordinate_generator import CoordinateGenerator
        
        print("✓ 所有模块导入成功")
        
        # 创建仿真环境
        env = simpy.Environment()
        
        # 1. 测试坐标生成器
        print("\n--- 测试1: 坐标生成器 ---")
        coord_gen = CoordinateGenerator(area_size=50)
        coordinates = coord_gen.generate_all_coordinates(2, 2, 1, 3)
        print(f"✓ 生成坐标成功: {len(coordinates['customers'])} 个客户点")
        
        # 2. 测试充电站
        print("\n--- 测试2: 充电站 ---")
        charging_station = ChargingStation(env, "cs1", 25, 25, battery_type='unlimited')
        print(f"✓ 充电站创建成功: {charging_station.station_id}")
        
        # 3. 测试配送中心
        print("\n--- 测试3: 配送中心 ---")
        dist_center = DistributionCenter(env, "dc1", 30, 30)
        print(f"✓ 配送中心创建成功: {dist_center.center_id}")
        
        # 4. 测试UAV和最短路径算法
        print("\n--- 测试4: UAV最短路径算法 ---")
        uav = UAV(env, "test_uav", 39.9042, 116.4074)
        print(f"✓ UAV创建成功: {uav.uav_id}")
        
        # 测试基本最短路径
        waypoints = [
            {'id': 'wp1', 'latitude': 39.9200, 'longitude': 116.4200},
            {'id': 'wp2', 'latitude': 39.9300, 'longitude': 116.4300},
        ]
        
        start_lat, start_lon = 39.9042, 116.4074
        end_lat, end_lon = 39.9500, 116.4500
        
        path, distance = uav.calculate_shortest_path_dijkstra(
            start_lat, start_lon, end_lat, end_lon, waypoints
        )
        
        print(f"✓ 最短路径计算成功: {len(path)} 个航点, 总距离 {distance:.2f} km")
        
        # 测试带充电站约束的路径
        charging_stations = [charging_station]
        uav.current_battery = 20  # 设置低电量
        
        enhanced_path, enhanced_distance = uav.plan_shortest_route_with_constraints(
            start_lat, start_lon, end_lat, end_lon, waypoints, charging_stations
        )
        
        print(f"✓ 充电约束路径计算成功: {len(enhanced_path)} 个航点, 总距离 {enhanced_distance:.2f} km")
        
        # 5. 测试路径执行（仿真）
        print("\n--- 测试5: 路径执行仿真 ---")
        def run_path_execution():
            yield env.process(uav.execute_shortest_path_route(
                start_lat, start_lon, 39.9200, 116.4200, 
                [waypoints[0]], charging_stations
            ))
            print(f"✓ 路径执行完成, UAV当前位置: ({uav.current_latitude:.4f}, {uav.current_longitude:.4f})")
        
        env.process(run_path_execution())
        env.run(until=20)
        
        print("\n✓ 所有测试完成成功!")
        print("\n系统功能摘要:")
        print("• 坐标生成: 自动生成客户点、充电站、配送中心、服务点")
        print("• 充电站管理: 支持有限/无限电池类型")
        print("• 配送中心: 固定卡车调度")
        print("• UAV智能路径规划: Dijkstra算法, 电池约束考虑")
        print("• 路径执行: 实时仿真飞行")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_features()
    if success:
        print("\n🎉 UAV物流仿真系统所有功能正常!")
    else:
        print("\n❌ 系统测试失败")
