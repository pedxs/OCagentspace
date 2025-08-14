import vertexai
from vertexai import agent_engines

# --- Your Configuration ---
PROJECT_ID = "cj-agentspace"
LOCATION = "us-central1"
AGENT_RESOURCE_NAME = "projects/291368973536/locations/us-central1/reasoningEngines/4193897988151574528"
# --- End Configuration ---

# Initialize connection to Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Get a reference to your deployed agent
remote_agent = agent_engines.get(AGENT_RESOURCE_NAME)
print(f"Successfully connected to agent:\n{AGENT_RESOURCE_NAME}")

# Start a conversation
print("\nSending 'hi there' to the agent...")
session = remote_agent.create_session(user_id="test_user")
print(f"Created session: {session['id']}")

print("\n--- Agent's Live Response ---")
for event in remote_agent.stream_query(
    user_id="test_user",
    session_id=session["id"],
    message="hi there"
):
    if "content" in event:
        print(event["content"], end="")
print("\n--------------------------")
