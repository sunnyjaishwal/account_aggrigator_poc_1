"""
This is a FastAPI application that starts a Firefox browser session with a specified URL.
It uses a shell script to launch the browser session.
"""
import subprocess
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/start-session")
async def start_browser_session(request: Request):
    '''
    Start a Firefox browser session with the specified URL.
    If no URL is provided, it defaults to "https://www.google.com".
    The browser session is started using a shell script located at 
    "/app/scripts/browser_session.sh".
    The script is executed in a subprocess, and the URL is passed as an argument.
    '''
    data = await request.json()
    url = data.get("url", "https://www.google.com")

    subprocess.Popen(["/app/scripts/browser_session.sh", url])

    return {
            "message": "Firefox session started", 
            "url": "http://localhost:6080/vnc_lite.html?autoconnect=true&host=localhost&port=6080"
        }
