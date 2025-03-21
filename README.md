# fineancial

## Overview
This app aims to leverage AI to simplify personal finance management. The goal is to help users better understand and optimize their spending habits with **minimal** effort. Future plans include building a comprehensive finance management system with advanced AI capabilities.

## Features
- **Transaction format standardization**: Ensure the standardisation of transaction data from an arbitrary bank transaction report to a standard transaction format.
- **Transaction classification**: Automatically categorize transactions (e.g., "food", "transport", "entertainment") based on transaction descriptions.
- **Future Roadmap**:
  - Savings goal tracking.
  - Real-time anomaly detection in spending patterns.
  - Personalized financial advice using AI insights.

## Getting Started
### Prerequisites
- Python 3.8 or above.
- Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/manuelmaior29/fineancial.git
   ```
2. Navigate to the project directory:
   ```bash
   cd fineancial
   ```

## Project Structure
```
fineancial/
├── data/                # Placeholder for datasets (raw/simulated)
├── notebooks/           # Jupyter notebooks for exploratory analysis and prototyping (temporary tracking)
├── specs/               # Files representing specifications (e.g., transaction data description)
├── src/                 # Core codebase for models, preprocessing, etc.
│   ├── preprocessing/   # Scripts for data cleaning and preparation
│   ├── ...              # Other folders for modelling
│   └── utils.py         # Helper functions
├── tests/               # Unit tests for code robustness
├── ui/                  # UI-related files for future integration
├── README.md            # Project documentation
├── requirements.txt     # Dependencies for the project
└── LICENSE              # License for open-source use
```

## Contributing
Contributions are welcome! If you have ideas for new features or improvements, feel free to:
- Open an issue.
- Submit a pull request.

Please ensure your code adheres to the project structure and is well-documented.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
