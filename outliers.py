import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import os
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import os
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import cv2
import os

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import os
import cv2
from queue import Queue

class DataQueue:
    def __init__(self):
        self.queue = Queue()

    def enqueue(self, item):
        self.queue.put(item)

    def dequeue(self):
        return self.queue.get()

    def is_empty(self):
        return self.queue.empty()

def fn1(col_name, df, operation):
    q = DataQueue()
    col_data = df[col_name]

    if operation == 'op1':
        cc1, cc3 = np.percentile(col_data.dropna(), [25, 75])
        iqccr = cc3 - cc1
        lower_bound = cc1 - 1.5 * iqccr
        upper_bound = cc3 + 1.5 * iqccr
        for idx, val in col_data.iteritems():
            if val < lower_bound or val > upper_bound:
                q.enqueue(idx)
    elif operation == 'op2':
        for idx, val in col_data.iteritems():
            if val < 0:
                q.enqueue(idx)

    return q

def fn2(col_name, df, operation, replacement=None):
    q = fn1(col_name, df, operation)
    while not q.is_empty():
        idx = q.dequeue()
        if operation == 'rmv':
            df = df.drop(index=idx)
        elif operation == 'rplc':
            df.at[idx, col_name] = replacement
    return df

def fn3(column_name, df):
    return fn1(column_name, df, 'op1')

def fn4(column_name, df):
    return fn1(column_name, df, 'op2')

def fn5(column_name, df, states='all'):
    total_rows = len(df)
    if states == 'neg':
        outlier_queue = fn4(column_name, df)
    else:
        outlier_queue = fn3(column_name, df)

    num_outliers = 0
    while not outlier_queue.is_empty():
        outlier_queue.dequeue()
        num_outliers += 1

    outlier_percentage = (num_outliers / total_rows) * 100
    return total_rows, num_outliers, round(outlier_percentage)

def fn6(column_name, df):
    outliers = fn3(column_name, df)
    total_rows, num_outliers, outlier_percentage = fn5(column_name, df)
    return outliers, total_rows, num_outliers, outlier_percentage

def fn7(column_name, df):
    negtiveOutliers = fn4(column_name, df)
    total_rows, num_outliers, outlier_percentage = fn5(column_name, df, 'neg')
    return negtiveOutliers, total_rows, num_outliers, outlier_percentage

def fn8(column_name, df, output_file):
    cleaned_df = fn2(column_name, df, 'rmv')
    cleaned_df.to_csv(output_file, index=False)
    return cleaned_df

def fn9(column_name, fileName):
    df = pd.read_csv(fileName)
    cleaned_df = fn2(column_name, df, 'rmv')
    if cleaned_df is not None:
        cleaned_df.to_csv(fileName, index=False)
    return cleaned_df

def fn10(df, column_name, plot_type):
    column_data = df[column_name]
    output_dir = "./img"
    
    if plot_type == 'Scatter_Plot':
        plot = go.Scatter(x=df.index, y=column_data, mode='markers', name='Data Points')
        layout = go.Layout(title=f"Scatter Plot of {column_name}",
                           xaxis=dict(title='Index'),
                           yaxis=dict(title=column_name))
    elif plot_type == 'Box_Plot':
        plot = go.Box(y=column_data, name='Data Distribution')
        layout = go.Layout(title=f"Box Plot of {column_name}", yaxis=dict(title=column_name))
    elif plot_type == 'Histogram':
        plot = go.Histogram(x=column_data, name='Data Distribution', nbinsx=20)
        layout = go.Layout(title=f"Histogram of {column_name}",
                           xaxis=dict(title=column_name),
                           yaxis=dict(title='Frequency'))
    elif plot_type == 'Line_Chart':
        plot = go.Scatter(x=df.index, y=column_data, mode='lines', name='Data Points')
        layout = go.Layout(title=f"Line Chart of {column_name}",
                           xaxis=dict(title='Index'),
                           yaxis=dict(title=column_name))
    else:
        print("Unknown plot type")
        return

    fig = go.Figure(data=[plot], layout=layout)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_name = os.path.join(output_dir, f"{column_name}_plot.png")
    pio.write_image(fig, output_file_name)
    
    saved_image = cv2.imread(output_file_name)
    cv2.imshow("Saved Image", saved_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




def remove_negative_rows(column_name,fileName):
    df = pd.read_csv(fileName)
    column_numeric = pd.to_numeric(df[column_name], errors='coerce')

    cleaned_df = df[column_numeric >= 0]
    if cleaned_df is not None:
       cleaned_df.to_csv(fileName, index=False)
    return cleaned_df


def save_and_display_plot(df, column_name, plot_type):
    column_data = df[column_name]
    output_dir = "./img"
    
    if plot_type == 'Scatter_Plot':
        plot = go.Scatter(x=df.index, y=column_data, mode='markers', name='Data Points')
        layout = go.Layout(title=f"Scatter Plot of {column_name}",
                           xaxis=dict(title='Index'),
                           yaxis=dict(title=column_name))
    elif plot_type == 'Box_Plot':
        plot = go.Box(y=column_data, name='Data Distribution')
        layout = go.Layout(title=f"Box Plot of {column_name}", yaxis=dict(title=column_name))
    elif plot_type == 'Histogram':
        plot = go.Histogram(x=column_data, name='Data Distribution', nbinsx=20)
        layout = go.Layout(title=f"Histogram of {column_name}",
                           xaxis=dict(title=column_name),
                           yaxis=dict(title='Frequency'))
    elif plot_type == 'Line_Chart':
        plot = go.Scatter(x=df.index, y=column_data, mode='lines', name='Data Points')
        layout = go.Layout(title=f"Line Chart of {column_name}",
                           xaxis=dict(title='Index'),
                           yaxis=dict(title=column_name))
    else:
        print("Unknown plot type")
        return

    fig = go.Figure(data=[plot], layout=layout)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_name = os.path.join(output_dir, f"{column_name}_plot.png")
    pio.write_image(fig, output_file_name)
    
    
    saved_image = cv2.imread(output_file_name)
    cv2.imshow("Saved Image", saved_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# تحميل البيانات


# Create Box Plot
# box_plot = go.Box(y=column_data, name='Data Distribution')
# box_layout = go.Layout(title=f"Box Plot of {column_name}", yaxis=dict(title=column_name))
# box_fig = go.Figure(data=[box_plot], layout=box_layout)

# # Save Box Plot as an Image
# box_plot_name = f"{column_name}_box_plot.png"
# pio.write_image(box_fig, box_plot_name)
# # Create Histogram
# histogram = go.Histogram(x=column_data, name='Data Distribution', nbinsx=20)
# hist_layout = go.Layout(title=f"Histogram of {column_name}",
#                         xaxis=dict(title=column_name),
#                         yaxis=dict(title='Frequency'))
# hist_fig = go.Figure(data=[histogram], layout=hist_layout)

# # Save Histogram as an Image
# histogram_name = f"{column_name}_histogram.png"
# pio.write_image(hist_fig, histogram_name)

# # Create Line Chart
# line_chart = go.Scatter(x=df.index, y=column_data, mode='lines', name='Data Points')
# line_layout = go.Layout(title=f"Line Chart of {column_name}",
#                         xaxis=dict(title='Index'),
#                         yaxis=dict(title=column_name))
# line_fig = go.Figure(data=[line_chart], layout=line_layout)
# def fun11(column_name, df, output_file):
#     """
#     Remove outliers from a numerical column of a DataFrame and save the cleaned data to a new file.

#     Args:
#     - column_name: Name of the column in the DataFrame to remove outliers.
#     - df: A pandas DataFrame containing the dataset.
#     - output_file: File path to save the cleaned data.

#     Returns:
#     - cleaned_df: A pandas DataFrame containing the cleaned data without outliers.
#     """
#     # Find rows with outliers in the specified column
#     outlier_rows = find_outliers_iqr(column_name, df)
    
#     # Remove outlier rows from the DataFrame
#     cleaned_df = df.drop(outlier_rows.index)
    
#     # Save the cleaned data to a new file
#     cleaned_df.to_csv(output_file, index=False)
    
#     return cleaned_df

# def remove_outliers_and_save(column_name,  output_file):
#     df = pd.read_csv(output_file)
#     # Find rows with outliers in the specified column
#     outlier_rows = find_outliers_iqr(column_name, df)
    
#     # Remove outlier rows from the DataFrame
#     cleaned_df = df.drop(outlier_rows.index)
    
#     # Save the cleaned data to a new file
#     cleaned_df.to_csv(output_file, index=False)
    
#     return cleaned_df
# # Save Line Chart as an Image
# line_chart_name = f"{column_name}_line_chart.png"
# pio.write_image(line_fig, line_chart_name)

# # Show the diagrams after saving
# os.system(f"start {scatter_plot_name}")
# os.system(f"start {box_plot_name}")
# os.system(f"start {histogram_name}")
# os.system(f"start {line_chart_name}")