# https://pytorch.org/get-started/locally/
# https://pytorch.org/tutorials/
# https://github.com/pytorch/pytorch
# 张量计算(如NumPy)具有强大的GPU加速
# 深度神经网络建立在基于磁带的自动光栅系统上
# https://zhuanlan.zhihu.com/p/66543791
import torch


def add(tensor3):
    tensor4 = torch.rand(5, 3)
    print('tensor3 + tensor4= ', tensor3 + tensor4)
    print('tensor3 + tensor4= ', torch.add(tensor3, tensor4))
    # 新声明一个 tensor 变量保存加法操作的结果
    result = torch.empty(5, 3)
    torch.add(tensor3, tensor4, out=result)
    print('add result= ', result)
    # 直接修改变量
    tensor3.add_(tensor4)
    print('tensor3= ', tensor3)


if __name__ == "__main__":
    x = torch.rand(5, 3)
    print(x)
