### PyQT

https://pythonspot.com/pyqt5/

PyQt是Qt框架的Python语言实现，由Riverbank Computing开发，是最强大的GUI库之一。
PyQt提供了一个设计良好的窗口控件集合，每一个PyQt控件都对应一个Qt控件，因此PyQt的API接口与Qt的API接口很接近，但PyQt不再使用QMake系统和Q_OBJECT宏。

优点：功能非常强大，可以用PyQt5开很漂亮的界面；另外它支持可视化界面设计，对新手非常友好。什么意思呢，就是你可以通过拖动一些模块就可以完成一些代码才能完成的工作，就跟C++的QT是一样的。

缺点：学习起来有一定难度。

### Install

```
pip install python-qt5

pip install PyQt5 -i https://pypi.douban.com/simple

```

### 安装 PyQt5-tools

PyQt5 不再提供常用Qt工具，比如图形界面开发工具Qt Designer、国际化翻译工具Liguist 如果开发中使用到这些，必须自行安装Qt工具。

这里我们还是采用脚本安装的方式。

`pip install PyQt5-tools`
或者使用镜像下载：

`pip install PyQt5-tools -i https://pypi.douban.com/simple`

### 添加环境变量

找到安装的位置： C:\Program Files\Python310\Lib\site-packages\pyqt5_tools
添加到Path 