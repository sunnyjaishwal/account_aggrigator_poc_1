"""
This module provides a function to launch a web browser with a specified URL.
It uses the `subprocess` module to call the browser executable with the URL as an argument.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from core.browser_launcher import launch_browser

router = APIRouter()

class SessionRequest(BaseModel):
    '''
    Request model for starting a session.
    Attributes:
        url (str): The URL to open in the browser.
    '''
    url: str

@router.post("/start-session")
async def start_session(req:SessionRequest):
    '''
    Starts a session by launching a web browser with the specified URL.
    Args:
        req (SessionRequest): The request object containing the URL to open.
        Returns:
            dict: A dictionary containing the status of the session launch.
    '''
    launch_browser(req.url)
    return {"status":"Launched", "url":req.url}
