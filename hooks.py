from agents import RunHooks, RunContextWrapper, Agent

class TestHooks(RunHooks):
    def __init__(self):
        super().__init__()

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        print(f"{agent.name} is processing your request. Thanks for your patience!")
        print("-------------------------------------------------------------------")
        
    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: any) -> None:
        print(f"{agent.name} has completed processing your request. Here is the Result:\n{output}")
        print("-------------------------------------------------------------------")
        
    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool) -> None:
        print(f"{agent.name} is using {tool.name} to process your request. Please wait while we assist you!")
        print("-------------------------------------------------------------------")
        
    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool, result: str) -> None:
        print(f"{agent.name} has finished using {tool.name}. Here is the result: {result}")
        print("-------------------------------------------------------------------")
        
    async def on_handoff(self, context: RunContextWrapper, from_agent, to_agent) -> None:
        print(f"{from_agent.name} ➡️ {to_agent.name}: Handoff in progress. Please wait...")
        print("-------------------------------------------------------------------")
        