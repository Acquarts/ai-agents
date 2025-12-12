from adk import MCPTool

def load_maps_tool():
    return MCPTool.from_google_service(
        service="maps",
        version="v1"
    )
