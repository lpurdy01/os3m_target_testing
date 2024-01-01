import pandas as pd
import plotly.graph_objects as go
import webbrowser
import os

# The input CSV filename.
csv_filename = '20231228T005051.csv'

# Read the CSV file into a DataFrame.
df = pd.read_csv(csv_filename)

# Convert the 'Timestamp' column to datetime.
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create a line plot of the readings over time.
fig = go.Figure(data=go.Scatter(x=df['Timestamp'], y=df['Reading'], mode='lines'))

# Set the title and labels.
fig.update_layout(title='Readings over Time', xaxis_title='Time', yaxis_title='Reading (mm)')

# Generate the HTML filename from the CSV filename.
html_filename = os.path.splitext(csv_filename)[0] + '.html'

# Save the plot as an HTML file.
fig.write_html(html_filename)

# Open the HTML file in a web browser.
webbrowser.open(html_filename)