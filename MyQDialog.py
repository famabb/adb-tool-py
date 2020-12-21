#
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog


class MyQDialog(QDialog):
    signal_close = pyqtSignal(str)

    def reject(self) -> None:
        self.signal_close.emit("close")
        super().reject()
