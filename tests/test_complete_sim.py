#!/usr/bin/env python3
# 测试complete_simulation导入

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

print("测试complete_simulation模块导入...")

try:
    print("尝试导入 models.complete_simulation...")
    from models.complete_simulation import run_complete_simulation_test
    print("✓ 导入成功")
    
    print("尝试运行测试函数...")
    simulation, stats = run_complete_simulation_test()
    print("✓ 测试函数运行成功")
    
except Exception as e:
    print(f"✗ 错误: {e}")
    import traceback
    traceback.print_exc()

print("测试完成")
