import asyncio
import random

async def producer(queue, n):
    for i in range(n):
        item = f"产品_{i}"
        await queue.put(item)
        print(f"生产: {item}")
        await asyncio.sleep(random.random())
    await queue.put(None)  # 结束信号

async def consumer(queue, name):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"{name} 消费: {item}")
        await asyncio.sleep(random.random() * 1.5)
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=3)
    prod_task = asyncio.create_task(producer(queue, 5))
    cons_tasks = [asyncio.create_task(consumer(queue, f"C{i}")) for i in range(2)]

    await prod_task
    await queue.join()      # 等待所有项目被处理
    for t in cons_tasks:
        t.cancel()          # 消费者收到取消信号后退出

if __name__ == "__main__":
    asyncio.run(main())