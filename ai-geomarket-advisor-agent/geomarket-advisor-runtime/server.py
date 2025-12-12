from fastapi import FastAPI
from agent import build_business_agent

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.genai import types

APP_NAME = "geomarket-advisor"

app = FastAPI()

agent = build_business_agent()
session_service = InMemorySessionService()
runner = Runner(app_name=APP_NAME, agent=agent, session_service=session_service)

@app.post("/run")
async def run_agent(payload: dict):
    query = payload.get("query", "").strip()
    if not query:
        return {"response": "Empty query."}

    user_id = payload.get("user_id", "local-user")
    session_id = payload.get("session_id", "local-session")

    try:
        await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    except AlreadyExistsError:
        pass

    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_text = None
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_text = event.content.parts[0].text
            break

    return {"response": final_text or "No final response captured."}
