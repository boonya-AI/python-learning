import tensorflow as tf
import numpy as np

# 创建训练数据
x_train = np.array([[1], [2], [3], [4], [5]])
y_train = np.array([2, 4, 6, 8, 10])

# 定义模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])

# 编译模型
model.compile(optimizer=tf.keras.optimizers.Adam(0.01), loss='mean_squared_error')

# 训练模型
history = model.fit(x_train, y_train, epochs=500)

# 预测新数据
x_test = np.array([[6]])
y_pred = model.predict(x_test)

print("预测值为：", y_pred[0][0])