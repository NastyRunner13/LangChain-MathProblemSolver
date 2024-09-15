# Streamlit Math Problem Solver

This is a Streamlit-based web application that serves as a Text to Math Problem Solver and Data Science Assistant. It uses the Groq API and LangChain to provide intelligent responses to mathematical questions and general queries.

## Features

- Solves mathematical problems
- Provides reasoning for complex questions
- Accesses Wikipedia for additional information
- Uses a chat-like interface for easy interaction

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- Pip (Python package manager)
- A Groq API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/NastyRunner13/LangChain-MathProblemSolver.git
   cd LangChain-MathProblemSolver
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter your Groq API key in the sidebar.

4. Type your mathematical question or general query in the text area.

5. Click "Find My Answer" to get a response.

## Configuration

The application uses the Mixtral 8x7B model from Groq. If you want to use a different model, you can modify the `model` parameter in the `ChatGroq` initialization:

```python
llm = ChatGroq(model="your-preferred-model", api_key=groq_api_key)
```

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## Contact

If you have any questions or feedback, please open an issue in this repository.
