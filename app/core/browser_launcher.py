"""
This module provides a function to launch a web browser with a specified URL.
It uses the `subprocess` module to call the browser executable with the URL as an argument.
"""
import subprocess

def launch_browser(url:str):
    '''Launches the default web browser with the given URL.
    Args:
        url (str): The URL to open in the browser.
    '''
    subprocess.Popen([
        "firefox",  # Change this to "chrome" or "firefox" if needed
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--start-fullscreen",
        url
    ])
