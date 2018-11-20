# PyQt

### - 子类setStyleSheet失效问题
在子类中重写paintEvent方法
```python
def paintEvent(self, e):
    opt = QStyleOption()
    opt.initFrom(self)
    p = QPainter(self)
    self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
```
### - 连接数据库问题：Driver not loaded

解决方案:将libmysql.dll 复制到site-packages/PyQt5/Qt/bin目录下

### - 打包成exe文件
```ssh
    pip install pyinstaller 
    or
    easy_install pyinstaller
```