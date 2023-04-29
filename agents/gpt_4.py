from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from linear_types import Issue
from linear_client import IssueInput
import re
import json


llm = OpenAI(temperature=0.0, model_name="gpt-4")

async def issue_evaluator(issue: Issue, **kwargs):
    """Evaluates an issue and returns whether it is done or not."""
    template = """
    You have been given this task:
    {issue}

    You must evaluate the task and return either "YES" if it is to be considered done, or "NO" if it is not.
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
    return await chain.arun({"issue": issue.dict()})

async def issue_creator(issue: Issue, linear_client=None, **kwargs):
    """Creates new sub-issues for the provided issue."""
    template = """
    You have been given this task:
    {issue}

    This task has sibling tasks:
    {siblings}

    This task already has children tasks of:
    {current_child_tasks}

    Given the title and description of the task and the sibling tasks, determine what (if any)
    sub-tasks should be created.

    Format your output as a JSON array of new sub-tasks. Each subtask should have a title and a description.
    Make sure to wrap the resulting JSON in triple backticks.
    
    For example:
    ```[{{"title": "My Title", "description": "My Description"}}]```

    ---
    Your Response:
    """

    prompt = PromptTemplate(
       input_variables=["issue", "siblings", "current_child_tasks"],
       template=template,
    )

    from langchain.chains import LLMChain
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    sibling_issues = []
    current_child_issues = []

    # result = canned_result
    result = await chain.arun({
        "issue": issue.dict(),
        "siblings": json.dumps(sibling_issues),
        "current_child_tasks": json.dumps(current_child_issues),
    })

    regexp = re.compile(r"```(.*)```", re.DOTALL)
    extracted = regexp.search(result).group(1)
    parsed = json.loads(extracted)

    print(extracted)
    print(parsed)
    parent_issue = issue

    for issue in parsed:
        input = IssueInput(
                title=issue["title"],
                description=issue["description"],
                parent_id=parent_issue.id,
                state='backlog',
                # assignee_id=bot_user_id,
            )
        if linear_client is not None:
            await linear_client.create_issue(input)
        else:
            print("missing linear client")
        # todo: assign to bot
    return parent_issue.description

async def GPT4(issue: Issue, **kwargs):
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
