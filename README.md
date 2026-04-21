# AutoStream AI Assistant

An AI-powered conversational agent designed to guide users from initial inquiry to structured lead capture. Built with Streamlit, LangGraph, and Groq.

## 1. How to run the project locally

Follow these steps to run the application on your local machine:

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd social-lead-agent
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

## 2. Architecture Explanation

**Why LangGraph was chosen:**
LangGraph was chosen over alternative frameworks because it allows us to represent the multi-turn conversational AI logic as a highly structured, stateful graph. This is specifically beneficial for lead generation, where the bot must seamlessly transition between distinct phases—like unstructured pleasantries (greeting), exploratory QA (RAG), and a highly rigid data collection funnel (lead capture). LangGraph makes these transitions securely controllable through strict conditional edges and router logic. This mitigates LLM hallucinations disrupting the flow and ensures a deterministic, step-by-step user journey until the lead information is completely captured.

**How state is managed:**
The conversation and operational context are managed centrally using LangGraph's `StateGraph` construct, governed by the `AgentState` TypedDict. This centralized context holds the current user message, the interpreted intent, progression of the `lead_stage`, generated responses, and the aggregated lead data (name, email, platform). As the graph transitions from one node to another (e.g., from `intent_node` to `lead_node`), the active node accesses this state, processes it, and returns a dictionary of updates which LangGraph merges. On the frontend, Streamlit caches this evolving graph state inside `st.session_state` to persist the conversational context across UI reruns.

## 3. WhatsApp Deployment Question

**How to integrate this agent with WhatsApp using Webhooks:**

To deploy this agent on WhatsApp, we would integrate it via the official Meta WhatsApp Business API using Webhooks. 

1. **Webhook Endpoint:** We would deploy a web framework service (e.g., FastAPI or Flask) to serve as our webhook listener. Meta's API would be configured to send a `POST` request to this endpoint every time a user sends a message.
2. **State Persistence:** Since webhooks are stateless server events, we'd replace the Streamlit session state with a persistent session store (like Redis or PostgreSQL). The user's WhatsApp phone number (extracted from the webhook payload) would act as the primary session key.
3. **Graph Invocation:** When a message comes in, our backend retrieves the user's current `AgentState` from the database. We would then pass the incoming text to our compiled LangGraph (`graph.invoke(state)`).
4. **Sending the Response:** Once LangGraph finishes processing and returns an updated state with a `response`, our webhook handling service would issue a synchronous `POST` request back to the WhatsApp API (`/messages` endpoint), delivering the AI's reply to the specific user's phone number.
5. **State Update:** Finally, the updated `AgentState` (including new lead extraction progress) is saved back to our database to await the next webhook event.
