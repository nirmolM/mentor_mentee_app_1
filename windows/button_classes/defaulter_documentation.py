# todo -> write the class and code here

from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QCalendarWidget, QPushButton, QComboBox, QLineEdit, \
    QRadioButton, QMessageBox, QFileDialog
from working_data import password_giver as pg


class DefaulterDocumentGenerator(QDialog):
    def __init__(self, table_object_1, table_object_2, db_name, mentee_name):
        super().__init__()
        self.tb1 = table_object_1
        self.tb2 = table_object_2
        self.db_name = db_name
        self.mentee_name = mentee_name
        self.mentor_name = QLabel(f"Mentor - {pg.get_username()}")
