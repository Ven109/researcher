Collecting workspace information# Article Summarizer and Report Generator

This project generates article summaries and clusters them into a structured report. It uses OpenAI's GPT-4 model to summarize articles and cluster the information into a Markdown and PDF report.

## Project Structure

```
.env
.gitignore
src/
    main.py
    my_types/
        __init__.py
        research_result.py
        search_result.py
        summary.py
    requirements.txt
    templates/
        report_template.html
```

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```sh
    pip install -r src/requirements.txt
    ```

4. **Set up the environment variables:**

    Create a .env file in the root directory with the following content:

    ```env
    OPENAPI_API_KEY=your_openai_api_key
    ```

## Usage

1. **Run the main script:**

    ```sh
    python src/main.py <search_context> <search_number>
    ```

    - `search_context`: The search context (e.g., "Obama").
    - `search_number`: The number of search results to fetch (default is 5).

2. **Output:**

    - A Markdown report will be generated as `output.md`.
    - A PDF report will be generated as `report.pdf`.

## Project Files

- **src/main.py**: The main script that orchestrates the entire process.
- **src/my_types/research_result.py**: Defines the `ResearchResult` type.
- **src/my_types/search_result.py**: Defines the `SearchResult` type.
- **src/my_types/summary.py**: Defines the `Summary` type.
- **src/templates/report_template.html**: The HTML template used for generating the PDF report.
- **src/requirements.txt**: Lists the required Python packages.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

