from PyQt5.QtWidgets import QWidget, QTextEdit


class YuToolsDailyPlan(QWidget):
    def __init__(self):
        super().__init__()
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(10, 10, 341, 71)
