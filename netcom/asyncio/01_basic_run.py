import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    # 方式1: 依次执行
    print(f"开始: {time.strftime('%X')}")
    await say_after(1, "你好")
    await say_after(2, "世界")
    print(f"依次结束: {time.strftime('%X')}")

    # 方式2: 并发执行（创建任务）
    task1 = asyncio.create_task(say_after(1, "并发你好"))
    task2 = asyncio.create_task(say_after(2, "并发世界"))
    print(f"并发开始: {time.strftime('%X')}")
    await task1
    await task2
    print(f"并发结束: {time.strftime('%X')}")

if __name__ == "__main__":
    asyncio.run(main())