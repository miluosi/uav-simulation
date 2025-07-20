# debug_run_tests.py
# 调试版本的run_tests.py

import sys
import os

# Add current directory and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

def debug_quick_functionality_test():
    """调试快速功能测试"""
    print("=== DEBUG: 快速功能验证测试 ===")
    
    try:
        print("1. 开始导入模块...")
        # Import all modules
        from models.coordinate_generator import CoordinateGenerator
        print("✓ CoordinateGenerator导入成功")
        
        from models.charging_station import ChargingStation
        print("✓ ChargingStation导入成功")
        
        from models.distribution_center import DistributionCenter
        print("✓ DistributionCenter导入成功")
        
        from models.uav_classes import UAV, Goods, Order
        print("✓ UAV classes导入成功")
        
        import simpy
        print("✓ simpy导入成功")
        
        print("2. 创建仿真环境...")
        env = simpy.Environment()
        print("✓ 仿真环境创建成功")
        
        print("3. 测试坐标生成...")
        generator = CoordinateGenerator(area_size=50)
        coordinates = generator.generate_all_coordinates(2, 3, 1, 3)
        print("✓ 坐标生成成功")
        
        print("4. 测试充电站创建...")
        # 使用正确的参数顺序
        station = ChargingStation(env, 'test_cs', 25, 25, 'limited', 20, 2, 0.5)
        print("✓ 充电站创建成功")
        
        print("5. 测试配送中心创建...")
        # 检查DistributionCenter的构造函数
        dc = DistributionCenter(env, 'test_dc', 30, 30)
        print("✓ 配送中心创建成功")
        
        print("6. 测试UAV创建...")
        uav = UAV(env, 'test_uav', 25, 25)
        print("✓ UAV创建成功")
        
        print("7. 测试货物和订单创建...")
        goods = Goods(env, 'test_goods')
        order = Order(env, 1, 0, 0, goods, 'direct')
        print("✓ 货物和订单创建成功")
        
        print("✓ 所有基本功能验证通过!")
        return True
        
    except Exception as e:
        print(f"✗ 功能验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_shortest_path_test():
    """调试最短路径测试"""
    print("\n=== DEBUG: 最短路径算法测试 ===")
    
    try:
        print("1. 导入必要模块...")
        from models.uav_classes import UAV, calculate_distance
        from models.charging_station import ChargingStation
        import simpy
        print("✓ 模块导入成功")
        
        print("2. 创建测试环境...")
        env = simpy.Environment()
        uav = UAV(env, "test_uav", 39.9042, 116.4074)
        print("✓ UAV创建成功")
        
        print("3. 测试基本最短路径...")
        waypoints = [
            {'id': 'wp1', 'latitude': 39.9200, 'longitude': 116.4200},
        ]
        
        path, distance = uav.calculate_shortest_path_dijkstra(
            39.9042, 116.4074, 39.9500, 116.4500, waypoints
        )
        print(f"✓ 最短路径计算成功: {len(path)} 航点, {distance:.2f} km")
        
        print("4. 测试充电站约束...")
        charging_station = ChargingStation(env, "cs1", 39.9250, 116.4250, battery_type='unlimited')
        enhanced_path, enhanced_distance = uav.plan_shortest_route_with_constraints(
            39.9042, 116.4074, 39.9500, 116.4500, waypoints, [charging_station]
        )
        print(f"✓ 充电约束路径计算成功: {len(enhanced_path)} 航点, {enhanced_distance:.2f} km")
        
        print("✓ 最短路径算法测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ 最短路径测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主调试函数"""
    print("UAV物流仿真系统 - 调试测试")
    print("=" * 60)
    
    # 测试1: 快速功能验证
    print("阶段1: 快速功能验证")
    quick_success = debug_quick_functionality_test()
    
    if not quick_success:
        print("❌ 快速功能验证失败")
        return False
    
    # 测试2: 最短路径算法
    print("\n阶段2: 最短路径算法测试")
    shortest_path_success = debug_shortest_path_test()
    
    # 结果总结
    print("\n" + "=" * 60)
    print("调试测试结果")
    print("=" * 60)
    print(f"快速功能验证: {'✓ PASS' if quick_success else '✗ FAIL'}")
    print(f"最短路径算法: {'✓ PASS' if shortest_path_success else '✗ FAIL'}")
    
    if quick_success and shortest_path_success:
        print("\n🎉 调试测试全部通过!")
        return True
    else:
        print("\n❌ 部分测试失败")
        return False

if __name__ == "__main__":
    print("开始调试测试...")
    success = main()
    
    if success:
        print("\n系统核心功能正常!")
    else:
        print("\n需要修复问题")
