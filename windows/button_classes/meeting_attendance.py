from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QCalendarWidget, QPushButton, QVBoxLayout, QFileDialog, \
    QMessageBox
from document_generators import meeting_attendance_generator as doc_gen
from working_data import username_password_giver as upg


class MeetingAttendanceWindow(QDialog):
    def __init__(self, table_object, db_name: str):
        super().__init__()
        self.setWindowTitle("Mentor Mentee Meeting Attendance Generator")
        self.date = None
        self.db_name = db_name
        self.table_object = table_object
        self.mentor_name = QLabel(f"Mentor - {upg.get_username()}")
        agenda_label = QLabel('Enter Meeting Agenda')
        self.agenda_input = QLineEdit()
        date_label = QLabel('Set Meeting Date')
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.on_date_selected)
        generate_document_button = QPushButton('Generate Meeting Attendance Sheet')
        generate_document_button.clicked.connect(self.generate_attendance_sheet)
        layout = QVBoxLayout()
        layout.addWidget(self.mentor_name)
        layout.addWidget(agenda_label)
        layout.addWidget(self.agenda_input)
        layout.addWidget(date_label)
        layout.addWidget(self.calendar)
        layout.addWidget(generate_document_button)
        self.setLayout(layout)

    def on_date_selected(self):
        selected_date = self.calendar.selectedDate()
        self.date = selected_date.toString()

    def generate_attendance_sheet(self):
        attendance_data = []
        for row in range(self.table_object.rowCount()):
            row_items = [self.table_object.item(row, col).text() for col in (2, 7, 8)]
            attendance_data.extend(row_items)
        doc = doc_gen.make_attendance_sheet(self.mentor_name.text(), self.agenda_input.text(),
                                            self.date, attendance_data)
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
        doc.save(f'{filepath}/{self.db_name} {self.date} meeting attendance.docx')
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setIcon(QMessageBox.Icon.Information)
        confirmation_widget.setText("The Attendance Sheet Generated successfully!")
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Ok:
            confirmation_widget.close()
