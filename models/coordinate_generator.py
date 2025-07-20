# coordinate_generator.py
# 需求点生成以及需求点的需求生成函数

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random

class CoordinateGenerator:
    """坐标生成器类"""
    
    def __init__(self, area_size=100, seed=42):
        self.area_size = area_size
        np.random.seed(seed)
        random.seed(seed)
    
    def generate_customer_points(self, num_customers=10):
        """生成顾客点坐标"""
        customers = []
        for i in range(num_customers):
            x = np.random.uniform(0, self.area_size)
            y = np.random.uniform(0, self.area_size)
            demand_rate = np.random.exponential(scale=2.0)  # 需求生成率
            customers.append({
                'id': i,
                'type': 'customer',
                'latitude': x,
                'longitude': y,
                'demand_rate': demand_rate
            })
        return customers
    
    def generate_charging_stations(self, num_stations=15):
        """生成充电站坐标（网格分布）"""
        stations = []
        grid_size = math.ceil(math.sqrt(num_stations))
        for i in range(num_stations):
            row = i // grid_size
            col = i % grid_size
            x = (row + 0.5) * self.area_size / grid_size + np.random.normal(0, 2)
            y = (col + 0.5) * self.area_size / grid_size + np.random.normal(0, 2)
            
            # 确保坐标在有效范围内
            x = max(0, min(self.area_size, x))
            y = max(0, min(self.area_size, y))
            
            # 随机选择电池类型：有限(limited)或无限(unlimited)
            battery_type = np.random.choice(['limited', 'unlimited'], p=[0.6, 0.4])
            
            stations.append({
                'id': i,
                'type': 'charging_station',
                'latitude': x,
                'longitude': y,
                'battery_type': battery_type,  # limited or unlimited
                'battery_capacity': np.random.randint(20, 50) if battery_type == 'limited' else float('inf'),
                'service_windows': np.random.randint(2, 6),  # N个服务窗口
                'service_time': 0.5,  # 固定服务时间
                'charge_time': np.random.uniform(2.0, 4.0) if battery_type == 'limited' else 0
            })
        return stations
    
    def generate_distribution_centers(self, num_centers=3):
        """生成配送中心坐标（战略位置）"""
        centers = []
        # 预设一些战略位置
        strategic_positions = [
            (self.area_size * 0.2, self.area_size * 0.2),
            (self.area_size * 0.8, self.area_size * 0.8),
            (self.area_size * 0.5, self.area_size * 0.5),
            (self.area_size * 0.2, self.area_size * 0.8),
            (self.area_size * 0.8, self.area_size * 0.2)
        ]
        
        for i in range(num_centers):
            if i < len(strategic_positions):
                x, y = strategic_positions[i]
            else:
                x = np.random.uniform(self.area_size * 0.2, self.area_size * 0.8)
                y = np.random.uniform(self.area_size * 0.2, self.area_size * 0.8)
            
            centers.append({
                'id': i,
                'type': 'distribution_center',
                'latitude': x,
                'longitude': y,
                'truck_capacity': np.random.randint(3, 8),
                'truck_speed': np.random.uniform(40, 60),
                'truck_schedule_interval': np.random.uniform(3.0, 6.0),  # 固定往返时间间隔
                'processing_time': np.random.uniform(0.3, 0.8)
            })
        return centers
    
    def generate_service_points(self, num_service_points=20):
        """生成服务点坐标"""
        service_points = []
        for i in range(num_service_points):
            x = np.random.uniform(0, self.area_size)
            y = np.random.uniform(0, self.area_size)
            service_points.append({
                'id': i,
                'type': 'service_point',
                'latitude': x,
                'longitude': y,
                'service_time': np.random.uniform(0.2, 0.8)
            })
        return service_points
    
    def generate_all_coordinates(self, num_customers=10, num_charging_stations=15, 
                               num_distribution_centers=3, num_service_points=20):
        """生成所有类型的坐标点"""
        coordinates = {
            'customers': self.generate_customer_points(num_customers),
            'charging_stations': self.generate_charging_stations(num_charging_stations),
            'distribution_centers': self.generate_distribution_centers(num_distribution_centers),
            'service_points': self.generate_service_points(num_service_points)
        }
        return coordinates
    
    def calculate_distance_matrix(self, coordinates):
        """计算所有点之间的距离矩阵"""
        all_points = []
        point_mapping = {}
        
        # 整合所有点
        idx = 0
        for category, points in coordinates.items():
            for point in points:
                all_points.append(point)
                point_mapping[f"{category}_{point['id']}"] = idx
                idx += 1
        
        n = len(all_points)
        distance_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    lat1, lon1 = all_points[i]['latitude'], all_points[i]['longitude']
                    lat2, lon2 = all_points[j]['latitude'], all_points[j]['longitude']
                    distance_matrix[i][j] = self.calculate_distance(lat1, lon1, lat2, lon2)
        
        return distance_matrix, point_mapping, all_points
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two points using haversine formula (in km)"""
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return c * r
    
    def visualize_coordinates(self, coordinates):
        """可视化所有坐标点"""
        plt.figure(figsize=(12, 10))
        
        colors = {
            'customers': 'red',
            'charging_stations': 'blue',
            'distribution_centers': 'green',
            'service_points': 'orange'
        }
        
        markers = {
            'customers': 'o',
            'charging_stations': 's',
            'distribution_centers': '^',
            'service_points': 'D'
        }
        
        for category, points in coordinates.items():
            x_coords = [p['latitude'] for p in points]
            y_coords = [p['longitude'] for p in points]
            plt.scatter(x_coords, y_coords, c=colors[category], 
                       marker=markers[category], s=100, label=category, alpha=0.7)
        
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.title('UAV Logistics Network Layout')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


class DemandGenerator:
    """需求生成器类"""
    
    def __init__(self, coordinates, env):
        self.coordinates = coordinates
        self.env = env
        self.order_counter = 0
        
    def generate_single_demand(self, customer_id, service_point_id=None):
        """生成单个需求订单"""
        if service_point_id is None:
            service_point_id = np.random.choice([sp['id'] for sp in self.coordinates['service_points']])
        
        customer = next(c for c in self.coordinates['customers'] if c['id'] == customer_id)
        service_point = next(sp for sp in self.coordinates['service_points'] if sp['id'] == service_point_id)
        
        # 计算距离决定配送模式
        distance = CoordinateGenerator.calculate_distance(
            customer['latitude'], customer['longitude'],
            service_point['latitude'], service_point['longitude']
        )
        
        # 距离大于50使用配送中心模式
        delivery_mode = 'distribution_center' if distance > 50 else 'direct'
        
        order = {
            'order_id': self.order_counter,
            'customer_id': customer_id,
            'service_point_id': service_point_id,
            'delivery_mode': delivery_mode,
            'priority': np.random.randint(1, 4),
            'weight': np.random.uniform(0.5, 2.0),
            'creation_time': self.env.now if hasattr(self.env, 'now') else 0,
            'status': 'pending'
        }
        
        self.order_counter += 1
        return order
    
    def generate_demand_batch(self, customer_id, num_orders=None):
        """生成一批需求订单"""
        if num_orders is None:
            num_orders = max(1, int(np.random.exponential(scale=2)))
        
        orders = []
        for _ in range(num_orders):
            order = self.generate_single_demand(customer_id)
            orders.append(order)
        
        return orders


def save_coordinates_to_file(coordinates, filename='coordinates.xlsx'):
    """保存坐标到Excel文件"""
    with pd.ExcelWriter(filename) as writer:
        for category, points in coordinates.items():
            df = pd.DataFrame(points)
            df.to_excel(writer, sheet_name=category, index=False)
    print(f"坐标数据已保存到 {filename}")


def load_coordinates_from_file(filename='coordinates.xlsx'):
    """从Excel文件加载坐标"""
    coordinates = {}
    
    try:
        with pd.ExcelFile(filename) as reader:
            for sheet_name in reader.sheet_names:
                df = pd.read_excel(reader, sheet_name=sheet_name)
                coordinates[sheet_name] = df.to_dict('records')
        print(f"坐标数据已从 {filename} 加载")
        return coordinates
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None


if __name__ == "__main__":
    # 测试坐标生成器
    print("测试坐标生成器...")
    
    generator = CoordinateGenerator(area_size=100)
    coordinates = generator.generate_all_coordinates(
        num_customers=8,
        num_charging_stations=12,
        num_distribution_centers=3,
        num_service_points=15
    )
    
    print("生成的坐标点数量:")
    for category, points in coordinates.items():
        print(f"  {category}: {len(points)}")
    
    # 可视化
    generator.visualize_coordinates(coordinates)
    
    # 保存到文件
    save_coordinates_to_file(coordinates)
    
    # 测试需求生成器
    print("\n测试需求生成器...")
    
    class MockEnv:
        def __init__(self):
            self.now = 0
    
    env = MockEnv()
    demand_gen = DemandGenerator(coordinates, env)
    
    # 生成一些测试订单
    for customer_id in range(3):
        orders = demand_gen.generate_demand_batch(customer_id, 2)
        print(f"顾客 {customer_id} 生成订单:")
        for order in orders:
            print(f"  订单 {order['order_id']}: {order['delivery_mode']} 模式")
    
    print("坐标生成器测试完成！")
