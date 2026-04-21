import streamlit as st

from graph.workflow import build_graph


st.set_page_config(
    page_title="AutoStream AI Assistant",
    page_icon="✨",
    layout="centered"
)

# Custom CSS for Premium Light UI
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header typography */
    h1 {
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 2rem;
        font-size: 3rem !important;
    }

    /* Chat message container styling */
    .stChatMessage {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 1rem;
    }
    
    /* User chat message styling */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #F8FAFC;
    }

    /* Chat input styling */
    .stChatFloatingInputContainer {
        padding-bottom: 2rem;
    }
    
    .stChatInput {
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>AutoStream AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280; margin-top: -20px; margin-bottom: 40px;'>Your lead generation assistant</p>", unsafe_allow_html=True)


# Build graph once
if "graph" not in st.session_state:

    st.session_state.graph = build_graph()


# Initialize state
if "state" not in st.session_state:

    st.session_state.state = {
        "message": "",
        "intent": "",
        "name": None,
        "email": None,
        "platform": None,
        "lead_stage": None
    }


# Chat history
if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# Show old messages
for role, msg in st.session_state.chat_history:

    st.chat_message(role).write(msg)


# Input
user_input = st.chat_input(
    "Ask something..."
)


if user_input:

    # Show user message
    st.chat_message("user").write(user_input)

    st.session_state.chat_history.append(
        ("user", user_input)
    )

    # Update message in state
    st.session_state.state["message"] = user_input

    # Run workflow
    result = st.session_state.graph.invoke(
        st.session_state.state
    )

    st.session_state.state = result

    response = result.get(
        "response",
        "Sorry, I couldn't process that."
    )

    # Show response
    st.chat_message("assistant").write(response)

    st.session_state.chat_history.append(
        ("assistant", response)
    )