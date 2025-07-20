import sys
import os

print("开始诊断...")
print("Current directory:", os.getcwd())
print("Python path:", sys.path[:3])

# 尝试逐步导入
try:
    print("尝试导入 test_coordinate_generator...")
    from test_coordinate_generator import run_all_tests
    print("成功！")
except Exception as e:
    print(f"失败: {e}")
    print("Trying alternative import...")
    try:
        import test_coordinate_generator
        print("Alternative import successful!")
        if hasattr(test_coordinate_generator, 'run_all_tests'):
            print("run_all_tests function found!")
        else:
            print("run_all_tests function not found!")
    except Exception as e2:
        print(f"Alternative import also failed: {e2}")

print("诊断完成")
