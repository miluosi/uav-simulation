#!/usr/bin/env python3
# minimal_test.py - 最小化测试来诊断问题

import sys
import os

print("=== 最小化测试开始 ===")

try:
    print("步骤1: 测试基本导入...")
    from test_coordinate_generator import run_all_tests
    print("✓ 成功导入 test_coordinate_generator")
    
    print("\n步骤2: 运行测试...")
    result = run_all_tests()
    print(f"✓ 测试完成，结果: {result}")
    
    print("\n✓ 所有步骤完成")
    
except Exception as e:
    print(f"✗ 错误: {e}")
    import traceback
    traceback.print_exc()

print("=== 最小化测试结束 ===")
