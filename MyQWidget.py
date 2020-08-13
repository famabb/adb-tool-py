from PyQt5.QtWidgets import QLineEdit


# 可以拖拽接收路径
class MyQLineEdit(QLineEdit):
    match_end = ''
    """实现文件拖放功能"""

    def __init__(self, parent=None, end=''):
        super().__init__(parent)
        self.match_end = end
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if self.match_end == '' or e.mimeData().text().lower().endswith(self.match_end):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text().replace('file:///', ''))
