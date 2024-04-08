"""
check out a branch agent-{parenthash}-{datestamp}

read index.py, write python code to do what it's intending to do, save it as index.py, check it in

push it to github
"""

import os
import subprocess
from datetime import datetime

from langchain_openai import ChatOpenAI


def name_agent():
    prefix = "agent-"
    hash = (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .decode("ascii")
        .strip()
    )
    datestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    name = prefix + hash + "-" + datestamp
    return name


def checkout_agent_branch(name):
    res = (
        subprocess.check_output(["git", "checkout", "-b", name]).decode("ascii").strip()
    )
    return res


if __name__ == "__main__":
    name = name_agent()
    res = checkout_agent_branch(name)
    # append branch name to versions.txt
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + "/versions.txt", "a") as f:
        f.write(name + "\n")
    # git commit versions.txt
    res = (
        subprocess.check_output(["git", "add", dir_path + "/versions.txt"])
        .decode("ascii")
        .strip()
    )
    res = (
        subprocess.check_output(["git", "commit", "-m", "add agent branch"])
        .decode("ascii")
        .strip()
    )

    # this function should

    # read the current agent implementation in index.py

    # use that implementation to generate a new implementation
    # on the fly, by using Langchain to access a large language model
    # that interprets the intent of the implementation in index.py

    # write the new agent implementation to index.py
    # check it in

    # Read the current agent implementation from index.py
    with open("index.py", "r") as file:
        current_implementation = file.read()

    # Initialize LangChain and OpenAI LLM
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Generate new implementation by interpreting the intent of the current implementation
    new_implementation = langchain_llm.generate(
        prompt=current_implementation,
        model_name="gpt-4",
        temperature=0,
    )

    # Write the new agent implementation to index.py
    with open("index.py", "w") as file:
        file.write(new_implementation)

    # Git add and commit the new implementation
    # subprocess.check_output(["git", "add", "index.py"])
    # subprocess.check_output(["git", "commit", "-m", "Update agent implementation"])
