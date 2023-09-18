from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QPushButton, QMainWindow, QLineEdit, QMessageBox, QComboBox, \
    QDialog, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QAction, QPixmap
import working_data.username_password_giver as upg
import working_data.year_semester_giver as ysg
from functions import database_options as db_opt
from functions import table_options as tb_opt
import windows.dasboard as wd


class MainWindow(QMainWindow):  # todo -> Add Icons
    def __init__(self):
        super().__init__()
        self.create_database_widget = None
        self.database_name_input = None
        self.setWindowTitle("Mentor-Mentee Database System")
        # self.showFullScreen()
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
        layout_main = QHBoxLayout()
        layout_col1 = QVBoxLayout()
        layout_col2 = QVBoxLayout()
        layout_main.addLayout(layout_col1, 2)
        layout_main.addLayout(layout_col2, 1)
        self.create_db_button = QPushButton("Create New Database")
        self.create_db_button.clicked.connect(self.create_database_menu)
        self.create_db_button.setDisabled(True)
        self.open_db_button = QPushButton("Open Existing Database")
        self.open_db_button.clicked.connect(self.open_database_menu)
        self.open_db_button.setDisabled(True)
        academic_year_label = QLabel(f"Academic Year: {ysg.give_academic_year()}")
        image_space = QLabel(self)
        image = QPixmap('SAKEC.png')
        image_space.setPixmap(image)
        title_label = QLabel("Mentor Mentee Automation App")
        about_content = """ 
                        <html> 
                            <body> 
                                <p>
                                <b>Welcome to the Mentor Mentee Automation App.</b><br>Please note that the app is still
                                 under development and will be finalized soon.<br>This app aims to make the 
                                 documentation aspect of mentor file just a matter of clicks where all documents will be 
                                 automatically generated.<br>This also aims to make a permanent database for mentee data 
                                 which can be easily fetched or migrated from other files and can be loaded via excel 
                                 sheet or google sheets.<br>Features of this app include:
                                <ul>
                                <li> Creating, Updating and Deleting Databases </li>
                                <li> One-time database creation and data entries in just few clicks </li>
                                <li> Generating all documents required in few clicks </li>
                                <li> Actions like mentee special action, leaves, academic achievements, etc all in one 
                                place </li>
                                <li> All data is tabulated and saved in database tables which can be easily fetched for 
                                individual mentees and all mentees together </li>
                                </ul>
                                </p>
                                <p><b>Special Request to user: </b><br>
                                If you encounter a bug, undesired output and/or a sudden crash then kindly note down,
                                what exactly was that you were doing during the aforementioned bug encountered so that
                                resolving the bug becomes easy<br>
                                Kindly email it on nirmol.munvar@sakec.ac.in
                                </p>
                            </body> 
                        </html>
                        """
        about_label = QLabel(about_content)
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
        self.select_database_label = QLabel("Select Database to Open")
        self.database_box = QComboBox()
        self.database_box.addItems(db_opt.show_databases())
        close_window_button = QPushButton("Exit")
        close_window_button.clicked.connect(self.close_window)
        layout_col1.addStretch()
        layout_col1.addWidget(image_space, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_col1.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_col1.addWidget(academic_year_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_col1.addWidget(about_label, alignment=Qt.AlignmentFlag.AlignJustify)
        layout_col1.addWidget(close_window_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_col1.addStretch()
        layout_col2.addStretch()
        layout_col2.setSpacing(20)
        layout_col2.addWidget(mentor_name_prompt, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_col2_row_2 = QHBoxLayout()
        layout_col2_row_2.setSpacing(5)
        layout_col2_row_2.addWidget(self.mentor_suffixes)
        layout_col2_row_2.addWidget(self.mentor_name_input)
        layout_col2.addLayout(layout_col2_row_2)
        layout_col2.addWidget(password_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_col2.addWidget(self.password_input)
        layout_col2.addWidget(password_accept_button)
        layout_col2_row_5 = QHBoxLayout()
        layout_col2_row_5.addWidget(self.create_db_button)
        layout_col2_row_5.addWidget(self.open_db_button)
        layout_col2.addLayout(layout_col2_row_5)
        layout_col2.addStretch()
        self.centralWidget.setLayout(layout_main)

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

    def close_window(self):
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Quit App?")
        confirmation_widget.setText("Are You Sure you want to quit?")
        confirmation_widget.setIcon(QMessageBox.Icon.Question)
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            confirmation_widget.close()

    def create_database_menu(self):
        self.open_db_button.setDisabled(True)
        self.create_db_button.setDisabled(True)
        self.create_database_widget = QDialog()
        create_database_widget_layout = QVBoxLayout()
        self.create_database_widget.setWindowTitle("Create Database")
        create_database_message = \
            "Enter Name for new Database\n" \
            "Ideal Database name should be\n " \
            "FE_<Division>_<Batch>_<Academic Year Admitted>\n" \
            "Example: FE_11_A_2023_24"
        create_database_label = QLabel(create_database_message)
        self.database_name_input = QLineEdit()
        self.database_name_input.setPlaceholderText("Example: FE_11_A_2023_24")
        create_database_widget_layout.addWidget(create_database_label)
        create_database_widget_layout.addWidget(self.database_name_input)
        create_button = QPushButton("Create")
        create_button.clicked.connect(self.create_database)
        create_database_widget_layout.addWidget(create_button)
        self.create_database_widget.setLayout(create_database_widget_layout)
        self.create_database_widget.exec()

    def create_database(self):
        self.create_database_widget.close()
        db_name = self.database_name_input.text()
        db_opt.create_database(db_name)
        tb_opt.create_table(db_name)
        self.close()
        table_window = wd.TableWindow(db_name, True)
        table_window.exec()

    def open_database_menu(self):
        self.create_db_button.setDisabled(True)
        self.open_db_button.setDisabled(True)
        open_database_widget = QDialog()
        open_database_widget_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        select_button = QPushButton("Open")
        select_button.clicked.connect(self.open_database)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_database)
        h_layout.addWidget(select_button)
        h_layout.addWidget(delete_button)
        select_database_label = QLabel("Select Database to Open")
        self.database_box = QComboBox()
        self.database_box.addItems(db_opt.show_databases())
        open_database_widget_layout.addWidget(select_database_label)
        open_database_widget_layout.addWidget(self.database_box)
        open_database_widget_layout.addLayout(h_layout)
        open_database_widget.setLayout(open_database_widget_layout)
        open_database_widget.exec()

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
