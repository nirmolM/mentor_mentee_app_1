import pandas as pd


def extract_from_xls(filepath: str):
    rows_local = []
    df = pd.read_excel(filepath)
    row_count = df.shape[0]
    df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])
    df['Date of Birth'] = df['Date of Birth'].dt.date
    for data in range(row_count):
        rows_local.append(list(df.iloc[data]))
    return rows_local


def give_rows_for_tables(rows_local: list, col_start: int = None, col_end: int = None):
    table_data_local = []
    if col_start is not None and col_end is not None:
        work_list = []
        sub_list_size = col_end - col_start + 1
        for data_local in rows_local:
            work_list.append(data_local[2])
            for elements_local in data_local[col_start:col_end]:
                work_list.append(elements_local)
        table_data_local = [work_list[i:i + sub_list_size] for i in range(0, len(work_list), sub_list_size)]
    else:
        for data_local in rows_local:
            table_data_local.append(data_local[:9])
    return table_data_local
