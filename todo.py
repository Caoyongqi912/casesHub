import asyncio
import time


async def async_function(n):
    """
    async修饰的异步函数，在该函数中可以添加await进行暂停并切换到其他异步函数中
    :return:
    """
    now = time.time()
    # 当执行await future这行代码时（future对象就是被await修饰的函数），
    # 首先future检查它自身是否已经完成，如果没有完成，挂起自身，告知当前的Task（任务）等待future完成。
    await asyncio.sleep(n)
    print('花费时间：{}秒'.format(time.time() - now))
    return "done"


def callBack(future):
    print(future.result())


def demo():
    loop = asyncio.get_event_loop()  # 通过get_event_loop方法获取事件循环对象

    events = [loop.create_task(async_function(num)) for num in range(1, 4)]  # 创建协程事件列表

    task = asyncio.wait(events)

    print(task)
    # task.add_done_callback(callBack)
    loop.run_until_complete(task)  # 直接运行event 直到其运行结束

    loop.close()


if __name__ == '__main__':
    print(demo())
