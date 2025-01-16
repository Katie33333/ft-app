import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_processing import read_weight_data, calculate_weekly_average, prepare_data_for_visualization

def read_and_prepare_historical_data(file_path):
    h_data = pd.read_csv(file_path)
    h_data.rename(columns={'date': 'Date (US)', 'weight': 'Weight in LB'}, inplace=True)
    h_data['Date (US)'] = pd.to_datetime(h_data['Date (US)'])
    return h_data[['Date (US)', 'Weight in LB']]

def main():
    st.title("Weekly Weight Average Tracker")

    # Load the current data
    current_data = read_weight_data('/Users/Katie/Dropbox/Fitness/Weight.csv')
    
    # Load and prepare the historical weight data
    historical_data = read_and_prepare_historical_data('/Users/Katie/Dropbox/Fitness/prepped/historical/historical_weight_data.csv')

    # Concatenate the historical data with the current data
    data = pd.concat([historical_data, current_data], ignore_index=True)

    # Exclude the outlier row
    outlier_date = pd.Timestamp('2020-08-22 06:08:16')
    data = data[data['Date (US)'] != outlier_date]

    # Calculate weekly average
    weekly_avg = calculate_weekly_average(data)

    #Calculate monthly average
    #monthly_avg = calculate_monthly_average(data)

    # Prepare data for visualization
    visualization_data = prepare_data_for_visualization(weekly_avg)
    #m_visualization_data = prepare_data_for_visualization(monthly_avg)

    # Plot the existing data using Matplotlib
    st.subheader("Existing Weekly Weight Average")
    fig1, ax1 = plt.subplots()
    ax1.plot(visualization_data['Date (US)'], visualization_data['Weight in LB'])
    ax1.set_xlabel('Date (US)')
    ax1.set_ylabel('Weight in LB')
    ax1.set_title('Weekly Weight Average')
    ax1.axhline(y=155, color='green', linestyle='--', label='Goal Weight 155')
    ax1.axvline(pd.Timestamp('2022-11-01'), color='b', linestyle='--', label='Quit Coffee Nov 2022')
    ax1.axvline(pd.Timestamp('2023-06-01'), color='purple', linestyle='--', label='Tried Intuitive Eating Jun 2023')
    ax1.axvline(pd.Timestamp('2018-09-18'), color='pink', linestyle='--', label='J')
    ax1.axvline(pd.Timestamp('2020-07-20'), color='pink', linestyle='--', label='R')   
    ax1.axvline(pd.Timestamp('2022-07-15'), color='pink', linestyle='--', label='B')
    ax1.axvline(pd.Timestamp('2024-01-05'), color='pink', linestyle='--', label='S')
    ax1.legend()
    st.pyplot(fig1)

    # Extend the date range to include future dates up to June 2025
    future_dates = pd.date_range(start='2025-01-01', end='2025-06-30', freq='W')
    future_data = pd.DataFrame({'Date (US)': future_dates})
    extended_data = pd.concat([visualization_data, future_data], ignore_index=True)

    # Create a goal line with two data points: 175 lbs on 1/1/2025 and 155 lbs on 6/30/2025
    goal_dates = [pd.Timestamp('2025-01-01'), pd.Timestamp('2025-06-30')]
    goal_weights = [175, 155]

    # Calculate the slope of the goal line
    slope = (goal_weights[1] - goal_weights[0]) / (goal_dates[1] - goal_dates[0]).days

    # Calculate the goal weight at each future date
    extended_data['Goal Weight'] = extended_data['Date (US)'].apply(
        lambda date: goal_weights[0] + slope * (date - goal_dates[0]).days if date >= goal_dates[0] else None
    )

    # Plot the new data using Matplotlib
    st.subheader("Projected Weekly Weight Average and Goal Weight")
    fig2, ax2 = plt.subplots()
    ax2.plot(extended_data['Date (US)'], extended_data['Weight in LB'], label='Weekly Average Weight')
    ax2.plot(goal_dates, goal_weights, linestyle='--', color='purple', label='Goal Weight')
    ax2.set_xlim([pd.Timestamp('2025-01-01'), pd.Timestamp('2025-06-30')])
    ax2.axhline(y=155, color='green', linestyle='--', label='Goal Weight 155')
    ax2.set_ylim(bottom=150) # Set the y-axis lower limit to 150
    ax2.set_xlabel('Date (US)')
    ax2.set_ylabel('Weight in LB')
    ax2.set_title('Weekly Weight Average and Goal Weight')
    ax2.legend()

    # Add light grey vertical lines to indicate weeks
    ax2.grid(True, which='both', axis='x', color='lightgrey', linestyle='-', linewidth=0.5)

    # Annotate the goal weight data points on a monthly basis
    monthly_dates = pd.date_range(start='2025-01-01', end='2025-06-30', freq='M')
    for date in monthly_dates:
        # Find the closest date in the extended_data DataFrame
        closest_date = extended_data['Date (US)'].iloc[(extended_data['Date (US)'] - date).abs().argsort()[:1]].values[0]
        weight = extended_data.loc[extended_data['Date (US)'] == closest_date, 'Goal Weight'].values
        if len(weight) > 0:
            ax2.annotate(f'{weight[0]:.1f}', xy=(closest_date, weight[0]), xytext=(5, 5), textcoords='offset points', color='g')

    # Annotate the most recent Weekly Average Weight
    most_recent_date = visualization_data['Date (US)'].max()
    most_recent_weight = extended_data.loc[extended_data['Date (US)'] == most_recent_date, 'Weight in LB'].values[0]
    print(f'Annotating most recent weight {most_recent_weight:.1f} on {most_recent_date}')
    ax2.annotate(f'{most_recent_weight:.1f}', xy=(most_recent_date, most_recent_weight), xytext=(5, 10),
                 textcoords='offset points', color='blue')
    #ax2.annotate(f'{most_recent_weight:.1f}', xy=(most_recent_date, most_recent_weight), xytext=(-40, 10),
                 #textcoords='offset points', arrowprops=dict(arrowstyle='->', color='blue'), color='blue')


    st.pyplot(fig2)

    print(data.head())

    # Calculate monthly average weight
    #data.set_index('Date (US)', inplace=True)
    monthly_avg = data.resample('M').mean().reset_index()

    # Plot the monthly average weight using Matplotlib
    st.subheader("Monthly Average Weight")
    fig3, ax3 = plt.subplots()
    ax3.plot(monthly_avg['Date (US)'], monthly_avg['Weight in LB'], marker='o')
    ax3.set_xlabel('Date (US)')
    ax3.set_ylabel('Weight in LB')
    ax3.set_title('Monthly Average Weight')
    ax3.axhline(y=155, color='r', linestyle='--', label='Goal Weight 155')
    ax3.legend()
    st.pyplot(fig3)

if __name__ == "__main__":
    main()