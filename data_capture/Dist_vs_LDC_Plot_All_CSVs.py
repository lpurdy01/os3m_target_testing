import pandas as pd
import plotly.graph_objects as go
import webbrowser
import os
from glob import glob

csv_list = glob('test_runs_to_keep/*.csv')

for csv_filename in csv_list:
    # The input CSV filename.
    #csv_filename = '.\\test_runs_to_keep\\' + '5_single_test_2_20231229T211902.csv'
    #csv_filename = '8_dual_static_1_20231230T140916.csv'
    print("Processing: " + csv_filename)

    # Read the CSV file into a DataFrame.
    df = pd.read_csv(csv_filename)

    # Convert the 'Timestamp' column to datetime.
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Plot 1: Readings over Time
    fig_time_vs_reading = go.Figure(data=go.Scatter(x=df['Timestamp'], y=df['Reading'], mode='lines'))
    fig_time_vs_reading.update_layout(title='Readings over Time, File: '+csv_filename, xaxis_title='Time', yaxis_title='Reading (mm)')

    # Plot 2: Distance vs LDC Value (Scatter Plot)
    #fig_dist_vs_ldc = go.Figure(data=go.Scatter(x=df['Reading'], y=df['LDC_Val_2'], mode='markers'))
    #fig_dist_vs_ldc.update_layout(title='Distance vs LDC Value'+csv_filename, xaxis_title='Distance (mm)', yaxis_title='LDC Value')
    # Plot scatter plot of LDC_Val_2 and LDC_Val_1 vs Reading
    fig_dist_vs_ldc = go.Figure()
    fig_dist_vs_ldc.add_trace(go.Scatter(x=df['Reading'], y=df['LDC_Val_2'], mode='markers', name='LDC_Val_2'))
    fig_dist_vs_ldc.add_trace(go.Scatter(x=df['Reading'], y=df['LDC_Val_1'], mode='markers', name='LDC_Val_1'))
    fig_dist_vs_ldc.update_layout(title='Distance vs LDC Value'+csv_filename, xaxis_title='Distance (mm)', yaxis_title='LDC Value')

    # Generate HTML filenames from the CSV filename
    base_filename = os.path.splitext(csv_filename)[0]
    html_filename_time_vs_reading = base_filename + '_time_vs_reading.html'
    html_filename_dist_vs_ldc = base_filename + '_dist_vs_ldc.html'

    # Save the plots as HTML files
    fig_time_vs_reading.write_html(html_filename_time_vs_reading)
    fig_dist_vs_ldc.write_html(html_filename_dist_vs_ldc)

    # Print the HTML filenames
    print("HTML filename: " + html_filename_time_vs_reading)
    print("HTML filename: " + html_filename_dist_vs_ldc)

    # Open the HTML files in a web browser
    #webbrowser.open(html_filename_time_vs_reading)
    #webbrowser.open(html_filename_dist_vs_ldc)
