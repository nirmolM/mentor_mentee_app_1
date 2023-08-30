from PyQt6.QtWidgets import QTableWidgetItem


def write_to_table(table, row_list):
    table.setRowCount(0)
    for row_number, row_data in enumerate(row_list):
        table.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


def loop_for_get_data_from_table(table, row, col, row_values_local):
    item = table.item(row, col)
    if item is not None:
        value = item.text()
        row_values_local.append(value)
    else:
        row_values_local.append(None)
    return row_values_local


def get_data_from_table(table, not_tab1: bool = True):
    value_list_local = []
    for row_index in range(table.rowCount()):
        row_values = []
        if not_tab1:
            for column_index in range(1, table.columnCount()):
                row_values = loop_for_get_data_from_table(table, row_index, column_index, row_values)
            value_list_local.append(row_values)
        else:
            for column_index in range(table.columnCount()):
                row_values = loop_for_get_data_from_table(table, row_index, column_index, row_values)
            value_list_local.append(row_values)
    return value_list_local


def give_rows_for_database(table_list: list):
    not_tab1_values = [False, True, True, True, True, True]
    table_values = list(map(lambda args: get_data_from_table(table=args[0], not_tab1=args[1]),
                            zip(table_list, not_tab1_values)))
    row_for_database = [t0 + t1 + t2 + t3 + t4 + t5 for t0, t1, t2, t3, t4, t5 in zip(*table_values)]
    return row_for_database
