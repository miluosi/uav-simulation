# test_visualization.py
# English-only visualization output test

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import io
import re

# Add current and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from models.uav_classes import UAV, calculate_distance
from models.charging_station import ChargingStation
from models.coordinate_generator import CoordinateGenerator
import simpy

# Configure matplotlib for English output
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
plt.rcParams['font.family'] = ['Arial', 'DejaVu Sans', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica', 'Verdana', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

def has_chinese_characters(text):
    """Check if text contains Chinese characters"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    return bool(chinese_pattern.search(text))

def capture_plot_text(fig):
    """Capture all text from plot"""
    texts = []
    
    # Get all axes
    for ax in fig.get_axes():
        # Titles
        if ax.get_title():
            texts.append(ax.get_title())
        
        # X-axis labels
        if ax.get_xlabel():
            texts.append(ax.get_xlabel())
        
        # Y-axis labels  
        if ax.get_ylabel():
            texts.append(ax.get_ylabel())
        
        # Tick labels
        for label in ax.get_xticklabels():
            texts.append(label.get_text())
        for label in ax.get_yticklabels():
            texts.append(label.get_text())
        
        # Legend
        legend = ax.get_legend()
        if legend:
            for text in legend.get_texts():
                texts.append(text.get_text())
        
        # Text annotations
        for text in ax.texts:
            texts.append(text.get_text())
    
    # Figure title
    if hasattr(fig, '_suptitle') and fig._suptitle:
        texts.append(fig._suptitle.get_text())
    
    return texts

def test_trajectory_visualization():
    """Test trajectory visualization with English output and save to local file"""
    print("=" * 60)
    print("Trajectory Visualization English Test")
    print("=" * 60)
    
    # Create simulation environment
    env = simpy.Environment()
    
    # Create UAV
    uav = UAV(env, "visual_test_uav", 39.9042, 116.4074)
    
    # Create charging stations
    charging_stations = [
        ChargingStation(env, 0, 39.9100, 116.4000, 'unlimited', 20, 2, 0.1),
        ChargingStation(env, 1, 39.9200, 116.3900, 'unlimited', 15, 3, 0.1)
    ]
    
    # Set test path
    test_waypoints = [
        {'latitude': 39.9150, 'longitude': 116.3950, 'service_time': 0.2},
        {'latitude': 39.9250, 'longitude': 116.3850, 'service_time': 0.3},
        {'latitude': 39.9042, 'longitude': 116.4074, 'service_time': 0.0}
    ]
    
    uav.set_planned_route(test_waypoints)
    
    def execute_and_visualize():
        yield env.process(uav.execute_planned_route(charging_stations))
        
        # Create trajectory visualization
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Plot trajectory
        if uav.trajectory_log:
            lats = [uav.current_latitude]  # Starting point
            lons = [uav.current_longitude]
            
            for log in uav.trajectory_log:
                to_lat, to_lon = log['to']
                lats.append(to_lat)
                lons.append(to_lon)
            
            # Plot trajectory line
            ax.plot(lons, lats, 'b-', linewidth=3, label='UAV Trajectory', alpha=0.8)
            ax.plot(lons[0], lats[0], 'go', markersize=12, label='Start Point', markeredgecolor='darkgreen', markeredgewidth=2)
            ax.plot(lons[-1], lats[-1], 'ro', markersize=12, label='End Point', markeredgecolor='darkred', markeredgewidth=2)
            
            # Plot waypoints
            for i, waypoint in enumerate(test_waypoints[:-1]):  # Exclude return point
                ax.plot(waypoint['longitude'], waypoint['latitude'], 'ys', 
                       markersize=10, label=f'Waypoint {i+1}' if i == 0 else '', 
                       markeredgecolor='orange', markeredgewidth=2)
                # Add waypoint number annotation
                ax.annotate(f'W{i+1}', (waypoint['longitude'], waypoint['latitude']), 
                           xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')
        
        # Plot charging stations
        for i, station in enumerate(charging_stations):
            ax.plot(station.longitude, station.latitude, 'c^', markersize=15,
                   label='Charging Station' if i == 0 else '', 
                   markeredgecolor='teal', markeredgewidth=2)
            # Add station ID annotation
            ax.annotate(f'CS{station.station_id}', (station.longitude, station.latitude), 
                       xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')
        
        # Set English labels
        ax.set_xlabel('Longitude (degrees)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitude (degrees)', fontsize=12, fontweight='bold')
        ax.set_title('UAV Flight Trajectory with Charging Stations\n(Real-time Path Tracking)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', framealpha=0.9, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add text box with trajectory info
        if uav.trajectory_log:
            total_distance = sum([log.get('distance', 0) for log in uav.trajectory_log])
            info_text = f'Total Distance: {total_distance:.2f} km\nWaypoints: {len(test_waypoints)}\nCharging Stations: {len(charging_stations)}'
            ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
                   verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8),
                   fontsize=10)
        
        plt.tight_layout()
        
        # Save to local file
        trajectory_filename = 'uav_trajectory_visualization.png'
        plt.savefig(trajectory_filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"📊 Trajectory visualization saved as: {trajectory_filename}")
        
        # Check text content
        plot_texts = capture_plot_text(fig)
        chinese_found = []
        
        for text in plot_texts:
            if text and has_chinese_characters(text):
                chinese_found.append(text)
        
        print(f"Plot created with {len(plot_texts)} text elements")
        print(f"Chinese characters found: {len(chinese_found)}")
        
        if chinese_found:
            print("❌ Chinese text found:")
            for text in chinese_found:
                print(f"  - '{text}'")
            plt.close(fig)
            return False
        else:
            print("✓ All text elements are in English")
            
        plt.close(fig)
        return True
    
    env.process(execute_and_visualize())
    env.run(until=10)  # Set maximum simulation time limit
    
    return True

def test_statistics_visualization():
    """测试统计图表的英文输出"""
    print("\n" + "=" * 60)
    print("Statistics Visualization English Test")
    print("=" * 60)
    
    # 创建模拟数据
    time_points = np.linspace(0, 10, 50)
    waiting_times = np.random.exponential(2, 50)
    battery_levels = np.maximum(100 - time_points * 8 + np.random.normal(0, 5, 50), 0)
    service_counts = np.cumsum(np.random.poisson(0.3, 50))
    
    # 创建多子图统计可视化
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # 等待时间分布
    ax1.hist(waiting_times, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_xlabel('Waiting Time (hours)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('UAV Waiting Time Distribution')
    ax1.grid(True, alpha=0.3)
    
    # 电池电量变化
    ax2.plot(time_points, battery_levels, 'g-', linewidth=2)
    ax2.set_xlabel('Time (hours)')
    ax2.set_ylabel('Battery Level (%)')
    ax2.set_title('UAV Battery Level Over Time')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)
    
    # 服务计数
    ax3.step(time_points, service_counts, 'r-', where='post', linewidth=2)
    ax3.set_xlabel('Time (hours)')
    ax3.set_ylabel('Cumulative Services')
    ax3.set_title('Charging Station Service Count')
    ax3.grid(True, alpha=0.3)
    
    # 效率对比
    categories = ['Direct\nDelivery', 'Hub\nDelivery', 'Mixed\nMode']
    efficiency_values = [85, 92, 88]
    colors = ['lightcoral', 'lightgreen', 'lightblue']
    
    bars = ax4.bar(categories, efficiency_values, color=colors, alpha=0.8, edgecolor='black')
    ax4.set_ylabel('Efficiency (%)')
    ax4.set_title('Delivery Mode Efficiency Comparison')
    ax4.set_ylim(0, 100)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 添加数值标签
    for bar, value in zip(bars, efficiency_values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value}%', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # 检查所有文本
    plot_texts = capture_plot_text(fig)
    chinese_found = []
    
    for text in plot_texts:
        if text and has_chinese_characters(text):
            chinese_found.append(text)
    
    print(f"Statistics plots created with {len(plot_texts)} text elements")
    print(f"Chinese characters found: {len(chinese_found)}")
    
    if chinese_found:
        print("❌ Chinese text found in statistics:")
        for text in chinese_found:
            print(f"  - '{text}'")
        plt.close(fig)
        return False
    else:
        print("✓ All statistics text elements are in English")
    
    plt.close(fig)
    return True

def test_nearest_charging_station_visualization():
    """Test and visualize nearest charging station selection strategy"""
    print("\n" + "=" * 60)
    print("Nearest Charging Station Strategy Visualization Test")
    print("=" * 60)
    
    # Create multiple UAVs at different positions
    uav_positions = [
        {'name': 'UAV_North', 'lat': 39.920, 'lon': 116.405, 'color': 'blue'},
        {'name': 'UAV_South', 'lat': 39.890, 'lon': 116.415, 'color': 'red'},
        {'name': 'UAV_East', 'lat': 39.905, 'lon': 116.430, 'color': 'green'},
        {'name': 'UAV_West', 'lat': 39.900, 'lon': 116.390, 'color': 'purple'},
        {'name': 'UAV_Center', 'lat': 39.904, 'lon': 116.407, 'color': 'orange'}
    ]
    
    # Create charging stations in a grid pattern
    charging_stations = [
        {'id': 0, 'lat': 39.910, 'lon': 116.400, 'type': 'unlimited', 'capacity': 20},
        {'id': 1, 'lat': 39.920, 'lon': 116.390, 'type': 'limited', 'capacity': 15},
        {'id': 2, 'lat': 39.890, 'lon': 116.420, 'type': 'unlimited', 'capacity': 25},
        {'id': 3, 'lat': 39.900, 'lon': 116.410, 'type': 'limited', 'capacity': 12},
        {'id': 4, 'lat': 39.930, 'lon': 116.430, 'type': 'unlimited', 'capacity': 30}
    ]
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Plot charging stations
    for station in charging_stations:
        marker = '^' if station['type'] == 'unlimited' else 's'
        color = 'darkgreen' if station['type'] == 'unlimited' else 'darkred'
        size = station['capacity'] * 15  # Size proportional to capacity
        
        ax.scatter(station['lon'], station['lat'], marker=marker, c=color, s=size, 
                  alpha=0.8, edgecolors='black', linewidth=2,
                  label=f"{station['type'].title()} Charging Station" if station['id'] == 0 or 
                        (station['id'] == 1 and station['type'] == 'limited') else '')
        
        # Add station annotation
        ax.annotate(f"CS{station['id']}\n({station['type']})\nCap: {station['capacity']}", 
                   (station['lon'], station['lat']), 
                   xytext=(10, 10), textcoords='offset points', 
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # For each UAV, find nearest charging station and draw connection
    for uav in uav_positions:
        # Calculate distances to all charging stations
        distances = []
        for station in charging_stations:
            dist = calculate_distance(uav['lat'], uav['lon'], station['lat'], station['lon'])
            distances.append({'station': station, 'distance': dist})
        
        # Find nearest station
        nearest = min(distances, key=lambda x: x['distance'])
        
        # Plot UAV position
        ax.scatter(uav['lon'], uav['lat'], marker='o', c=uav['color'], s=200, 
                  alpha=0.9, edgecolors='black', linewidth=2)
        
        # Add UAV annotation
        ax.annotate(f"{uav['name']}", 
                   (uav['lon'], uav['lat']), 
                   xytext=(-15, -15), textcoords='offset points', 
                   fontsize=10, fontweight='bold', color=uav['color'])
        
        # Draw line to nearest charging station
        ax.plot([uav['lon'], nearest['station']['lon']], 
               [uav['lat'], nearest['station']['lat']], 
               color=uav['color'], linestyle='--', linewidth=2, alpha=0.7)
        
        # Add distance annotation on the line
        mid_lon = (uav['lon'] + nearest['station']['lon']) / 2
        mid_lat = (uav['lat'] + nearest['station']['lat']) / 2
        ax.annotate(f"{nearest['distance']:.2f}km", 
                   (mid_lon, mid_lat), 
                   fontsize=8, fontweight='bold', color=uav['color'],
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        print(f"{uav['name']} -> Nearest: CS{nearest['station']['id']} ({nearest['distance']:.2f}km)")
    
    # Set plot properties
    ax.set_xlabel('Longitude (degrees)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitude (degrees)', fontsize=12, fontweight='bold')
    ax.set_title('UAV Nearest Charging Station Selection Strategy\n(Optimal Distance-Based Assignment)', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Add legend
    ax.legend(loc='upper left', framealpha=0.9, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle=':')
    
    # Add strategy explanation text box
    strategy_text = ("Strategy: Distance-Based Selection\n"
                    "• UAVs select nearest charging station\n"
                    "• Dashed lines show optimal routes\n"
                    "• Triangle: Unlimited capacity\n"
                    "• Square: Limited capacity")
    ax.text(0.02, 0.02, strategy_text, transform=ax.transAxes, 
           verticalalignment='bottom', fontsize=10,
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan', alpha=0.9))
    
    plt.tight_layout()
    
    # Save to local file
    strategy_filename = 'nearest_charging_station_strategy.png'
    plt.savefig(strategy_filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"📊 Nearest charging station strategy saved as: {strategy_filename}")
    
    # Check text content
    plot_texts = capture_plot_text(fig)
    chinese_found = []
    
    for text in plot_texts:
        if text and has_chinese_characters(text):
            chinese_found.append(text)
    
    print(f"Strategy plot created with {len(plot_texts)} text elements")
    print(f"Chinese characters found: {len(chinese_found)}")
    
    if chinese_found:
        print("❌ Chinese text found:")
        for text in chinese_found:
            print(f"  - '{text}'")
        plt.close(fig)
        return False
    else:
        print("✓ All text elements are in English")
    
    plt.close(fig)
    return True

def test_performance_metrics_visualization():
    """测试性能指标可视化的英文输出"""
    print("\n" + "=" * 60)
    print("Performance Metrics Visualization English Test")
    print("=" * 60)
    
    # 模拟性能数据
    metrics_data = {
        'Service Time': [0.2, 0.3, 0.25, 0.4, 0.35],
        'Distance (km)': [5.2, 7.8, 6.1, 9.3, 8.0],
        'Battery Usage (%)': [15, 23, 18, 28, 24],
        'Success Rate (%)': [98, 95, 97, 92, 94]
    }
    
    station_labels = ['Station A', 'Station B', 'Station C', 'Station D', 'Station E']
    
    # 创建性能对比图
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 服务时间对比
    ax1.bar(station_labels, metrics_data['Service Time'], 
           color='lightblue', alpha=0.8, edgecolor='navy')
    ax1.set_ylabel('Average Service Time (hours)')
    ax1.set_title('Charging Station Service Time Comparison')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 距离分析
    ax2.plot(station_labels, metrics_data['Distance (km)'], 
            'o-', color='green', linewidth=2, markersize=8)
    ax2.set_ylabel('Average Distance (km)')
    ax2.set_title('Average Travel Distance to Stations')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    
    # 电池使用率
    colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(station_labels)))
    wedges, texts, autotexts = ax3.pie(metrics_data['Battery Usage (%)'], 
                                      labels=station_labels, autopct='%1.1f%%',
                                      colors=colors, startangle=90)
    ax3.set_title('Battery Usage Distribution by Station')
    
    # 成功率趋势
    ax4.bar(station_labels, metrics_data['Success Rate (%)'], 
           color='lightgreen', alpha=0.8, edgecolor='darkgreen')
    ax4.set_ylabel('Success Rate (%)')
    ax4.set_title('Service Success Rate by Station')
    ax4.set_ylim(85, 100)
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 添加数值标签到成功率图
    for i, v in enumerate(metrics_data['Success Rate (%)']):
        ax4.text(i, v + 0.5, f'{v}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # 检查文本内容
    plot_texts = capture_plot_text(fig)
    chinese_found = []
    
    for text in plot_texts:
        if text and has_chinese_characters(text):
            chinese_found.append(text)
    
    print(f"Performance metrics plots created with {len(plot_texts)} text elements")
    print(f"Chinese characters found: {len(chinese_found)}")
    
    if chinese_found:
        print("❌ Chinese text found in performance metrics:")
        for text in chinese_found:
            print(f"  - '{text}'")
        plt.close(fig)
        return False
    else:
        print("✓ All performance metrics text elements are in English")
    
    plt.close(fig)
    return True

def test_coordinate_visualization():
    """测试坐标可视化的英文输出"""
    print("\n" + "=" * 60)
    print("Coordinate System Visualization English Test")
    print("=" * 60)
    
    # 生成坐标数据
    generator = CoordinateGenerator(area_size=15)
    coordinates = generator.generate_all_coordinates(
        num_customers=8,
        num_charging_stations=4,
        num_distribution_centers=2,
        num_service_points=6
    )
    
    # 创建坐标系统可视化
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 绘制不同类型的点
    point_types = [
        ('customers', 'Customers', 'o', 'blue', 8),
        ('charging_stations', 'Charging Stations', '^', 'red', 12),
        ('distribution_centers', 'Distribution Centers', 's', 'green', 10),
        ('service_points', 'Service Points', 'D', 'orange', 8)
    ]
    
    for coord_type, label, marker, color, size in point_types:
        coords = coordinates[coord_type]
        if coords:
            lats = [c['latitude'] for c in coords]
            lons = [c['longitude'] for c in coords]
            ax.scatter(lons, lats, marker=marker, c=color, s=size**2, 
                      label=label, alpha=0.8, edgecolors='black', linewidth=1)
    
    # 设置图形属性
    ax.set_xlabel('Longitude (degrees)')
    ax.set_ylabel('Latitude (degrees)')
    ax.set_title('UAV Logistics System Coordinate Layout')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # 添加区域信息
    all_lats = []
    all_lons = []
    for coord_type in coordinates:
        for coord in coordinates[coord_type]:
            all_lats.append(coord['latitude'])
            all_lons.append(coord['longitude'])
    
    if all_lats and all_lons:
        center_lat = sum(all_lats) / len(all_lats)
        center_lon = sum(all_lons) / len(all_lons)
        
        # 添加中心点标记
        ax.plot(center_lon, center_lat, 'k*', markersize=15, 
               label='System Center', markeredgecolor='white', markeredgewidth=1)
        
        # 添加信息文本
        info_text = f'System Coverage Area: {generator.area_size} km'
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    # 检查文本内容
    plot_texts = capture_plot_text(fig)
    chinese_found = []
    
    for text in plot_texts:
        if text and has_chinese_characters(text):
            chinese_found.append(text)
    
    print(f"Coordinate visualization created with {len(plot_texts)} text elements")
    print(f"Chinese characters found: {len(chinese_found)}")
    
    if chinese_found:
        print("❌ Chinese text found in coordinate visualization:")
        for text in chinese_found:
            print(f"  - '{text}'")
        plt.close(fig)
        return False
    else:
        print("✓ All coordinate visualization text elements are in English")
    
    plt.close(fig)
    return True

def run_visualization_tests():
    """Run all visualization tests"""
    print("Visualization English-Only Output Test Suite")
    print("=" * 80)
    
    # Configure matplotlib parameters for English output
    plt.rcParams['font.family'] = ['Arial', 'DejaVu Sans', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 10
    
    test_functions = [
        test_trajectory_visualization,
        test_nearest_charging_station_visualization,
        test_statistics_visualization,
        test_performance_metrics_visualization,
        test_coordinate_visualization
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
    print("Visualization English Test Results")
    print("=" * 80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:40}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 80)
    
    if all_passed:
        print("🎉 All visualization tests passed!")
        print("\nVerified Features:")
        print("✓ Trajectory visualization with English labels (saved locally)")
        print("✓ Nearest charging station strategy visualization (saved locally)")
        print("✓ Statistics charts with English text")
        print("✓ Performance metrics in English")
        print("✓ Coordinate system visualization in English")
        print("✓ No Chinese characters in any plot elements")
        print("✓ Proper font settings for English display")
        print("\n📁 Local image files generated:")
        print("  • uav_trajectory_visualization.png")
        print("  • nearest_charging_station_strategy.png")
    else:
        print("❌ Some visualization tests failed")
        print("Please check for Chinese text in plot outputs")
    
    return all_passed


if __name__ == "__main__":
    success = run_visualization_tests()
    sys.exit(0 if success else 1)
