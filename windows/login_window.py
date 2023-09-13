from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QPushButton, QMainWindow, QLineEdit, QMessageBox, QComboBox, \
    QDialog
from PyQt6.QtGui import QAction, QPixmap
import working_data.username_password_giver as upg
from functions import database_options as db_opt
from functions import table_options as tb_opt
import windows.dasboard as wd


class MainWindow(QMainWindow):  # todo -> Add Icons
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mentor-Mentee Database System")
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        self.add_database_action = QAction("Create Database", self)
        self.open_database_action = QAction("Open Database", self)
        self.add_database_action.triggered.connect(self.create_database_menu)
        self.add_database_action.setDisabled(True)
        self.open_database_action.triggered.connect(self.open_database_menu)
        self.open_database_action.setDisabled(True)
        file_menu_item.addAction(self.add_database_action)
        file_menu_item.addAction(self.open_database_action)
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QGridLayout()
        self.create_db_button = QPushButton("Create New Database")
        self.create_db_button.clicked.connect(self.create_database_menu)
        self.create_db_button.setDisabled(True)
        self.open_db_button = QPushButton("Open Existing Database")
        self.open_db_button.clicked.connect(self.open_database_menu)
        self.open_db_button.setDisabled(True)
        image_space = QLabel(self)
        image = QPixmap('SAKEC.png')
        image_space.setPixmap(image)
        title_label = QLabel("Mentor Mentee Automation App")
        password_label = QLabel("Please Enter Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_accept_button = QPushButton("Login")
        password_accept_button.clicked.connect(self.login)
        mentor_name_prompt = QLabel("Enter Mentor Name")
        suffixes = ['Prof.', 'Dr.']
        self.mentor_suffixes = QComboBox()
        self.mentor_suffixes.addItems(suffixes)
        self.mentor_name_input = QLineEdit()
        create_database_message = \
            "Enter Name for new Database\n" \
            "Ideal Database name should be\n " \
            "FE_<Division>_<Batch>_<Academic Year Admitted>\n" \
            "Example: FE_11_A_2023_24"
        self.create_database_label = QLabel(create_database_message)
        self.database_name_input = QLineEdit()
        self.database_name_input.setPlaceholderText("Example: FE_11_A_2023_24")
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_database)
        self.select_database_label = QLabel("Select Database to Open")
        self.database_box = QComboBox()
        self.database_box.addItems(db_opt.show_databases())
        self.select_button = QPushButton("Open")
        self.select_button.clicked.connect(self.open_database)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_database)
        self.layout.addWidget(image_space, 0, 0)
        self.layout.addWidget(title_label, 0, 1)
        self.layout.addWidget(mentor_name_prompt, 1, 0, 1, 4)
        self.layout.addWidget(self.mentor_suffixes, 2, 0)
        self.layout.addWidget(self.mentor_name_input, 2, 1, 1, 3)
        self.layout.addWidget(password_label, 3, 0, 1, 2)
        self.layout.addWidget(self.password_input, 4, 0, 1, 4)
        self.layout.addWidget(password_accept_button, 4, 5)
        self.layout.addWidget(self.create_db_button, 5, 0, 1, 2)
        self.layout.addWidget(self.open_db_button, 5, 2, 1, 2)
        self.centralWidget.setLayout(self.layout)

    def login(self):
        login_password = self.password_input.text()
        self.password_input.clear()
        if login_password == upg.give_password():
            mentor_name = f"{self.mentor_suffixes.currentText()} {self.mentor_name_input.text()}"
            upg.set_username(mentor_name)
            self.create_db_button.setDisabled(False)
            self.open_db_button.setDisabled(False)
            self.add_database_action.setDisabled(False)
            self.open_database_action.setDisabled(False)
        else:
            incorrect_password_prompt_widget = QMessageBox()
            incorrect_password_prompt_widget.setWindowTitle("Incorrect Password")
            incorrect_password_prompt_widget.setText("Please Enter Correct Password")
            incorrect_password_prompt_widget.setIcon(QMessageBox.Icon.Critical)
            incorrect_password_prompt_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
            message = incorrect_password_prompt_widget.exec()
            if message == QMessageBox.StandardButton.Ok:
                incorrect_password_prompt_widget.close()

    def create_database_menu(self):
        self.open_db_button.setDisabled(True)
        self.layout.addWidget(self.create_database_label, 6, 0, 1, 2)
        self.layout.addWidget(self.database_name_input, 7, 0, 1, 2)
        self.layout.addWidget(self.create_button, 8, 0)

    def create_database(self):
        db_name = self.database_name_input.text()
        db_opt.create_database(db_name)
        tb_opt.create_table(db_name)
        self.close()
        table_window = wd.TableWindow(db_name, True)
        table_window.exec()

    def open_database_menu(self):
        self.create_db_button.setDisabled(True)
        self.layout.addWidget(self.select_database_label, 6, 2)
        self.layout.addWidget(self.database_box, 7, 2, 1, 2)
        self.layout.addWidget(self.select_button, 8, 2)
        self.layout.addWidget(self.delete_button, 8, 3)

    def open_database(self):
        db_name = str(self.database_box.currentText())
        self.close()
        table_window = wd.TableWindow(db_name, False)
        table_window.exec()

    def about(self):
        pass

    def delete_database(self):
        dialog = DeleteDatabaseDialog(str(self.database_box.currentText()))
        dialog.exec()
        self.database_box.clear()
        self.database_box.addItems(db_opt.show_databases())


class DeleteDatabaseDialog(QDialog):
    def __init__(self, db_name: str):
        super().__init__()
        self.db_name = db_name
        self.setWindowTitle("Delete Mentee Database")
        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?\nThis will permanently delete the database")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)
        yes.clicked.connect(self.delete_database)
        no.clicked.connect(self.close_window)

    def delete_database(self):
        db_opt.delete_database(self.db_name)
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The Database was deleted successfully!")
        confirmation_widget.exec()

    def close_window(self):
        self.close()
