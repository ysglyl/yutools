import os
from PyQt5.QtWidgets import QWidget, QTreeView, QInputDialog, QPushButton, QTextEdit, QFileSystemModel, QLineEdit, \
    QRadioButton
from PyQt5.QtGui import QFont


class YuToolsNoteViewer(QWidget):

    def __init__(self):
        super(YuToolsNoteViewer, self).__init__()

        self.tv_notes = QTreeView(self)
        self.tv_notes.setGeometry(10, 40, 311, 630)
        self.tv_notes.setExpandsOnDoubleClick(False)
        self.tv_notes.clicked.connect(self.click_tv_item)
        self.tv_notes.doubleClicked.connect(self.doubleclick_tv_item)

        self.te_note = QTextEdit(self)
        font_default = QFont()
        font_default.setPointSize(12)
        self.te_note.setFont(font_default)
        self.te_note.setGeometry(330, 40, 451, 630)

        self.btn_add_root = QPushButton(self)
        self.btn_add_root.setText('Add Root')
        self.btn_add_root.setGeometry(10, 10, 75, 23)
        self.btn_add_root.clicked.connect(self.btn_click)

        self.btn_add_sub = QPushButton(self)
        self.btn_add_sub.setText('Add Sub')
        self.btn_add_sub.setDisabled(True)
        self.btn_add_sub.setGeometry(100, 10, 75, 23)
        self.btn_add_sub.clicked.connect(self.btn_click)

        self.btn_add_note = QPushButton(self)
        self.btn_add_note.setText('Add Note')
        self.btn_add_note.setDisabled(True)
        self.btn_add_note.setGeometry(190, 10, 75, 23)
        self.btn_add_note.clicked.connect(self.btn_click)

        self.rb_fonts_small = QRadioButton(self)
        self.rb_fonts_small.setText('Small')
        self.rb_fonts_small.setGeometry(350, 10, 60, 23)
        self.rb_fonts_small.clicked.connect(self.change_font_size)
        self.rb_fonts_normal = QRadioButton(self)
        self.rb_fonts_normal.setText('Normal')
        self.rb_fonts_normal.setGeometry(420, 10, 60, 23)
        self.rb_fonts_normal.clicked.connect(self.change_font_size)
        self.rb_fonts_normal.setChecked(True)
        self.rb_fonts_big = QRadioButton(self)
        self.rb_fonts_big.setText('Big')
        self.rb_fonts_big.setGeometry(490, 10, 60, 23)
        self.rb_fonts_big.clicked.connect(self.change_font_size)
        self.rb_fonts_bigger = QRadioButton(self)
        self.rb_fonts_bigger.setText('Bigger')
        self.rb_fonts_bigger.setGeometry(560, 10, 60, 23)
        self.rb_fonts_bigger.clicked.connect(self.change_font_size)
        self.rb_fonts_biggest = QRadioButton(self)
        self.rb_fonts_biggest.setText('Biggest')
        self.rb_fonts_biggest.setGeometry(630, 10, 60, 23)
        self.rb_fonts_biggest.clicked.connect(self.change_font_size)

        self.btn_save_note = QPushButton(self)
        self.btn_save_note.setText('Save')
        self.btn_save_note.setDisabled(True)
        self.btn_save_note.setGeometry(710, 10, 75, 23)
        self.btn_save_note.clicked.connect(self.btn_click)

        self.select_path = None

        self.init_tree()

    def init_tree(self):
        model = QFileSystemModel()
        path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'notes'
        model.setRootPath(path)
        self.tv_notes.setModel(model)
        self.tv_notes.setRootIndex(model.index(path))
        self.tv_notes.setHeaderHidden(True)
        self.tv_notes.resizeColumnToContents(0)
        self.tv_notes.setColumnHidden(1, True)
        self.tv_notes.setColumnHidden(2, True)
        self.tv_notes.setColumnHidden(3, True)

    def click_tv_item(self, index):
        is_dir = index.model().isDir(index)
        self.select_path = index.model().filePath(index)
        if is_dir:
            self.btn_add_sub.setDisabled(False)
            self.btn_add_note.setDisabled(False)
            self.btn_save_note.setDisabled(True)
            self.te_note.clear()
            self.te_note.setDisabled(True)
        else:
            self.te_note.clear()
            self.btn_add_sub.setDisabled(True)
            self.btn_add_note.setDisabled(True)
            self.btn_save_note.setDisabled(False)
            self.te_note.setDisabled(False)
            file = open(self.select_path, mode='r')
            for line in file.readlines():
                self.te_note.append(line.strip('\n'))
            file.close()

    def doubleclick_tv_item(self, index):
        is_dir = index.model().isDir(index)
        self.select_path = index.model().filePath(index)
        path, ordinary_filename = os.path.split(self.select_path)
        file_name, success = QInputDialog.getText(self, "Title", "File Name:", QLineEdit.Normal,
                                                  ordinary_filename.split('.')[0])
        if success:
            if is_dir:
                os.rename(self.select_path, path + os.path.sep + file_name)
            else:
                os.rename(self.select_path, path + os.path.sep + file_name + '.txt')

    def btn_click(self):
        btn = self.sender()
        if btn == self.btn_save_note:
            content = self.te_note.toPlainText()
            lines = content.split('\n')
            file = open(self.select_path, mode='w+')
            for line in lines:
                file.write(line + '\n')
            file.close()
        else:
            file_name, success = QInputDialog.getText(self, "Title", "File Name:", QLineEdit.Normal, '')
            if success:
                if btn == self.btn_add_root:
                    path = os.path.dirname(
                        os.path.realpath(__file__)) + os.path.sep + 'notes' + os.path.sep + file_name.lower()
                    if not os.path.exists(path):
                        os.mkdir(path)
                elif btn == self.btn_add_sub:
                    path = self.select_path + os.path.sep + file_name.lower()
                    if not os.path.exists(path):
                        os.mkdir(path)
                elif btn == self.btn_add_note:
                    path = self.select_path + os.path.sep + file_name.lower() + '.txt'
                    if not os.path.exists(path):
                        open(path, mode='w')

    def change_font_size(self):
        rb = self.sender()
        font = QFont()
        if rb == self.rb_fonts_small:
            font.setPointSize(10)
        elif rb == self.rb_fonts_normal:
            font.setPointSize(12)
        elif rb == self.rb_fonts_big:
            font.setPointSize(14)
        elif rb == self.rb_fonts_bigger:
            font.setPointSize(18)
        elif rb == self.rb_fonts_biggest:
            font.setPointSize(20)
        self.te_note.setFont(font)
