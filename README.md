# ☀️ Suntrack — PV Dashboard

A real-time PV monitoring dashboard built with Python and Streamlit.

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/talha-sueluen/suntrack.git
   cd suntrack
```

2. Install dependencies:
```bash
   pip install requests python-dotenv streamlit pandas plotly
```

3. Create a `.env` file in the root directory:
```bash
PV_API_KEY=your_api_key_here
PV_API_URL=https://jupyterhub-wi.rz.fh-ingolstadt.de:8443/data
```

## Usage

```bash
python -m streamlit run frontend/dashboard.py
```

> ⚠️ API is only accessible on the THI campus network (Eduroam) or VPN.

## Project Structure
```
suntrack/
├── backend/
│   ├── fetcher.py       # Fetches PV data from API
│   ├── cleaner.py       # Cleans raw data
│   ├── storage.py       # Saves data to CSV
│   ├── calculator.py    # Calculates metrics
│   └── logger.py        # Logging configuration
├── frontend/
│   └── dashboard.py     # Streamlit dashboard
├── tests/               # Unit and integration tests
├── .env                 # API credentials (not tracked)
├── Dockerfile
└── pyproject.toml
```

## Development

This project was developed by Ibrahim Talha Sülün.