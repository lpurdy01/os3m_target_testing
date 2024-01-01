import pandas as pd
import numpy as np
from scipy import stats
from glob import glob


def calculate_outliers(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound


def process_file(filename):
    df = pd.read_csv(filename)
    sectioned_filename = filename.split('\\')[-1].split('_')
    summary = {
        'target': sectioned_filename[0],
        'num_ldcs': sectioned_filename[1],
        'test_run': sectioned_filename[3],
        'test_distance': df['Reading'].mode()[0],  # Assuming mode as the test distance
    }

    for col in ['LDC_Val_1', 'LDC_Val_2']:
        data = df[col]
        summary[f'{col}_mean'] = data.mean()
        summary[f'{col}_median'] = data.median()
        summary[f'{col}_mode'] = data.mode()[0] if not data.mode().empty else 'N/A'
        summary[f'{col}_stdev'] = data.std()
        lower_outlier, upper_outlier = calculate_outliers(data)
        summary[f'{col}_lower_outlier'] = lower_outlier
        summary[f'{col}_upper_outlier'] = upper_outlier

    return summary


def main():
    files = glob('test_runs_to_keep/*_static_*.csv')
    summaries = [process_file(file) for file in files]

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv('summary_static_tests.csv', index=False)
    print("Summary CSV created: summary_static_tests.csv")


if __name__ == "__main__":
    main()
