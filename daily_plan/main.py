from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QComboBox, QSpinBox, QDateEdit, \
    QCheckBox, QPushButton, QLabel, QFrame, QTableView, QCalendarWidget, QLineEdit, QMenuBar, QStatusBar

from daily_plan.db_helper import PlanFrequency


class YuToolsDailyPlan(QWidget):
    def __init__(self):
        super().__init__()

        self.txt_content = QPlainTextEdit(self)
        self.txt_content.setGeometry(10, 10, 341, 51)

        self.lbl_begin = QLabel(self)
        self.lbl_begin.setText("Begin ")
        self.lbl_begin.setGeometry(10, 70, 41, 22)

        self.le_begin = QLineEdit(self)
        self.le_begin.setGeometry(50, 70, 91, 22)

        self.lbl_deadline = QLabel(self)
        self.lbl_deadline.setText("Deadline")
        self.lbl_deadline.setGeometry(170, 70, 51, 22)

        self.le_deadline = QLineEdit(self)
        self.le_deadline.setGeometry(230, 70, 91, 22)

        self.calendar_select = QCalendarWidget(self)
        self.calendar_select.setGeometry(10, 100, 256, 191)

        self.combo_frequency = QComboBox(self)
        self.combo_frequency.addItem(PlanFrequency.NoRepeat.name)
        self.combo_frequency.addItem(PlanFrequency.Day.name)
        self.combo_frequency.addItem(PlanFrequency.Week.name)
        self.combo_frequency.addItem(PlanFrequency.Month.name)
        self.combo_frequency.addItem(PlanFrequency.Quarter.name)
        self.combo_frequency.addItem(PlanFrequency.Year.name)
        self.combo_frequency.setGeometry(280, 100, 69, 26)

        self.sb_repeat = QSpinBox(self)
        self.sb_repeat.setGeometry(280, 130, 71, 26)

        self.cb_batch_op = QCheckBox(self)
        self.cb_batch_op.setText("Batch Op")
        self.cb_batch_op.setGeometry(280, 160, 70, 26)

        self.combo_importance = QComboBox(self)
        self.combo_importance.addItem('Important')
        self.combo_importance.addItem('Unimportant')
        self.combo_importance.setGeometry(280, 190, 69, 26)

        self.combo_urgency = QComboBox(self)
        self.combo_urgency.addItem('Urgent')
        self.combo_urgency.addItem('Non-Urgent')
        self.combo_urgency.setGeometry(280, 220, 69, 26)

        self.btn_save = QPushButton(self)
        self.btn_save.setGeometry(280, 260, 71, 26)
        self.btn_save.setText("Save")
        self.btn_save.clicked.connect(self.save_plan)

        self.tb_plan = QTableView(self)
        self.tb_plan.setGeometry(370, 10, 421, 281)

        self.line_importance = QFrame(self)
        self.line_importance.setGeometry(390, 290, 20, 441)
        self.line_importance.setFrameShape(QFrame.VLine)
        self.line_importance.setFrameShadow(QFrame.Sunken)

        self.line_urgency = QFrame(self)
        self.line_urgency.setGeometry(0, 500, 791, 16)
        self.line_urgency.setFrameShape(QFrame.HLine)
        self.line_urgency.setFrameShadow(QFrame.Sunken)

        self.tb_ac_first = QTableView(self)
        self.tb_ac_first.setGeometry(410, 300, 381, 201)

        self.tb_ac_third = QTableView(self)
        self.tb_ac_third.setGeometry(10, 520, 381, 201)

        self.tb_ac_second = QTableView(self)
        self.tb_ac_second.setGeometry(10, 300, 381, 201)

        self.tb_ac_fourth = QTableView(self)
        self.tb_ac_fourth.setGeometry(410, 520, 381, 201)

    def save_plan(self):
        content = self.txt_content.toPlainText().replace('\n', '<br />')
