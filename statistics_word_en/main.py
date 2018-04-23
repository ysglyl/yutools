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

        self.line = QFrame(self)
        self.line.setGeometry(10, 326, 781, 5)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.ls_waste = QListWidget(self)
        self.ls_waste.setGeometry(10, 335, 131, 340)
        self.ls_waste.itemDoubleClicked.connect(self.remove_waste)

        self.tb_word_his = QTableView(self)
        self.tb_word_his.horizontalHeader().setStretchLastSection(True)
        self.tb_word_his.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.tb_word_his.setGeometry(165, 335, 291, 340)
        self.tb_word_his.clicked.connect(self.tb_click)

        self.txt_explain = QTextEdit(self)
        self.txt_explain.setReadOnly(True)
        self.txt_explain.setGeometry(470, 335, 321, 310)

        self.btn_edit_explain = QPushButton(self)
        self.btn_edit_explain.setText('Edit')
        self.btn_edit_explain.clicked.connect(self.click_handler)
        self.btn_edit_explain.setGeometry(730, 650, 60, 26)
        self.edit_explain_flag = False

        self.wastes = []
        self.refresh_list_waste()

        self.refresh_tb_word()

        self.show_explain_word = None

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
            if self.edit_explain_flag:
                self.edit_explain_flag = False
                WordDao.update(self.show_explain_word, self.txt_explain.toPlainText())
                sender.setText('Edit')
                self.txt_explain.setReadOnly(True)
            else:
                if self.show_explain_word:
                    self.edit_explain_flag = True
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
                '!').strip(':').strip('(').strip(')').strip('[').strip(']').strip('{').strip(']')
            if not word or word in self.wastes:
                continue
            if word in list(results.keys()):
                results[word] = results[word] + 1
            else:
                results[word] = 1
        return sorted(results.items(), key=lambda kv: kv[1], reverse=True)

    def refresh_list_waste(self):
        self.ls_waste.clear()
        self.wastes.clear()
        wastes = WasteDao.query_wastes()
        for waste in wastes:
            self.wastes.append(waste.word)
            self.ls_waste.addItem(waste.word)

    def refresh_tb_word(self):
        words = WordDao.query_words()
        rows = len(words)
        if rows == 0:
            return
        model = QStandardItemModel(rows, 2)
        model.setHorizontalHeaderLabels(['Word', 'Amount'])
        row_index = 0
        for word in words:
            qsi_word = QStandardItem(word.word)
            qsi_word.setEditable(False)
            qsi_amount = QStandardItem(str(word.amount))
            qsi_amount.setEditable(False)
            model.setItem(row_index, 0, qsi_word)
            model.setItem(row_index, 1, qsi_amount)
            row_index += 1
        self.tb_word_his.setModel(model)
        self.tb_word_his.setColumnWidth(0, 150)
        self.tb_word_his.setColumnWidth(1, 80)

    def tb_click(self, index):
        tb = self.sender()
        if tb == self.tb_word_cur:
            if index.column() == 0:
                menu = QMenu(self.tb_word_cur)
                search_act = menu.addAction(QIcon('icons/statistics_word_en/search.png'), 'Search')
                copy_act = menu.addAction(QIcon('icons/statistics_word_en/copy.png'), 'Copy')
                word_act = menu.addAction(QIcon('icons/statistics_word_en/word.png'), 'Word')
                waste_act = menu.addAction(QIcon('icons/statistics_word_en/waste.png'), 'Waste')
                i = index.row() - tb.verticalScrollBar().sliderPosition()
                act = menu.exec_(
                    self.mapToGlobal(
                        QPoint(tb.x() + 60 * index.column() + 30, tb.y() + 30 * i + 5)))
                word = index.model().item(index.row(), index.column()).text()
                if act == search_act:
                    self.show_word_explain(word)
                elif act == copy_act:
                    pyperclip.copy(word)
                elif act == word_act:
                    amount = int(index.model().item(index.row(), index.column() + 1).text())
                    WordDao.add(Word(word=word, amount=amount))
                    self.refresh_tb_word()
                elif act == waste_act:
                    WasteDao.add(Waste(word=word))
                    self.refresh_list_waste()
        elif tb == self.tb_word_his:
            self.show_word_explain(index.model().item(index.row(), 0).text())

    def show_word_explain(self, word):
        if self.show_explain_word != word:
            self.show_explain_word = word
            exist_word = WordDao.query_by_word(word)
            if exist_word:
                self.txt_explain.setText(exist_word.explain)
            else:
                self.txt_explain.setText('')

    def remove_waste(self, item):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to remove this Waste?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            WasteDao.remove(item.text())
            self.refresh_list_waste()
