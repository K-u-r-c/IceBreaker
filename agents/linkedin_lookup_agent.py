from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from dotenv import load_dotenv
from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    # llm = ChatOllama(temperature=0, model="llama3")

    template = """
        Given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page. 
        Your answer should contain ONLY the complete LinkedIn profile URL starting with https://linkedin.com/in/ or https://www.linkedin.com/in/
        Do not include any other text, explanations, or markdown formatting - just the URL.
        The URL must be a direct link to a specific person's profile, not a search results page or directory.
    """
    
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    
    tools_for_agent = [
        Tool(
            name="Crawl Google for Linkedin profile page",
            func=get_profile_url_tavily,
            description="Useful for when you need to get Linkedin profile page URL"
        )
    ]
    
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    
    linkedin_profile_url = result["output"]
    return linkedin_profile_url
