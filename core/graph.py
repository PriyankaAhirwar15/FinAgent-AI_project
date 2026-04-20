from langgraph.graph import StateGraph, END
from core.state import AgentState
from agents.supervisor import supervisor_node
from agents.market_researcher import market_researcher_node
from agents.news_analyzer import news_analyzer_node
from agents.portfolio_optimizer import portfolio_optimizer_node
from agents.risk_assessor import risk_assessor_node
from agents.report_generator import report_generator_node


def should_continue(state: AgentState) -> str:
    # If error exists and retry limit not reached, go back to supervisor
    if state.get("error") and state.get("retry_count", 0) < 3:
        return "supervisor"

    next_step = state.get("next_step", "end")

    # Safety check — if next_step is invalid, go to end
    valid_steps = ["market_researcher", "supervisor", "end"]
    if next_step not in valid_steps:
        return "end"

    return next_step


def handle_agent_error(state: AgentState) -> str:
    # If retry limit exceeded, skip to report with whatever data we have
    if state.get("retry_count", 0) >= 3:
        return "report_generator"

    # Otherwise try again from supervisor
    return "supervisor"


def build_graph():
    workflow = StateGraph(AgentState)

    # Add all agent nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("market_researcher", market_researcher_node)
    workflow.add_node("news_analyzer", news_analyzer_node)
    workflow.add_node("portfolio_optimizer", portfolio_optimizer_node)
    workflow.add_node("risk_assessor", risk_assessor_node)
    workflow.add_node("report_generator", report_generator_node)

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Supervisor decides which agent runs next
    workflow.add_conditional_edges(
        "supervisor",
        should_continue,
        {
            "market_researcher": "market_researcher",
            "end": END,
            "supervisor": "supervisor"
        }
    )

    # Main pipeline flow
    workflow.add_edge("market_researcher", "news_analyzer")
    workflow.add_edge("news_analyzer", "portfolio_optimizer")
    workflow.add_edge("portfolio_optimizer", "risk_assessor")
    workflow.add_edge("risk_assessor", "report_generator")
    workflow.add_edge("report_generator", END)

    return workflow.compile()


# Global graph instance — built once at startup
graph = build_graph()