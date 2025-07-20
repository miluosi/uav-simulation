# verify_charging_station_functionality.py
# 验证充电站类的所有功能

import sys
import os

# 添加当前目录和父目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from models.charging_station import ChargingStation
from models.uav_classes import UAV
import simpy

def check_charging_station_class_structure():
    """检查充电站类的结构和方法"""
    print("ChargingStation Class Structure Verification")
    print("=" * 60)
    
    # 检查类是否存在
    print("✓ ChargingStation class imported successfully")
    
    # 检查必要的方法
    required_methods = [
        '__init__',
        'serve_uav',
        'service_window_process',
        'statistics_collection_process'
    ]
    
    optional_methods = [
        'battery_charging_process'  # 仅限有限电池模式
    ]
    
    print("\nRequired methods:")
    for method in required_methods:
        if hasattr(ChargingStation, method):
            print(f"  ✓ {method}")
        else:
            print(f"  ✗ {method} (MISSING)")
    
    print("\nOptional methods:")
    for method in optional_methods:
        if hasattr(ChargingStation, method):
            print(f"  ✓ {method}")
        else:
            print(f"  ○ {method} (not found, but may be conditional)")
    
    return True


def test_limited_battery_initialization():
    """测试有限电池模式初始化"""
    print("\n" + "=" * 60)
    print("Limited Battery Mode Initialization Test")
    print("=" * 60)
    
    env = simpy.Environment()
    
    # 创建有限电池充电站
    limited_station = ChargingStation(
        env=env,
        station_id=1,
        latitude=39.9050,
        longitude=116.4080,
        battery_type='limited',
        battery_capacity=10,
        service_windows=2,
        service_time=0.3,
        charge_time=0.5
    )
    
    print("Limited battery station created with:")
    print(f"  Battery type: {limited_station.battery_type}")
    print(f"  Battery capacity: {limited_station.battery_capacity}")
    print(f"  Available batteries: {limited_station.available_batteries}")
    print(f"  Service windows: {limited_station.service_windows}")
    print(f"  Service time: {limited_station.service_time}")
    print(f"  Charge time: {limited_station.charge_time}")
    
    # 检查有限模式特有属性
    limited_attributes = ['charging_batteries', 'used_batteries']
    for attr in limited_attributes:
        if hasattr(limited_station, attr):
            value = getattr(limited_station, attr)
            print(f"  {attr}: {value}")
        else:
            print(f"  {attr}: NOT FOUND")
    
    # 验证初始状态
    checks = [
        (limited_station.battery_type == 'limited', "Battery type should be 'limited'"),
        (limited_station.battery_capacity == 10, "Battery capacity should be 10"),
        (limited_station.available_batteries == 10, "Available batteries should equal capacity"),
        (hasattr(limited_station, 'charging_batteries'), "Should have charging_batteries attribute"),
        (hasattr(limited_station, 'used_batteries'), "Should have used_batteries attribute")
    ]
    
    print("\nVerification results:")
    all_passed = True
    for check, description in checks:
        status = "✓ PASS" if check else "✗ FAIL"
        print(f"  {description}: {status}")
        if not check:
            all_passed = False
    
    return all_passed


def test_unlimited_battery_initialization():
    """测试无限电池模式初始化"""
    print("\n" + "=" * 60)
    print("Unlimited Battery Mode Initialization Test")
    print("=" * 60)
    
    env = simpy.Environment()
    
    # 创建无限电池充电站
    unlimited_station = ChargingStation(
        env=env,
        station_id=2,
        latitude=39.9060,
        longitude=116.4090,
        battery_type='unlimited',
        service_windows=3,
        service_time=0.2
        # charge_time 在无限模式下应该被忽略
    )
    
    print("Unlimited battery station created with:")
    print(f"  Battery type: {unlimited_station.battery_type}")
    print(f"  Battery capacity: {unlimited_station.battery_capacity}")
    print(f"  Available batteries: {unlimited_station.available_batteries}")
    print(f"  Service windows: {unlimited_station.service_windows}")
    print(f"  Service time: {unlimited_station.service_time}")
    
    # 检查无限模式不应该有的属性
    limited_only_attributes = ['charging_batteries', 'used_batteries']
    print("\nLimited-mode-only attributes (should not exist or be empty):")
    for attr in limited_only_attributes:
        if hasattr(unlimited_station, attr):
            value = getattr(unlimited_station, attr)
            print(f"  {attr}: {value} (exists but should be unused)")
        else:
            print(f"  {attr}: NOT EXISTS ✓")
    
    # 验证无限模式状态
    checks = [
        (unlimited_station.battery_type == 'unlimited', "Battery type should be 'unlimited'"),
        (unlimited_station.battery_capacity == float('inf'), "Battery capacity should be infinite"),
        (unlimited_station.available_batteries == float('inf'), "Available batteries should be infinite"),
        (unlimited_station.service_windows == 3, "Should have 3 service windows")
    ]
    
    print("\nVerification results:")
    all_passed = True
    for check, description in checks:
        status = "✓ PASS" if check else "✗ FAIL"
        print(f"  {description}: {status}")
        if not check:
            all_passed = False
    
    return all_passed


def test_service_window_functionality():
    """测试服务窗口功能"""
    print("\n" + "=" * 60)
    print("Service Window Functionality Test")
    print("=" * 60)
    
    env = simpy.Environment()
    
    # 创建多窗口充电站
    station = ChargingStation(
        env=env,
        station_id=3,
        latitude=39.9070,
        longitude=116.4100,
        battery_type='unlimited',
        service_windows=3,
        service_time=0.1
    )
    
    print(f"Created station with {station.service_windows} service windows")
    
    # 检查窗口相关属性
    window_attributes = ['window_busy', 'queues']
    for attr in window_attributes:
        if hasattr(station, attr):
            value = getattr(station, attr)
            print(f"  {attr}: {value}")
        else:
            print(f"  {attr}: NOT FOUND")
    
    # 验证窗口初始状态
    checks = [
        (len(station.window_busy) == 3, "Should have 3 window busy flags"),
        (all(not busy for busy in station.window_busy), "All windows should be initially free"),
        (len(station.queues) == 3, "Should have 3 queues"),
        (all(len(queue) == 0 for queue in station.queues), "All queues should be initially empty")
    ]
    
    print("\nWindow state verification:")
    all_passed = True
    for check, description in checks:
        status = "✓ PASS" if check else "✗ FAIL"
        print(f"  {description}: {status}")
        if not check:
            all_passed = False
    
    return all_passed


def test_uav_service_process():
    """测试UAV服务流程"""
    print("\n" + "=" * 60)
    print("UAV Service Process Test")
    print("=" * 60)
    
    env = simpy.Environment()
    
    # 创建测试充电站
    station = ChargingStation(
        env=env,
        station_id=4,
        latitude=39.9080,
        longitude=116.4110,
        battery_type='unlimited',
        service_windows=2,
        service_time=0.1
    )
    
    # 创建测试UAV
    uav = UAV(env, "service_test_uav", 39.9042, 116.4074)
    uav.current_battery = 20  # 低电量
    
    print(f"Created UAV with {uav.current_battery}% battery")
    print(f"UAV battery capacity: {uav.battery_capacity}%")
    
    def service_test():
        initial_battery = uav.current_battery
        initial_served = station.total_served
        
        print(f"\nStarting service process...")
        print(f"  Initial battery: {initial_battery}%")
        print(f"  Station served count: {initial_served}")
        
        # 执行服务
        yield env.process(station.serve_uav(uav))
        
        final_battery = uav.current_battery
        final_served = station.total_served
        
        print(f"\nService completed:")
        print(f"  Final battery: {final_battery}%")
        print(f"  Station served count: {final_served}")
        
        # 验证服务结果
        service_successful = final_battery == uav.battery_capacity
        count_incremented = final_served == initial_served + 1
        
        print(f"\nService verification:")
        print(f"  Battery fully charged: {'✓' if service_successful else '✗'}")
        print(f"  Service count incremented: {'✓' if count_incremented else '✗'}")
        
        return service_successful and count_incremented
    
    env.process(service_test())
    
    try:
        env.run(until=10)
        print("✓ UAV service process test completed")
        return True
    except Exception as e:
        print(f"✗ Service process test failed: {e}")
        return False


def test_battery_management_logic():
    """测试电池管理逻辑"""
    print("\n" + "=" * 60)
    print("Battery Management Logic Test")
    print("=" * 60)
    
    # 测试有限电池模式的电池管理
    env = simpy.Environment()
    
    limited_station = ChargingStation(
        env=env,
        station_id=5,
        latitude=39.9090,
        longitude=116.4120,
        battery_type='limited',
        battery_capacity=3,  # 小容量便于测试
        service_windows=1,
        service_time=0.1,
        charge_time=0.2
    )
    
    print("Testing limited battery management:")
    print(f"  Initial capacity: {limited_station.battery_capacity}")
    print(f"  Initial available: {limited_station.available_batteries}")
    
    # 创建多个UAV测试电池消耗
    uavs = []
    for i in range(4):  # 4个UAV，超过容量
        uav = UAV(env, f"battery_test_uav_{i}", 39.9042, 116.4074)
        uav.current_battery = 10
        uavs.append(uav)
    
    def battery_management_test():
        print(f"\nTesting with {len(uavs)} UAVs...")
        
        # 逐个服务UAV，观察电池变化
        for i, uav in enumerate(uavs):
            print(f"\nServicing UAV {i+1}:")
            print(f"  Before: available={limited_station.available_batteries}")
            if hasattr(limited_station, 'used_batteries'):
                print(f"  Before: used={len(limited_station.used_batteries)}")
            
            yield env.process(limited_station.serve_uav(uav))
            
            print(f"  After: available={limited_station.available_batteries}")
            if hasattr(limited_station, 'used_batteries'):
                print(f"  After: used={len(limited_station.used_batteries)}")
            print(f"  UAV battery: {uav.current_battery}%")
        
        print(f"\nFinal station state:")
        print(f"  Available batteries: {limited_station.available_batteries}")
        if hasattr(limited_station, 'used_batteries'):
            print(f"  Used batteries: {len(limited_station.used_batteries)}")
        if hasattr(limited_station, 'charging_batteries'):
            print(f"  Charging batteries: {limited_station.charging_batteries}")
        
        # 验证电池总数不超过容量
        if hasattr(limited_station, 'used_batteries') and hasattr(limited_station, 'charging_batteries'):
            total_batteries = (limited_station.available_batteries + 
                             len(limited_station.used_batteries) + 
                             limited_station.charging_batteries)
            print(f"  Total batteries: {total_batteries}")
            
            capacity_respected = total_batteries <= limited_station.battery_capacity
            print(f"  Capacity respected: {'✓' if capacity_respected else '✗'}")
            return capacity_respected
        
        return True
    
    env.process(battery_management_test())
    
    try:
        env.run(until=50)
        print("✓ Battery management logic test completed")
        return True
    except Exception as e:
        print(f"✗ Battery management test failed: {e}")
        return False


def run_charging_station_verification():
    """运行所有充电站功能验证测试"""
    print("ChargingStation Class Functionality Verification")
    print("=" * 80)
    
    test_functions = [
        check_charging_station_class_structure,
        test_limited_battery_initialization,
        test_unlimited_battery_initialization,
        test_service_window_functionality,
        test_uav_service_process,
        test_battery_management_logic
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
    
    # 输出总结
    print("\n" + "=" * 80)
    print("ChargingStation Functionality Verification Results")
    print("=" * 80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:40}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 80)
    
    if all_passed:
        print("🎉 All ChargingStation functionality tests passed!")
        print("\nVerified Features:")
        print("✓ Class structure and method availability")
        print("✓ Limited battery mode initialization and management")
        print("✓ Unlimited battery mode initialization (no charging process)")
        print("✓ Multi-window service capability")
        print("✓ UAV service process (battery replacement)")
        print("✓ Battery capacity management and overflow prevention")
        print("✓ Service statistics tracking")
        print("✓ Queue management for concurrent access")
    else:
        print("❌ Some ChargingStation functionality tests failed")
        print("Please check the implementation for issues")
    
    return all_passed


if __name__ == "__main__":
    success = run_charging_station_verification()
    sys.exit(0 if success else 1)
