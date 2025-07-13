from typing import Tuple
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_patries.linkedin import scrape_linkedin_profile
from output_parsers import Summary, summary_parser


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_url, mock=False
    )

    summary_template = """
        Given the {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        \n{format_instructions}
    """

    summpary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    # llm = ChatOllama(temperature=0, model="llama3")

    chain = summpary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("photoUrl")


if __name__ == "__main__":
    load_dotenv()

    ice_break_with("Jakub Kurc")
