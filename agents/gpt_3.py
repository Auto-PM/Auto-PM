from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os


llm = OpenAI(temperature=0.9, model_name="gpt-3.5-turbo")


async def gpt_3_agent(issue):
    """Uses GPT-3.5 to accomplish an issue. Fast but leess powerful. Does not use any tools."""
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
    print(" LLM ARUN START")
    r =  await chain.arun({"task": issue})
    print(" LLM ARUN DONE")
    return r
