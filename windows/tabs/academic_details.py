from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget


class AcademicDetailTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        table_header = ("Name",
                        "SEM1 Ptr", "SEM2 Ptr",
                        "SEM3 Ptr", "SEM4 Ptr",
                        "SEM5 Ptr", "SEM6 Ptr",
                        "SEM7 Ptr", "SEM8 Ptr")
        self.table.setHorizontalHeaderLabels(table_header)
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table, 0, 0, 1, 3)
        self.setLayout(self.layout)
