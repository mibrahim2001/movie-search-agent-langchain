# Movie Search Agent

A Langchain and Streamlit powered movie search agent that helps users find and get information about movies.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

Mac/Linux:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your API keys:
```
OPENAI_API_KEY=your_key_here
```

5. Run the Streamlit app:
```bash
streamlit run src/streamlit_app.py
```

## Project Structure

```
project_root/
├── src/
│   ├── agents/           # Agent-related code
│   ├── chains/           # Langchain chains
│   ├── config/           # Configuration files
│   ├── utils/            # Utility functions
│   └── streamlit_app.py  # Main Streamlit application
└── tests/                # Test directory
```

## Features

- Movie search functionality
- Detailed movie information retrieval
- Interactive Streamlit interface
- Powered by LangChain for intelligent processing

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 