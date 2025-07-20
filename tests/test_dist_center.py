#!/usr/bin/env python3
# 测试distribution_center导入

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

print("测试distribution_center模块导入...")

try:
    print("尝试导入 models.distribution_center...")
    from models.distribution_center import test_distribution_center
    print("✓ 导入成功")
    
    print("尝试运行测试函数...")
    test_distribution_center()
    print("✓ 测试函数运行成功")
    
except Exception as e:
    print(f"✗ 错误: {e}")
    import traceback
    traceback.print_exc()

print("测试完成")
