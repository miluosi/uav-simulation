#!/usr/bin/env python3
# working_run_tests.py - 可以工作的测试套件

import sys
import os
import numpy as np
import time

print("=== UAV物流仿真系统测试套件 ===")
print("版本: 工作版本")

# Add current directory and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

# 创建输出文件夹
plot_dir = os.path.join(current_dir, 'plot')
result_dir = os.path.join(current_dir, 'result')

# 如果文件夹不存在则创建
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
    print(f"Created plot directory: {plot_dir}")

if not os.path.exists(result_dir):
    os.makedirs(result_dir)
    print(f"Created result directory: {result_dir}")

print(f"Plot files will be saved to: {plot_dir}")
print(f"Result files will be saved to: {result_dir}")

def test_coordinate_generator():
    """Test coordinate generator"""
    print("=" * 60)
    print("Test 1: Coordinate Generator Module")
    print("=" * 60)
    
    try:
        from test_coordinate_generator import run_all_tests
        success = run_all_tests()
        return success
    except Exception as e:
        print(f"Coordinate generator test failed: {e}")
        return False

def test_charging_station():
    """Test charging station functionality"""
    print("\n" + "=" * 60)
    print("Test 2: Charging Station Functionality")
    print("=" * 60)
    
    try:
        from models.charging_station import test_charging_station
        test_charging_station()
        print("✓ Charging station test completed")
        return True
    except Exception as e:
        print(f"Charging station test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_distribution_center():
    """Test distribution center functionality"""
    print("\n" + "=" * 60)
    print("Test 3: Distribution Center Functionality")
    print("=" * 60)
    
    try:
        from models.distribution_center import test_distribution_center
        test_distribution_center()
        print("✓ Distribution center test completed")
        return True
    except Exception as e:
        print(f"Distribution center test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complete_system():
    """Test complete system functionality"""
    print("\n" + "=" * 60)
    print("Test 4: Complete System Functionality")
    print("=" * 60)
    
    try:
        from models.complete_simulation import run_complete_simulation_test
        simulation, stats = run_complete_simulation_test()
        print("✓ Complete system test completed")
        return True
    except Exception as e:
        print(f"Complete system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_quick_functionality_test():
    """Run quick functionality test"""
    print("\n" + "=" * 60)
    print("Quick Functionality Verification Test")
    print("=" * 60)
    
    try:
        # Import all modules
        from models.coordinate_generator import CoordinateGenerator
        from models.charging_station import ChargingStation
        from models.distribution_center import DistributionCenter
        from models.uav_classes import UAV, Goods, Order
        import simpy
        
        print("✓ All modules imported successfully")
        
        # Create simple test environment
        env = simpy.Environment()
        
        # Test basic functionality
        generator = CoordinateGenerator(area_size=50)
        station = ChargingStation(env, 'test_cs', 25, 25, 'limited', 20, 2, 0.5)
        dc = DistributionCenter(env, 'test_dc', 30, 30)
        uav = UAV(env, 'test_uav', 25, 25)
        goods = Goods(env, 'test_goods')
        order = Order(env, 1, 0, 0, goods, 'direct')
        
        print("✓ All objects created successfully")
        return True
        
    except Exception as e:
        print(f"Quick functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_shortest_path_algorithm():
    """Test shortest path algorithm with extended simulation and trajectory visualization"""
    print("\n" + "=" * 60)
    print("Test 5: Shortest Path Algorithm - Extended Testing")
    print("=" * 60)
    
    try:
        from models.uav_classes import UAV, calculate_distance, Order, Goods
        from models.charging_station import ChargingStation
        import simpy
        import matplotlib.pyplot as plt
        import numpy as np
        
        env = simpy.Environment()
        
        # 创建更多的充电站
        charging_stations = [
            ChargingStation(env, "cs1", 39.9200, 116.4200, battery_type='unlimited'),
            ChargingStation(env, "cs2", 39.9350, 116.4350, battery_type='unlimited'), 
            ChargingStation(env, "cs3", 39.9100, 116.4450, battery_type='unlimited'),
            ChargingStation(env, "cs4", 39.9400, 116.4100, battery_type='limited', battery_capacity=15, service_windows=3, service_time=0.5),
            ChargingStation(env, "cs5", 39.8900, 116.4300, battery_type='unlimited'),
            ChargingStation(env, "cs6", 39.9300, 116.4500, battery_type='limited', battery_capacity=12, service_windows=2, service_time=0.8)
        ]
        
        print(f"创建了 {len(charging_stations)} 个充电站:")
        for i, cs in enumerate(charging_stations):
            print(f"  充电站{i+1}: ({cs.latitude:.4f}, {cs.longitude:.4f}), 类型: {cs.battery_type}")
        
        # 定义测试航点（模拟顾客点和服务点）
        test_waypoints = [
            {'id': 'customer1', 'latitude': 39.9180, 'longitude': 116.4180, 'type': 'customer'},
            {'id': 'service1', 'latitude': 39.9220, 'longitude': 116.4380, 'type': 'service'},
            {'id': 'customer2', 'latitude': 39.9320, 'longitude': 116.4320, 'type': 'customer'},
            {'id': 'service2', 'latitude': 39.9420, 'longitude': 116.4420, 'type': 'service'},
            {'id': 'customer3', 'latitude': 39.9080, 'longitude': 116.4280, 'type': 'customer'},
            {'id': 'service3', 'latitude': 39.9380, 'longitude': 116.4480, 'type': 'service'}
        ]
        
        print(f"\n测试航点:")
        for wp in test_waypoints:
            print(f"  {wp['id']}: ({wp['latitude']:.4f}, {wp['longitude']:.4f}) - {wp['type']}")
        
        # 测试起点和终点
        start_lat, start_lon = 39.9042, 116.4074  # 北京天安门
        end_lat, end_lon = 39.9500, 116.4600      # 目标点
        
        # 准备绘图
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('UAV Path Planning Algorithm Comparison Test', fontsize=16, fontweight='bold')
        
        # 测试案例1: 基本Dijkstra最短路径
        print(f"\n=== 测试案例1: 基本Dijkstra最短路径 ===")
        uav1 = UAV(env, "uav_dijkstra", start_lat, start_lon, max_no_charge_distance=25.0)
        uav1.current_battery = 80  # 设置初始电量
        
        path1, distance1 = uav1.calculate_shortest_path_dijkstra(
            start_lat, start_lon, end_lat, end_lon, test_waypoints[:4]
        )
        
        print(f"路径1 - Dijkstra算法:")
        print(f"  总距离: {distance1:.2f} km")
        print(f"  航点数量: {len(path1)}")
        for i, wp in enumerate(path1):
            print(f"    {i+1}. {wp['id']}: ({wp['latitude']:.4f}, {wp['longitude']:.4f})")
        
        # 绘制路径1
        ax1 = axes[0, 0]
        plot_path(ax1, path1, charging_stations, "Dijkstra Shortest Path", 'blue')
        
        # 测试案例2: 最近充电站策略
        print(f"\n=== 测试案例2: 最近充电站策略 ===")
        uav2 = UAV(env, "uav_nearest", start_lat, start_lon, max_no_charge_distance=25.0)
        uav2.current_battery = 40  # 设置较低电量
        
        # 使用现有的find_nearest_charging_station方法
        nearest_station = uav2.find_nearest_charging_station(charging_stations)
        path2 = [
            {'id': 'start', 'latitude': start_lat, 'longitude': start_lon, 'type': 'start'},
            {'id': f'charging_{nearest_station.station_id}', 'latitude': nearest_station.latitude, 
             'longitude': nearest_station.longitude, 'type': 'charging'},
            {'id': 'end', 'latitude': end_lat, 'longitude': end_lon, 'type': 'end'}
        ]
        
        distance2 = (calculate_distance(start_lat, start_lon, nearest_station.latitude, nearest_station.longitude) +
                    calculate_distance(nearest_station.latitude, nearest_station.longitude, end_lat, end_lon))
        
        print(f"路径2 - 最近充电站策略:")
        print(f"  总距离: {distance2:.2f} km")
        print(f"  选择充电站: {nearest_station.station_id}")
        print(f"  充电站位置: ({nearest_station.latitude:.4f}, {nearest_station.longitude:.4f})")
        
        # 绘制路径2
        ax2 = axes[0, 1]
        plot_path(ax2, path2, charging_stations, "Nearest Charging Station Strategy", 'red')
        
        # 测试案例3: 带约束条件的最短路径
        print(f"\n=== 测试案例3: 带约束条件的最短路径 ===")
        uav3 = UAV(env, "uav_constrained", start_lat, start_lon, max_no_charge_distance=25.0)
        uav3.current_battery = 60  # 设置中等电量
        
        path3, distance3 = uav3.plan_shortest_route_with_constraints(
            start_lat, start_lon, end_lat, end_lon, test_waypoints[:4], charging_stations
        )
        
        print(f"路径3 - 带约束条件的最短路径:")
        print(f"  总距离: {distance3:.2f} km")
        print(f"  航点数量: {len(path3)}")
        for i, wp in enumerate(path3):
            wp_type = wp.get('type', 'waypoint')
            print(f"    {i+1}. {wp['id']}: ({wp['latitude']:.4f}, {wp['longitude']:.4f}) - {wp_type}")
        
        # 绘制路径3
        ax3 = axes[1, 0]
        plot_path(ax3, path3, charging_stations, "Constrained Shortest Path", 'green')
        
        # 测试案例4: 订单完成时间测试
        print(f"\n=== 测试案例4: 订单完成时间测试 ===")
        
        # 创建测试订单
        test_goods = Goods(env, "goods_001", weight=1.5, priority=2)
        test_order = Order(env, 1, "customer1", "service1", test_goods, 'direct', priority=2)
        
        print(f"创建测试订单:")
        print(f"  订单ID: {test_order.order_id}")
        print(f"  客户ID: {test_order.customer_id}")
        print(f"  服务点ID: {test_order.service_point_id}")
        print(f"  配送模式: {test_order.delivery_mode}")
        print(f"  创建时间: {test_order.creation_time}")
        
        # 模拟订单执行过程
        def simulate_order_execution():
            test_order.start_time = env.now
            test_order.status = 'in_progress'
            print(f"  订单开始执行时间: {test_order.start_time}")
            
            # 模拟从顾客点到服务点的配送时间
            yield env.timeout(25.5)  # 模拟配送用时
            
            test_order.completion_time = env.now
            test_order.status = 'completed'
            
            total_service_time = test_order.completion_time - test_order.creation_time
            delivery_time = test_order.completion_time - test_order.start_time
            
            print(f"  订单完成时间: {test_order.completion_time}")
            print(f"  总服务时间: {total_service_time:.2f} 时间单位")
            print(f"  实际配送时间: {delivery_time:.2f} 时间单位")
        
        # 运行订单仿真
        env.process(simulate_order_execution())
        env.run(until=80)  # 运行80个时间单位
        
        # 对比分析
        print(f"\n=== 路径对比分析 ===")
        results_data = [
            ("Dijkstra Shortest Path", distance1, len(path1), "blue"),
            ("Nearest Charging Station", distance2, len(path2), "red"),
            ("Constrained Shortest Path", distance3, len(path3), "green")
        ]
        
        print(f"{'Strategy':<20} {'Distance(km)':<12} {'Waypoints':<10} {'Efficiency':<10}")
        print("-" * 60)
        
        min_distance = min(distance1, distance2, distance3)
        for name, dist, points, color in results_data:
            efficiency = min_distance / dist * 100
            print(f"{name:<20} {dist:<12.2f} {points:<10} {efficiency:<10.1f}%")
        
        # 绘制对比图表
        ax4 = axes[1, 1]
        strategies = [data[0] for data in results_data]
        distances = [data[1] for data in results_data]
        colors = ['blue', 'red', 'green']
        
        bars = ax4.bar(strategies, distances, color=colors, alpha=0.7)
        ax4.set_title('Path Distance Comparison', fontweight='bold')
        ax4.set_ylabel('Distance (km)')
        ax4.set_xlabel('Path Strategy')
        
        # 添加数值标签
        for bar, distance in zip(bars, distances):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{distance:.2f}km', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图表
        path_comparison_plot = os.path.join(plot_dir, 'uav_path_comparison.png')
        plt.savefig(path_comparison_plot, dpi=300, bbox_inches='tight')
        print(f"\n✓ Path comparison chart saved as '{path_comparison_plot}'")
        
        plt.show()
        
        print("✓ Extended shortest path algorithm test completed")
        return True
        
    except Exception as e:
        print(f"Shortest path algorithm test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_extended_scenarios():
    """Test extended scenarios with multiple UAVs, different battery levels, and complex routes"""
    print("\n" + "=" * 60)
    print("Test 6: Extended Scenario Testing")
    print("=" * 60)
    
    try:
        from models.uav_classes import UAV, calculate_distance, Order, Goods
        from models.charging_station import ChargingStation
        import simpy
        import matplotlib.pyplot as plt
        import numpy as np
        import time
        
        env = simpy.Environment()
        
        # 创建更大规模的充电站网络
        charging_stations = [
            ChargingStation(env, "cs1", 39.9000, 116.4000, battery_type='unlimited'),
            ChargingStation(env, "cs2", 39.9200, 116.4200, battery_type='limited', battery_capacity=20, service_windows=4, service_time=0.3),
            ChargingStation(env, "cs3", 39.9400, 116.4400, battery_type='unlimited'),
            ChargingStation(env, "cs4", 39.9100, 116.4100, battery_type='limited', battery_capacity=15, service_windows=3, service_time=0.5),
            ChargingStation(env, "cs5", 39.9300, 116.4300, battery_type='unlimited'),
            ChargingStation(env, "cs6", 39.9500, 116.4500, battery_type='limited', battery_capacity=25, service_windows=5, service_time=0.2),
            ChargingStation(env, "cs7", 39.8900, 116.4100, battery_type='unlimited'),
            ChargingStation(env, "cs8", 39.9350, 116.4150, battery_type='limited', battery_capacity=18, service_windows=2, service_time=0.4),
        ]
        
        print(f"Created {len(charging_stations)} charging stations for extended testing")
        
        # 定义多个测试场景的航点
        extended_waypoints = [
            {'id': 'depot', 'latitude': 39.9042, 'longitude': 116.4074, 'type': 'depot'},
            {'id': 'customer1', 'latitude': 39.9180, 'longitude': 116.4180, 'type': 'customer'},
            {'id': 'customer2', 'latitude': 39.9320, 'longitude': 116.4320, 'type': 'customer'},
            {'id': 'customer3', 'latitude': 39.9080, 'longitude': 116.4280, 'type': 'customer'},
            {'id': 'customer4', 'latitude': 39.9450, 'longitude': 116.4450, 'type': 'customer'},
            {'id': 'customer5', 'latitude': 39.8950, 'longitude': 116.4150, 'type': 'customer'},
            {'id': 'service1', 'latitude': 39.9220, 'longitude': 116.4380, 'type': 'service'},
            {'id': 'service2', 'latitude': 39.9420, 'longitude': 116.4420, 'type': 'service'},
            {'id': 'service3', 'latitude': 39.9380, 'longitude': 116.4480, 'type': 'service'},
            {'id': 'service4', 'latitude': 39.9120, 'longitude': 116.4220, 'type': 'service'},
            {'id': 'service5', 'latitude': 39.8980, 'longitude': 116.4080, 'type': 'service'},
        ]
        
        # 准备大型对比图表 (3x2 布局)
        fig, axes = plt.subplots(3, 2, figsize=(20, 18))
        fig.suptitle('Extended UAV Scenario Testing - Multiple Configurations', fontsize=18, fontweight='bold')
        
        test_results = []
        
        # 场景1: 低电量长距离测试
        print(f"\n=== Scenario 1: Low Battery Long Distance Test ===")
        start_point = extended_waypoints[0]  # depot
        end_point = extended_waypoints[4]    # customer4 (远距离)
        
        uav_low_battery = UAV(env, "uav_low_battery", start_point['latitude'], start_point['longitude'], max_no_charge_distance=20.0)
        uav_low_battery.current_battery = 25  # 低电量
        
        path_low, distance_low = uav_low_battery.plan_shortest_route_with_constraints(
            start_point['latitude'], start_point['longitude'], 
            end_point['latitude'], end_point['longitude'], 
            extended_waypoints[1:6], charging_stations
        )
        
        test_results.append(("Low Battery Long Distance", distance_low, len(path_low)))
        print(f"Low battery route: {distance_low:.2f} km, {len(path_low)} waypoints")
        
        # 绘制场景1
        plot_path(axes[0, 0], path_low, charging_stations, "Low Battery Long Distance", 'red')
        
        # 场景2: 高电量短距离测试
        print(f"\n=== Scenario 2: High Battery Short Distance Test ===")
        start_point2 = extended_waypoints[1]  # customer1
        end_point2 = extended_waypoints[6]    # service1 (短距离)
        
        uav_high_battery = UAV(env, "uav_high_battery", start_point2['latitude'], start_point2['longitude'], max_no_charge_distance=35.0)
        uav_high_battery.current_battery = 95  # 高电量
        
        path_high, distance_high = uav_high_battery.calculate_shortest_path_dijkstra(
            start_point2['latitude'], start_point2['longitude'], 
            end_point2['latitude'], end_point2['longitude'], 
            extended_waypoints[2:8]
        )
        
        test_results.append(("High Battery Short Distance", distance_high, len(path_high)))
        print(f"High battery route: {distance_high:.2f} km, {len(path_high)} waypoints")
        
        # 绘制场景2
        plot_path(axes[0, 1], path_high, charging_stations, "High Battery Short Distance", 'green')
        
        # 场景3: 多点配送路线测试
        print(f"\n=== Scenario 3: Multi-Point Delivery Route Test ===")
        depot = extended_waypoints[0]
        customers = extended_waypoints[1:4]  # 3个客户
        
        uav_multi = UAV(env, "uav_multi", depot['latitude'], depot['longitude'], max_no_charge_distance=28.0)
        uav_multi.current_battery = 70
        
        # 构建多点路径
        multi_path = [depot]
        total_multi_distance = 0
        current_pos = depot
        
        for customer in customers:
            segment_path, segment_dist = uav_multi.calculate_shortest_path_dijkstra(
                current_pos['latitude'], current_pos['longitude'],
                customer['latitude'], customer['longitude'],
                extended_waypoints[5:] if len(multi_path) > 1 else extended_waypoints[4:]
            )
            multi_path.extend(segment_path[1:])  # 排除起点重复
            total_multi_distance += segment_dist
            current_pos = customer
        
        test_results.append(("Multi-Point Delivery", total_multi_distance, len(multi_path)))
        print(f"Multi-point route: {total_multi_distance:.2f} km, {len(multi_path)} waypoints")
        
        # 绘制场景3
        plot_path(axes[1, 0], multi_path, charging_stations, "Multi-Point Delivery Route", 'blue')
        
        # 场景4: 电池约束优化测试
        print(f"\n=== Scenario 4: Battery Constraint Optimization Test ===")
        uav_optimized = UAV(env, "uav_optimized", depot['latitude'], depot['longitude'], max_no_charge_distance=15.0)
        uav_optimized.current_battery = 45  # 中等电量，需要优化
        
        path_optimized, distance_optimized = uav_optimized.plan_shortest_route_with_constraints(
            depot['latitude'], depot['longitude'],
            extended_waypoints[9]['latitude'], extended_waypoints[9]['longitude'],  # service4
            extended_waypoints[1:9], charging_stations
        )
        
        test_results.append(("Battery Constraint Optimized", distance_optimized, len(path_optimized)))
        print(f"Optimized route: {distance_optimized:.2f} km, {len(path_optimized)} waypoints")
        
        # 绘制场景4
        plot_path(axes[1, 1], path_optimized, charging_stations, "Battery Constraint Optimized", 'purple')
        
        # 场景5: 极限距离测试
        print(f"\n=== Scenario 5: Extreme Distance Challenge Test ===")
        extreme_start = extended_waypoints[0]
        extreme_end = extended_waypoints[10]  # service5 (最远点)
        
        uav_extreme = UAV(env, "uav_extreme", extreme_start['latitude'], extreme_start['longitude'], max_no_charge_distance=40.0)
        uav_extreme.current_battery = 30  # 低电量面对极限挑战
        
        path_extreme, distance_extreme = uav_extreme.plan_shortest_route_with_constraints(
            extreme_start['latitude'], extreme_start['longitude'],
            extreme_end['latitude'], extreme_end['longitude'],
            extended_waypoints[1:], charging_stations
        )
        
        test_results.append(("Extreme Distance Challenge", distance_extreme, len(path_extreme)))
        print(f"Extreme distance route: {distance_extreme:.2f} km, {len(path_extreme)} waypoints")
        
        # 绘制场景5
        plot_path(axes[2, 0], path_extreme, charging_stations, "Extreme Distance Challenge", 'orange')
        
        # 场景6: 性能基准测试
        print(f"\n=== Scenario 6: Performance Benchmark Test ===")
        
        # 测试多种算法性能
        benchmark_results = []
        test_pairs = [
            (extended_waypoints[0], extended_waypoints[3]),
            (extended_waypoints[1], extended_waypoints[7]),
            (extended_waypoints[2], extended_waypoints[8])
        ]
        
        performance_data = []
        
        for i, (start, end) in enumerate(test_pairs):
            uav_benchmark = UAV(env, f"uav_benchmark_{i}", start['latitude'], start['longitude'], max_no_charge_distance=25.0)
            uav_benchmark.current_battery = 60
            
            # 测试Dijkstra算法性能
            start_time = time.time()
            path_dijkstra, dist_dijkstra = uav_benchmark.calculate_shortest_path_dijkstra(
                start['latitude'], start['longitude'],
                end['latitude'], end['longitude'],
                extended_waypoints[4:8]
            )
            dijkstra_time = time.time() - start_time
            
            # 测试约束路径算法性能
            start_time = time.time()
            path_constrained, dist_constrained = uav_benchmark.plan_shortest_route_with_constraints(
                start['latitude'], start['longitude'],
                end['latitude'], end['longitude'],
                extended_waypoints[4:8], charging_stations
            )
            constrained_time = time.time() - start_time
            
            performance_data.append({
                'pair': i+1,
                'dijkstra_dist': dist_dijkstra,
                'dijkstra_time': dijkstra_time,
                'constrained_dist': dist_constrained,
                'constrained_time': constrained_time
            })
        
        # 绘制性能对比图
        ax_perf = axes[2, 1]
        algorithms = ['Dijkstra', 'Constrained']
        avg_distances = [
            np.mean([p['dijkstra_dist'] for p in performance_data]),
            np.mean([p['constrained_dist'] for p in performance_data])
        ]
        avg_times = [
            np.mean([p['dijkstra_time'] for p in performance_data]) * 1000,  # 转换为毫秒
            np.mean([p['constrained_time'] for p in performance_data]) * 1000
        ]
        
        # 双Y轴图表
        ax_perf2 = ax_perf.twinx()
        
        bars1 = ax_perf.bar([x-0.2 for x in range(len(algorithms))], avg_distances, 0.4, 
                           label='Average Distance (km)', color='skyblue', alpha=0.7)
        bars2 = ax_perf2.bar([x+0.2 for x in range(len(algorithms))], avg_times, 0.4, 
                            label='Average Time (ms)', color='lightcoral', alpha=0.7)
        
        ax_perf.set_xlabel('Algorithm')
        ax_perf.set_ylabel('Distance (km)', color='blue')
        ax_perf2.set_ylabel('Computation Time (ms)', color='red')
        ax_perf.set_title('Performance Benchmark Comparison', fontweight='bold')
        ax_perf.set_xticks(range(len(algorithms)))
        ax_perf.set_xticklabels(algorithms)
        
        # 添加数值标签
        for bar, dist in zip(bars1, avg_distances):
            height = bar.get_height()
            ax_perf.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{dist:.2f}km', ha='center', va='bottom')
        
        for bar, time_val in zip(bars2, avg_times):
            height = bar.get_height()
            ax_perf2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                         f'{time_val:.2f}ms', ha='center', va='bottom')
        
        test_results.append(("Performance Benchmark", np.mean(avg_distances), len(algorithms)))
        print(f"Performance benchmark completed: Avg distance {np.mean(avg_distances):.2f} km")
        
        # 综合结果分析
        print(f"\n=== Extended Scenarios Results Summary ===")
        print(f"{'Scenario':<30} {'Distance(km)':<12} {'Waypoints':<10} {'Complexity':<12}")
        print("-" * 70)
        
        for name, distance, waypoints in test_results:
            complexity = "High" if waypoints > 5 else "Medium" if waypoints > 3 else "Low"
            print(f"{name:<30} {distance:<12.2f} {waypoints:<10} {complexity:<12}")
        
        # 保存扩展测试图表
        plt.tight_layout()
        extended_plot_path = os.path.join(plot_dir, 'uav_extended_scenarios.png')
        plt.savefig(extended_plot_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Extended scenarios chart saved as '{extended_plot_path}'")
        
        # 运行扩展仿真测试
        print(f"\n=== Extended Simulation Testing ===")
        
        # 创建多个测试订单
        test_orders = []
        for i in range(5):
            goods = Goods(env, f"goods_{i:03d}", weight=1.0 + i*0.5, priority=1 + (i % 3))
            order = Order(env, i+1, f"customer{i+1}", f"service{i+1}", goods, 'direct', priority=1 + (i % 3))
            test_orders.append(order)
        
        # 模拟并行订单执行
        def simulate_multiple_orders():
            for i, order in enumerate(test_orders):
                order.start_time = env.now + i * 5  # 错开开始时间
                order.status = 'in_progress'
                
                # 模拟不同的配送时间
                delivery_time = 15.0 + i * 3.0 + np.random.uniform(0, 5)
                yield env.timeout(delivery_time)
                
                order.completion_time = env.now
                order.status = 'completed'
                
                total_time = order.completion_time - order.creation_time
                print(f"  Order {order.order_id} completed: {total_time:.2f} time units")
        
        # 运行扩展仿真
        env.process(simulate_multiple_orders())
        env.run(until=120)  # 运行120个时间单位
        
        plt.show()
        
        print("✓ Extended scenario testing completed successfully")
        return True
        
    except Exception as e:
        print(f"Extended scenario testing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mixed_transportation_modes():
    """Test mixed transportation modes with detailed visualization of charging station usage, UAV paths, and truck trajectories"""
    print("\n" + "=" * 60)
    print("Test 7: Mixed Transportation Mode Testing")
    print("=" * 60)
    
    try:
        # 获取全局文件夹路径
        global plot_dir, result_dir
        
        from models.uav_classes import UAV, calculate_distance, Order, Goods
        from models.charging_station import ChargingStation
        from models.distribution_center import DistributionCenter
        import simpy
        import matplotlib.pyplot as plt
        import numpy as np
        import time
        from collections import defaultdict
        
        env = simpy.Environment()
        
        # 创建测试基础设施
        print("Setting up mixed transportation test infrastructure...")
        
        # 创建不同类型的充电站
        charging_stations = [
            ChargingStation(env, "fast_cs1", 39.9100, 116.4100, battery_type='unlimited', service_time=0.3),
            ChargingStation(env, "slow_cs1", 39.9200, 116.4200, battery_type='limited', battery_capacity=10, service_windows=2, service_time=0.8),
            ChargingStation(env, "fast_cs2", 39.9300, 116.4300, battery_type='unlimited', service_time=0.2),
            ChargingStation(env, "slow_cs2", 39.9150, 116.4350, battery_type='limited', battery_capacity=8, service_windows=3, service_time=1.0),
            ChargingStation(env, "medium_cs", 39.9250, 116.4150, battery_type='limited', battery_capacity=15, service_windows=4, service_time=0.5),
        ]
        
        # 创建单个配送中心
        distribution_center = DistributionCenter(env, "main_dc", 39.9200, 116.4250)
        
        # 创建单个服务点
        service_point = {'id': 'service_point_1', 'latitude': 39.9350, 'longitude': 116.4400, 'type': 'service'}
        
        # 创建多个需求点（客户）
        demand_points = [
            {'id': 'customer_1', 'latitude': 39.9080, 'longitude': 116.4120, 'type': 'customer'},
            {'id': 'customer_2', 'latitude': 39.9180, 'longitude': 116.4180, 'type': 'customer'},
            {'id': 'customer_3', 'latitude': 39.9280, 'longitude': 116.4280, 'type': 'customer'},
            {'id': 'customer_4', 'latitude': 39.9380, 'longitude': 116.4380, 'type': 'customer'},
            {'id': 'customer_5', 'latitude': 39.9120, 'longitude': 116.4320, 'type': 'customer'},
            {'id': 'customer_6', 'latitude': 39.9220, 'longitude': 116.4420, 'type': 'customer'},
            {'id': 'customer_7', 'latitude': 39.9050, 'longitude': 116.4250, 'type': 'customer'},
            {'id': 'customer_8', 'latitude': 39.9150, 'longitude': 116.4050, 'type': 'customer'},
        ]
        
        print(f"Created {len(charging_stations)} charging stations")
        print(f"Created 1 distribution center: {distribution_center.center_id}")
        print(f"Created 1 service point: {service_point['id']}")
        print(f"Created {len(demand_points)} demand points")
        
        # 准备可视化图表 - 分开保存
        print("Preparing separate visualizations...")
        
        # 数据收集容器
        charging_usage_data = defaultdict(list)
        uav_path_data = []
        truck_trajectory_data = []
        delivery_stats = {'direct': [], 'distribution_center': []}
        
        # 需求生成和处理统计
        demand_stats = {
            'total_generated': 0,
            'total_completed': 0,
            'total_failed': 0,
            'completion_times': [],
            'satisfaction_rate': 0.0,
            'avg_completion_time': 0.0
        }
        
        # 创建订单队列和统计
        orders = []
        order_queue = []  # 等待处理的订单队列
        active_orders = []  # 正在处理的订单
        completed_orders = []  # 已完成的订单
        failed_orders = []  # 失败的订单
        
        # 统一使用最短路径算法
        # 可选择的路径规划模式：'shortest_path', 'nearest_charging', 'given_path'
        PATH_PLANNING_MODE = 'shortest_path'  # 统一的路径规划模式
        
        print(f"All UAVs will use {PATH_PLANNING_MODE} for route planning")
        print("Setting up Poisson demand generation process...")
        
        # 创建UAV实例用于测试
        uavs = []
        for i in range(6):  # 增加UAV数量以处理更多需求
            uav = UAV(env, f"uav_{i+1}", 39.9200, 116.4200, max_no_charge_distance=20.0)
            uav.current_battery = 60 + i*5  # 不同的初始电量
            uav.is_busy = False  # 添加忙碌状态标记
            uavs.append(uav)
        
        # 仿真过程跟踪函数
        def poisson_demand_generator():
            """泊松分布需求生成器"""
            order_id = 1
            arrival_rate = 2.0  # 平均每个时间单位生成2个需求
            
            while True:
                # 等待下一个需求到达（指数分布间隔时间）
                inter_arrival_time = np.random.exponential(1.0 / arrival_rate)
                yield env.timeout(inter_arrival_time)
                
                # 随机选择客户点
                customer = np.random.choice(demand_points)
                
                # 创建货物
                goods = Goods(env, f"goods_{order_id:03d}", 
                            weight=np.random.uniform(0.5, 3.0), 
                            priority=np.random.randint(1, 4))
                
                # 50%概率直接配送，50%概率配送中心
                delivery_mode = 'direct' if np.random.random() < 0.5 else 'distribution_center'
                
                # 创建订单
                order = Order(env, order_id, customer['id'], service_point['id'], 
                            goods, delivery_mode, priority=goods.priority)
                order.creation_time = env.now
                order.customer_location = customer
                
                # 添加到订单队列
                order_queue.append(order)
                demand_stats['total_generated'] += 1
                
                print(f"Time {env.now:.1f}: Generated Order {order_id} - {customer['id']} -> {service_point['id']}, Mode: {delivery_mode}")
                
                order_id += 1
                
                # 如果仿真快结束，停止生成新需求
                if env.now > 120:  # 在仿真最后30个时间单位停止生成
                    break
        
        def order_dispatcher():
            """订单分派器 - 将订单分配给可用的UAV"""
            while True:
                # 检查是否有等待的订单和可用的UAV
                if order_queue and any(not uav.is_busy for uav in uavs):
                    # 获取下一个订单
                    order = order_queue.pop(0)
                    
                    # 寻找可用的UAV
                    available_uav = None
                    for uav in uavs:
                        if not uav.is_busy:
                            available_uav = uav
                            break
                    
                    if available_uav:
                        # 分配订单给UAV
                        available_uav.is_busy = True
                        active_orders.append(order)
                        order.assigned_uav = available_uav
                        order.start_time = env.now
                        
                        # 启动订单处理
                        env.process(process_single_order(order, available_uav))
                        
                        print(f"Time {env.now:.1f}: Assigned Order {order.order_id} to {available_uav.uav_id}")
                
                yield env.timeout(0.5)  # 每0.5个时间单位检查一次
        
        def track_charging_usage():
            """跟踪充电站使用情况"""
            while True:
                current_time = env.now
                for cs in charging_stations:
                    # 记录每个充电站的使用情况
                    active_windows = sum(1 for busy in cs.window_busy if busy)
                    charging_usage_data[cs.station_id].append({
                        'time': current_time,
                        'active_windows': active_windows,
                        'queue_length': sum(len(queue) for queue in cs.queues),
                        'available_batteries': cs.available_batteries if cs.battery_type == 'limited' else 999
                    })
                yield env.timeout(2.0)  # 每2个时间单位记录一次
        
        def process_single_order(order, uav):
            """处理单个订单"""
            try:
                customer = order.customer_location
                order.status = 'in_progress'
                
                # 保存路径数据到本地文件
                path_log_file = os.path.join(result_dir, "uav_truck_paths_log.txt")
                
                # 初始化日志文件（仅第一次）
                if order.order_id == 1:
                    with open(path_log_file, 'w', encoding='utf-8') as f:
                        f.write("=== UAV & Truck Route Planning Log ===\n")
                        f.write(f"Path Planning Mode: {PATH_PLANNING_MODE}\n")
                        f.write(f"Demand Generation: Poisson Process (λ=2.0)\n")
                        f.write(f"Delivery Mode: 50% Direct, 50% Distribution Center\n")
                        f.write(f"Simulation Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # 根据统一的路径规划模式选择算法
                def get_path_by_mode(start_lat, start_lon, end_lat, end_lon):
                    if PATH_PLANNING_MODE == 'shortest_path':
                        return uav.plan_shortest_route_with_constraints(
                            start_lat, start_lon, end_lat, end_lon, [], charging_stations
                        )
                    elif PATH_PLANNING_MODE == 'nearest_charging':
                        # 使用最近充电站策略
                        nearest_station = uav.find_nearest_charging_station(charging_stations)
                        path = [
                            {'id': 'start', 'latitude': start_lat, 'longitude': start_lon, 'type': 'start'},
                            {'id': f'charging_{nearest_station.station_id}', 'latitude': nearest_station.latitude, 
                             'longitude': nearest_station.longitude, 'type': 'charging'},
                            {'id': 'end', 'latitude': end_lat, 'longitude': end_lon, 'type': 'end'}
                        ]
                        distance = (calculate_distance(start_lat, start_lon, nearest_station.latitude, nearest_station.longitude) +
                                  calculate_distance(nearest_station.latitude, nearest_station.longitude, end_lat, end_lon))
                        return path, distance
                    else:  # given_path - 简单直线路径
                        path = [
                            {'id': 'start', 'latitude': start_lat, 'longitude': start_lon, 'type': 'start'},
                            {'id': 'end', 'latitude': end_lat, 'longitude': end_lon, 'type': 'end'}
                        ]
                        distance = calculate_distance(start_lat, start_lon, end_lat, end_lon)
                        return path, distance
                
                if order.delivery_mode == 'direct':
                    # 直接运输模式
                    # 从UAV位置到客户点
                    path_to_customer, dist_to_customer = get_path_by_mode(
                        uav.current_latitude, uav.current_longitude,
                        customer['latitude'], customer['longitude']
                    )
                    
                    # 从客户点到服务点
                    path_to_service, dist_to_service = get_path_by_mode(
                        customer['latitude'], customer['longitude'],
                        service_point['latitude'], service_point['longitude']
                    )
                    
                    total_distance = dist_to_customer + dist_to_service
                    delivery_time = total_distance * 0.8 + 2.0  # 基于距离的时间加上装卸时间
                    
                    # 记录UAV路径
                    full_path = path_to_customer + path_to_service[1:]  # 合并路径
                    uav_path_data.append({
                        'order_id': order.order_id,
                        'mode': 'direct',
                        'path': full_path,
                        'distance': total_distance,
                        'uav_id': uav.uav_id,
                        'planning_mode': PATH_PLANNING_MODE
                    })
                    
                    # 保存路径到文件
                    with open(path_log_file, 'a', encoding='utf-8') as f:
                        f.write(f"\n--- Order {order.order_id} (Direct Delivery) ---\n")
                        f.write(f"Creation Time: {order.creation_time:.2f}\n")
                        f.write(f"Start Time: {order.start_time:.2f}\n")
                        f.write(f"UAV ID: {uav.uav_id}\n")
                        f.write(f"Path Planning: {PATH_PLANNING_MODE}\n")
                        f.write(f"Total Distance: {total_distance:.2f} km\n")
                        f.write(f"Estimated Delivery Time: {delivery_time:.2f}\n")
                        f.write(f"Waypoints ({len(full_path)}):\n")
                        for j, wp in enumerate(full_path):
                            f.write(f"  {j+1}. {wp['id']}: ({wp['latitude']:.4f}, {wp['longitude']:.4f}) - {wp.get('type', 'waypoint')}\n")
                    
                else:
                    # 配送中心模式
                    # 从客户点到配送中心
                    path_to_dc, dist_to_dc = get_path_by_mode(
                        customer['latitude'], customer['longitude'],
                        distribution_center.latitude, distribution_center.longitude
                    )
                    
                    delivery_time = dist_to_dc * 0.8 + 5.0  # 配送中心处理时间更长
                    
                    # 记录UAV到配送中心的路径
                    uav_path_data.append({
                        'order_id': order.order_id,
                        'mode': 'to_distribution_center',
                        'path': path_to_dc,
                        'distance': dist_to_dc,
                        'uav_id': uav.uav_id,
                        'planning_mode': PATH_PLANNING_MODE
                    })
                    
                    # 模拟卡车从配送中心到服务点
                    truck_distance = calculate_distance(
                        distribution_center.latitude, distribution_center.longitude,
                        service_point['latitude'], service_point['longitude']
                    )
                    truck_time = truck_distance * 1.2 + 3.0  # 卡车速度较慢
                    
                    truck_trajectory_data.append({
                        'order_id': order.order_id,
                        'start_point': {'lat': distribution_center.latitude, 'lon': distribution_center.longitude},
                        'end_point': {'lat': service_point['latitude'], 'lon': service_point['longitude']},
                        'distance': truck_distance,
                        'time': truck_time
                    })
                    
                    delivery_time += truck_time
                    
                    # 保存路径到文件
                    with open(path_log_file, 'a', encoding='utf-8') as f:
                        f.write(f"\n--- Order {order.order_id} (Distribution Center) ---\n")
                        f.write(f"Creation Time: {order.creation_time:.2f}\n")
                        f.write(f"Start Time: {order.start_time:.2f}\n")
                        f.write(f"UAV ID: {uav.uav_id}\n")
                        f.write(f"UAV Path Planning: {PATH_PLANNING_MODE}\n")
                        f.write(f"UAV Distance: {dist_to_dc:.2f} km\n")
                        f.write(f"Estimated Delivery Time: {delivery_time:.2f}\n")
                        f.write(f"UAV Waypoints ({len(path_to_dc)}):\n")
                        for j, wp in enumerate(path_to_dc):
                            f.write(f"  {j+1}. {wp['id']}: ({wp['latitude']:.4f}, {wp['longitude']:.4f}) - {wp.get('type', 'waypoint')}\n")
                        f.write(f"Truck Distance: {truck_distance:.2f} km\n")
                        f.write(f"Truck Route: DC({distribution_center.latitude:.4f}, {distribution_center.longitude:.4f}) -> SP({service_point['latitude']:.4f}, {service_point['longitude']:.4f})\n")
                
                # 等待配送完成
                yield env.timeout(delivery_time)
                
                # 订单完成
                order.completion_time = env.now
                order.status = 'completed'
                
                # 更新统计数据
                total_time = order.completion_time - order.creation_time
                waiting_time = order.start_time - order.creation_time
                service_time = order.completion_time - order.start_time
                
                delivery_stats[order.delivery_mode].append({
                    'order_id': order.order_id,
                    'total_time': total_time,
                    'waiting_time': waiting_time,
                    'service_time': service_time,
                    'delivery_time': delivery_time,
                    'distance': total_distance if order.delivery_mode == 'direct' else dist_to_dc
                })
                
                # 更新全局统计
                demand_stats['total_completed'] += 1
                demand_stats['completion_times'].append(total_time)
                
                # 移动到已完成队列
                if order in active_orders:
                    active_orders.remove(order)
                completed_orders.append(order)
                
                # 释放UAV
                uav.is_busy = False
                
                print(f"Time {env.now:.1f}: Order {order.order_id} completed - Total time: {total_time:.2f}, Waiting: {waiting_time:.2f}, Service: {service_time:.2f}")
                
            except Exception as e:
                # 订单失败
                order.status = 'failed'
                order.failure_reason = str(e)
                
                if order in active_orders:
                    active_orders.remove(order)
                failed_orders.append(order)
                
                demand_stats['total_failed'] += 1
                uav.is_busy = False
                
                print(f"Time {env.now:.1f}: Order {order.order_id} failed - Reason: {e}")
        
        def statistics_collector():
            """统计数据收集器"""
            while True:
                yield env.timeout(10.0)  # 每10个时间单位更新统计
                
                # 计算满足率
                total_processed = demand_stats['total_completed'] + demand_stats['total_failed']
                if total_processed > 0:
                    demand_stats['satisfaction_rate'] = demand_stats['total_completed'] / total_processed * 100
                
                # 计算平均完成时间
                if demand_stats['completion_times']:
                    demand_stats['avg_completion_time'] = np.mean(demand_stats['completion_times'])
                
                print(f"Time {env.now:.1f}: Stats - Generated: {demand_stats['total_generated']}, "
                      f"Completed: {demand_stats['total_completed']}, "
                      f"Failed: {demand_stats['total_failed']}, "
                      f"Queue: {len(order_queue)}, "
                      f"Active: {len(active_orders)}, "
                      f"Satisfaction Rate: {demand_stats['satisfaction_rate']:.1f}%, "
                      f"Avg Completion Time: {demand_stats['avg_completion_time']:.2f}")
        
        def simulate_mixed_deliveries():
            """启动混合运输仿真的主函数（已简化，逻辑移至其他函数）"""
            # 仿真结束后保存总结
            yield env.timeout(149)  # 等到仿真快结束
            
            path_log_file = os.path.join(result_dir, "uav_truck_paths_log.txt")
            with open(path_log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n=== Final Simulation Summary ===\n")
                f.write(f"Total Demands Generated: {demand_stats['total_generated']}\n")
                f.write(f"Total Orders Completed: {demand_stats['total_completed']}\n")
                f.write(f"Total Orders Failed: {demand_stats['total_failed']}\n")
                f.write(f"Orders in Queue: {len(order_queue)}\n")
                f.write(f"Active Orders: {len(active_orders)}\n")
                f.write(f"Satisfaction Rate: {demand_stats['satisfaction_rate']:.2f}%\n")
                f.write(f"Average Completion Time: {demand_stats['avg_completion_time']:.2f}\n")
                f.write(f"UAV Routes Generated: {len(uav_path_data)}\n")
                f.write(f"Truck Routes Generated: {len(truck_trajectory_data)}\n")
                f.write(f"Path Planning Mode: {PATH_PLANNING_MODE}\n")
                f.write(f"Simulation End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"\n✓ Route paths and demand statistics saved to: {path_log_file}")
        
        # 启动仿真进程
        env.process(poisson_demand_generator())
        env.process(order_dispatcher())
        env.process(track_charging_usage())
        env.process(statistics_collector())
        env.process(simulate_mixed_deliveries())
        
        # 运行仿真
        print(f"\nRunning Poisson demand generation simulation for 150 time units...")
        print("Demand arrival rate: λ=2.0 demands per time unit")
        print("Delivery mode: 50% direct, 50% distribution center")
        env.run(until=150)
        
        # 保存仿真数据到numpy文件
        print("\nSaving simulation data to files...")
        
        # 保存统计数据
        stats_data = {
            'total_generated': demand_stats['total_generated'],
            'total_completed': demand_stats['total_completed'],
            'total_failed': demand_stats['total_failed'],
            'satisfaction_rate': demand_stats['satisfaction_rate'],
            'avg_completion_time': demand_stats['avg_completion_time'],
            'completion_times': demand_stats['completion_times'],
            'queue_length': len(order_queue),
            'active_orders': len(active_orders)
        }
        stats_file = os.path.join(result_dir, 'simulation_statistics.npz')
        np.savez(stats_file, **stats_data)
        
        # 保存路径数据
        if uav_path_data:
            uav_paths_array = np.array([(p['order_id'], p['mode'], p['distance'], p['uav_id']) for p in uav_path_data])
            uav_paths_file = os.path.join(result_dir, 'uav_paths_data.npy')
            np.save(uav_paths_file, uav_paths_array)
        
        if truck_trajectory_data:
            truck_data_array = np.array([(t['order_id'], t['distance'], t['time']) for t in truck_trajectory_data])
            truck_file = os.path.join(result_dir, 'truck_trajectory_data.npy')
            np.save(truck_file, truck_data_array)
        
        # 保存配送统计数据
        if delivery_stats['direct']:
            direct_stats = np.array([(d['order_id'], d['total_time'], d['waiting_time'], d['service_time'], d['distance']) 
                                   for d in delivery_stats['direct']])
            direct_file = os.path.join(result_dir, 'direct_delivery_stats.npy')
            np.save(direct_file, direct_stats)
        
        if delivery_stats['distribution_center']:
            dc_stats = np.array([(d['order_id'], d['total_time'], d['waiting_time'], d['service_time'], d['distance']) 
                               for d in delivery_stats['distribution_center']])
            dc_file = os.path.join(result_dir, 'distribution_center_stats.npy')
            np.save(dc_file, dc_stats)
        
        print("✓ Simulation data saved to .npy and .npz files")
        
        # 分别创建和保存各个图表
        create_separate_visualizations(charging_usage_data, uav_path_data, truck_trajectory_data, 
                                     delivery_stats, demand_stats, charging_stations, 
                                     distribution_center, service_point, demand_points, plot_dir, result_dir)
        
        return True
        
    except Exception as e:
        print(f"Mixed transportation mode testing failed: {e}")
        traceback.print_exc()
        return False


def create_separate_visualizations(charging_usage_data, uav_path_data, truck_trajectory_data, 
                                 delivery_stats, demand_stats, charging_stations, 
                                 distribution_center, service_point, demand_points, plot_dir, result_dir):
    """创建分离的可视化图表"""
    import matplotlib.pyplot as plt
    
    print("\nCreating separate visualization charts...")
    print(f"Saving charts to: {plot_dir}")
    print(f"Saving data tables to: {result_dir}")
    
    # 图表1: 充电站使用时间分析
    plt.figure(figsize=(12, 8))
    for cs_id, usage_data in charging_usage_data.items():
        times = [data['time'] for data in usage_data]
        active_windows = [data['active_windows'] for data in usage_data]
        plt.plot(times, active_windows, label=f'{cs_id}', linewidth=2, marker='o', markersize=3)
    
    plt.title('Charging Station Usage Over Time', fontweight='bold', fontsize=14)
    plt.xlabel('Time')
    plt.ylabel('Active Charging Windows')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    chart1_path = os.path.join(plot_dir, '01_charging_station_usage.png')
    plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {chart1_path}")
    
    # 图表2: UAV和卡车综合路径图
    plt.figure(figsize=(14, 10))
    
    # 绘制基础设施
    cs_lats = [cs.latitude for cs in charging_stations]
    cs_lons = [cs.longitude for cs in charging_stations]
    plt.scatter(cs_lons, cs_lats, c='orange', s=150, marker='s', 
               label='Charging Stations', alpha=0.8, edgecolors='black')
    
    plt.scatter(distribution_center.longitude, distribution_center.latitude, 
               c='blue', s=200, marker='D', label='Distribution Center', 
               alpha=0.8, edgecolors='black')
    
    plt.scatter(service_point['longitude'], service_point['latitude'], 
               c='green', s=200, marker='^', label='Service Point', 
               alpha=0.8, edgecolors='black')
    
    # 绘制需求点
    demand_lats = [dp['latitude'] for dp in demand_points]
    demand_lons = [dp['longitude'] for dp in demand_points]
    plt.scatter(demand_lons, demand_lats, c='red', s=100, marker='o', 
               label='Demand Points', alpha=0.7, edgecolors='black')
    
    # 绘制UAV路径 (前10条以免过于密集)
    uav_colors = ['purple', 'brown', 'pink', 'gray', 'cyan', 'magenta', 'olive', 'navy', 'lime', 'coral']
    for i, path_data in enumerate(uav_path_data[:10]):  # 只显示前10条路径
        path = path_data['path']
        color = uav_colors[i % len(uav_colors)]
        path_lats = [wp['latitude'] for wp in path]
        path_lons = [wp['longitude'] for wp in path]
        
        plt.plot(path_lons, path_lats, color=color, linewidth=2, 
                linestyle='-', alpha=0.8, marker='o', markersize=3,
                label=f"UAV-{path_data['order_id']} ({path_data['mode'][:6]})")
    
    # 绘制卡车轨迹 (前5条)
    truck_colors = ['darkgreen', 'darkblue', 'darkred', 'darkorange', 'darkviolet']
    for i, truck_data in enumerate(truck_trajectory_data[:5]):  # 只显示前5条轨迹
        start = truck_data['start_point']
        end = truck_data['end_point']
        color = truck_colors[i % len(truck_colors)]
        
        plt.plot([start['lon'], end['lon']], [start['lat'], end['lat']], 
                color=color, linewidth=3, linestyle='--', alpha=0.8,
                label=f"Truck-{truck_data['order_id']}")
        
        # 添加箭头指示方向
        plt.annotate('', xy=(end['lon'], end['lat']), xytext=(start['lon'], start['lat']),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2, alpha=0.8))
    
    plt.title('Integrated UAV & Truck Transportation Routes\n(UAV: solid lines, Truck: dashed lines)', 
             fontweight='bold', fontsize=14)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    chart2_path = os.path.join(plot_dir, '02_integrated_routes.png')
    plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {chart2_path}")
    
    # 图表3: 充电站电池可用性
    plt.figure(figsize=(12, 8))
    limited_stations = [cs for cs in charging_stations if cs.battery_type == 'limited']
    
    for cs in limited_stations:
        if cs.station_id in charging_usage_data:
            times = [data['time'] for data in charging_usage_data[cs.station_id]]
            batteries = [data['available_batteries'] for data in charging_usage_data[cs.station_id]]
            plt.plot(times, batteries, label=f'{cs.station_id}', linewidth=2, marker='s', markersize=3)
    
    plt.title('Battery Availability at Limited Charging Stations', fontweight='bold', fontsize=14)
    plt.xlabel('Time')
    plt.ylabel('Available Batteries')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    chart3_path = os.path.join(plot_dir, '03_battery_availability.png')
    plt.savefig(chart3_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {chart3_path}")
    
    # 图表4: 运输模式性能对比
    plt.figure(figsize=(10, 8))
    
    # 计算统计数据
    direct_times = [stat['total_time'] for stat in delivery_stats['direct']]
    dc_times = [stat['total_time'] for stat in delivery_stats['distribution_center']]
    
    # 箱线图
    box_data = [direct_times, dc_times]
    box_labels = ['Direct\nDelivery', 'Distribution\nCenter']
    
    bp = plt.boxplot(box_data, labels=box_labels, patch_artist=True)
    if len(bp['boxes']) > 0:
        bp['boxes'][0].set_facecolor('lightblue')
    if len(bp['boxes']) > 1:
        bp['boxes'][1].set_facecolor('lightcoral')
    
    plt.title('Delivery Time Comparison by Mode', fontweight='bold', fontsize=14)
    plt.ylabel('Total Delivery Time')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    chart4_path = os.path.join(plot_dir, '04_delivery_time_comparison.png')
    plt.savefig(chart4_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {chart4_path}")
    
    # 图表5: 系统总体性能指标
    plt.figure(figsize=(12, 8))
    
    # 性能指标
    direct_times = [stat['total_time'] for stat in delivery_stats['direct']]
    dc_times = [stat['total_time'] for stat in delivery_stats['distribution_center']]
    direct_distances = [stat['distance'] for stat in delivery_stats['direct']]
    dc_distances = [stat['distance'] for stat in delivery_stats['distribution_center']]
    
    metrics = ['Avg Direct Time', 'Avg DC Time', 'Avg Direct Dist', 'Avg DC Dist', 'Satisfaction Rate']
    values = [
        np.mean(direct_times) if direct_times else 0,
        np.mean(dc_times) if dc_times else 0,
        np.mean(direct_distances) if direct_distances else 0,
        np.mean(dc_distances) if dc_distances else 0,
        demand_stats['satisfaction_rate']
    ]
    
    bars = plt.bar(range(len(metrics)), values, 
                  color=['skyblue', 'lightcoral', 'lightgreen', 'orange', 'purple'])
    
    plt.title('System Performance Metrics', fontweight='bold', fontsize=14)
    plt.ylabel('Value')
    plt.xticks(range(len(metrics)), metrics, rotation=45, ha='right')
    
    # 添加数值标签
    for bar, val in zip(bars, values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    chart5_path = os.path.join(plot_dir, '05_performance_metrics.png')
    plt.savefig(chart5_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {chart5_path}")
    
    # 图表6: 需求生成和处理统计
    plt.figure(figsize=(12, 8))
    
    # 创建两个子图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左图：需求统计饼图
    labels = ['Completed', 'Failed', 'In Queue', 'Active']
    sizes = [demand_stats['total_completed'], demand_stats['total_failed'], 
             len([]), len([])]  # 队列长度在这里无法获取，设为0
    colors = ['lightgreen', 'lightcoral', 'lightyellow', 'lightblue']
    
    # 过滤掉为0的数据
    filtered_labels = []
    filtered_sizes = []
    filtered_colors = []
    for label, size, color in zip(labels, sizes, colors):
        if size > 0:
            filtered_labels.append(label)
            filtered_sizes.append(size)
            filtered_colors.append(color)
    
    if filtered_sizes:
        ax1.pie(filtered_sizes, labels=filtered_labels, colors=filtered_colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Order Status Distribution', fontweight='bold')
    
    # 右图：完成时间分布直方图
    if demand_stats['completion_times']:
        ax2.hist(demand_stats['completion_times'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.set_xlabel('Completion Time')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Completion Time Distribution', fontweight='bold')
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    chart6_path = os.path.join(plot_dir, '06_demand_statistics.png')
    plt.savefig(chart6_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {chart6_path}")
    
    # 创建详细的数据报告表格
    create_detailed_data_tables(delivery_stats, demand_stats, charging_usage_data, result_dir)
    
    print("\n✓ All visualization charts created and saved separately")


def create_detailed_data_tables(delivery_stats, demand_stats, charging_usage_data, result_dir):
    """创建详细的数据表格"""
    import pandas as pd
    
    print("\nCreating detailed data tables...")
    print(f"Saving tables to: {result_dir}")
    
    try:
        # 表格1: 总体统计摘要
        summary_data = {
            'Metric': ['Total Generated', 'Total Completed', 'Total Failed', 
                      'Satisfaction Rate (%)', 'Avg Completion Time', 'Min Completion Time', 
                      'Max Completion Time', 'Std Completion Time'],
            'Value': [
                demand_stats['total_generated'],
                demand_stats['total_completed'], 
                demand_stats['total_failed'],
                demand_stats['satisfaction_rate'],
                demand_stats['avg_completion_time'],
                min(demand_stats['completion_times']) if demand_stats['completion_times'] else 0,
                max(demand_stats['completion_times']) if demand_stats['completion_times'] else 0,
                np.std(demand_stats['completion_times']) if demand_stats['completion_times'] else 0
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_file = os.path.join(result_dir, 'summary_statistics.csv')
        summary_df.to_csv(summary_file, index=False)
        print(f"✓ Saved: {summary_file}")
        
        # 表格2: 直接配送统计
        if delivery_stats['direct']:
            direct_df = pd.DataFrame(delivery_stats['direct'])
            direct_file = os.path.join(result_dir, 'direct_delivery_detailed.csv')
            direct_df.to_csv(direct_file, index=False)
            print(f"✓ Saved: {direct_file}")
        
        # 表格3: 配送中心配送统计
        if delivery_stats['distribution_center']:
            dc_df = pd.DataFrame(delivery_stats['distribution_center'])
            dc_file = os.path.join(result_dir, 'distribution_center_detailed.csv')
            dc_df.to_csv(dc_file, index=False)
            print(f"✓ Saved: {dc_file}")
        
        # 表格4: 配送模式对比
        comparison_data = {
            'Delivery_Mode': ['Direct', 'Distribution Center'],
            'Count': [len(delivery_stats['direct']), len(delivery_stats['distribution_center'])],
            'Avg_Total_Time': [
                np.mean([s['total_time'] for s in delivery_stats['direct']]) if delivery_stats['direct'] else 0,
                np.mean([s['total_time'] for s in delivery_stats['distribution_center']]) if delivery_stats['distribution_center'] else 0
            ],
            'Avg_Waiting_Time': [
                np.mean([s['waiting_time'] for s in delivery_stats['direct']]) if delivery_stats['direct'] else 0,
                np.mean([s['waiting_time'] for s in delivery_stats['distribution_center']]) if delivery_stats['distribution_center'] else 0
            ],
            'Avg_Service_Time': [
                np.mean([s['service_time'] for s in delivery_stats['direct']]) if delivery_stats['direct'] else 0,
                np.mean([s['service_time'] for s in delivery_stats['distribution_center']]) if delivery_stats['distribution_center'] else 0
            ],
            'Avg_Distance': [
                np.mean([s['distance'] for s in delivery_stats['direct']]) if delivery_stats['direct'] else 0,
                np.mean([s['distance'] for s in delivery_stats['distribution_center']]) if delivery_stats['distribution_center'] else 0
            ]
        }
        comparison_df = pd.DataFrame(comparison_data)
        comparison_file = os.path.join(result_dir, 'delivery_mode_comparison.csv')
        comparison_df.to_csv(comparison_file, index=False)
        print(f"✓ Saved: {comparison_file}")
        
        print("✓ All data tables created successfully")
        
    except ImportError:
        print("⚠ pandas not available, creating simple CSV files with basic data")
        
        # 简单的CSV创建（不使用pandas）
        simple_file = os.path.join(result_dir, 'simple_summary.csv')
        with open(simple_file, 'w', encoding='utf-8') as f:
            f.write("Metric,Value\n")
            f.write(f"Total Generated,{demand_stats['total_generated']}\n")
            f.write(f"Total Completed,{demand_stats['total_completed']}\n")
            f.write(f"Total Failed,{demand_stats['total_failed']}\n")
            f.write(f"Satisfaction Rate,{demand_stats['satisfaction_rate']:.2f}%\n")
            f.write(f"Avg Completion Time,{demand_stats['avg_completion_time']:.2f}\n")
        
        print(f"✓ Saved: {simple_file}")
        
        # 打印详细统计报告
        print(f"\n=== Poisson Demand Generation & Mixed Transportation Results ===")
        print(f"Total simulation time: 150 time units")
        print(f"Demand generation: Poisson process (λ=2.0 demands/time unit)")
        print(f"Expected demands: ~{150 * 2.0:.0f}, Actual generated: {demand_stats['total_generated']}")
        
        # 需求满足率和完成时间统计
        print(f"\n=== Demand Satisfaction Analysis ===")
        print(f"Total demands generated: {demand_stats['total_generated']}")
        print(f"Orders completed: {demand_stats['total_completed']}")
        print(f"Orders failed: {demand_stats['total_failed']}")
        print(f"Orders in queue: {len(order_queue)}")
        print(f"Active orders: {len(active_orders)}")
        print(f"Demand satisfaction rate: {demand_stats['satisfaction_rate']:.2f}%")
        print(f"Average completion time: {demand_stats['avg_completion_time']:.2f} time units")
        
        if demand_stats['completion_times']:
            completion_times = demand_stats['completion_times']
            print(f"Completion time statistics:")
            print(f"  Min: {min(completion_times):.2f} time units")
            print(f"  Max: {max(completion_times):.2f} time units")
            print(f"  Median: {np.median(completion_times):.2f} time units")
            print(f"  Std Dev: {np.std(completion_times):.2f} time units")
        
        # 配送模式分析
        direct_orders = [stat for stat in delivery_stats['direct']]
        dc_orders = [stat for stat in delivery_stats['distribution_center']]
        
        print(f"\n=== Delivery Mode Performance Analysis ===")
        print(f"Direct delivery orders: {len(direct_orders)} ({len(direct_orders)/(len(direct_orders)+len(dc_orders))*100:.1f}%)")
        print(f"Distribution center orders: {len(dc_orders)} ({len(dc_orders)/(len(direct_orders)+len(dc_orders))*100:.1f}%)")
        
        if direct_orders:
            direct_times = [stat['total_time'] for stat in direct_orders]
            direct_waiting = [stat['waiting_time'] for stat in direct_orders]
            direct_service = [stat['service_time'] for stat in direct_orders]
            direct_distances = [stat['distance'] for stat in direct_orders]
            
            print(f"\nDirect Delivery Performance:")
            print(f"  Average total time: {np.mean(direct_times):.2f} time units")
            print(f"  Average waiting time: {np.mean(direct_waiting):.2f} time units")
            print(f"  Average service time: {np.mean(direct_service):.2f} time units")
            print(f"  Average distance: {np.mean(direct_distances):.2f} km")
            print(f"  Min/Max total time: {min(direct_times):.2f}/{max(direct_times):.2f}")
        
        if dc_orders:
            dc_times = [stat['total_time'] for stat in dc_orders]
            dc_waiting = [stat['waiting_time'] for stat in dc_orders]
            dc_service = [stat['service_time'] for stat in dc_orders]
            dc_distances = [stat['distance'] for stat in dc_orders]
            
            print(f"\nDistribution Center Performance:")
            print(f"  Average total time: {np.mean(dc_times):.2f} time units")
            print(f"  Average waiting time: {np.mean(dc_waiting):.2f} time units")
            print(f"  Average service time: {np.mean(dc_service):.2f} time units")
            print(f"  Average UAV distance: {np.mean(dc_distances):.2f} km")
            print(f"  Min/Max total time: {min(dc_times):.2f}/{max(dc_times):.2f}")
        
        print(f"\nCharging Station Analysis:")
        for cs in charging_stations:
            if cs.station_id in charging_usage_data:
                max_usage = max(data['active_windows'] for data in charging_usage_data[cs.station_id])
                avg_queue = np.mean([data['queue_length'] for data in charging_usage_data[cs.station_id]])
                print(f"  {cs.station_id}: Max usage {max_usage}/{cs.service_windows} windows, Avg queue: {avg_queue:.1f}")
        
        print(f"\n=== System Efficiency Metrics ===")
        total_processed = demand_stats['total_completed'] + demand_stats['total_failed']
        if total_processed > 0:
            print(f"Processing efficiency: {demand_stats['total_completed']/total_processed*100:.2f}%")
        
        if demand_stats['total_generated'] > 0:
            throughput = demand_stats['total_completed'] / 150  # orders per time unit
            print(f"System throughput: {throughput:.3f} orders/time unit")
            print(f"Utilization rate: {demand_stats['total_completed']/demand_stats['total_generated']*100:.2f}%")
        
        print("\n✓ All data files, charts, and reports have been generated and saved locally")
        print("✓ Poisson demand generation and mixed transportation testing completed successfully")
        return True
        
    except Exception as e:
        print(f"Mixed transportation mode testing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def plot_path(ax, path, charging_stations, title, path_color):
    """绘制路径图"""
    # 绘制充电站
    cs_lats = [cs.latitude for cs in charging_stations]
    cs_lons = [cs.longitude for cs in charging_stations]
    ax.scatter(cs_lons, cs_lats, c='orange', s=100, marker='s', 
               label='Charging Stations', alpha=0.8, edgecolors='black')
    
    # 绘制路径点
    path_lats = [wp['latitude'] for wp in path]
    path_lons = [wp['longitude'] for wp in path]
    
    # 绘制路径线
    ax.plot(path_lons, path_lats, color=path_color, linewidth=2, 
            marker='o', markersize=6, label='Path')
    
    # 标记起点和终点
    ax.scatter(path_lons[0], path_lats[0], c='green', s=150, 
               marker='*', label='Start', edgecolors='black')
    ax.scatter(path_lons[-1], path_lats[-1], c='red', s=150, 
               marker='*', label='End', edgecolors='black')
    
    # 添加航点标签
    for i, wp in enumerate(path):
        wp_type = wp.get('type', 'waypoint')
        if wp_type == 'charging':
            marker_color = 'yellow'
        elif wp_type in ['customer', 'service']:
            marker_color = 'lightblue'
        else:
            marker_color = 'white'
            
        ax.annotate(f"{i+1}", (wp['longitude'], wp['latitude']), 
                   xytext=(5, 5), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=marker_color),
                   fontsize=8)
    
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')

def main():
    """Main test function"""
    print("UAV Logistics Simulation System - 完整测试套件")
    print("=" * 80)
    
    results = []
    
    # 0. Quick functionality verification
    print("Stage 0: Quick Functionality Verification")
    quick_test_success = run_quick_functionality_test()
    results.append(("Quick Functionality", quick_test_success))
    
    if not quick_test_success:
        print("❌ Quick functionality verification failed, stopping tests")
        return False
    
    # 1. Coordinate generator test
    print("\nStage 1: Coordinate Generator Test")
    coord_test_success = test_coordinate_generator()
    results.append(("Coordinate Generator", coord_test_success))
    
    # 2. Charging station test
    print("\nStage 2: Charging Station Test")
    charging_test_success = test_charging_station()
    results.append(("Charging Station", charging_test_success))
    
    # 3. Distribution center test
    print("\nStage 3: Distribution Center Test")
    dc_test_success = test_distribution_center()
    results.append(("Distribution Center", dc_test_success))
    
    # 4. Complete system test (if previous tests pass)
    if all(result[1] for result in results):
        print("\nStage 4: Complete System Test")
        system_test_success = test_complete_system()
        results.append(("Complete System", system_test_success))
    else:
        print("\nSkipping complete system test due to previous failures")
        results.append(("Complete System", False))
    
    # 5. Shortest path algorithm test
    print("\nStage 5: Shortest Path Algorithm Test")
    shortest_path_success = test_shortest_path_algorithm()
    results.append(("Shortest Path Algorithm", shortest_path_success))
    
    # 6. Extended scenario testing
    print("\nStage 6: Extended Scenario Testing")
    extended_scenario_success = test_extended_scenarios()
    results.append(("Extended Scenarios", extended_scenario_success))
    
    # 7. Mixed transportation mode testing
    print("\nStage 7: Mixed Transportation Mode Testing")
    mixed_transport_success = test_mixed_transportation_modes()
    results.append(("Mixed Transportation", mixed_transport_success))
    
    # Display results
    print("\n" + "=" * 80)
    print("测试结果摘要")
    print("=" * 80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:25}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 80)
    
    if all_passed:
        print("🎉 所有测试通过！UAV物流仿真系统功能正常。")
        print("系统特性:")
        print("• 坐标生成: 自动生成顾客点、充电站、配送中心、服务点")
        print("• 充电站: 支持有限/无限电池类型，多窗口服务，等待时间统计")
        print("• 配送中心: 货物接收、处理、卡车配送，完整的物流流程")
        print("• UAV系统: 智能路径规划、自动充电、两种配送模式")
        print("• 完整仿真: 订单生成、任务分配、性能统计")
        print("• 最短路径算法: Dijkstra算法优化路径，电池约束考虑")
        print("• 扩展测试: 多充电站测试、轨迹可视化、三种路径对比")
        print("• 订单跟踪: 完整的服务时间计算，从顾客点离开到返回")
        print("• 智能充电: max/2规则，最优充电站选择策略")
        print("• 扩展场景: 6种测试场景，包含低电量长距离、多点配送、性能基准测试")
        print("• 并行仿真: 多订单并行处理，120时间单位扩展仿真")
        print("• 性能分析: 算法计算时间对比，距离优化效率评估")
        print("• 混合运输: 直接配送vs配送中心模式，充电桩使用时间可视化")
        print("• 轨迹跟踪: UAV飞行路径和卡车配送轨迹完整记录")
        print("• 实时监控: 充电站实时使用情况，电池可用性动态追踪")
        return True
    else:
        print("❌ 部分测试失败，请检查错误信息。")
        return False

if __name__ == "__main__":
    print("开始完整测试套件...")
    success = main()
    
    if success:
        print("\n系统就绪，可以开始使用！")
        sys.exit(0)
    else:
        print("\n请修复问题后再使用。")
        sys.exit(1)
