from langgraph.graph import StateGraph
from news_agent.agents.state import NewsState
from news_agent.agents.nodes import (
    fetch_node,
    filter_node,
    rank_node,
    summarize_node,
    critic_node,
    notify_node,
    memory_node
)

def build_graph():
    builder = StateGraph(NewsState)

    builder.add_node("fetch", fetch_node)
    builder.add_node("filter", filter_node)
    builder.add_node("rank", rank_node)
    builder.add_node("summarize", summarize_node)
    builder.add_node("critic", critic_node)
    builder.add_node("notify", notify_node)
    builder.add_node("memory", memory_node)

    builder.set_entry_point("fetch")

    builder.add_edge("fetch", "filter")
    builder.add_edge("filter", "rank")
    builder.add_edge("rank", "summarize")
    builder.add_edge("summarize", "critic")
    builder.add_edge("critic", "memory")
    builder.add_edge("memory", "notify")

    return builder.compile()