from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import AgentExecutor
from langchain.agents import create_openai_functions_agent
from langchain_experimental.tools import PythonREPLTool


tools = [PythonREPLTool()]


# requires OPENAI_API_KEY env var to be set
llm = ChatOpenAI(model="gpt-4", temperature=0)

db = SQLDatabase.from_uri("sqlite:///agent.db")

# ).partial(dialect=db.dialect, dbcontext=db.get_context(), top_k=3)

instructions = """You are an agent designed to write and execute python code to power a todo app.
You have access to a python REPL, which you can use to execute python code.
Connect to the SQLite database addressable at the uri "sqlite:///agent.db" 
When interacting with the database, use only valid sqlite SQL.
Read the existing schema;
then decide whether the existing tables can be used, perhaps with alteration, to accomplish your task;
then decide if any create or alter statements are necessary;
then after any alter statements run necessary inserts or selects taking into account any creates and alters.
If you get an error, debug your code and try again.
Write comments in the code and in the SQL statements to explain your thinking.
Query the database after taking action to confirm that the expected change has occurred.
Avoid having to wait on a lock on the database.

If it does not seem like you can write code to perform the task, explain why not.
"""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

insert_task = """
    <task>
    remind me to show this to alix asap
    </task>

"""

agent = create_openai_functions_agent(ChatOpenAI(temperature=0), tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "perform the following task %s" % insert_task})

agent_executor.invoke({"input": "what are all of my todos?"})
