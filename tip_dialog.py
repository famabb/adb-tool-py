from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton


class TipDialog:

    def showTip(self, tip):
        vbox = QVBoxLayout()  # 纵向布局
        panel = QLabel()
        panel.setText(tip)
        panel.setAlignment(Qt.AlignCenter)
        self.dialog = QDialog()
        self.dialog.setWindowTitle("提示")
        self.dialog.resize(300, 200)
        self.dialog.setMaximumWidth(300)
        vbox.addWidget(panel)
        okBtn = QPushButton("确定")
        okBtn.clicked.connect(self.ok)
        vbox.addWidget(okBtn)

        self.dialog.setLayout(vbox)
        self.dialog.setWindowModality(Qt.ApplicationModal)  # 该模式下，只有该dialog关闭，才可以关闭父界面
        self.dialog.exec_()

    def ok(self):
        self.dialog.close()
