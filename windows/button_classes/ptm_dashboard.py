import concurrent.futures
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QLabel, QCalendarWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from document_generators import parent_meet_document_generator as doc_gen
from working_data import password_giver as pg


class PTMDashboard(QDialog):
    def __init__(self, table_object2, table_object1, db_name: str):
        super().__init__()
        self.setWindowTitle("PTM Documents Generator")
        self.date = None
        self.db_name = db_name
        self.table_object2 = table_object2
        self.table_object1 = table_object1
        self.mentor_name = QLabel(f"Mentor - {pg.get_username()}")
        date_label = QLabel('Set PTM Date')
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.on_date_selected)
        generate_document_button = QPushButton('Generate Meeting Attendance Sheet')
        generate_document_button.clicked.connect(self.generate_ptm_docs)
        delay_warning_label = QLabel("Please Note, Document generation may take a few seconds")
        layout = QVBoxLayout()
        layout.addWidget(self.mentor_name)
        layout.addWidget(date_label)
        layout.addWidget(self.calendar)
        layout.addWidget(generate_document_button)
        layout.addWidget(delay_warning_label)
        self.setLayout(layout)

    def on_date_selected(self):
        selected_date = self.calendar.selectedDate()
        self.date = selected_date.toString()

    def generate_ptm_docs(self):
        names = [self.table_object2.item(row, 0).text() for row in range(self.table_object2.rowCount())]
        mentee_details = [self.table_object2.item(row, col).text() for row in range(self.table_object2.rowCount()) for
                          col in range(6, 15)]
        new_list = [self.table_object1.item(row, col).text() for row in range(self.table_object1.rowCount()) for col in
                    range(7, 9)]
        roll_no_div_list = list(zip(new_list[1::2], new_list[::2]))
        basic_details = [[name, *roll_no_div] for name, roll_no_div in zip(names, roll_no_div_list)]
        par_det_list = [mentee_details[i:i + 9] for i in range(0, len(mentee_details), 9)]
        final_details = [[*basic_detail, *par_det] for basic_detail, par_det in zip(basic_details, par_det_list)]
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save files')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures, merged_doc_list = [], []
            for details in final_details:
                future = executor.submit(doc_gen.make_parent_meet_documents, self.mentor_name.text(), self.date,
                                         details)
                futures.append(future)
            for future in concurrent.futures.as_completed(futures):
                merged_doc = future.result()
                merged_doc_list.append(merged_doc)
        doc_gen.super_merger(merged_doc_list, filepath, self.date)
        doc_gen.ptm_attendance_generator(self.mentor_name.text(), filepath, self.date, final_details)
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setIcon(QMessageBox.Icon.Information)
        confirmation_widget.setText(f"Thank you for waiting patiently\n"
                                    f"The Documents are generated successfully!\n"
                                    f"Please Note the Documents may not be roll number wise ordered")
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Ok:
            confirmation_widget.close()
