from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from linear_types import Issue
from linear_client import IssueInput
import os
import re
import json


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

    Format your output as a JSON array of new sub-tasks. Each subtask should have a title and a description. Make sure to wrap the resulting JSON in triple backticks.
    
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
    '''
    result = await chain.arun({
        "issue": issue.dict(),
        "siblings": json.dumps(sibling_issues),
        "current_child_tasks": json.dumps(current_child_issues),
    })
    '''

    result = """
```[
  {"title": "Understand macOS app distribution methods", "description": "Research the different ways a macOS app can be distributed, including the Mac App Store and direct downloads from a website."},
  {"title": "Study macOS app packaging and installation", "description": "Learn about the process of packaging a macOS app for distribution, including creating .dmg files or installer packages, and the user experience of installing the app."},
  {"title": "Explore frameworks and tools for simplifying app installation", "description": "Research frameworks and tools that can help create easy-to-install macOS apps, such as Electron or other app bundling tools."},
  {"title": "Analyze popular macOS apps for installation ease", "description": "Study popular macOS apps to understand what makes their installation process easy for users, and identify best practices to incorporate in your own app."},
  {"title": "Create a step-by-step guide for creating an easy-to-install macOS app", "description": "Combine the knowledge gathered from the above research to create a comprehensive guide outlining the steps for creating an easy-to-install macOS app."}
]```
    """

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
            )
        if linear_client is not None:
            await linear_client.create_issue(input)
        else:
            print("missing linear client")
        # todo: assign to bot
    return "ok"

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
