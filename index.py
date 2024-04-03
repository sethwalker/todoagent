from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# requires OPENAI_API_KEY env var to be set
llm = ChatOpenAI()

db = SQLDatabase.from_uri("sqlite:///agent.db")

system = """You are a frontend to a todo app
You will receive messages from a user requesting to add, update, or remove
todo items from their various lists, and to retrieve todo items.

You are a {dialect} SQL expert. Given an input question, creat a syntactically correct {dialect} query to run.

Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

The existing database contains the following context:
<context>
{dbcontext}
</context>

Annotate the SQL with {dialect} valid comments to explain what you're doing.

Output the final query SQL only."""
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{query}")]
).partial(dialect=db.dialect, dbcontext=db.get_context(), top_k=3)

output_parser = StrOutputParser()

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
