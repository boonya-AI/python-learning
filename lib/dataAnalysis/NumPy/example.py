# 一个用于数值计算的库
import numpy as np

# 创建一个数组
arr = np.array([1, 2, 3, 4, 5])

# 打印数组形状
print("数组形状: ", arr.shape)

# 改变数组形状
arr = arr.reshape((5, 1))
print("数组形状: ", arr.shape)

# 计算数组元素平均值
mean = np.mean(arr)
print("数组元素平均值: ", mean)

# 计算数组元素方差
var = np.var(arr)
print("数组元素方差: ", var)

# 计算数组元素标准差
std = np.std(arr)
print("数组元素标准差: ", std)
