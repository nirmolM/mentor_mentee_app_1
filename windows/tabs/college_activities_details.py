from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget


class CollegeActivityDetailTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        table_header = ("Name",
                        "Courses Done", "Internship Status",
                        "Publication Details", "Copyright Details",
                        "Products Developed", "Professional Bodies",
                        "Project Competitions Attended")
        self.table.setHorizontalHeaderLabels(table_header)
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table, 0, 0, 1, 3)
        self.setLayout(self.layout)