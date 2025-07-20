# test_coordinate_generator.py
# 测试需求点生成py文件

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from models.coordinate_generator import CoordinateGenerator, DemandGenerator

def test_coordinate_generator():
    """测试坐标生成器"""
    print("=" * 50)
    print("测试坐标生成器")
    print("=" * 50)
    
    # 创建坐标生成器
    generator = CoordinateGenerator(area_size=100, seed=42)
    
    # 测试各类坐标生成
    print("1. 测试顾客点生成...")
    customers = generator.generate_customer_points(5)
    print(f"   生成 {len(customers)} 个顾客点")
    for customer in customers[:2]:  # 显示前2个
        print(f"   顾客 {customer['id']}: ({customer['latitude']:.1f}, {customer['longitude']:.1f}), "
              f"需求率: {customer['demand_rate']:.2f}")
    
    print("\n2. 测试充电站生成...")
    charging_stations = generator.generate_charging_stations(8)
    print(f"   生成 {len(charging_stations)} 个充电站")
    for station in charging_stations[:2]:  # 显示前2个
        print(f"   充电站 {station['id']}: ({station['latitude']:.1f}, {station['longitude']:.1f}), "
              f"类型: {station['battery_type']}, 窗口: {station['service_windows']}")
    
    print("\n3. 测试配送中心生成...")
    distribution_centers = generator.generate_distribution_centers(3)
    print(f"   生成 {len(distribution_centers)} 个配送中心")
    for dc in distribution_centers:
        print(f"   配送中心 {dc['id']}: ({dc['latitude']:.1f}, {dc['longitude']:.1f}), "
              f"卡车容量: {dc['truck_capacity']}, 调度间隔: {dc['truck_schedule_interval']:.1f}")
    
    print("\n4. 测试服务点生成...")
    service_points = generator.generate_service_points(6)
    print(f"   生成 {len(service_points)} 个服务点")
    for sp in service_points[:2]:  # 显示前2个
        print(f"   服务点 {sp['id']}: ({sp['latitude']:.1f}, {sp['longitude']:.1f}), "
              f"服务时间: {sp['service_time']:.2f}")
    
    print("\n5. 测试完整坐标生成...")
    coordinates = generator.generate_all_coordinates(
        num_customers=5,
        num_charging_stations=8,
        num_distribution_centers=3,
        num_service_points=6
    )
    
    print("   完整坐标生成结果:")
    for category, points in coordinates.items():
        print(f"     {category}: {len(points)} 个")
    
    print("\n6. 测试距离矩阵计算...")
    distance_matrix, point_mapping, all_points = generator.calculate_distance_matrix(coordinates)
    print(f"   距离矩阵大小: {distance_matrix.shape}")
    print(f"   总点数: {len(all_points)}")
    print(f"   点映射数量: {len(point_mapping)}")
    
    # 显示一些距离示例
    print("   部分距离示例:")
    for i in range(min(3, len(all_points))):
        for j in range(min(3, len(all_points))):
            if i != j:
                print(f"     点{i} -> 点{j}: {distance_matrix[i][j]:.2f}")
    
    return coordinates


def test_demand_generator():
    """测试需求生成器"""
    print("\n" + "=" * 50)
    print("测试需求生成器")
    print("=" * 50)
    
    # 创建测试环境和坐标
    class MockEnv:
        def __init__(self):
            self.now = 0
    
    env = MockEnv()
    
    # 生成测试坐标
    generator = CoordinateGenerator(area_size=80, seed=42)
    coordinates = generator.generate_all_coordinates(
        num_customers=4,
        num_charging_stations=6,
        num_distribution_centers=2,
        num_service_points=5
    )
    
    # 创建需求生成器
    demand_gen = DemandGenerator(coordinates, env)
    
    print("1. 测试单个需求生成...")
    for customer_id in range(3):
        order = demand_gen.generate_single_demand(customer_id)
        print(f"   订单 {order['order_id']}: 顾客 {order['customer_id']} -> "
              f"服务点 {order['service_point_id']}, 模式: {order['delivery_mode']}, "
              f"优先级: {order['priority']}")
    
    print("\n2. 测试批量需求生成...")
    for customer_id in range(2):
        orders = demand_gen.generate_demand_batch(customer_id, 3)
        print(f"   顾客 {customer_id} 生成 {len(orders)} 个订单:")
        for order in orders:
            print(f"     订单 {order['order_id']}: -> 服务点 {order['service_point_id']}, "
                  f"模式: {order['delivery_mode']}")
    
    print("\n3. 测试配送模式决策...")
    direct_count = 0
    dc_count = 0
    
    for _ in range(20):
        order = demand_gen.generate_single_demand(0)
        if order['delivery_mode'] == 'direct':
            direct_count += 1
        else:
            dc_count += 1
    
    print(f"   20个订单中:")
    print(f"     直接配送: {direct_count}")
    print(f"     配送中心: {dc_count}")


def test_file_operations():
    """测试文件操作"""
    print("\n" + "=" * 50)
    print("测试文件操作")
    print("=" * 50)
    
    from models.coordinate_generator import save_coordinates_to_file, load_coordinates_from_file
    
    # 生成测试坐标
    generator = CoordinateGenerator(area_size=60, seed=123)
    coordinates = generator.generate_all_coordinates(3, 5, 2, 4)
    
    print("1. 测试保存坐标到文件...")
    filename = 'test_coordinates.xlsx'
    save_coordinates_to_file(coordinates, filename)
    
    print("2. 测试从文件加载坐标...")
    loaded_coordinates = load_coordinates_from_file(filename)
    
    if loaded_coordinates:
        print("   加载成功！对比结果:")
        for category in coordinates.keys():
            original_count = len(coordinates[category])
            loaded_count = len(loaded_coordinates[category])
            print(f"     {category}: 原始 {original_count}, 加载 {loaded_count}, "
                  f"匹配: {'✓' if original_count == loaded_count else '✗'}")
    
    # 清理测试文件
    try:
        os.remove(filename)
        print("   测试文件已清理")
    except:
        pass


def test_visualization():
    """测试可视化功能"""
    print("\n" + "=" * 50)
    print("测试可视化功能")
    print("=" * 50)
    
    # 生成测试坐标
    generator = CoordinateGenerator(area_size=60, seed=456)
    coordinates = generator.generate_all_coordinates(4, 6, 2, 5)
    
    print("1. 生成可视化图表...")
    try:
        generator.visualize_coordinates(coordinates)
        print("   可视化成功！")
    except Exception as e:
        print(f"   可视化失败: {e}")


def run_all_tests():
    """运行所有测试"""
    print("开始测试坐标生成器模块")
    print("=" * 70)
    
    try:
        # 测试坐标生成
        coordinates = test_coordinate_generator()
        
        # 测试需求生成
        test_demand_generator()
        
        # 测试文件操作
        test_file_operations()
        
        # 测试可视化
        test_visualization()
        
        print("\n" + "=" * 70)
        print("所有测试完成！")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n✓ 坐标生成器测试通过")
    else:
        print("\n✗ 坐标生成器测试失败")
        sys.exit(1)
