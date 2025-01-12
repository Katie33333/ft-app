# Streamlit Weight Tracker

This project is a Streamlit application that visualizes weight data from a CSV file. It calculates and displays the weekly weight average in a line graph.

## Project Structure

```
streamlit-app
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

3. Ensure that the CSV file containing weight data is located at `/Users/Katie/Dropbox/Fitness/Weight.csv`.

## Usage

To run the Streamlit application, execute the following command:
```
streamlit run src/app.py
```

## Metrics

The application calculates the weekly weight average and displays it in a line graph, allowing users to track their weight trends over time.