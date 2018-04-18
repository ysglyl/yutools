import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QComboBox, QSpinBox, \
    QCheckBox, QPushButton, QFrame, QTableView, QCalendarWidget, QDateEdit, QRadioButton, \
    QMessageBox, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from daily_plan.db_helper import PlanFrequency, Plan, Action, PlanDao, ActionDao


class YuToolsDailyPlan(QWidget):
    def __init__(self):
        super().__init__()
        self.status_label = {0: 'Wait', 1: 'Going', 2: 'Done', 3: 'Expire'}

        self.txt_content = QPlainTextEdit(self)
        self.txt_content.setGeometry(10, 10, 350, 50)

        self.rb_begin = QRadioButton(self)
        self.rb_begin.setText('Begin')
        self.rb_begin.setChecked(True)
        self.rb_begin.setGeometry(10, 70, 50, 22)

        self.de_begin = QDateEdit(self)
        self.de_begin.setDate(QDate.currentDate())
        self.de_begin.setGeometry(70, 70, 90, 22)

        self.rb_begin.clicked.connect(lambda: self.rb_select_date(self.de_begin))

        self.rb_deadline = QRadioButton(self)
        self.rb_deadline.setText("Deadline")
        self.rb_deadline.setGeometry(180, 70, 60, 22)

        self.de_deadline = QDateEdit(self)
        self.de_deadline.setDate(QDate.currentDate().addDays(7))
        self.de_deadline.setGeometry(250, 70, 90, 22)

        self.rb_deadline.clicked.connect(lambda: self.rb_select_date(self.de_deadline))

        self.calendar_select = QCalendarWidget(self)
        self.calendar_select.setGeometry(10, 100, 256, 190)
        self.calendar_select.clicked.connect(self.select_date)

        self.combo_frequency = QComboBox(self)
        self.combo_frequency.addItem(PlanFrequency.NoRepeat.name)
        self.combo_frequency.addItem(PlanFrequency.Day.name)
        self.combo_frequency.addItem(PlanFrequency.Week.name)
        self.combo_frequency.addItem(PlanFrequency.Month.name)
        self.combo_frequency.addItem(PlanFrequency.Quarter.name)
        self.combo_frequency.addItem(PlanFrequency.Year.name)
        self.combo_frequency.setGeometry(280, 100, 80, 26)

        self.sb_repeat = QSpinBox(self)
        self.sb_repeat.setMinimum(1)
        self.sb_repeat.setGeometry(280, 130, 80, 26)

        self.cb_include = QCheckBox(self)
        self.cb_include.setText("Include Begin")
        self.cb_include.setChecked(True)
        self.cb_include.setGeometry(280, 160, 80, 26)

        self.combo_importance = QComboBox(self)
        self.combo_importance.addItem('Important')
        self.combo_importance.addItem('Unimportant')
        self.combo_importance.setGeometry(280, 190, 80, 26)

        self.combo_urgency = QComboBox(self)
        self.combo_urgency.addItem('Urgent')
        self.combo_urgency.addItem('Non-Urgent')
        self.combo_urgency.setGeometry(280, 220, 80, 26)

        self.btn_save = QPushButton(self)
        self.btn_save.setGeometry(280, 260, 80, 26)
        self.btn_save.setText("Save")
        self.btn_save.clicked.connect(self.save_plan)

        self.tb_plan = QTableView(self)
        self.tb_plan.horizontalHeader().setStretchLastSection(True)
        self.tb_plan.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_plan.setGeometry(370, 10, 421, 281)

        self.line_importance = QFrame(self)
        self.line_importance.setGeometry(390, 295, 20, 435)
        self.line_importance.setFrameShape(QFrame.VLine)
        self.line_importance.setFrameShadow(QFrame.Sunken)

        self.line_urgency = QFrame(self)
        self.line_urgency.setGeometry(5, 480, 791, 16)
        self.line_urgency.setFrameShape(QFrame.HLine)
        self.line_urgency.setFrameShadow(QFrame.Sunken)

        self.tb_ac_first = QTableView(self)
        self.tb_ac_first.horizontalHeader().setStretchLastSection(True)
        self.tb_ac_first.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_ac_first.setGeometry(410, 300, 381, 180)

        self.tb_ac_second = QTableView(self)
        self.tb_ac_second.horizontalHeader().setStretchLastSection(True)
        self.tb_ac_second.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_ac_second.setGeometry(10, 300, 381, 180)

        self.tb_ac_third = QTableView(self)
        self.tb_ac_third.horizontalHeader().setStretchLastSection(True)
        self.tb_ac_third.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_ac_third.setGeometry(10, 495, 381, 180)

        self.tb_ac_fourth = QTableView(self)
        self.tb_ac_fourth.horizontalHeader().setStretchLastSection(True)
        self.tb_ac_fourth.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_ac_fourth.setGeometry(410, 495, 381, 180)

        self.refresh_tb_plan()
        for index in range(1, 5):
            self.refresh_tb_action(index)

    def rb_select_date(self, de_target):
        self.calendar_select.setSelectedDate(de_target.date())

    def select_date(self):
        date = self.calendar_select.selectedDate()
        if self.rb_begin.isChecked():
            self.de_begin.setDate(date)
        elif self.rb_deadline.isChecked():
            self.de_deadline.setDate(date)

    def save_plan(self):
        code, data = self.valid_check()
        if code == -1:
            QMessageBox.critical(self, 'Error', data)
            return

        code2, actions = self.generate_actions(data)
        if code2 == -1:
            QMessageBox.critical(self, 'Error', actions)
            return
        PlanDao.add_plan(data)
        ActionDao.add_actions(actions, data.id)

        self.txt_content.clear()

        self.refresh_tb_plan()
        self.refresh_tb_action(tb_index=code)

    def valid_check(self):
        content = self.txt_content.toPlainText().replace('\n', '.')
        if content.strip(' ').strip('.').strip(' ') == '':
            return -1, 'Content must be a normal string!'
        begin = self.de_begin.date()
        deadline = self.de_deadline.date()
        now = QDate.currentDate()
        diff_begin = now.daysTo(begin)
        diff_deadline = now.daysTo(deadline)
        if diff_begin < 0 or diff_deadline < 0 or diff_deadline < diff_begin:
            return -1, 'Deadline date must be farther than begin date and both of them must be farther than Now'
        begin_date = datetime.date(begin.year(), begin.month(), begin.day())
        deadline = datetime.date(deadline.year(), deadline.month(), deadline.day())
        frequency = self.combo_frequency.currentText()
        repeat = self.sb_repeat.value()
        importance = self.combo_importance.currentText()
        degree_importance = False if importance.lower().startswith('un') else True
        urgent = self.combo_urgency.currentText()
        degree_urgent = False if urgent.lower().startswith('non') else True
        plan = Plan(content=content, begin_date=begin_date, deadline=deadline, frequency=PlanFrequency[frequency],
                    repeat=repeat, degree_importance=degree_importance, degree_urgency=degree_urgent)
        if degree_importance and degree_urgent:
            code = 1
        elif degree_importance and not degree_urgent:
            code = 2
        elif not degree_importance and not degree_urgent:
            code = 3
        elif not degree_importance and degree_urgent:
            code = 4
        return code, plan

    def generate_actions(self, plan):
        action_list = []
        begin = QDate(plan.begin_date)
        deadline = QDate(plan.deadline)

        include = self.cb_include.isChecked()
        if plan.frequency == PlanFrequency.NoRepeat:
            days = begin.daysTo(deadline)
            if not include:
                if days == 0:
                    return -1, 'There is not time to complete the plan'
            for i in range(plan.repeat):
                action = Action(content=plan.content, begin_date=plan.begin_date, deadline=plan.deadline,
                                degree_importance=plan.degree_importance, degree_urgency=plan.degree_urgency, status=1)
                action_list.append(action)
        elif plan.frequency == PlanFrequency.Day:
            days = begin.daysTo(deadline)
            if not include:
                if days == 0:
                    return -1, 'There is not time to complete the plan'
            for day in range(days + 1):
                if not include and day == 0:
                    continue
                begin_date = begin.addDays(day)
                begin_date = datetime.date(begin_date.year(), begin_date.month(), begin_date.day())
                for i in range(plan.repeat):
                    action = Action(content=plan.content, begin_date=begin_date, deadline=begin_date,
                                    degree_importance=plan.degree_importance, degree_urgency=plan.degree_urgency,
                                    status=1)
                    action_list.append(action)
        elif plan.frequency == PlanFrequency.Week:
            begin_week, begin_year = begin.weekNumber()
            begin_day_of_week = begin.dayOfWeek()
            deadline_week, deadline_year = deadline.weekNumber()
            weeks = deadline_week + (deadline_year - begin_year) * 52 - begin_week
            if not include:
                if weeks == 0:
                    return -1, 'There is not time to complete the plan'
            current_week_deadline = begin.addDays(7 - begin_day_of_week)
            for week in range(weeks + 1):
                if not include and week == 0:
                    continue
                current_week_deadline = current_week_deadline.addDays(7 * week)
                current_week_begin = current_week_deadline.addDays(-6)
                if week == 0:
                    begin_date = plan.begin_date
                    deadline = datetime.date(current_week_deadline.year(), current_week_deadline.month(),
                                             current_week_deadline.day())
                elif week == weeks:
                    begin_date = datetime.date(current_week_begin.year(), current_week_begin.month(),
                                               current_week_begin.day())
                    deadline = plan.deadline
                else:
                    begin_date = datetime.date(current_week_begin.year(), current_week_begin.month(),
                                               current_week_begin.day())
                    deadline = datetime.date(current_week_deadline.year(), current_week_deadline.month(),
                                             current_week_deadline.day())
                for i in range(plan.repeat):
                    action = Action(content=plan.content, begin_date=begin_date, deadline=deadline,
                                    degree_importance=plan.degree_importance, degree_urgency=plan.degree_urgency,
                                    status=1)
                    action_list.append(action)
        elif plan.frequency == PlanFrequency.Month:
            begin_year = begin.year()
            deadline_year = deadline.year()
            years = deadline_year - begin_year
            begin_month = begin.month()
            deadline_month = deadline.month()
            months = deadline_month + 12 * years - begin_month
            if not include:
                if months == 0:
                    return -1, 'There is not time to complete the plan'
            current_year = begin_year
            for month in range(months + 1):
                if not include and month == 0:
                    continue
                current_month = begin_month + month
                if current_month > 12:
                    current_month -= 12
                    current_year += 1
                if month == 0:
                    begin_date = plan.begin_date
                    if month == months:
                        deadline = plan.deadline
                    else:
                        deadline = datetime.date(current_year, current_month, begin.daysInMonth())
                elif month == months:
                    begin_date = datetime.date(current_year, current_month, 1)
                    deadline = plan.deadline
                else:
                    begin_date = datetime.date(current_year, current_month, 1)
                    deadline = datetime.date(current_year, current_month, 1)
                    deadline = datetime.date(current_year, current_month,
                                             QDate(deadline.year(), deadline.month(), deadline.day()).daysInMonth())
                for i in range(plan.repeat):
                    action = Action(content=plan.content, begin_date=begin_date, deadline=deadline,
                                    degree_importance=plan.degree_importance, degree_urgency=plan.degree_urgency,
                                    status=1)
                    action_list.append(action)
        elif plan.frequency == PlanFrequency.Quarter:
            begin_year = begin.year()
            deadline_year = deadline.year()
            years = deadline_year - begin_year
            begin_month = begin.month()
            deadline_month = deadline.month()
            begin_quarter = (begin_month + 2) / 3
            deadline_quarter = (deadline_month + 2) / 3
            quarters = deadline_quarter + years * 4 - begin_quarter
            if not include:
                if quarters == 0:
                    return -1, 'There is not time to complete the plan'
            current_year = begin_year
            for quarter in range(quarters + 1):
                if not include and quarter == 0:
                    continue
                current_quarter = begin_quarter + quarter
                if current_quarter > 4:
                    current_quarter -= 4
                    current_year += 1
                begin_month = (current_quarter - 1) * 3 + 1
                deadline_month = begin_month + 2
                if quarter == 0:
                    begin_date = plan.begin_date
                    deadline = datetime.date(current_year, deadline_month, (30 if deadline_month == 4 else 31))
                elif quarter == quarters:
                    begin_date = datetime.date(current_year, begin_month, 1)
                    deadline = plan.deadline
                else:
                    begin_date = datetime.date(current_year, begin_month, 1)
                    deadline = datetime.date(current_year, deadline_month, (30 if deadline_month == 4 else 31))
                for i in range(plan.repeat):
                    action = Action(content=plan.content, begin_date=begin_date, deadline=deadline,
                                    degree_importance=plan.degree_importance, degree_urgency=plan.degree_urgency,
                                    status=1)
                    action_list.append(action)
        elif plan.frequency == PlanFrequency.Year:
            begin_year = begin.year()
            deadline_year = deadline.year()
            years = deadline_year - begin_year
            if not include:
                if years == 0:
                    return -1, 'There is not time to complete the plan'
            for year in range(years + 1):
                if not include and year == 0:
                    continue
                current_year = begin_year + year
                if year == 0:
                    begin_date = plan.begin_date
                    deadline = datetime.date(current_year, 12, 31)
                elif year == years:
                    begin_date = datetime.date(current_year, 1, 1)
                    deadline = plan.deadline
                else:
                    begin_date = datetime.date(current_year, 1, 1)
                    deadline = datetime.date(current_year, 12, 31)
                for i in range(plan.repeat):
                    action = Action(content=plan.content, begin_date=begin_date, deadline=deadline,
                                    degree_importance=plan.degree_importance, degree_urgency=plan.degree_urgency,
                                    status=1)
                    action_list.append(action)
        return 0, action_list

    def refresh_tb_plan(self):
        plans = PlanDao.query_plans()
        model = QStandardItemModel(len(plans), 3)
        model.setHorizontalHeaderLabels(['Content', 'Frequency', 'Flag'])
        row_index = 0
        for plan in plans:
            model.setItem(row_index, 0, QStandardItem(plan.content))
            # model.setItem(row_index, 1, QStandardItem(plan.begin_date.strftime("%Y/%m/%d")))
            # model.setItem(row_index, 2, QStandardItem(plan.deadline.strftime("%Y/%m/%d")))
            model.setItem(row_index, 1, QStandardItem(plan.frequency.name))
            # model.setItem(row_index, 2, QStandardItem(str(plan.repeat)))
            model.setItem(row_index, 2,
                          QStandardItem('{},{}'.format('Important' if plan.degree_importance else 'Unimportant',
                                                       'Urgency' if plan.degree_urgency else 'Non-urgency')))

            row_index += 1
        self.tb_plan.setModel(model)

    def refresh_tb_action(self, tb_index):
        actions = ActionDao.query_actions(tb_index)
        model = QStandardItemModel(len(actions), 3)
        model.setHorizontalHeaderLabels(['Content', 'Begin', 'Deadline'])
        row_index = 0
        for action in actions:
            model.setItem(row_index, 0, QStandardItem(action.content))
            model.setItem(row_index, 1, QStandardItem(action.begin_date.strftime("%Y/%m/%d")))
            model.setItem(row_index, 2, QStandardItem(action.deadline.strftime("%Y/%m/%d")))
            # model.setItem(row_index, 3, QStandardItem(self.status_label[action.status]))
            row_index += 1
        if tb_index == 1:
            self.tb_ac_first.setModel(model)
        elif tb_index == 2:
            self.tb_ac_second.setModel(model)
        elif tb_index == 3:
            self.tb_ac_third.setModel(model)
        elif tb_index == 4:
            self.tb_ac_fourth.setModel(model)
