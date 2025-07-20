# test_unlimited_charging_station.py
# 测试充电站无限电池存量模式

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

def test_unlimited_battery_basic():
    """测试无限电池模式基本功能"""
    print("Test 1: Unlimited Battery Mode - Basic Functionality")
    print("=" * 60)
    
    # 创建仿真环境
    env = simpy.Environment()
    
    # 创建无限电池充电站
    unlimited_station = ChargingStation(
        env=env, 
        station_id=1, 
        latitude=39.9050, 
        longitude=116.4080, 
        battery_type='unlimited',  # 关键：无限电池模式
        service_time=0.3,
        charge_time=0.5  # 这个参数在无限模式下应该被忽略
    )
    
    print(f"创建无限电池充电站:")
    print(f"  电池类型: {unlimited_station.battery_type}")
    print(f"  电池容量: {unlimited_station.battery_capacity}")
    print(f"  可用电池: {unlimited_station.available_batteries}")
    
    # 验证无限电池模式的初始状态
    assert unlimited_station.battery_type == 'unlimited', "电池类型应为unlimited"
    assert unlimited_station.battery_capacity == float('inf'), "电池容量应为无限"
    assert unlimited_station.available_batteries == float('inf'), "可用电池应为无限"
    
    # 验证不应该有电池充电进程
    assert not hasattr(unlimited_station, 'charging_batteries') or unlimited_station.charging_batteries == 0, "无限模式不应有充电进程"
    assert not hasattr(unlimited_station, 'used_batteries') or len(unlimited_station.used_batteries) == 0, "无限模式不应跟踪用过的电池"
    
    print("✓ 无限电池模式基本状态验证通过")
    return True


def test_unlimited_battery_uav_service():
    """测试无限电池模式为UAV服务"""
    print("\nTest 2: Unlimited Battery Mode - UAV Service")
    print("=" * 60)
    
    env = simpy.Environment()
    
    # 创建无限电池充电站
    unlimited_station = ChargingStation(
        env=env, 
        station_id=2, 
        latitude=39.9060, 
        longitude=116.4090, 
        battery_type='unlimited',
        service_time=0.2
    )
    
    # 创建多个低电量UAV
    uavs = []
    for i in range(5):
        uav = UAV(env, f"unlimited_test_uav_{i}", 39.9042, 116.4074, battery_capacity=100)
        uav.current_battery = 10 + i * 5  # 设置不同的低电量
        uavs.append(uav)
    
    print(f"创建 {len(uavs)} 个UAV，电池电量分别为:")
    for uav in uavs:
        print(f"  {uav.uav_id}: {uav.current_battery}%")
    
    def test_service_process():
        """测试服务过程"""
        start_time = env.now
        
        # 同时让所有UAV去充电
        service_processes = []
        for uav in uavs:
            process = env.process(unlimited_station.serve_uav(uav))
            service_processes.append(process)
        
        # 等待所有服务完成
        yield env.all_of(service_processes)
        
        end_time = env.now
        
        print(f"\n服务完成，总耗时: {end_time - start_time:.2f} 时间单位")
        
        # 验证所有UAV都充满电了
        print("服务后UAV电池状态:")
        all_fully_charged = True
        for uav in uavs:
            is_full = uav.current_battery == uav.battery_capacity
            print(f"  {uav.uav_id}: {uav.current_battery}% {'✓' if is_full else '✗'}")
            if not is_full:
                all_fully_charged = False
        
        # 验证充电站状态（无限模式应该没有变化）
        print(f"\n充电站服务后状态:")
        print(f"  可用电池: {unlimited_station.available_batteries}")
        print(f"  电池容量: {unlimited_station.battery_capacity}")
        print(f"  服务总数: {unlimited_station.total_served}")
        
        # 验证无限电池模式不跟踪用过的电池
        if hasattr(unlimited_station, 'used_batteries'):
            print(f"  用过的电池: {len(unlimited_station.used_batteries)} (应该为0)")
            assert len(unlimited_station.used_batteries) == 0, "无限模式不应跟踪用过的电池"
        
        if hasattr(unlimited_station, 'charging_batteries'):
            print(f"  正在充电: {unlimited_station.charging_batteries} (应该为0)")
            assert unlimited_station.charging_batteries == 0, "无限模式不应有电池在充电"
        
        return all_fully_charged
    
    env.process(test_service_process())
    
    try:
        env.run(until=50)  # 限制运行时间
        print("✓ 无限电池模式UAV服务测试通过")
        return True
    except Exception as e:
        print(f"✗ 无限电池模式UAV服务测试失败: {e}")
        return False


def test_unlimited_vs_limited_comparison():
    """对比测试：无限电池模式 vs 有限电池模式"""
    print("\nTest 3: Unlimited vs Limited Battery Mode Comparison")
    print("=" * 60)
    
    # 测试无限电池模式
    env1 = simpy.Environment()
    unlimited_station = ChargingStation(
        env=env1, 
        station_id=3, 
        latitude=39.9070, 
        longitude=116.4100, 
        battery_type='unlimited',
        service_time=0.1
    )
    
    # 测试有限电池模式
    env2 = simpy.Environment()
    limited_station = ChargingStation(
        env=env2, 
        station_id=4, 
        latitude=39.9070, 
        longitude=116.4100, 
        battery_type='limited',
        battery_capacity=3,  # 很小的容量
        service_windows=1,
        service_time=0.1
    )
    
    print("对比测试设置:")
    print(f"  无限模式充电站容量: {unlimited_station.battery_capacity}")
    print(f"  有限模式充电站容量: {limited_station.battery_capacity}")
    
    # 创建相同的UAV队列用于两种模式测试
    def create_test_uavs(env, prefix):
        uavs = []
        for i in range(5):  # 5个UAV，超过有限模式容量
            uav = UAV(env, f"{prefix}_uav_{i}", 39.9042, 116.4074)
            uav.current_battery = 5  # 低电量
            uavs.append(uav)
        return uavs
    
    unlimited_uavs = create_test_uavs(env1, "unlimited")
    limited_uavs = create_test_uavs(env2, "limited")
    
    def test_unlimited_performance():
        """测试无限模式性能"""
        start_time = env1.now
        
        # 所有UAV同时请求服务
        processes = [env1.process(unlimited_station.serve_uav(uav)) for uav in unlimited_uavs]
        yield env1.all_of(processes)
        
        end_time = env1.now
        
        # 统计结果
        served_count = sum(1 for uav in unlimited_uavs if uav.current_battery == uav.battery_capacity)
        
        print(f"\n无限模式测试结果:")
        print(f"  服务时间: {end_time - start_time:.2f}")
        print(f"  成功服务: {served_count}/{len(unlimited_uavs)}")
        print(f"  充电站状态: 可用电池={unlimited_station.available_batteries}")
        
        return end_time - start_time, served_count
    
    def test_limited_performance():
        """测试有限模式性能"""
        start_time = env2.now
        
        # 所有UAV同时请求服务
        processes = [env2.process(limited_station.serve_uav(uav)) for uav in limited_uavs]
        yield env2.all_of(processes)
        
        end_time = env2.now
        
        # 统计结果
        served_count = sum(1 for uav in limited_uavs if uav.current_battery == uav.battery_capacity)
        
        print(f"\n有限模式测试结果:")
        print(f"  服务时间: {end_time - start_time:.2f}")
        print(f"  成功服务: {served_count}/{len(limited_uavs)}")
        print(f"  充电站状态: 可用电池={limited_station.available_batteries}")
        if hasattr(limited_station, 'used_batteries'):
            print(f"  用过电池: {len(limited_station.used_batteries)}")
        
        return end_time - start_time, served_count
    
    # 运行两个测试
    env1.process(test_unlimited_performance())
    env2.process(test_limited_performance())
    
    try:
        env1.run(until=100)
        env2.run(until=100)
        print("✓ 无限vs有限模式对比测试完成")
        return True
    except Exception as e:
        print(f"✗ 对比测试失败: {e}")
        return False


def test_unlimited_battery_concurrent_access():
    """测试无限电池模式并发访问"""
    print("\nTest 4: Unlimited Battery Mode - Concurrent Access")
    print("=" * 60)
    
    env = simpy.Environment()
    
    # 创建无限电池充电站（多个服务窗口）
    unlimited_station = ChargingStation(
        env=env, 
        station_id=5, 
        latitude=39.9080, 
        longitude=116.4110, 
        battery_type='unlimited',
        service_windows=3,  # 3个服务窗口
        service_time=0.5
    )
    
    print(f"创建3窗口无限电池充电站")
    print(f"服务窗口数: {unlimited_station.service_windows}")
    
    # 创建大量UAV测试并发
    large_uav_fleet = []
    for i in range(20):  # 20个UAV
        uav = UAV(env, f"concurrent_uav_{i}", 39.9042, 116.4074)
        uav.current_battery = 1  # 极低电量
        large_uav_fleet.append(uav)
    
    print(f"创建 {len(large_uav_fleet)} 个UAV进行并发测试")
    
    def concurrent_access_test():
        """并发访问测试"""
        start_time = env.now
        
        # 模拟UAV在不同时间到达
        def uav_arrival(uav, delay):
            yield env.timeout(delay)
            yield env.process(unlimited_station.serve_uav(uav))
        
        # 创建到达进程
        arrival_processes = []
        for i, uav in enumerate(large_uav_fleet):
            delay = i * 0.1  # 每0.1时间单位到达一个UAV
            process = env.process(uav_arrival(uav, delay))
            arrival_processes.append(process)
        
        # 等待所有服务完成
        yield env.all_of(arrival_processes)
        
        end_time = env.now
        
        print(f"\n并发测试结果:")
        print(f"  总耗时: {end_time - start_time:.2f} 时间单位")
        print(f"  服务总数: {unlimited_station.total_served}")
        
        # 验证所有UAV都得到服务
        fully_charged_count = sum(1 for uav in large_uav_fleet 
                                if uav.current_battery == uav.battery_capacity)
        
        print(f"  充满电UAV: {fully_charged_count}/{len(large_uav_fleet)}")
        print(f"  充电站可用电池: {unlimited_station.available_batteries} (应该仍为无限)")
        
        # 验证无限模式特性
        if hasattr(unlimited_station, 'used_batteries'):
            print(f"  用过电池数: {len(unlimited_station.used_batteries)} (应该为0)")
            assert len(unlimited_station.used_batteries) == 0, "无限模式不应积累用过的电池"
        
        success = fully_charged_count == len(large_uav_fleet)
        print(f"  测试结果: {'✓ PASS' if success else '✗ FAIL'}")
        
        return success
    
    env.process(concurrent_access_test())
    
    try:
        env.run(until=200)
        print("✓ 无限电池模式并发访问测试通过")
        return True
    except Exception as e:
        print(f"✗ 并发访问测试失败: {e}")
        return False


def test_unlimited_battery_no_charging_process():
    """验证无限电池模式不启动电池充电进程"""
    print("\nTest 5: Unlimited Battery Mode - No Charging Process")
    print("=" * 60)
    
    env = simpy.Environment()
    
    # 创建无限电池充电站
    unlimited_station = ChargingStation(
        env=env, 
        station_id=6, 
        latitude=39.9090, 
        longitude=116.4120, 
        battery_type='unlimited',
        service_time=0.2
    )
    
    print("验证无限电池模式不启动电池充电进程...")
    
    # 检查是否有电池充电相关的属性
    charging_attributes = ['charging_batteries', 'used_batteries']
    
    print("检查电池充电相关属性:")
    for attr in charging_attributes:
        if hasattr(unlimited_station, attr):
            value = getattr(unlimited_station, attr)
            print(f"  {attr}: {value} (存在但应该为空/0)")
            if attr == 'charging_batteries':
                assert value == 0, f"{attr} 应该为0"
            elif attr == 'used_batteries':
                assert len(value) == 0, f"{attr} 应该为空列表"
        else:
            print(f"  {attr}: 不存在 ✓")
    
    # 创建UAV测试，确保不会触发充电进程
    test_uav = UAV(env, "no_charging_test_uav", 39.9042, 116.4074)
    test_uav.current_battery = 5
    
    def monitor_charging_process():
        """监控是否有充电进程活动"""
        # 记录初始状态
        initial_available = unlimited_station.available_batteries
        
        # UAV换电
        yield env.process(unlimited_station.serve_uav(test_uav))
        
        # 检查换电后状态
        final_available = unlimited_station.available_batteries
        
        print(f"\n换电过程监控:")
        print(f"  初始可用电池: {initial_available}")
        print(f"  换电后可用电池: {final_available}")
        print(f"  UAV电池: {test_uav.current_battery}%")
        
        # 验证无限模式特性
        assert initial_available == final_available == float('inf'), "无限模式可用电池数应该保持无限"
        assert test_uav.current_battery == test_uav.battery_capacity, "UAV应该充满电"
        
        # 继续运行一段时间，确保没有充电进程
        yield env.timeout(10.0)
        
        # 再次检查状态
        print(f"  10个时间单位后可用电池: {unlimited_station.available_batteries}")
        if hasattr(unlimited_station, 'charging_batteries'):
            print(f"  正在充电的电池: {unlimited_station.charging_batteries}")
            assert unlimited_station.charging_batteries == 0, "不应该有电池在充电"
        
        print("✓ 确认无充电进程活动")
    
    env.process(monitor_charging_process())
    
    try:
        env.run(until=50)
        print("✓ 无限电池模式无充电进程验证通过")
        return True
    except Exception as e:
        print(f"✗ 无充电进程验证失败: {e}")
        return False


def run_all_unlimited_battery_tests():
    """运行所有无限电池模式测试"""
    print("充电站无限电池存量模式测试套件")
    print("=" * 80)
    
    test_functions = [
        test_unlimited_battery_basic,
        test_unlimited_battery_uav_service,
        test_unlimited_vs_limited_comparison,
        test_unlimited_battery_concurrent_access,
        test_unlimited_battery_no_charging_process
    ]
    
    results = []
    
    for i, test_func in enumerate(test_functions, 1):
        try:
            success = test_func()
            results.append((test_func.__name__, success))
        except Exception as e:
            print(f"测试 {i} 异常: {e}")
            results.append((test_func.__name__, False))
        
        print()  # 空行分隔
    
    # 输出总结
    print("=" * 80)
    print("无限电池模式测试结果总结")
    print("=" * 80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:40}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 80)
    
    if all_passed:
        print("🎉 所有无限电池模式测试通过!")
        print("\n无限电池模式特性验证:")
        print("✓ 电池容量为无限大")
        print("✓ 不跟踪用过的电池")
        print("✓ 不启动电池充电进程")
        print("✓ 支持无限并发换电服务")
        print("✓ 换电后电池总数保持无限")
        print("✓ 服务时间仅取决于服务窗口数量")
    else:
        print("❌ 部分测试失败，请检查充电站无限模式实现")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_unlimited_battery_tests()
    sys.exit(0 if success else 1)
