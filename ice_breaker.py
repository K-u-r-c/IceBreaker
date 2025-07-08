from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from third_patries.linkedin import scrape_linkedin_profile

load_dotenv()

if __name__ == "__main__":
    summary_template = """
        Given the {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    summpary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    llm = ChatOllama(temperature=0, model="llama3")

    chain = summpary_prompt_template | llm | StrOutputParser()

    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/jakub-kurc-3565ab287/",
        mock=True,
    )

    res = chain.invoke(input={"information": linkedin_data})

    print(res)
