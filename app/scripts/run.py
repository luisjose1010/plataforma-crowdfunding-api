import uvicorn
from core.config import Settings

def run():
    uvicorn.run(app=Settings.SERVER_APP, host=Settings.SERVER_HOST, port=Settings.SERVER_PORT,
                reload=Settings.SERVER_RELOAD, log_level=Settings.SERVER_LOG_LEVEL)