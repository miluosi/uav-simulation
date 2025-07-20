# simple_run_tests.py
# 简化版本的run_tests.py来诊断问题

import sys
import os

# Add current directory and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

def simple_test():
    """简单测试"""
    print("UAV物流仿真系统 - 简化测试套件")
    print("=" * 60)
    
    results = []
    
    # 1. 快速功能验证
    print("阶段1: 快速功能验证")
    try:
        from models.coordinate_generator import CoordinateGenerator
        from models.charging_station import ChargingStation
        from models.distribution_center import DistributionCenter
        from models.uav_classes import UAV, Goods, Order
        import simpy
        
        env = simpy.Environment()
        generator = CoordinateGenerator(area_size=50)
        station = ChargingStation(env, 'test_cs', 25, 25, 'limited', 20, 2, 0.5)
        dc = DistributionCenter(env, 'test_dc', 30, 30)
        uav = UAV(env, 'test_uav', 25, 25)
        goods = Goods(env, 'test_goods')
        order = Order(env, 1, 0, 0, goods, 'direct')
        
        print("✓ 基本功能验证通过")
        results.append(("基本功能", True))
    except Exception as e:
        print(f"✗ 基本功能验证失败: {e}")
        results.append(("基本功能", False))
    
    # 2. 最短路径算法测试
    print("\n阶段2: 最短路径算法测试")
    try:
        from models.uav_classes import UAV, calculate_distance
        from models.charging_station import ChargingStation
        import simpy
        
        env = simpy.Environment()
        uav = UAV(env, "test_uav", 39.9042, 116.4074)
        
        waypoints = [{'id': 'wp1', 'latitude': 39.9200, 'longitude': 116.4200}]
        path, distance = uav.calculate_shortest_path_dijkstra(
            39.9042, 116.4074, 39.9500, 116.4500, waypoints
        )
        
        charging_station = ChargingStation(env, "cs1", 39.9250, 116.4250, battery_type='unlimited')
        enhanced_path, enhanced_distance = uav.plan_shortest_route_with_constraints(
            39.9042, 116.4074, 39.9500, 116.4500, waypoints, [charging_station]
        )
        
        print(f"✓ 最短路径算法测试通过 (距离: {distance:.2f} km)")
        results.append(("最短路径算法", True))
    except Exception as e:
        print(f"✗ 最短路径算法测试失败: {e}")
        import traceback
        traceback.print_exc()
        results.append(("最短路径算法", False))
    
    # 3. 坐标生成测试
    print("\n阶段3: 坐标生成测试")
    try:
        from test_coordinate_generator import run_all_tests
        success = run_all_tests()
        if success:
            print("✓ 坐标生成测试通过")
            results.append(("坐标生成", True))
        else:
            print("✗ 坐标生成测试失败")
            results.append(("坐标生成", False))
    except Exception as e:
        print(f"✗ 坐标生成测试失败: {e}")
        results.append(("坐标生成", False))
    
    # 4. 充电站测试
    print("\n阶段4: 充电站测试")
    try:
        from models.charging_station import test_charging_station
        test_charging_station()
        print("✓ 充电站测试通过")
        results.append(("充电站", True))
    except Exception as e:
        print(f"✗ 充电站测试失败: {e}")
        results.append(("充电站", False))
    
    # 输出结果
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:15}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("🎉 所有测试通过！系统正常运行。")
        return True
    else:
        print("❌ 部分测试失败，请检查错误信息。")
        return False

if __name__ == "__main__":
    print("开始简化测试套件...")
    success = simple_test()
    
    if success:
        print("\n系统就绪，可以开始使用！")
        sys.exit(0)
    else:
        print("\n请修复问题后再使用。")
        sys.exit(1)
