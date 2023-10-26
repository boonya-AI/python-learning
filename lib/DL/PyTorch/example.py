# https://pytorch.org/get-started/locally/
# https://pytorch.org/tutorials/
# https://github.com/pytorch/pytorch
# 张量计算(如NumPy)具有强大的GPU加速
# 深度神经网络建立在基于磁带的自动光栅系统上
import torch

if __name__ == "__main__":
    x = torch.rand(5, 3)
    print(x)
