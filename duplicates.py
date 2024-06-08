import pandas as pd

def binary_search(arr, x):
    """
    Perform binary search on a sorted list.
    
    Args:
    - arr: The sorted list to search in.
    - x: The value to search for.
    
    Returns:
    - index: The index of the value in the list if found, otherwise -1.
    """
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

def fx1(df, columns_to_check='all'):
    if columns_to_check == "all":
        duplicate_rows = df[df.duplicated(keep=False)]
    else:
        duplicate_rows = df[df.duplicated(subset=columns_to_check, keep=False)]

    return duplicate_rows

def fx2(df, columns_to_check='all'):
    if columns_to_check == "all":
        duplicate_rows = df[df.duplicated()].count().max()
        total_rows = df.count().max()
        pers = round((duplicate_rows / total_rows) * 100)
        return pers, duplicate_rows, total_rows
    else:
        duplicate_rows = df[df.duplicated(subset=columns_to_check)].count().max()
        total_rows = df.count().max()
        pers = round((duplicate_rows / total_rows) * 100)
        return pers, duplicate_rows, total_rows

def fx3(df):
    column_names = df.columns.tolist()
    return column_names

def fx4(input_filename, columns_to_check='all'):
    df = pd.read_csv('uploads/' + input_filename)
    if columns_to_check == "all":
        df_no_duplicates = df.drop_duplicates()
    else:
        df_no_duplicates = df.drop_duplicates(subset=columns_to_check)

    df_no_duplicates.to_csv('uploads/' + input_filename, index=False)

def remove_duplicates_and_save_binary(input_filename, columns_to_check='all'):
    df = pd.read_csv('uploads/' + input_filename)
    sorted_df = df.sort_values(by=columns_to_check)
    duplicate_indices = []
    for col in columns_to_check:
        sorted_col_values = sorted_df[col].tolist()
        for i in range(1, len(sorted_col_values)):
            if sorted_col_values[i] == sorted_col_values[i - 1]:
                idx = binary_search(sorted_col_values, sorted_col_values[i])
                duplicate_indices.append(idx)
    df_no_duplicates = df.drop(duplicate_indices)
    df_no_duplicates.to_csv('uploads/' + input_filename, index=False)

# filename = 'data.csv'
# df = pd.read_csv(filename)
# pers, effectedRows, totalRows = fx2(df, ['id', 'Name'])

# print(f"pers: {pers}")
# print(f"effectedRows: {effectedRows}")
# print(f"totalRows: {totalRows}")
# fx4(filename, ['id', 'Name'])
# print('#'*50)
# pers, effectedRows, totalRows = fx2(df, ['id', 'Name'])

# print(f"pers: {pers}")
# print(f"effectedRows: {effectedRows}")
# print(f"totalRows: {totalRows}")

# remove_duplicates_and_save_binary(filename, ['id', 'Name'])
