# from mitmproxy import http
# import json
# import os

# cookie_log_path = "/app/logs/cookies.json"

# def request(flow: http.HTTPFlow):
#     cookies = flow.request.cookies.fields
#     if cookies:
#         os.makedirs(os.path.dirname(cookie_log_path), exist_ok=True)
#         with open(cookie_log_path, "a") as f:
#             json.dump({flow.request.host: cookies}, f)
#             f.write("\n")


from mitmproxy import http
import json
import os

LOG_FILE = "/app/logs/network_log.json"

# Ensure log file directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def is_static_file(flow: http.HTTPFlow) -> bool:
    static_exts = (".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot", ".otf", ".map")
    return flow.request.path.lower().endswith(static_exts)

def log_flow(flow: http.HTTPFlow):
    entry = {
        "method": flow.request.method,
        "url": flow.request.pretty_url,
        "request_headers": dict(flow.request.headers),
        "request_body": None,
        "response_code": flow.response.status_code if flow.response else None,
        "response_headers": dict(flow.response.headers) if flow.response else {},
        "response_body": None
    }

    # Log JSON request body
    if "application/json" in flow.request.headers.get("content-type", ""):
        try:
            entry["request_body"] = json.loads(flow.request.get_text())
        except Exception:
            entry["request_body"] = flow.request.get_text()

    # Log JSON response body
    if flow.response and "application/json" in flow.response.headers.get("content-type", ""):
        try:
            entry["response_body"] = json.loads(flow.response.get_text())
        except Exception:
            entry["response_body"] = flow.response.get_text()

    # Append to file
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, indent=2) + ",\n")

def request(flow: http.HTTPFlow):
    if is_static_file(flow):
        return
    if flow.request.method in ["POST", "GET"]:
        log_flow(flow)

def response(flow: http.HTTPFlow):
    if is_static_file(flow):
        return
    if flow.request.method in ["POST", "GET"]:
        log_flow(flow)
