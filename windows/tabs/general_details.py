from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget


class GeneralDetailTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        columns = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        sizes = (70, 100, 300, 90, 400, 400, 100, 100, 100)
        for column, size in zip(columns, sizes):
            self.table.setColumnWidth(column, size)
        table_header = ("Reg Id", "Smart Card No", "Name", "Admitted Year",
                        "sakec e-mail ID", "microsoft e-mail ID", "Mobile",
                        "Current Division", "Current Roll No")
        self.table.setHorizontalHeaderLabels(table_header)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table, 0, 0, 1, 3)
        self.setLayout(layout)


