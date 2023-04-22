class AgentRouter:
    """
    A class to route input strings to specified agent functions.

    Attributes:
        agents (dict): A dictionary containing agent functions with their names as keys.

    Example usage:

        def agent1(input_str):
            return input_str.upper()

        def agent2(input_str):
            return input_str.lower()

        agents = [agent1, agent2]
        router = AgentRouter(agents)

        input_str = "Hello, World!"
        print(router.run(input_str, "agent1"))  # Output: HELLO, WORLD!
        print(router.run(input_str, "agent2"))  # Output: hello, world!
    """

    def __init__(self, agents):
        """
        Initializes the AgentRouter with a list of agent functions.

        Args:
            agents (list): A list of functions that expect a string input and have a string output.
        """
        self.agents = {}
        for agent in agents:
            self.agents[agent.__name__] = agent

    def run(self, input_str, agent_name):
        """
        Takes an input string and an agent name, and runs the input string through the chosen agent function.

        Args:
            input_str (str): The input string to be processed.
            agent_name (str): The name of the agent function to process the input string.

        Returns:
            str: The output of the chosen agent function.

        Raises:
            ValueError: If no agent is found with the given name.
        """
        if agent_name in self.agents:
            return self.agents[agent_name](input_str)
        else:
            raise ValueError(f"No agent found with name: {agent_name}")
