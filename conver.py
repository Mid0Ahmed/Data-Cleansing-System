import pyodbc
import pandas as pd
import socket
import os


def get_sql_server_databases(server):
          try:
              connection_string = f"DRIVER=SQL Server;SERVER={server};UID={''};PWD={''}"
              connection = pyodbc.connect(connection_string)
              cursor = connection.cursor()
              databases = []
              cursor.execute("SELECT name FROM sys.databases")
              rows = cursor.fetchall()
              for row in rows:
                  databases.append(row[0])
              return databases
          except Exception as e:
              print("Error:", e)
              return None
def get_server_name():
          try:
              server_name = socket.gethostname()
              return server_name
          except Exception as e:
              print("Error:", e)
              return None    


def db_convert(db):
    try:    
        def convert_all_tables_to_csv(server, db):
            sql_server_connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db + ';Trusted_Connection=yes;'
            conn = pyodbc.connect(sql_server_connection_string)
            cursor = conn.cursor()
            tables = cursor.tables(tableType='TABLE')
            table_names = [table.table_name for table in tables]
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)  # Create upload directory if it doesn't exist
            for table_name in table_names:
                query = f'SELECT * FROM {table_name}'
                df = pd.read_sql_query(query, conn)
                csv_file_path = os.path.join(upload_dir, f'{table_name}.csv')  # Path to save CSV in upload directory
                df.to_csv(csv_file_path, index=False)
            conn.close()
        
        server = get_server_name()  # Assuming you have a function to get server name
        convert_all_tables_to_csv(server, db)
    except Exception as e:
        return None
    

# server=get_server_name()
get_sql_server_databases("DESKTOP-OA4UFIV")

