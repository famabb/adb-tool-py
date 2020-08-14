from PyQt5.QtWidgets import QLineEdit


# 可以拖拽接收路径
class MyQLineEdit(QLineEdit):
    """实现文件拖放功能"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        text = e.mimeData().text().lower()
        if text.endswith('.apk') or text.endswith('.apks'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text().replace('file:///', ''))
