# USASpending API Analysis

This project implements a Python client for the USASpending API to analyze federal spending data and provides suggestions for API improvements.

## Project Structure

```
usa-spending-analysis/
├── docs/
│   ├── api_improvements.md       # API improvement proposals
│   └── practical_implementation.md  # Implementation details
├── src/
│   └── practical_implementation.py  # Python client implementation
├── requirements.txt              # Project dependencies
└── README.md                    # This file
```

## Setup and Installation

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the analysis script:
```bash
python src/practical_implementation.py
```

This will execute the three required queries:
1. Calculate average loan amount to Texas in FY 2019
2. Find state with highest grant value per resident in 2023
3. Determine NASA's budget resources vs new awards ratio for FY 2024

## Documentation

- See `docs/practical_implementation.md` for detailed implementation notes
- See `docs/api_improvements.md` for API improvement proposals

## Dependencies

- requests==2.31.0
- typing-extensions==4.9.0


