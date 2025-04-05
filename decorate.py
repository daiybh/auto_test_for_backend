import sys
import inspect
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)  # 保留原函数元信息（如函数名、文档字符串）
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # 执行原函数
        end_time = time.time()
        print(f"[{func.__name__}] 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper



def decorate_all_functions(module):
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            setattr(module, name, timing_decorator(obj))
    return module

# 在模块末尾调用（装饰当前模块所有函数）
decorate_all_functions(sys.modules[__name__])

# 示例函数（会被自动装饰）
def auto_timed_function():
    time.sleep(0.3)

auto_timed_function()  # 输出计时信息