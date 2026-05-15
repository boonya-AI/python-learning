import asyncio

async def worker(lock, name):
    async with lock:
        print(f"{name} 获得了锁")
        await asyncio.sleep(1)
    print(f"{name} 释放了锁")

async def waiter(event, name):
    print(f"{name} 等待事件触发...")
    await event.wait()
    print(f"{name} 事件已触发，继续执行")

async def main():
    # 异步锁示例
    lock = asyncio.Lock()
    await asyncio.gather(worker(lock, "A"), worker(lock, "B"))

    # 事件示例
    event = asyncio.Event()
    waiters = [asyncio.create_task(waiter(event, f"W{i}")) for i in range(3)]
    print("主线程：休眠2秒后设置事件...")
    await asyncio.sleep(2)
    event.set()
    await asyncio.gather(*waiters)

if __name__ == "__main__":
    asyncio.run(main())