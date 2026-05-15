import asyncio

async def eternity():
    await asyncio.sleep(3600)
    print("这行永远不会打印（如果超时）")

async def main():
    # wait_for 超时
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print("超时了！")

    # wait 设置返回条件
    async def one():
        await asyncio.sleep(1)
        return 1
    async def two():
        await asyncio.sleep(2)
        return 2

    tasks = [one(), two()]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"最先完成的任务个数: {len(done)}")
    # 清理未完成的任务
    for p in pending:
        p.cancel()

if __name__ == "__main__":
    asyncio.run(main())