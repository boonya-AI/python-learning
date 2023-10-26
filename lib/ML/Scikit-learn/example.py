import numpy as np
from sklearn.linear_model import LinearRegression

# 创建训练数据
x_train = np.array([[1], [2], [3], [4], [5]])
y_train = np.array([2, 4, 6, 8, 10])

# 创建线性回归模型
model = LinearRegression()

# 训练模型
model.fit(x_train, y_train)

# 预测新数据
x_test = np.array([[6]])
y_pred = model.predict(x_test)

print("预测值为：", y_pred[0])