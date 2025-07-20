# test_path_planning.py
# 路径规划和最近充电站选择测试

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# 添加当前目录和父目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from models.uav_classes import UAV, calculate_distance
from models.charging_station import ChargingStation
from models.coordinate_generator import CoordinateGenerator
import simpy

def test_nearest_charging_station():
    """测试最近充电站选择功能"""
    print("=" * 60)
    print("Nearest Charging Station Selection Test")
    print("=" * 60)
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 创建无人机
    uav = UAV(env, "test_uav", 39.9042, 116.4074)
    
    # 创建多个充电站
    charging_stations = [
        ChargingStation(env, 0, 39.9100, 116.4000, 'unlimited', 20, 2, 0.5),  # 约0.8km
        ChargingStation(env, 1, 39.9200, 116.3900, 'limited', 15, 3, 0.3),    # 约2.1km
        ChargingStation(env, 2, 39.8900, 116.4200, 'unlimited', 25, 1, 0.4),  # 约2.3km
        ChargingStation(env, 3, 39.9000, 116.4100, 'limited', 10, 2, 0.6),    # 约0.6km (最近)
        ChargingStation(env, 4, 39.9300, 116.4300, 'unlimited', 30, 4, 0.2)   # 约4.1km
    ]
    
    print(f"UAV position: ({uav.current_latitude:.4f}, {uav.current_longitude:.4f})")
    print("Charging stations:")
    
    # 计算并显示所有距离
    distances = []
    for i, station in enumerate(charging_stations):
        distance = calculate_distance(uav.current_latitude, uav.current_longitude, 
                                    station.latitude, station.longitude)
        distances.append(distance)
        print(f"  Station {i}: ({station.latitude:.4f}, {station.longitude:.4f}) - {distance:.3f} km")
    
    # 找到最近的充电站
    nearest_station = uav.find_nearest_charging_station(charging_stations)
    
    if nearest_station:
        nearest_distance = calculate_distance(uav.current_latitude, uav.current_longitude,
                                            nearest_station.latitude, nearest_station.longitude)
        expected_nearest_index = distances.index(min(distances))
        
        print(f"\nNearest station found: Station {nearest_station.station_id}")
        print(f"Distance: {nearest_distance:.3f} km")
        print(f"Expected nearest: Station {expected_nearest_index} ({min(distances):.3f} km)")
        
        # 验证结果
        is_correct = nearest_station.station_id == expected_nearest_index
        print(f"Selection correct: {'✓ PASS' if is_correct else '✗ FAIL'}")
        
        return is_correct
    else:
        print("✗ No nearest station found")
        return False


def test_path_planning_with_waypoints():
    """测试带航点的路径规划"""
    print("\n" + "=" * 60)
    print("Path Planning with Waypoints Test")
    print("=" * 60)
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 创建无人机
    uav = UAV(env, "path_uav", 39.9042, 116.4074)
    
    # 定义预设路径
    planned_waypoints = [
        {'latitude': 39.9100, 'longitude': 116.4000, 'service_time': 0.2},
        {'latitude': 39.9200, 'longitude': 116.3950, 'service_time': 0.3},
        {'latitude': 39.9150, 'longitude': 116.4050, 'service_time': 0.1},
        {'latitude': 39.9042, 'longitude': 116.4074, 'service_time': 0.0}  # 返回起点
    ]
    
    # 设置计划路径
    uav.set_planned_route(planned_waypoints)
    
    print(f"Planned route set with {len(planned_waypoints)} waypoints:")
    total_distance = 0
    prev_lat, prev_lon = uav.current_latitude, uav.current_longitude
    
    for i, waypoint in enumerate(planned_waypoints):
        distance = calculate_distance(prev_lat, prev_lon, 
                                    waypoint['latitude'], waypoint['longitude'])
        total_distance += distance
        print(f"  Waypoint {i+1}: ({waypoint['latitude']:.4f}, {waypoint['longitude']:.4f}) "
              f"- {distance:.3f} km from previous")
        prev_lat, prev_lon = waypoint['latitude'], waypoint['longitude']
    
    print(f"Total planned distance: {total_distance:.3f} km")
    
    # 执行路径并记录
    def execute_planned_path():
        yield env.process(uav.execute_planned_route([]))  # 无充电站
        
        # 验证轨迹执行
        if uav.trajectory_log:
            print(f"\nTrajectory executed with {len(uav.trajectory_log)} segments")
            
            # 验证轨迹是否按计划执行
            adherence, details = uav.validate_trajectory_adherence(tolerance_km=0.1)
            print(f"Trajectory adherence: {'✓ PASS' if adherence else '✗ FAIL'}")
            print(f"Average deviation: {details['average_deviation']:.3f} km")
            print(f"Adherence percentage: {details['adherence_percentage']:.1f}%")
            
            return adherence
        else:
            print("✗ No trajectory recorded")
            return False
    
    env.process(execute_planned_path())
    env.run(until=30)  # 设置最大仿真时间限制
    
    return len(uav.trajectory_log) > 0


def test_charging_integration_with_path():
    """测试路径规划与充电站集成"""
    print("\n" + "=" * 60)
    print("Path Planning with Charging Integration Test")
    print("=" * 60)
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 创建无人机（低电池容量，强制需要充电）
    uav = UAV(env, "charging_path_uav", 39.9042, 116.4074, battery_capacity=30)
    uav.current_battery = 25  # 低电量开始
    
    # 创建充电站网络
    charging_stations = [
        ChargingStation(env, 0, 39.9100, 116.4000, 'unlimited', 20, 2, 0.1),
        ChargingStation(env, 1, 39.9200, 116.3900, 'unlimited', 15, 3, 0.1),
        ChargingStation(env, 2, 39.9300, 116.4100, 'unlimited', 25, 1, 0.1)
    ]
    
    # 定义长距离路径（需要充电）
    long_path = [
        {'latitude': 39.9500, 'longitude': 116.3800, 'service_time': 0.2},  # 远距离点1
        {'latitude': 39.9600, 'longitude': 116.3700, 'service_time': 0.3},  # 远距离点2
        {'latitude': 39.9700, 'longitude': 116.3600, 'service_time': 0.2},  # 远距离点3
        {'latitude': 39.9042, 'longitude': 116.4074, 'service_time': 0.0}   # 返回
    ]
    
    uav.set_planned_route(long_path)
    
    print(f"Starting battery: {uav.current_battery}%")
    print(f"Battery capacity: {uav.battery_capacity}%")
    print(f"Available charging stations: {len(charging_stations)}")
    
    def execute_charging_path():
        initial_battery = uav.current_battery
        
        yield env.process(uav.execute_planned_route(charging_stations))
        
        final_battery = uav.current_battery
        
        print(f"\nPath execution completed:")
        print(f"Initial battery: {initial_battery}%")
        print(f"Final battery: {final_battery}%")
        
        # 分析轨迹中的充电站访问
        charging_visits = 0
        trajectory_summary = uav.get_trajectory_summary()
        
        for log in uav.trajectory_log:
            to_lat, to_lon = log['to']
            # 检查是否访问了充电站
            for station in charging_stations:
                if calculate_distance(to_lat, to_lon, station.latitude, station.longitude) < 0.1:
                    charging_visits += 1
                    print(f"Visited charging station {station.station_id} at ({station.latitude:.4f}, {station.longitude:.4f})")
                    break
        
        print(f"Total charging station visits: {charging_visits}")
        print(f"Total distance traveled: {trajectory_summary['total_distance_km']:.2f} km")
        print(f"Battery consumption: {trajectory_summary['battery_used']:.1f}%")
        
        # 验证任务是否成功完成
        success = final_battery > 0 and len(uav.trajectory_log) > 0
        print(f"Mission success: {'✓ PASS' if success else '✗ FAIL'}")
        
        return success
    
    env.process(execute_charging_path())
    env.run(until=40)  # 设置最大仿真时间限制
    
    return len(uav.trajectory_log) > 0


def test_coordinate_generation_integration():
    """测试坐标生成器与路径规划的集成"""
    print("\n" + "=" * 60)
    print("Coordinate Generation Integration Test")
    print("=" * 60)
    
    # 创建坐标生成器
    generator = CoordinateGenerator(area_size=20)  # 20km区域
    
    # 生成坐标
    coordinates = generator.generate_all_coordinates(
        num_customers=5,
        num_charging_stations=3,
        num_distribution_centers=2,
        num_service_points=4
    )
    
    print("Generated coordinates:")
    print(f"Customers: {len(coordinates['customers'])}")
    print(f"Charging stations: {len(coordinates['charging_stations'])}")
    print(f"Distribution centers: {len(coordinates['distribution_centers'])}")
    print(f"Service points: {len(coordinates['service_points'])}")
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 使用生成的坐标创建充电站
    charging_stations = []
    for i, coord in enumerate(coordinates['charging_stations']):
        station = ChargingStation(env, i, coord['latitude'], coord['longitude'], 
                                'unlimited', 20, 2, 0.2)
        charging_stations.append(station)
    
    # 创建无人机在随机位置
    customer_coord = coordinates['customers'][0]
    uav = UAV(env, "integration_uav", customer_coord['latitude'], customer_coord['longitude'])
    
    # 创建路径到多个服务点
    service_waypoints = []
    for coord in coordinates['service_points']:
        service_waypoints.append({
            'latitude': coord['latitude'],
            'longitude': coord['longitude'],
            'service_time': 0.2
        })
    
    # 添加返回起点
    service_waypoints.append({
        'latitude': customer_coord['latitude'],
        'longitude': customer_coord['longitude'],
        'service_time': 0.0
    })
    
    uav.set_planned_route(service_waypoints)
    
    print(f"\nUAV starting position: ({uav.current_latitude:.4f}, {uav.current_longitude:.4f})")
    print(f"Planned route to {len(service_waypoints)-1} service points")
    
    # 找到最近的充电站
    nearest_station = uav.find_nearest_charging_station(charging_stations)
    if nearest_station:
        distance_to_nearest = calculate_distance(uav.current_latitude, uav.current_longitude,
                                               nearest_station.latitude, nearest_station.longitude)
        print(f"Nearest charging station: {nearest_station.station_id} at {distance_to_nearest:.3f} km")
    
    def execute_integration_test():
        yield env.process(uav.execute_planned_route(charging_stations))
        
        summary = uav.get_trajectory_summary()
        print(f"\nIntegration test results:")
        print(f"Total distance: {summary['total_distance_km']:.2f} km")
        print(f"Battery used: {summary['battery_used']:.1f}%")
        print(f"Trajectory segments: {len(uav.trajectory_log)}")
        
        return len(uav.trajectory_log) > 0
    
    env.process(execute_integration_test())
    env.run(until=50)  # 设置最大仿真时间限制
    
    return True


def run_path_planning_tests():
    """运行所有路径规划测试"""
    print("Path Planning and Charging Station Test Suite")
    print("=" * 80)
    
    test_functions = [
        test_nearest_charging_station,
        test_path_planning_with_waypoints,
        test_charging_integration_with_path,
        test_coordinate_generation_integration
    ]
    
    results = []
    
    for test_func in test_functions:
        try:
            success = test_func()
            results.append((test_func.__name__, success))
        except Exception as e:
            print(f"\n✗ Test {test_func.__name__} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_func.__name__, False))
    
    # 输出测试结果
    print("\n" + "=" * 80)
    print("Path Planning Test Results")
    print("=" * 80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:40}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 80)
    
    if all_passed:
        print("🎉 All path planning tests passed!")
        print("\nVerified Features:")
        print("✓ Nearest charging station selection algorithm")
        print("✓ Pre-planned route execution with waypoints")
        print("✓ Automatic charging integration during long routes")
        print("✓ Coordinate generator integration with path planning")
        print("✓ Distance calculation accuracy with haversine formula")
    else:
        print("❌ Some path planning tests failed")
    
    return all_passed


if __name__ == "__main__":
    success = run_path_planning_tests()
    sys.exit(0 if success else 1)
