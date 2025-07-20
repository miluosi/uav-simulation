# complete_simulation.py
# Complete system functionality simulation

import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .coordinate_generator import CoordinateGenerator, DemandGenerator
from .uav_classes import UAV, Order, Goods, DemandPoint
from .charging_station import ChargingStation
from .distribution_center import DistributionCenter


class CompleteUAVLogisticsSimulation:
    """Complete UAV logistics simulation system"""
    
    def __init__(self, coordinates, simulation_time=50):
        self.env = simpy.Environment()
        self.coordinates = coordinates
        self.simulation_time = simulation_time
        
        # 初始化各类设施
        self.charging_stations = {}
        self.distribution_centers = {}
        self.demand_points = {}
        self.service_points = coordinates['service_points']
        
        # 订单和统计
        self.all_orders = []
        self.completed_orders = []
        
        self._initialize_infrastructure()
        self._initialize_demand_points()
        
        # Start statistics collection
        self.env.process(self._statistics_collection())
    
    def _initialize_infrastructure(self):
        """Initialize infrastructure"""
        print("Initializing infrastructure...")
        
        # Create charging stations
        for station_data in self.coordinates['charging_stations']:
            station = ChargingStation(
                self.env,
                station_data['id'],
                station_data['latitude'],
                station_data['longitude'],
                battery_type=station_data['battery_type'],
                battery_capacity=station_data.get('battery_capacity', 30),
                service_windows=station_data['service_windows'],
                service_time=station_data['service_time'],
                charge_time=station_data.get('charge_time', 2.0)
            )
            self.charging_stations[station_data['id']] = station
        
        # Create distribution centers
        for dc_data in self.coordinates['distribution_centers']:
            dc = DistributionCenter(
                self.env,
                dc_data['id'],
                dc_data['latitude'],
                dc_data['longitude'],
                truck_count=2,
                truck_capacity=dc_data['truck_capacity'],
                truck_speed=dc_data['truck_speed'],
                schedule_interval=dc_data['truck_schedule_interval'],
                processing_time=dc_data['processing_time']
            )
            self.distribution_centers[dc_data['id']] = dc
            
            # Start truck scheduling
            dc.start_truck_schedules(self.service_points)
        
        print(f"Created {len(self.charging_stations)} charging stations")
        print(f"Created {len(self.distribution_centers)} distribution centers")
    
    def _initialize_demand_points(self):
        """Initialize demand points"""
        print("Initializing demand points...")
        
        for customer_data in self.coordinates['customers']:
            uav_count = np.random.randint(2, 5)  # 2-4 UAVs per demand point
            
            demand_point = DemandPoint(
                self.env,
                customer_data['id'],
                customer_data['latitude'],
                customer_data['longitude'],
                uav_count,
                customer_data['demand_rate']
            )
            
            self.demand_points[customer_data['id']] = demand_point
            
            # Start demand generation process
            self.env.process(demand_point.generate_demand_process(
                self.service_points,
                list(self.distribution_centers.values()),
                list(self.charging_stations.values())
            ))
        
        print(f"Created {len(self.demand_points)} demand points")
    
    def _statistics_collection(self):
        """Statistics information collection"""
        while True:
            yield self.env.timeout(5.0)  # Collect every 5 time units
            
            # Collect completed orders
            for demand_point in self.demand_points.values():
                for uav in demand_point.uav_queue:
                    if (hasattr(uav, 'current_order') and 
                        uav.current_order and 
                        uav.current_order.status == 'completed' and
                        uav.current_order not in self.completed_orders):
                        self.completed_orders.append(uav.current_order)
    
    def run_simulation(self):
        """Run simulation"""
        print(f"Starting complete simulation system, duration: {self.simulation_time} time units...")
        print("=" * 60)
        
        self.env.run(until=self.simulation_time)
        
        print("=" * 60)
        print("Simulation completed!")
    
    def get_comprehensive_statistics(self):
        """Get comprehensive statistical information"""
        stats = {}
        
        # Overall statistics
        total_orders = sum(dp.orders_generated for dp in self.demand_points.values())
        total_completed = len(self.completed_orders)
        
        stats['overall'] = {
            'simulation_time': self.simulation_time,
            'total_orders_generated': total_orders,
            'total_orders_completed': total_completed,
            'completion_rate': (total_completed / max(1, total_orders)) * 100
        }
        
        # Demand point statistics
        stats['demand_points'] = {}
        total_uavs = 0
        active_uavs = 0
        
        for dp_id, dp in self.demand_points.items():
            uav_stats = []
            for uav in dp.uav_queue:
                total_uavs += 1
                if uav.total_orders_completed > 0:
                    active_uavs += 1
                    uav_stats.append({
                        'uav_id': uav.uav_id,
                        'orders_completed': uav.total_orders_completed,
                        'total_distance': uav.total_distance,
                        'total_flight_time': uav.total_flight_time
                    })
            
            stats['demand_points'][dp_id] = {
                'orders_generated': dp.orders_generated,
                'uav_count': len(dp.uav_queue),
                'active_uavs': len([u for u in dp.uav_queue if u.total_orders_completed > 0]),
                'uav_statistics': uav_stats
            }
        
        stats['overall']['total_uavs'] = total_uavs
        stats['overall']['active_uavs'] = active_uavs
        
        # Charging station statistics
        stats['charging_stations'] = {}
        for station_id, station in self.charging_stations.items():
            stats['charging_stations'][station_id] = station.get_statistics()
        
        # Distribution center statistics
        stats['distribution_centers'] = {}
        for dc_id, dc in self.distribution_centers.items():
            stats['distribution_centers'][dc_id] = dc.get_statistics()
        
        # Order completion time analysis
        if self.completed_orders:
            completion_times = [
                order.completion_time - order.creation_time 
                for order in self.completed_orders 
                if order.completion_time is not None
            ]
            
            if completion_times:
                stats['order_analysis'] = {
                    'avg_completion_time': np.mean(completion_times),
                    'max_completion_time': np.max(completion_times),
                    'min_completion_time': np.min(completion_times),
                    'std_completion_time': np.std(completion_times)
                }
                
                # Classify by delivery mode
                direct_orders = [o for o in self.completed_orders if o.delivery_mode == 'direct']
                dc_orders = [o for o in self.completed_orders if o.delivery_mode == 'distribution_center']
                
                stats['order_analysis']['direct_delivery_count'] = len(direct_orders)
                stats['order_analysis']['distribution_center_count'] = len(dc_orders)
        
        return stats
    
    def print_statistics(self, stats):
        """Print statistical information"""
        print("\n" + "="*60)
        print("Simulation Statistics Results")
        print("="*60)
        
        # Overall statistics
        overall = stats['overall']
        print(f"Simulation duration: {overall['simulation_time']}")
        print(f"Total orders generated: {overall['total_orders_generated']}")
        print(f"Completed orders: {overall['total_orders_completed']}")
        print(f"Completion rate: {overall['completion_rate']:.1f}%")
        print(f"Total UAVs: {overall['total_uavs']}")
        print(f"Active UAVs: {overall['active_uavs']}")
        
        # Order analysis
        if 'order_analysis' in stats:
            analysis = stats['order_analysis']
            print(f"\nOrder completion time analysis:")
            print(f"  Average completion time: {analysis['avg_completion_time']:.2f}")
            print(f"  Maximum completion time: {analysis['max_completion_time']:.2f}")
            print(f"  Minimum completion time: {analysis['min_completion_time']:.2f}")
            print(f"  Direct delivery orders: {analysis['direct_delivery_count']}")
            print(f"  Distribution center orders: {analysis['distribution_center_count']}")
        
        # Charging station statistics
        print(f"\nCharging station statistics:")
        total_charged = 0
        active_stations = 0
        
        for station_id, station_stats in stats['charging_stations'].items():
            if station_stats['total_served'] > 0:
                active_stations += 1
                total_charged += station_stats['total_served']
                print(f"  Charging Station {station_id} ({station_stats['battery_type']}):")
                print(f"    Service count: {station_stats['total_served']}")
                print(f"    Average waiting time: {station_stats['avg_waiting_time']:.2f}")
                print(f"    Service windows: {station_stats['service_windows']}")
        
        print(f"  Active charging stations: {active_stations}")
        print(f"  Total charging sessions: {total_charged}")
        
        # Distribution center statistics
        print(f"\nDistribution center statistics:")
        total_dc_goods = 0
        
        for dc_id, dc_stats in stats['distribution_centers'].items():
            total_dc_goods += dc_stats['total_goods_received']
            print(f"  Distribution Center {dc_id}:")
            print(f"    Received goods: {dc_stats['total_goods_received']}")
            print(f"    Processed goods: {dc_stats['total_goods_processed']}")
            print(f"    Served UAVs: {dc_stats['total_uavs_served']}")
            print(f"    Truck count: {dc_stats['truck_count']}")
        
        print(f"  Total distribution center goods: {total_dc_goods}")
    
    def visualize_results(self, stats):
        """Visualize simulation results"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Configure matplotlib for English output
        plt.rcParams['font.family'] = ['Arial', 'DejaVu Sans', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 1. UAV performance distribution
        uav_orders = []
        for dp_stats in stats['demand_points'].values():
            for uav_stat in dp_stats['uav_statistics']:
                uav_orders.append(uav_stat['orders_completed'])
        
        if uav_orders:
            axes[0,0].hist(uav_orders, bins=max(10, len(set(uav_orders))), alpha=0.7, color='skyblue')
            axes[0,0].set_title('UAV Completed Orders Distribution')
            axes[0,0].set_xlabel('Completed Orders')
            axes[0,0].set_ylabel('Number of UAVs')
        
        # 2. Charging station utilization
        station_ids = []
        served_counts = []
        battery_types = []
        
        for station_id, station_stats in stats['charging_stations'].items():
            station_ids.append(f"CS{station_id}")
            served_counts.append(station_stats['total_served'])
            battery_types.append(station_stats['battery_type'])
        
        colors = ['blue' if bt == 'limited' else 'green' for bt in battery_types]
        axes[0,1].bar(range(len(station_ids)), served_counts, alpha=0.7, color=colors)
        axes[0,1].set_title('Charging Station Service Count')
        axes[0,1].set_xlabel('Charging Station ID')
        axes[0,1].set_ylabel('Service Count')
        axes[0,1].set_xticks(range(len(station_ids)))
        axes[0,1].set_xticklabels(station_ids, rotation=45)
        
        # 3. Delivery mode comparison
        if 'order_analysis' in stats:
            direct_count = stats['order_analysis']['direct_delivery_count']
            dc_count = stats['order_analysis']['distribution_center_count']
            
            modes = ['Direct Delivery', 'Distribution Center']
            counts = [direct_count, dc_count]
            colors = ['lightcoral', 'lightgreen']
            
            axes[1,0].pie(counts, labels=modes, autopct='%1.1f%%', colors=colors)
            axes[1,0].set_title('Delivery Mode Distribution')
        
        # 4. Distribution center performance
        dc_ids = []
        goods_received = []
        
        for dc_id, dc_stats in stats['distribution_centers'].items():
            dc_ids.append(f"DC{dc_id}")
            goods_received.append(dc_stats['total_goods_received'])
        
        if dc_ids:
            axes[1,1].bar(dc_ids, goods_received, alpha=0.7, color='orange')
            axes[1,1].set_title('Distribution Center Received Goods')
            axes[1,1].set_xlabel('Distribution Center ID')
            axes[1,1].set_ylabel('Received Goods Count')
        
        plt.tight_layout()
        plt.show()


def run_complete_simulation_test():
    """Run complete simulation test"""
    print("Starting complete simulation system test...")
    
    # Generate coordinates
    generator = CoordinateGenerator(area_size=80, seed=42)
    coordinates = generator.generate_all_coordinates(
        num_customers=6,
        num_charging_stations=10,
        num_distribution_centers=3,
        num_service_points=12
    )
    
    # Visualize network layout
    generator.visualize_coordinates(coordinates)
    
    # Create and run simulation
    simulation = CompleteUAVLogisticsSimulation(coordinates, simulation_time=30)
    simulation.run_simulation()
    
    # Get and display statistical results
    stats = simulation.get_comprehensive_statistics()
    simulation.print_statistics(stats)
    
    # Visualize results
    simulation.visualize_results(stats)
    
    return simulation, stats


if __name__ == "__main__":
    simulation, stats = run_complete_simulation_test()
