# 用于数据分析和清洗的库
# 有大量的Python软件包设计用于处理复杂的数据集。但是可以说，Pandas是最重要的。
# Pandas可以帮助您处理和分析大量数据，而无需学习专门的数据处理语言（例如R）。
import pandas as pd

# 创建数据字典
data = {'name': ['张三', '李四', '王五', '赵六', '孙七'],
        'age': [25, 30, 35, 40, 45],
        'city': ['北京', '上海', '广州', '深圳', '杭州']}

# 创建DataFrame
df = pd.DataFrame(data)

# 打印DataFrame
print("DataFrame: \n", df)

# 按照年龄排序
df = df.sort_values(by='age')
print("\n按照年龄排序: \n", df)

# 计算每个城市人数
city_counts = df['city'].value_counts()
print("\n城市人数统计: \n", city_counts)
