from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from linear_types import Issue
import os


llm = OpenAI(temperature=0.9, model_name="gpt-4")

async def issue_evaluator(issue):
    """Evaluates an issue and returns a score from 0 to 1 as to how complete it is."""
    template = """
    You have been given this task:
    {issue}

    You must evaluate the task and return a score from 0 to 1 as to how complete it is.
    ---
    Your Response:
    """

    prompt = PromptTemplate(
        input_variables=["issue"],
        template=template,
    )
    from langchain.chains import LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)
    # chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
    return await chain.arun({"issue": json.dumps(issue)})

async def issue_creator(issue: Issue, linear_client=None):
    """Creates new sub-issues for the provided issue."""
    template = """
    You have been given this task:
    {issue}

    This task has sibling tasks:
    {siblings}

    This task already has children tasks of:
    {current_child_tasks}

    Given the title and description of the task and the sibling tasks, determine what (if any) sub-tasks should be created.

    Format your response as a list of sub-tasks, each with a title and description.
    ---
    Your Response:
    """

    prompt = PromptTemplate(
       input_variables=["issue"],
       template=template,
    )

    from langchain.chains import LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)
    sibling_issues = []
    current_child_issues = []
    return await chain.arun({
        "issue": json.dumps(issue),
        "siblings": json.dumps(sibling_issues),
        "current_child_tasks": json.dumps(current_child_issues),
    })

async def GPT4(issue: Issue):
    """Uses GPT-4 to accomplish an issue. Powerful but slower. Does not use any tools."""
    template = """
    You have been given this task:
    {task}

    ---
    Your Response:

    """

    prompt = PromptTemplate(
            input_variables=["task"],
            template=template,
            )

    from langchain.chains import LLMChain

    chain = LLMChain(llm=llm, prompt=prompt)
    # chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
    return await chain.arun({"task": issue.dict(include={"title", "description"})})
