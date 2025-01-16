# Streamlit Fitness Tracker App

This project is a Streamlit application that visualizes fitness data from a CSV file. It calculates and displays fitness metrics in line graphs and other visualizations.

## Project Structure

```
ft-app
├── src
│   ├── app.py                # Main entry point of the Streamlit application
│   └── utils
│       └── data_processing.py # Utility functions for processing weight data
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure that the CSV file containing fitness data is located at `/Users/Katie/Dropbox/Fitness/Weight.csv`.

## Usage

To run the Streamlit application, execute the following command:
```
streamlit run src/app.py
```

## Metrics
