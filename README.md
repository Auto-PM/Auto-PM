# AutoPM: AI-Powered Task Management for Linear.app

AutoPM is a ChatGPT plugin that seamlessly integrates AI and agents into your existing project management workflow. It provides a conversational interface to Linear.app, allowing you to manage tasks effortlessly. With the power of langchain tools and OpenAI plugins, AutoPM streamlines your task management process, improving productivity and collaboration within your team.

## Features

- AI-driven task management for Linear.app projects
- Conversational interface for easy interaction
- Leverages langchain tools and OpenAI plugins for powerful task automation
- Enhances productivity and collaboration in project management workflows

## Requirements

- Python (3.11+)

## Installation

To get started with AutoPM, please ensure you have the latest version of Python installed. 

### Set up virtualenv:
```shell
$ make venv
````
This command will also install all requirements.

### Activate virtual environement:
```shell
$ source venv/bin/activate
````

### Copy example.env, name it .env, and add your API keys
It should be named ".env" and look something like this:
```
LINEAR_API_KEY = lin_api_abc123
OPENAI_API_KEY = sk-abc123
LINEAR_TEAM_NAME="Example Name"
SERPAPI_API_KEY=abc123
```

Make sure that you use the exact name of your project or it will not work!

### Start the Server
```shell
$ uvicorn main:app --reload
````

You should now be up and running! To start using the ChatGPT plugin simply paste 'http://127.0.0.1:8000/' as the plugin link when adding a local plugin to ChatGPT.



## How it Works

AutoPM connects to your Linear.app project and provides a conversational interface for managing tasks. This intuitive interface allows you to easily interact with your project and team members. The plugin leverages langchain tools and OpenAI plugins to assist in task completion, boosting efficiency in your project management workflow.

## Examples

- Assign tasks to team members through natural language commands
- Get quick updates on project status by asking the AI agent
- Use langchain tools to automate repetitive tasks, such as updating deadlines or prioritizing issues

## Limitations & Future Improvements

AutoPM is constantly being updated and improved. While it's already a powerful tool, we're actively working on making it even better. If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

