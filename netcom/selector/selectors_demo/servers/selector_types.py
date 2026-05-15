"""
演示各种 Selector 实现类的可用性检测

展示当前平台可用的 Selector 类:
- DefaultSelector (总是可用)
- SelectSelector (总是可用)
- PollSelector (仅 Unix/Linux)
- EpollSelector (仅 Linux)
- DevpollSelector (仅 Solaris/BSD)
- KqueueSelector (仅 macOS/BSD)

运行方式:
    python -m selectors_demo.servers.selector_types
"""

import selectors
import sys


def check_selector_availability():
    """检测当前平台可用的 Selector 类"""
    print("=" * 50)
    print("Selector 实现类可用性检测")
    print("=" * 50)
    print(f"\n当前平台: {sys.platform}")
    print(f"Python 版本: {sys.version}")

    selector_classes = [
        ("DefaultSelector", "selectors.DefaultSelector",
         "当前平台最高效实现的别名（推荐使用）"),
        ("SelectSelector", "selectors.SelectSelector",
         "基于 select.select()，跨平台"),
        ("PollSelector", "selectors.PollSelector",
         "基于 select.poll()，Unix/Linux"),
        ("EpollSelector", "selectors.EpollSelector",
         "基于 select.epoll()，仅 Linux"),
        ("DevpollSelector", "selectors.DevpollSelector",
         "基于 select.devpoll()，仅 Solaris/BSD"),
        ("KqueueSelector", "selectors.KqueueSelector",
         "基于 select.kqueue()，仅 macOS/BSD"),
    ]

    print("\n可用性检测结果:")
    print("-" * 60)

    for name, full_name, description in selector_classes:
        cls = getattr(selectors, name, None)
        if cls is not None:
            try:
                # 尝试实例化来确认真正可用
                instance = cls()
                instance.close()
                status = "[OK] 可用"
            except (OSError, NotImplementedError):
                status = "[NO] 不可用（当前系统不支持）"
        else:
            status = "[NO] 不可用（类未定义）"

        print(f"  {status}  {name}")
        print(f"         {description}")

    # 显示 DefaultSelector 的实际类型
    print("\n" + "-" * 60)
    default_sel = selectors.DefaultSelector()
    print(f"\nDefaultSelector 的实际实现类:")
    print(f"  类型: {type(default_sel).__name__}")
    print(f"  MRO: {' -> '.join(c.__name__ for c in type(default_sel).__mro__)}")
    default_sel.close()


def demo_selector_fileno():
    """演示部分 Selector 的 fileno() 方法"""
    print("\n" + "=" * 50)
    print("Selector fileno() 方法演示")
    print("=" * 50)
    print("\n某些 Selector 实现提供 fileno() 方法，返回底层系统调用使用的文件描述符:")

    selectors_to_check = []

    # EpollSelector
    if hasattr(selectors, 'EpollSelector'):
        selectors_to_check.append(('EpollSelector', selectors.EpollSelector))

    # KqueueSelector
    if hasattr(selectors, 'KqueueSelector'):
        selectors_to_check.append(('KqueueSelector', selectors.KqueueSelector))

    # DevpollSelector
    if hasattr(selectors, 'DevpollSelector'):
        selectors_to_check.append(('DevpollSelector', selectors.DevpollSelector))

    if not selectors_to_check:
        print("\n  当前平台（Windows）没有提供 fileno() 的 Selector 实现")
        print("  fileno() 仅在 EpollSelector、KqueueSelector、DevpollSelector 上可用")
        return

    for name, cls in selectors_to_check:
        try:
            instance = cls()
            if hasattr(instance, 'fileno'):
                print(f"\n  {name}.fileno() = {instance.fileno()}")
            instance.close()
        except (OSError, NotImplementedError) as e:
            print(f"\n  {name}: 不可用 ({e})")


if __name__ == "__main__":
    check_selector_availability()
    demo_selector_fileno()
