def read_weight_data(file_path):
    import pandas as pd
    data = pd.read_csv(file_path)
    data['Date (US)'] = pd.to_datetime(data['Date (US)'])
    return data

def calculate_weekly_average(data):
    data.set_index('Date (US)', inplace=True)
    weekly_average = data.resample('W').mean()
    return weekly_average

def prepare_data_for_visualization(weekly_average):
    return weekly_average.reset_index()