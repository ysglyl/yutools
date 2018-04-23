import os
from PyQt5.QtWidgets import QWidget, QTreeView, QInputDialog, QPushButton, QTextEdit, QFileSystemModel, QLineEdit
from PyQt5.QtGui import QStandardItem, QIcon, QFont


class YuToolsNoteViewer(QWidget):

    def __init__(self):
        super(YuToolsNoteViewer, self).__init__()

        self.tv_notes = QTreeView(self)
        self.tv_notes.setGeometry(10, 40, 311, 751)
        self.tv_notes.clicked.connect(self.click_tv_item)
        self.tv_notes.doubleClicked.connect(self.doubleclick_tv_item)

        self.te_note = QTextEdit(self)
        self.te_note.setGeometry(330, 40, 461, 751)

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

    def click_tv_item(self, index):
        is_dir = index.model().isDir(index)
        self.select_path = index.model().filePath(index)
        if is_dir:
            self.btn_add_sub.setDisabled(False)
            self.btn_add_note.setDisabled(False)
            self.btn_save_note.setDisabled(True)
            self.te_note.setDisabled(True)
        else:
            self.btn_add_sub.setDisabled(True)
            self.btn_add_note.setDisabled(True)
            self.btn_save_note.setDisabled(False)
            self.te_note.setDisabled(False)

    def doubleclick_tv_item(self, index):
        pass

    def btn_click(self):
        btn = self.sender()
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
            elif btn == self.btn_save_note:
                pass
