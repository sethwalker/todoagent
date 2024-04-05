from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.agent_toolkits import create_sql_agent


# requires OPENAI_API_KEY env var to be set
llm = ChatOpenAI(model="gpt-4", temperature=0)

db = SQLDatabase.from_uri("sqlite:///agent.db")

# ).partial(dialect=db.dialect, dbcontext=db.get_context(), top_k=3)

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

agent_executor.invoke(
    """
    You have permission to create and alter tables.
    Execute any necessary SQL to accomplish this task in the context of a todo app,
    including creating or altering tables.
    Break queries down into subqueries if appropriate.
    Add comments to all queries to explain what they are doing.
    Write and execute a final query that confirms that the expected change has happened.

    <task>
    remind me to show this to alix asap
    </task>
    """
)

output_parser = StrOutputParser()

exit()

chain = prompt | llm | output_parser

chain.get_prompts()[0].pretty_print()

# todo: combine this with the following query or predetermine the schema. Currently bombs on the first run
# through if the generated query doesn't match the generated schema
res = chain.invoke(
    {"query": "create a table to store todo items if it does not already exist"}
)
print("schema: ", res)

# db.run(res)

res = chain.invoke({"query": "remind me to buy the milk before next tuesday"})
print("insert: ", res)

db.run(res)

res = chain.invoke({"query": "what's on my todo list?"})

todos = db.run(res)
print(todos)
