# Chelsea District Finder

This Flask web application helps residents of Chelsea find their district information, including their ward, precinct, polling location, and current representatives. It provides information about both district-specific and at-large representatives.

## Features

- Address lookup to find district information
- Display of current district representatives
- Information about at-large representatives
- Polling location information
- School committee information

## Requirements

- Python 3.7+
- Required Python packages (install using `pip install -r requirements.txt`):
  - Flask
  - pandas
  - Other dependencies listed in requirements.txt

## Setup

1. Clone this repository
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure you're in the project directory and your virtual environment is activated
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Enter your Chelsea address in the search box
2. The application will display:
   - Your district number
   - Ward and precinct information
   - Polling location
   - Current district representatives
   - At-large representatives
   - School committee members

## Data Sources

- Address and district data is maintained in `addresses_district.csv`
- Representative information is managed through the `city_councilor_info.py` module

## Notes

- The application uses address normalization to handle various address formats
- Make sure the `addresses_district.csv` file is present in the root directory
- The application runs in debug mode by default for development purposes 