import asyncio

async def slow_operation(n):
    await asyncio.sleep(1)
    return n * 2

async def main():
    # 创建任务，并绑定回调
    task = asyncio.create_task(slow_operation(5))
    task.add_done_callback(lambda t: print(f"回调结果: {t.result()}"))
    result = await task
    print(f"直接获取结果: {result}")

    # 使用 asyncio.gather 并发收集结果
    results = await asyncio.gather(
        slow_operation(1),
        slow_operation(2),
        slow_operation(3)
    )
    print(f"gather结果: {results}")

    # as_completed 顺序处理完成的任务
    print("as_completed:")
    for coro in asyncio.as_completed([slow_operation(i) for i in range(3, 0, -1)]):
        result = await coro
        print(f"  完成了一个结果: {result}")

if __name__ == "__main__":
    asyncio.run(main())