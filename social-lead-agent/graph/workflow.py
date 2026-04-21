from langgraph.graph import StateGraph

from agents.intent_agent import detect_intent
from agents.rag_agent import rag_answer
from agents.lead_agent import handle_lead


def greeting_node(state):

    return {
        "response": "Hello! How can I help you today?"
    }


def intent_node(state):

    message = state["message"]

    intent = detect_intent(message)

    return {"intent": intent}


def rag_node(state):

    question = state["message"]

    answer = rag_answer(question)

    return {"response": answer}


def lead_node(state):

    return handle_lead(state)


def router(state):

    if state.get("lead_stage") and state.get("lead_stage") != "done":
        return "lead"

    intent = state.get("intent", "")

    if intent == "greeting":
        return "greeting"

    if intent == "high_intent":
        return "lead"

    return "rag"


from typing import TypedDict, Optional

class AgentState(TypedDict):
    message: str
    intent: str
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
    response: str
    lead_stage: Optional[str]

def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node(
        "intent",
        intent_node
    )

    workflow.add_node(
        "greeting",
        greeting_node
    )

    workflow.add_node(
        "rag",
        rag_node
    )

    workflow.add_node(
        "lead",
        lead_node
    )

    workflow.set_entry_point("intent")

    workflow.add_conditional_edges(
        "intent",
        router,
        {
            "greeting": "greeting",
            "rag": "rag",
            "lead": "lead"
        }
    )

    workflow.set_finish_point("greeting")
    workflow.set_finish_point("rag")
    workflow.set_finish_point("lead")

    return workflow.compile()