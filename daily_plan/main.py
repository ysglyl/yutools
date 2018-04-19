import datetime

from PyQt5.QtCore import QDate, QPoint
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QComboBox, QSpinBox, \
    QCheckBox, QPushButton, QFrame, QTableView, QCalendarWidget, QDateEdit, QRadioButton, \
    QMessageBox, QHeaderView, QItemDelegate, QMenu
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon

from daily_plan.db_helper import PlanFrequency, Plan, Action, PlanDao, ActionDao


class YuToolsDailyPlan(QWidget):
    def __init__(self):
        super().__init__()

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
        self.tb_plan.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.tb_plan.verticalHeader().hide()
        self.tb_plan.setGeometry(370, 10, 421, 281)

        self.line_importance = QFrame(self)
        self.line_importance.setGeometry(390, 295, 20, 435)
        self.line_importance.setFrameShape(QFrame.VLine)
        self.line_importance.setFrameShadow(QFrame.Sunken)

        self.line_urgency = QFrame(self)
        self.line_urgency.setGeometry(5, 480, 791, 16)
        self.line_urgency.setFrameShape(QFrame.HLine)
        self.line_urgency.setFrameShadow(QFrame.Sunken)

        self.cb_show_all = QCheckBox(self)
        self.cb_show_all.setGeometry(393, 475, 26, 26)
        self.cb_show_all.stateChanged.connect(self.change_tb_ac_list)

        self.tb_ac_first = QTableView(self)
        self.tb_ac_first.horizontalHeader().setStretchLastSection(True)
        self.tb_ac_first.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.tb_ac_first.verticalHeader().hide()
        self.tb_ac_first.setItemDelegateForColumn(3, ActionStatusDelegate(self.tb_ac_first))
        self.tb_ac_first.setGeometry(410, 300, 381, 180)

        self.tb_ac_second = QTableView(self)
        self.tb_ac_second.horizontalHeader().setStretchLastSection(True)
        self.tb_ac_second.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.tb_ac_second.verticalHeader().hide()
        self.tb_ac_second.setItemDelegateForColumn(3, ActionStatusDelegate(self.tb_ac_second))
        self.tb_ac_second.setGeometry(10, 300, 381, 180)

        self.tb_ac_third = QTableView(self)
        self.tb_ac_third.horizontalHeader().setStretchLastSection(True)
        self.tb_ac_third.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.tb_ac_third.verticalHeader().hide()
        self.tb_ac_third.setItemDelegateForColumn(3, ActionStatusDelegate(self.tb_ac_third))
        self.tb_ac_third.setGeometry(10, 495, 381, 180)

        self.tb_ac_fourth = QTableView(self)
        self.tb_ac_fourth.horizontalHeader().setStretchLastSection(True)
        self.tb_ac_fourth.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.tb_ac_fourth.verticalHeader().hide()
        self.tb_ac_fourth.setItemDelegateForColumn(3, ActionStatusDelegate(self.tb_ac_fourth))
        self.tb_ac_fourth.setGeometry(410, 495, 381, 180)

        self.tb_acs = {1: self.tb_ac_first, 2: self.tb_ac_second, 3: self.tb_ac_third, 4: self.tb_ac_fourth}

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
        plan_id = PlanDao.add_plan(data)
        ActionDao.add_actions(actions, plan_id)

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
                    if week == weeks:
                        deadline = plan.deadline
                    else:
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
                    if quarter == quarters:
                        deadline = plan.deadline
                    else:
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
                    if year == years:
                        deadline = plan.deadline
                    else:
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

    def change_tb_ac_list(self):
        for index in range(1, 5):
            self.refresh_tb_action(index)

    def refresh_tb_plan(self):
        plans = PlanDao.query_plans()
        model = QStandardItemModel(len(plans), 3)
        model.setHorizontalHeaderLabels(['Content', 'Frequency', 'Flag'])
        row_index = 0
        for plan in plans:
            qsi_content = QStandardItem(plan.content)
            qsi_content.setEditable(False)
            qsi_frequency = QStandardItem(plan.frequency.name)
            qsi_frequency.setEditable(False)
            qsi_flag = QStandardItem('{},{}'.format('Important' if plan.degree_importance else 'Unimportant',
                                                    'Urgency' if plan.degree_urgency else 'Non-urgency'))
            qsi_flag.setEditable(False)
            model.setItem(row_index, 0, qsi_content)
            model.setItem(row_index, 1, qsi_frequency)
            model.setItem(row_index, 2, qsi_flag)
            row_index += 1
        self.tb_plan.setModel(model)
        self.tb_plan.setColumnWidth(0, 220)
        self.tb_plan.setColumnWidth(1, 70)
        self.tb_plan.setColumnWidth(2, 100)

    def refresh_tb_action(self, tb_index):
        tb_action = self.tb_acs[tb_index]
        show_all = self.cb_show_all.isChecked()
        actions = ActionDao.query_actions(tb_index,show_all)
        model = QStandardItemModel(len(actions), 3)
        model.setHorizontalHeaderLabels(['Content', 'Begin', 'Deadline', 'Status'])
        row_index = 0
        for action in actions:
            qsi_content = QStandardItem(action.content)
            qsi_content.setEditable(False)
            qsi_begin_date = QStandardItem(action.begin_date.strftime("%Y/%m/%d"))
            qsi_content.setEditable(False)
            qsi_deadline = QStandardItem(action.deadline.strftime("%Y/%m/%d"))
            qsi_deadline.setEditable(False)
            qsi_status = QStandardItem()
            qsi_status.setData({'id': action.id, 'status': action.status})
            qsi_status.setEditable(False)
            model.setItem(row_index, 0, qsi_content)
            model.setItem(row_index, 1, qsi_begin_date)
            model.setItem(row_index, 2, qsi_deadline)
            model.setItem(row_index, 3, qsi_status)
            row_index += 1
        tb_action.setModel(model)
        tb_action.setColumnWidth(0, 160)
        tb_action.setColumnWidth(1, 70)
        tb_action.setColumnWidth(2, 70)
        tb_action.setColumnWidth(3, 40)

    def change_status(self, tb_action, act_id, status):
        if status == 0:
            QMessageBox.information(self, 'Tip', 'Please wait for beginning')
        elif status == 1:
            menu = QMenu(tb_action)
            done_act = menu.addAction(QIcon('icons/daily_plan/done.png'), 'Done')
            cancel_act = menu.addAction(QIcon('icons/daily_plan/cancel.png'), 'Cancel')
            act = menu.exec_(tb_action.mapToGlobal(QPoint(self.sender().x(), self.sender().y() + 10)))
            refresh = False
            if act == done_act:
                ActionDao.update_action(act_id, 2)
                refresh = True
            elif act == cancel_act:
                ActionDao.update_action(act_id, 3)
                refresh = True
            if refresh:
                self.refresh_tb_action(list(self.tb_acs.keys())[list(self.tb_acs.values()).index(tb_action)])
        elif status == 2:
            QMessageBox.information(self, 'Tip', 'You are good that had completed the task')
        elif status == 3:
            QMessageBox.information(self, 'Tip', 'It is sadly you had canceled this task')
        elif status == 4:
            QMessageBox.information(self, 'Tip', 'It is sorry that this task had expired and you cannot operate it')


class ActionStatusDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ActionStatusDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            data = index.model().item(index.row(), index.column()).data()
            btn = QPushButton(ActionDao.status_label[data['status']], self.parent())
            if data['status'] == 0:
                btn.setIcon(QIcon('icons/daily_plan/wait.png'))
            elif data['status'] == 1:
                btn.setIcon(QIcon('icons/daily_plan/going.png'))
            elif data['status'] == 2:
                btn.setIcon(QIcon('icons/daily_plan/done.png'))
            elif data['status'] == 3:
                btn.setIcon(QIcon('icons/daily_plan/cancel.png'))
            elif data['status'] == 4:
                btn.setIcon(QIcon('icons/daily_plan/expire'))
            btn.clicked.connect(lambda: self.parent().parent().change_status(self.parent(), data['id'], data['status']))
            self.parent().setIndexWidget(index, btn)
