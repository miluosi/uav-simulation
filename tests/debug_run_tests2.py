#!/usr/bin/env python3
# 调试版本的run_tests.py - 添加更多输出来诊断问题

import sys
import os

print("=== 调试版本run_tests.py开始 ===")
print(f"当前目录: {os.getcwd()}")
print(f"Python路径: {sys.path[0]}")

# Add current directory and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

print(f"脚本目录: {current_dir}")
print(f"父目录: {parent_dir}")

def test_coordinate_generator():
    """Test coordinate generator"""
    print("=" * 60)
    print("Test 1: Coordinate Generator Module")
    print("=" * 60)
    
    try:
        print("尝试导入 test_coordinate_generator...")
        from test_coordinate_generator import run_all_tests
        print("导入成功，运行测试...")
        success = run_all_tests()
        print(f"测试完成，结果: {success}")
        return success
    except Exception as e:
        print(f"Coordinate generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_quick_functionality_test():
    """Run quick functionality test"""
    print("\n" + "=" * 60)
    print("Quick Functionality Verification Test")
    print("=" * 60)
    
    try:
        print("导入模块...")
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

def main():
    """Main test function"""
    print("UAV Logistics Simulation System - 调试版测试套件")
    print("=" * 80)
    
    results = []
    
    # 1. Quick functionality verification
    print("Stage 0: Quick Functionality Verification")
    quick_test_success = run_quick_functionality_test()
    results.append(("Quick Functionality", quick_test_success))
    
    if not quick_test_success:
        print("❌ Quick functionality verification failed, stopping tests")
        return False
    
    # 2. Coordinate generator test
    print("\nStage 1: Coordinate Generator Test")
    coord_test_success = test_coordinate_generator()
    results.append(("Coordinate Generator", coord_test_success))
    
    # 输出结果
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("🎉 测试通过！")
        return True
    else:
        print("❌ 部分测试失败。")
        return False

if __name__ == "__main__":
    print("开始调试版测试套件...")
    try:
        success = main()
        
        if success:
            print("\n系统就绪！")
            sys.exit(0)
        else:
            print("\n请修复问题。")
            sys.exit(1)
    except Exception as e:
        print(f"主函数执行错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print("=== 调试版本run_tests.py结束 ===")
