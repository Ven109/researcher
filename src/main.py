import argparse
import getpass
import os
from textwrap import dedent

from jinja2 import Environment, FileSystemLoader
from langchain_community.document_loaders import PlaywrightURLLoader
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI
from my_types import SearchResult, Summary, ResearchResult
from weasyprint import HTML


def ensure_api_key() -> None:
    """Ensure that the OPENAI_API_KEY environment variable is set."""
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")


def create_llm() -> ChatOpenAI:
    """Create and return a ChatOpenAI instance."""
    return ChatOpenAI(model="gpt-4o-mini")


def create_summary_prompt(
    content: str, search_context: str = "Obama"
) -> list[tuple[str, str]]:
    """Create the prompt messages for summarizing an article."""
    system_message = dedent(f"""\
        You are a helpful assistant that writes summaries of articles about {search_context}.
        If the article is not relevant, please skip it.
        In any case, provide information on whether the article was skipped or not.
    """)
    return [
        ("system", system_message),
        ("human", content),
    ]


def fetch_information(
    result: SearchResult, llm_output, search_context: str = "Obama"
) -> str | None:
    """
    Load a webpage, create a summary prompt and invoke the LLM.
    Return the summary text (with source) or None if the article is skipped.
    """
    loader = PlaywrightURLLoader([result["link"]])
    docs = loader.load()
    if not docs:
        return None

    prompt = create_summary_prompt(docs[0].page_content, search_context)
    output = llm_output.invoke(prompt)
    if getattr(output, "skipped", False):
        return None

    return f"{output.summary}\nSource: {result['link']}"


def create_blog_post(summaries: list[str], llm_research) -> BaseMessage:
    """
    Cluster the list of article summaries by invoking the LLM.
    Returns a structured blog post object.
    """
    summaries_text = "\n".join(summaries)
    system_message = dedent("""\
        You are a helpful assistant that clusters the provided information.
        You will receive a list of summaries of articles about Obama.
        Please cluster the information: add a title and then a bullet list of the relevant key points for each cluster.
        Also, include behind each bullet point the source of the information and the link of the source.
    """)
    messages = [
        ("system", system_message),
        ("human", summaries_text),
    ]
    return llm_research.invoke(messages)


def generate_pdf_report(
    output_filename: str, template_filename: str, context: dict
) -> None:
    """
    Render a Jinja2 template with the given context and generate a PDF report.
    """
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_filename)
    html_content = template.render(context)
    HTML(string=html_content).write_pdf(output_filename)
    print(f"PDF report generated: {output_filename}")


def write_markdown_report(blog_post: ResearchResult, output_filepath: str) -> None:
    """
    Write the clustered blog post to a Markdown file.
    """
    with open(output_filepath, "w") as md_file:
        for cluster in blog_post.clusters:
            md_file.write(f"# {cluster.cluster_title}\n")
            for key_point in cluster.key_points:
                md_file.write(
                    f"* {key_point.value}\n  [{key_point.source}]({key_point.source_link})\n"
                )
            md_file.write("\n")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate article summaries and cluster them into a report."
    )
    parser.add_argument(
        "search_context", type=str, help="The search context (e.g., Obama)"
    )
    parser.add_argument(
        "search_number",
        type=int,
        help="The number of search results to fetch",
        default=5,
    )
    return parser.parse_args()


def main() -> None:
    ensure_api_key()
    args = parse_args()
    search_context = args.search_context
    search_number = args.search_number

    # Set up LLMs and search tool
    llm = create_llm()
    llm_output = llm.with_structured_output(Summary)
    llm_research = llm.with_structured_output(ResearchResult)
    search_tool = DuckDuckGoSearchResults(
        output_format="list", num_results=search_number
    )

    search_results: list[SearchResult] = search_tool.invoke(search_context)
    summaries: list[str] = []

    for result in search_results:
        summary = fetch_information(result, llm_output, search_context)
        if summary:
            summaries.append(summary)

    if not summaries:
        print("No valid summaries generated.")
        return

    blog_post = create_blog_post(summaries, llm_research)
    write_markdown_report(blog_post, "output.md")
    generate_pdf_report(
        "report.pdf", "./templates/report_template.html", blog_post.model_dump()
    )


if __name__ == "__main__":
    main()
