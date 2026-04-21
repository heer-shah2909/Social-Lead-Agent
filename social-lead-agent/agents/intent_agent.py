from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from config import MODEL_NAME


llm = ChatGroq(
    model_name=MODEL_NAME,
    temperature=0
)


prompt = PromptTemplate(
    input_variables=["message"],
    template="""
Classify the intent of the user message strictly into one of these exact labels:
- greeting: Simple hellos, hi, good morning, etc.
- product_inquiry: Questions about what the product is, features, pricing, etc.
- high_intent: The user is explicitly expressing a desire to buy, try, purchase, or start a plan (e.g., "I want to try the Pro plan", "I want to try the Basic plan", "Let's start", "Sign me up").

User message:
{message}

You must return ONLY the exact label name (greeting, product_inquiry, or high_intent) and nothing else. No punctuation, no explanation.
"""
)


def detect_intent(message):

    chain = prompt | llm

    result = chain.invoke(
        {"message": message}
    )

    label = result.content.strip().lower()
    
    if "greeting" in label: return "greeting"
    if "high_intent" in label: return "high_intent"
    return "product_inquiry"