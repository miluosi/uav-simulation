#!/usr/bin/env python3
# run_final_test.py - 运行最终的混合运输模式测试

import sys
import os

print("=== 最终混合运输模式测试 ===")
print("运行混合运输测试，统一路径规划模式，综合可视化")

# Add current directory and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

def run_final_mixed_transportation_test():
    """运行最终的混合运输模式测试"""
    try:
        from working_run_tests import test_mixed_transportation_modes
        
        print("开始运行混合运输模式测试...")
        print("特性：")
        print("• 统一的无人机路径规划模式（最短路径算法）")
        print("• 无人机路径和卡车轨迹在同一图表显示")
        print("• 无人机路径：实线，卡车轨迹：虚线")
        print("• 路径详细信息保存到本地文件")
        print("• 多个需求点综合测试")
        print("-" * 60)
        
        success = test_mixed_transportation_modes()
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 混合运输模式测试完成！")
            print("输出文件：")
            print("• mixed_transportation_analysis.png - 综合分析图表")
            print("• uav_truck_paths_log.txt - 详细路径日志")
            print("=" * 60)
            
            # 显示生成的文件信息
            output_files = [
                "mixed_transportation_analysis.png",
                "uav_truck_paths_log.txt"
            ]
            
            print("\n生成的文件详情：")
            for filename in output_files:
                filepath = os.path.join(os.getcwd(), filename)
                if os.path.exists(filepath):
                    file_size = os.path.getsize(filepath)
                    print(f"✓ {filename} ({file_size} bytes)")
                else:
                    print(f"⚠ {filename} (未找到)")
            
            return True
        else:
            print("\n❌ 测试失败，请检查错误信息")
            return False
            
    except Exception as e:
        print(f"运行测试时发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("启动最终混合运输模式测试...")
    success = run_final_mixed_transportation_test()
    
    if success:
        print("\n系统测试完成，所有文件已生成！")
        print("您可以查看以下文件：")
        print("1. mixed_transportation_analysis.png - 查看综合路径图表")
        print("2. uav_truck_paths_log.txt - 查看详细路径信息")
        sys.exit(0)
    else:
        print("\n测试失败，请修复问题后重试。")
        sys.exit(1)
