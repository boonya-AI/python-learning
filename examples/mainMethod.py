# A model's  __name__
# 每个模块都有一个名称，模块中的语句可以找到其模块的名称。
# 这对于确定模块是独立运行还是导入的特定目的非常方便。
# 如前所述，当第一次导入模块时，它包含的代码将被执行。
# 我们可以使用它来让模块以不同的方式运行，这取决于它是被自己使用还是从另一个模块导入。
# 这可以使用模块的__name__属性来实现。
if __name__ == '__main__':
    print('This program is being run by itself')
else:
    print('I am being imported from another module')