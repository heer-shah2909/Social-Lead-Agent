from tools.lead_capture import mock_lead_capture


def handle_lead(state):

    message = state["message"]
    stage = state.get("lead_stage")

    if not stage:
        return {"response": "May I have your name?", "lead_stage": "name"}

    if stage == "name":
        return {"name": message, "response": "Please provide your email.", "lead_stage": "email"}

    if stage == "email":
        return {"email": message, "response": "Which platform do you create content on?", "lead_stage": "platform"}

    if stage == "platform":
        mock_lead_capture(
            state.get("name"),
            state.get("email"),
            message
        )
        return {"platform": message, "response": "Thank you! Your details have been captured.", "lead_stage": "done"}

    return {"response": "Lead already captured."}