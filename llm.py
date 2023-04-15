from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0.9)

template = """
    You are an expert project manager assigned to break projects down into manageable chunks. If the task is already small enough you do not need to break it down further. use your discretion as an expert project manager to determine what is  valid task and what is too large and must be broken down. 


    Break the following task down into a list of steps:
    {task}

    ---
    Steps:


    """


prompt = PromptTemplate(
    input_variables=["task"],
    template=template,
)

from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)


print(chain.run("Water my plant"))
