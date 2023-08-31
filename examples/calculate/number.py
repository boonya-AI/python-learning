# 将x转换为一个整数
def parse_int(x):
    int(x)


# #将x转换为一个长整数
# def parse_long(x):
#     long(x)

# 将x转换到一个浮点数
def parse_float(x):
    float(x)


# # 创建一个复数
# def parse_complex(x,keyword):
# complex(x,keyword)


# 将对象 x 转换为字符串
def parse_str(x):
    str(x)


# 将对象 x 转换为表达式字符串
def parse_repr(x):
    repr(x)


# 用来计算在字符串中的有效Python表达式,并返回一个对象
def parse_eval(x):
    eval(str)


# 将序列 s 转换为一个元组
def parse_tuple(s):
    tuple(s)


# 将序列 s 转换为一个列表
def parse_list(s):
    return list(s)


# 将一个整数转换为一个字符
def parse_chr(x):
    chr(x)


# # 将一个整数转换为Unicode字符
# def parse_unicode(x):
#     unicodedata(x)


# 将一个字符转换为它的整数值
def parse_ord(x):
    ord(x)


# 将一个整数转换为一个十六进制字符串
def parse_hex(x):
    hex(x)


# 将一个整数转换为一个八进制字符串
def parse_oct(x):
    oct(x)
