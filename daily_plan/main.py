from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QComboBox, QSpinBox, QDateEdit, \
    QCheckBox, QPushButton

from daily_plan.db_helper import PlanFrequency


class YuToolsDailyPlan(QWidget):
    def __init__(self):
        super().__init__()

        self.txt_content = QPlainTextEdit(self)
        self.txt_content.setGeometry(10, 10, 350, 52)

        self.combo_frequency = QComboBox(self)
        self.combo_frequency.addItem(PlanFrequency.NoRepeat.name)
        self.combo_frequency.addItem(PlanFrequency.Day.name)
        self.combo_frequency.addItem(PlanFrequency.Week.name)
        self.combo_frequency.addItem(PlanFrequency.Month.name)
        self.combo_frequency.addItem(PlanFrequency.Quarter.name)
        self.combo_frequency.addItem(PlanFrequency.Year.name)
        self.combo_frequency.setGeometry(10, 100, 100, 26)

        self.spin_repeat = QSpinBox(self)
        self.spin_repeat.setGeometry(120, 100, 100, 26)

        self.cb_can_op_all = QCheckBox(self)
        self.cb_can_op_all.setText('Enable Batch Operate')
        self.cb_can_op_all.setGeometry(230, 100, 150, 26)

        self.de_begin_time = QDateEdit(self)
        self.de_begin_time.setDate(QDate.currentDate())
        self.de_begin_time.setGeometry(10, 140, 100, 26)

        self.de_deadline = QDateEdit(self)
        self.de_deadline.setDate(QDate.currentDate())
        self.de_deadline.setGeometry(120, 140, 100, 26)

        self.combo_importance = QComboBox(self)
        self.combo_importance.addItem('Important')
        self.combo_importance.addItem('Unimportant')
        self.combo_importance.setGeometry(10, 180, 100, 26)

        self.combo_urgency = QComboBox(self)
        self.combo_urgency.addItem('Urgent')
        self.combo_urgency.addItem('Non-Urgent')
        self.combo_urgency.setGeometry(120, 180, 100, 26)

        self.btn_save = QPushButton(self)
        self.btn_save.setText('Save')
        self.btn_save.setGeometry(10, 220, 200, 26)
        self.btn_save.clicked.connect(self.save_plan)

    def save_plan(self):
        content = self.txt_content.toPlainText().replace('\n', '<br />')
