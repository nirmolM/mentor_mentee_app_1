import os
from PyQt6.QtWidgets import QLabel, QGridLayout, QDialog, QTabWidget, QPushButton, QFileDialog, QMessageBox
from functions import data_extractor as de
from functions import table_options as tb_opt
from functions import dashboard_options as dash_b_opt
from working_data import password_giver as pg
from windows.tabs.general_details import GeneralDetailTab
from windows.tabs.personal_details import PersonalDetailTab
from windows.tabs.pre_admission_details import PreAdmissionDetailTab
from windows.tabs.academic_details import AcademicDetailTab
from windows.tabs.outcome_details import OutcomeDetailTab
from windows.tabs.college_activities_details import CollegeActivityDetailTab
from windows.button_classes.meeting_attendance import MeetingAttendanceWindow
from windows.button_classes.leave_calculator import LeaveCalculatorDashboard
from windows.button_classes.ptm_dashboard import PTMDashboard
from windows.button_classes.academic_achievement_record import AcademicAchievementsDashboard
from windows.button_classes.defaulter_documentation import DefaulterDocumentGenerator


class TableWindow(QDialog):  # todo -> make button for parent letter for defaulters(template given by vidya mam in mail)
    def __init__(self, db_name: str, created_now: bool):
        super().__init__()
        self.roll_no = None
        self.current_div = None
        self.address, self.father_name = None, None
        self.mentee_name, self.path = None, None
        self.db_name = db_name
        self.setWindowTitle("Mentor - Mentee Dashboard")
        # self.showFullScreen()
        self.setMinimumSize(1280, 720)
        layout = QGridLayout()
        path_label = QLabel("Select xls/xlsx file to load data")
        get_path_button = QPushButton("Open")
        get_path_button.clicked.connect(self.get_file_path)
        dashboard_label = QLabel(f"Mentor - {pg.get_username()}")
        close_window_button = QPushButton("Exit")
        close_window_button.clicked.connect(self.close_window)
        self.tab1 = GeneralDetailTab()
        self.tab2 = PersonalDetailTab()
        self.tab3 = PreAdmissionDetailTab()
        self.tab4 = AcademicDetailTab()
        self.tab5 = CollegeActivityDetailTab()
        self.tab6 = OutcomeDetailTab()
        tab_widget = QTabWidget()
        tabs = [self.tab1, self.tab2, self.tab3, self.tab4, self.tab5, self.tab6]
        tab_names = ['General Details', 'Personal Details', 'Pre-Admission Academic Details', 'Academic Details',
                     'College Activities Details', 'Outcome Details']
        for tab, tab_name in zip(tabs, tab_names):
            tab_widget.addTab(tab, tab_name)
        self.load_data_button = QPushButton("Load Data from Table")
        self.load_data_button.clicked.connect(self.load_data_from_database)
        self.write_table_button = QPushButton("Write Table")
        self.write_table_button.clicked.connect(self.write_to_database)
        self.update_table_button = QPushButton("Update Table")
        self.update_table_button.clicked.connect(self.update_database)
        self.tab_tables = [self.tab1.table, self.tab2.table, self.tab3.table,
                           self.tab4.table, self.tab5.table, self.tab6.table]
        for table in self.tab_tables:
            table.cellClicked.connect(self.enable_button)
        all_mentee_action_label = QLabel("Actions for all the Mentee: ")
        individual_mentee_action_label = QLabel("Actions for Individual Mentee: ")
        self.generate_attendance_pdf_button = QPushButton("Generate Mentor-Mentee Meeting Attendance")
        self.generate_attendance_pdf_button.clicked.connect(self.meeting_attendance)
        self.generate_attendance_pdf_button.setDisabled(True)
        self.generate_student_details_button = QPushButton("Show Student Details")
        self.generate_student_details_button.clicked.connect(self.student_detail)
        self.generate_student_details_button.setDisabled(True)
        # todo-> Write logic of mentee special action
        self.generate_mentee_action_ticket = QPushButton("Generate Mentee Special Action Document")
        self.generate_ptm_docs_button = QPushButton("Generate PTM Documents")
        self.generate_ptm_docs_button.clicked.connect(self.generate_ptm_docs)
        self.generate_ptm_docs_button.setDisabled(True)
        self.generate_leave_button = QPushButton("Generate Leave Record")
        self.generate_leave_button.setDisabled(True)
        self.generate_leave_button.clicked.connect(self.leave_calculator)
        self.generate_academic_achievement_lor_loa_button = \
            QPushButton("Generate Academic Achievement and/or LoR/LoA Record")
        self.generate_academic_achievement_lor_loa_button.clicked.connect(self.academic_achievement_record)
        self.generate_academic_achievement_lor_loa_button.setDisabled(True)
        self.generate_defaulter_document_button = QPushButton("Generate Defaulter Document")
        self.generate_defaulter_document_button.clicked.connect(self.defaulter_documentation)
        self.generate_defaulter_document_button.setDisabled(True)
        if not created_now:
            self.update_table_button.setDisabled(True)
            layout.addWidget(self.load_data_button, 1, 3)
            layout.addWidget(self.update_table_button, 1, 4)
            layout.addWidget(all_mentee_action_label, 3, 0, 1, 5)
            layout.addWidget(self.generate_attendance_pdf_button, 4, 0)
            layout.addWidget(self.generate_ptm_docs_button, 4, 1)
            layout.addWidget(individual_mentee_action_label, 5, 0, 1, 5)
            layout.addWidget(self.generate_mentee_action_ticket, 6, 0)
            layout.addWidget(self.generate_leave_button, 6, 1)
            layout.addWidget(self.generate_academic_achievement_lor_loa_button, 6, 2)
            layout.addWidget(self.generate_defaulter_document_button, 6, 3)
            layout.addWidget(self.generate_student_details_button, 6, 4)
        else:
            self.write_table_button.setDisabled(True)
            layout.addWidget(self.write_table_button, 3, 0)
            layout.addWidget(path_label, 1, 3)
            layout.addWidget(get_path_button, 1, 4)
        layout.addWidget(dashboard_label, 0, 0)
        layout.addWidget(close_window_button, 1, 4)
        layout.addWidget(tab_widget, 2, 0, 1, 5)
        self.setLayout(layout)

    def close_window(self):
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Quit App?")
        confirmation_widget.setText("Are You Sure you want to quit?\nAny changes will be left un-updated")
        confirmation_widget.setIcon(QMessageBox.Icon.Question)
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            confirmation_widget.close()

    def get_file_path(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getOpenFileName(parent=self, caption='Select a file', directory=os.getcwd(),
                                               filter=file_filter, initialFilter='Excel File (*.xlsx *.xls)')
        self.path = str(response[0])  # todo -> $BUG$ Rectify crash when QFileDialog is closed without selecting file
        self.load_data_from_xls()

    def load_data_from_xls(self):
        rows = de.extract_from_xls(self.path)
        self.table_write_function_calls(rows)
        self.write_table_button.setDisabled(False)

    def write_to_database(self):
        tb_opt.write_data_in_table(self.db_name, dash_b_opt.give_rows_for_database(self.tab_tables))
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setIcon(QMessageBox.Icon.Information)
        confirmation_widget.setText("The Data was written to Database successfully!\n"
                                    "System will now exit, please restart app and open same Database")
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Ok:
            confirmation_widget.close()
        self.close()

    def update_database(self):
        tb_opt.update_data_in_table(self.db_name, dash_b_opt.give_rows_for_database(self.tab_tables))
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setIcon(QMessageBox.Icon.Information)
        confirmation_widget.setText("The Data was updated to Database successfully!")
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Yes)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Yes:
            confirmation_widget.close()

    def load_data_from_database(self):
        rows = tb_opt.get_data_from_database(self.db_name)
        rows = [list(row) for row in rows]
        self.table_write_function_calls(rows)
        self.update_table_button.setDisabled(False)
        self.generate_attendance_pdf_button.setDisabled(False)
        self.generate_ptm_docs_button.setDisabled(False)

    def table_write_function_calls(self, rows: list):
        ranges = [(rows, None, None), (rows, 9, 20), (rows, 20, 29), (rows, 29, 37), (rows, 37, 44), (rows, 44, 47)]

        def write_to_table_wrapper(args):
            table, (rows_local, start, end) = args
            row_list = de.give_rows_for_tables(rows_local, start, end)
            dash_b_opt.write_to_table(table=table, row_list=row_list)

        list(map(write_to_table_wrapper, zip(self.tab_tables, ranges)))

    def enable_button(self, row):
        self.generate_leave_button.setDisabled(False)
        self.generate_student_details_button.setDisabled(False)
        self.generate_academic_achievement_lor_loa_button.setDisabled(False)
        self.generate_defaulter_document_button.setDisabled(False)
        self.mentee_name = self.tab1.table.item(row, 2).text()
        self.father_name = self.tab2.table.item(8)
        self.address = self.tab2.table.item(3)
        self.current_div = self.tab1.table.item(7)
        self.roll_no = self.tab1.table.item(8)

    def meeting_attendance(self):
        meeting_attendance_window = MeetingAttendanceWindow(self.tab1.table, self.db_name)
        meeting_attendance_window.exec()

    def student_detail(self):  # todo -> Write logic to display student details on GUI, not on console
        print(tb_opt.fetch_leave_details(self.db_name, self.mentee_name))
        print(tb_opt.fetch_academic_achievements(self.db_name, self.mentee_name))
        print(tb_opt.fetch_lor_loa_details(self.db_name, self.mentee_name))

    def leave_calculator(self):
        leave_calculator_window = LeaveCalculatorDashboard(self.db_name, self.mentee_name)
        leave_calculator_window.exec()

    def generate_ptm_docs(self):
        generate_ptm_window = PTMDashboard(self.tab2.table, self.db_name)
        generate_ptm_window.exec()

    def academic_achievement_record(self):
        academic_achievement_record = AcademicAchievementsDashboard(self.db_name, self.mentee_name)
        academic_achievement_record.exec()

    def defaulter_documentation(self):
        defaulter_documentation = DefaulterDocumentGenerator(self.db_name, self.mentee_name,
                                                             self.father_name, self.address, self.roll_no,
                                                             self.current_div)
        defaulter_documentation.exec()
