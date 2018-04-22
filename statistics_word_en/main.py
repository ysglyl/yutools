import datetime
import threading
import pyperclip

from PyQt5.QtCore import QDate, QPoint, QEvent
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QComboBox, QListWidget, \
    QCheckBox, QPushButton, QFrame, QTableView, QCalendarWidget, QDateEdit, QRadioButton, \
    QMessageBox, QHeaderView, QItemDelegate, QMenu, QLabel, QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont

from statistics_word_en.db_helper import Waste, Word, WasteDao, WordDao


class YuToolsStatisticsWordEn(QWidget):
    def __init__(self):
        super().__init__()

        self.lbl_now = QLabel(self)
        self.lbl_now.setGeometry(10, 10, 180, 22)
        font = QFont()
        font.setPointSize(12)
        self.lbl_now.setFont(font)
        self.lbl_now.setStyleSheet("color: rgb(255, 0, 0);")
        self.lbl_now.setText(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        self.txt_content = QPlainTextEdit(self)
        self.txt_content.setGeometry(10, 40, 500, 280)

        self.btn_statistics = QPushButton(self)
        self.btn_statistics.setText('>>')
        self.btn_statistics.setGeometry(520, 170, 30, 26)
        self.btn_statistics.clicked.connect(self.click_handler)

        self.lbl_op_tips = QLabel(self)
        self.lbl_op_tips.setText('Double click table cell for more operations')
        self.lbl_op_tips.setFont(font)
        self.lbl_op_tips.setStyleSheet("color: rgb(0, 0, 255);")
        self.lbl_op_tips.setGeometry(440, 10, 350, 22)

        self.tb_word_cur = QTableView(self)
        self.tb_word_cur.horizontalHeader().setStretchLastSection(True)
        self.tb_word_cur.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.tb_word_cur.setGeometry(560, 40, 230, 280)
        self.tb_word_cur.clicked.connect(self.tb_click)
        self.tb_word_cur.doubleClicked.connect(self.tb_double_click)

        self.line = QFrame(self)
        self.line.setGeometry(10, 326, 781, 5)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.ls_waste = QListWidget(self)
        self.ls_waste.setGeometry(10, 335, 131, 340)

        self.tb_word_his = QTableView(self)
        self.tb_word_his.setGeometry(165, 335, 291, 340)

        self.txt_explain = QTextEdit(self)
        self.txt_explain.setReadOnly(True)
        self.txt_explain.setGeometry(470, 335, 321, 310)

        self.btn_edit_explain = QPushButton(self)
        self.btn_edit_explain.setText('Edit')
        self.btn_edit_explain.clicked.connect(self.click_handler)
        self.btn_edit_explain.setGeometry(730, 650, 60, 26)
        self.explain_edit_flag = False

        self.wastes = ['a', 'one', 'the', 'on', 'in', 'to']
        self.ls_waste.addItems(self.wastes)

        threading.Timer(1, self.show_now_time).start()

    def show_now_time(self):
        self.lbl_now.setText(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if self.parent().parent().parent().app_running:
            threading.Timer(1, self.show_now_time).start()

    def click_handler(self):
        sender = self.sender()
        if sender == self.btn_statistics:
            self.refresh_tb_statistics()
        elif sender == self.btn_edit_explain:
            if self.explain_edit_flag:
                self.explain_edit_flag = False
                sender.setText('Edit')
                self.txt_explain.setReadOnly(True)
            else:
                self.explain_edit_flag = True
                self.txt_explain.setReadOnly(False)
                sender.setText('Save')

    def refresh_tb_statistics(self):
        results = self.statistics_word()
        rows = len(results)
        if rows == 0:
            return
        model = QStandardItemModel(rows, len(results[0]))
        model.setHorizontalHeaderLabels(['Word', 'Amount'])
        row_index = 0
        for item in results:
            for i in range(len(item)):
                qsi_item = QStandardItem(str(item[i]))
                qsi_item.setEditable(False)
                model.setItem(row_index, i, qsi_item)
            row_index += 1
        self.tb_word_cur.setModel(model)
        self.tb_word_cur.setColumnWidth(0, 120)
        self.tb_word_cur.setColumnWidth(1, 60)

    def statistics_word(self):
        content = self.txt_content.toPlainText().replace('\n', ' ').strip('')
        words = content.split(' ')
        results = {}
        for word in words:
            word = word.lower().strip(' ').strip('.').strip(',').strip('"').strip('\'').strip(';').strip('?').strip(
                '!').strip(':')
            if not word or word in self.wastes:
                continue
            if word in list(results.keys()):
                results[word] = results[word] + 1
            else:
                results[word] = 1
        return sorted(results.items(), key=lambda kv: kv[1], reverse=True)

    def tb_double_click(self, index):
        if index.column() == 0:
            menu = QMenu(self.tb_word_cur)
            copy_act = menu.addAction(QIcon('icons/statistics_word_en/copy.png'), 'Copy')
            word_act = menu.addAction(QIcon('icons/statistics_word_en/word.png'), 'Word')
            waste_act = menu.addAction(QIcon('icons/statistics_word_en/waste.png'), 'Waste')
            i = index.row()
            i = i if i < 9 else 8
            act = menu.exec_(
                self.mapToGlobal(
                    QPoint(self.sender().x() + 60 * index.column() + 30, self.sender().y() + 30 * i + 5)))
            refresh = False
            if act == copy_act:
                pyperclip.copy(index.model().item(index.row(), index.column()).text())
            elif act == word_act:
                refresh = True
            elif act == waste_act:
                refresh = True

    def tb_click(self, index):
        print(index)
