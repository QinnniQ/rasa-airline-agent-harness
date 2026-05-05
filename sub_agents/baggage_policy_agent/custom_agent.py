from rasa.agents.protocol.mcp.mcp_open_agent import MCPOpenAgent


class BaggagePolicyAgent(MCPOpenAgent):
    """Custom baggage policy ReAct sub-agent.

    Kept intentionally minimal for now. The sub-agent behavior is controlled
    through the prompt template and MCP tool filtering in config.yml.
    """