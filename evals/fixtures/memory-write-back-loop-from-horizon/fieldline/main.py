from google.adk.runners import Runner

from fieldline.agent import root_agent
from fieldline.services import APP_NAME, memory_service, session_service

runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service(),
                memory_service=memory_service())
