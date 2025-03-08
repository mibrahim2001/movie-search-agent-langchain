# Movie Search Agent

A Langchain and Streamlit powered movie search agent that helps users find and get information about movies.

![Movie Search Agent Screenshot](docs/images/app-demo.gif)

## Features

- Movie search functionality with detailed information retrieval
- Integration with Google Search and YouTube for comprehensive results
- Real-time streaming responses
- Interactive Streamlit interface
- Powered by LangChain and OpenAI for intelligent processing

## Architecture

The application follows a modular architecture:

```ascii
┌─────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                 │     │                   │     │                   │
│  Streamlit UI   │────▶│  MovieSearchAgent │────▶│  Search Tools     │
│                 │     │                   │     │                   │
└─────────────────┘     └───────────────────┘     └───────────────────┘
                               │                          │
                               ▼                          ▼
                        ┌─────────────┐           ┌─────────────────┐
                        │             │           │                 │
                        │  LLM Model  │           │  External APIs  │
                        │             │           │                 │
                        └─────────────┘           └─────────────────┘
```

- **Streamlit UI**: Provides the user interface for interacting with the agent
- **MovieSearchAgent**: Core component that processes user queries and coordinates responses
- **Search Tools**: Collection of tools for retrieving information from various sources
- **LLM Model**: Language model that powers the agent's understanding and response generation
- **External APIs**: Google Search and YouTube APIs for retrieving movie information

## Setup

### Prerequisites

- Python 3.8 or higher
- API keys for:
  - OpenAI or OpenRouter (for the language model)
  - Google Search API
  - Google Custom Search Engine ID

### Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/movie-search-agent.git
  cd movie-search-agent
  ```

2. Create a virtual environment:
  ```bash
  python -m venv .venv
  ```

3. Activate the virtual environment:

  Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

  Mac/Linux:
  ```bash
  source .venv/bin/activate
  ```

4. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

5. Create a `.env` file and add your API keys, you can find required keys in the .env.example file in the root of the project.
  Note: Google Search API and Custom Search Engine ID are optional, you can use DuckDuckGo as a search engine.

### Running the Application

Start the Streamlit app:
```bash
streamlit run src/streamlit.py
```

The application will be available at http://localhost:8501

## Usage Examples

### Finding Movie Information

1. Enter a query like "Tell me about Inception"
2. The agent will search for information about the movie and return details including:
   - Release date
   - Director and cast
   - IMDB rating
   - Genre
   - Plot summary
   - Trailer link

### Comparing Movies

1. Enter a query like "Compare The Matrix and Inception"
2. The agent will search for information about both movies and provide a comparison

### Finding Movies by Criteria

1. Enter a query like "What are some good sci-fi movies from the 90s?"
2. The agent will search for and recommend movies matching your criteria

## Challenges Faced

- **Incomplete Search Results**: Search queries sometimes returned incomplete information (e.g., missing movie ratings), requiring prompt engineering to get more detailed information.
- **Tool Naming Conventions**: Resolved issues with function calling by implementing proper naming conventions for tools to ensure correct invocation and prompt engineering.
- **StreamlitCallBackHandler Compatibility**: Overcame integration challenges between the latest LangChain agent implementation and Streamlit's callback handler by implementing a custom solution based on community contributions. [Github Issue](https://github.com/langchain-ai/langgraph/issues/101)
- **API Rate Limiting**: Faced rate limiting issues with the APIs, so implemented multiple providers e.g Google Search and DuckDuckGo.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.