from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class RootQWidget(QWidget):
    signal_close = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    # 添加一个退出的提示事件
    def closeEvent(self, event):
        self.signal_close.emit('closeEvent')
        event.accept()
