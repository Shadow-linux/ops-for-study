import threading
import time
from functools import wraps

task_list = []

def time_limited(timer):
    '''
    一个规定函数执行时间的装饰器
    :param timer:
    :return:
    '''
    @wraps(func)
    def wrapper(func):
        def __wrapper():
            # 通过设置守护线程强制规定函数的运行时间
            t = threading.Thread(target=func)
            t.setDaemon(True)
            t.start()
            # print(dir(t))
            task_list.append((t, timer))
            # t.join(timeout=timer)

            # time.sleep(timer)
            # if t.is_alive():
            #     # 若在规定的运行时间未结束守护进程，则主动抛出异常
            #     # raise Exception('Function execution timeout')
            #     return

        return __wrapper

    return wrapper


# @time_limited(5)
def func():
    @time_limited(1)
    def _func():
        print('开始')
        time.sleep(3)
        print('结束')
    return _func()


def task():
    for tt in task_list:
        tt[0].join(tt[1])

tt = threading.Thread(target=task)
tt.start()

# func()
n = 0
while True:
    n += 1
    print(n)
    func()
    if n > 100:
        break

