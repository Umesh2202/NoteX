import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from fpdf import FPDF


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad")  # * giving titile
        self.screen_width, self.screen_height = self.geometry(
        ).width(), self.geometry().height()
        self.setWindowIcon(QIcon("./icons/notepad.ico"))  # * giving icon
        self.resize(self.screen_width, self.screen_height)

        self.filtertypes = 'Text Document (*.txt);; Python (*.py);; Markdown (*.md)'

        self.path = None

        self.setFixedWidth(900)
        self.setFixedHeight(900)

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)

        mainLayout = QVBoxLayout()

        # *Editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(fixedfont)
        mainLayout.addWidget(self.editor)

        # *Status Bar
        self.statusBar = self.statusBar()

        # *Container
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        # *************** File Menu
        file_menu = self.menuBar().addMenu('&File')
        # ********************

        # *************** File Toolbar
        file_toolbar = QToolBar('File')
        file_toolbar.setIconSize(QSize(50, 50))
        self.addToolBar(Qt.BottomToolBarArea, file_toolbar)
        # ********************

        # *****  File Open
        open_file_action = QAction(
            QIcon('./icons/file_open.ico'), "Open File...", self)
        open_file_action.setStatusTip("Open File")
        open_file_action.setShortcut(QKeySequence.Open)
        open_file_action.triggered.connect(self.file_open)

        # ***** File Save
        save_file_action = self.create_action(
            self, "./icons/file_save.ico", "Save File", "Save File", self.file_save)
        save_file_action.setShortcut(QKeySequence.Save)

        # ***** File Save As
        save_fileAs_action = self.create_action(
            self, "./icons/file_save_as.ico", "Save File As", "Save File As", self.file_save_as)
        save_fileAs_action.setShortcut(QKeySequence('Ctrl+Shift+S'))

        # ***** File Print
        print_file_action = self.create_action(
            self, "./icons/file_print.ico", "Print File", "Print File", self.file_print)
        print_file_action.setShortcut(QKeySequence.Print)

        # ***** Export as pdf
        export_pdf_action = self.create_action(
            self, "./icons/pdf.ico", "Export as PDF", "Export as PDF", self.export_as_pdf)

        # !! Adding actions to the file menu
        file_menu.addActions(
            [open_file_action, save_file_action, save_fileAs_action, print_file_action, export_pdf_action])
        file_toolbar.addActions(
            [open_file_action, save_file_action, save_fileAs_action, print_file_action, export_pdf_action])

        # *************** Add Separator
        file_menu.addSeparator()
        file_toolbar.addSeparator()

        # *************** Edit Menu
        edit_menu = self.menuBar().addMenu('&Edit')
        # ********************

        # *************** Edit Toolbar
        edit_toolbar = QToolBar('Edit')
        edit_toolbar.setIconSize(QSize(50, 50))
        self.addToolBar(Qt.BottomToolBarArea, edit_toolbar)
        # ********************

        # ***** File Undo
        file_undo_action = self.create_action(
            self, "./icons/file_undo.ico", "Undo File", "Undo File", self.editor.undo)
        file_undo_action.setShortcut(QKeySequence.Undo)

        # ***** File Redo
        file_redo_action = self.create_action(
            self, "./icons/file_redo.ico", "Redo File", "Redo File", self.editor.redo)
        file_redo_action.setShortcut(QKeySequence.Redo)

        # ***** Clear
        file_clear_action = self.create_action(
            self, "./icons/clear.ico", "Clear", "Clear", self.clear)
        file_clear_action.setShortcut('Ctrl+Shift+C')

        # ***** File Cut
        file_cut_action = self.create_action(
            self, "./icons/file_cut.ico", "Cut File", "Cut File", self.editor.cut)
        file_cut_action.setShortcut(QKeySequence.Cut)

        # ***** File Copy
        file_copy_action = self.create_action(
            self, "./icons/file_copy.ico", "Copy File", "Copy File", self.editor.copy)
        file_copy_action.setShortcut(QKeySequence.Copy)

        # ***** File Paste
        file_paste_action = self.create_action(
            self, "./icons/file_paste.ico", "Paste File", "Paste File", self.editor.paste)
        file_paste_action.setShortcut(QKeySequence.Paste)

        # *****  Select All
        selectAll_action = self.create_action(
            self, "./icons/file_select_all.ico", "Select All", "Select All", self.editor.selectAll)
        selectAll_action.setShortcut(QKeySequence.SelectAll)

        # !! Adding actions to the edit menu
        edit_menu.addActions(
            [file_cut_action, file_copy_action, file_paste_action, selectAll_action, file_clear_action, file_undo_action, file_redo_action])
        edit_toolbar.addActions(
            [file_cut_action, file_copy_action, file_paste_action, selectAll_action, file_clear_action, file_undo_action, file_redo_action])

        # *************** Add Separator
        edit_menu.addSeparator()
        edit_toolbar.addSeparator()

        # *************** Wrap text
        wrap_text_action = self.create_action(
            self, "./icons/wrap.ico", "Wrap Text", "Wrap Text", self.wrap_text)
        wrap_text_action.setShortcut('Ctrl+W')

        # !! Adding action to the edit menu
        edit_menu.addAction(wrap_text_action)
        edit_toolbar.addAction(wrap_text_action)

        # *************** Colour Menu
        colour_menu = self.menuBar().addMenu('&Colour')
        # ********************

        # ************Red colour

        red_colour_action = self.create_action_colour(
            self, "Red", "Red", lambda: self.setStyleSheet("background-color:red"))

        # ************Green colour

        green_colour_action = self.create_action_colour(
            self, "Green", "Green", lambda: self.setStyleSheet("background-color:green"))

        # ************Blue colour

        blue_colour_action = self.create_action_colour(
            self, "Blue", "Blue", lambda: self.setStyleSheet("background-color:blue"))

        # ************Purple colour

        purple_colour_action = self.create_action_colour(
            self, "Purple", "Purple", lambda: self.setStyleSheet("background-color:purple"))

        # ************White colour

        white_colour_action = self.create_action_colour(
            self, "White", "White", lambda: self.setStyleSheet("background-color:white"))

        # ************Yellow colour

        yellow_colour_action = self.create_action_colour(
            self, "Yellow", "Yellow", lambda: self.setStyleSheet("background-color:yellow"))


# !!!!!!!!!!Adding actions to colour menu and toolbar
        colour_menu.addAction(red_colour_action)

        colour_menu.addAction(green_colour_action)

        colour_menu.addAction(blue_colour_action)

        colour_menu.addAction(purple_colour_action)

        colour_menu.addAction(white_colour_action)

        colour_menu.addAction(yellow_colour_action)

        self.update_title()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self, caption="Open file", directory="", filter=self.filtertypes)

        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path:
            try:
                with open(self.path, 'w') as f:
                    f.write(self.editor.toPlainText())
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
        else:
            self.file_save_as()

    def file_save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", self.filtertypes)

        text = self.editor.toPlainText()

        if not path:
            return
        else:
            try:
                with open(path, 'w') as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.update_title()
        self.show_info_messagebox()

    def file_print(self):
        printDialog = QPrintDialog()
        if printDialog.exec_():
            self.editor.print_(printDialog.printer())

    def update_title(self):
        self.setWindowTitle(
            '{0} - NotepadX'.format(os.path.basename(self.path) if self.path else 'Untitled'))

    def clear(self):
        self.editor.setPlainText('')

    def wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())

    def takefilename(self):
        filename = QInputDialog.getText(
            self, 'Input Dialog', 'Enter your name:')
        return filename

    def show_info_messagebox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("File saved successfully")

        msg.setWindowTitle("Information")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()

    def show_warning_messagebox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText("File not found")

        msg.setWindowTitle("Warning")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()

    def export_as_pdf(self):
        pass
        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", size=15)

        filename, done = QInputDialog.getText(
            self, 'Input Dialog', 'Enter your name:')

        try:
            f = open(f"{str(filename)}.txt", "r")
        except IOError:
            self.show_warning_messagebox()
            return

        for x in f:
            pdf.cell(200, 10, txt=x, ln=1, align='C')

        pdf.output(f"{filename}.pdf")

    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def create_action(self, parent, icon_path, action_name, set_status_tip, triggered_method):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action

    def create_action_colour(self, parent, action_name, set_status_tip, triggered_method):
        action = QAction(action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action


app = QApplication(sys.argv)
notepad = AppDemo()
notepad.show()  # ?????????????
sys.exit(app.exec_())
