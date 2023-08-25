# 此处使用import关键字引入模块
# 自定义模块如：DefinedModel.py
import sys
import DefinedModel as model

print('The command line arguments are:')
for i in sys.argv:
    print(i)
    model.say_hi();

print('\n\nThe PYTHONPATH is', sys.path, '\n')
