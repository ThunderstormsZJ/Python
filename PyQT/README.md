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