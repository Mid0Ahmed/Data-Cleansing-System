import pandas as pd
class Node:
    def __init__(self, data, dtype):
        self.data = data
        self.dtype = dtype
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data, dtype):
        new_node = Node(data, dtype)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
    
    def get_columns(self):
        columns = []
        current = self.head
        while current:
            columns.append(current.data)
            current = current.next
        return columns
    
    def get_dtype(self, data):
        current = self.head
        while current:
            if current.data == data:
                return current.dtype
            current = current.next
        return None
def extract_nan_columns_ll(linked_list, dtype):
    nan_columns_int = []
    nan_columns_str = []
    for column in linked_list.get_columns():
        if linked_list.get_dtype(column) == dtype and any(pd.isnull(column)):
            if dtype == 'float64':
                nan_columns_int.append(column)
            else:
                nan_columns_str.append(column)
    return nan_columns_str if dtype == 'str' else nan_columns_int
# Create a linked list
ll = LinkedList()

# Append columns (data should be in form of pandas Series)
ll.append(pd.Series([1, 2, None, 4]), 'float64')
ll.append(pd.Series([None, 'b', 'c', 'd']), 'str')
ll.append(pd.Series([5.5, None, 6.7, None]), 'float64')

# Manage missing data
ll = (ll, 'mean', 'unknown')

# Print the processed linked list
current = ll.head
while current:
    print(current.data)
    current = current.next
