# OC Agent

This project implements an AI-powered agent for summarizing OC Morning Call meetings.

## Overview

The OC Agent is designed to take a meeting transcript as input and generate a summary in Thai. The summary is structured around 6 main topics to provide a clear and concise overview of the meeting.

## Agent Details

The key features of the OC Agent include:

| Feature            | Description             |
| ------------------ | ----------------------- |
| _Interaction Type_ | Conversational          |
| _Complexity_       | Basic                   |
| _Agent Type_       | Single Agent            |
| _Components_       | None                    |
| _Vertical_         | Internal Communications |

### Agent Architecture

The agent is a simple agent that uses the Gemini model to generate a summary based on a given transcript. It does not use any external tools.

### Key Features

- **Meeting Summary:**
  - Generates a summary of a meeting transcript in Thai.
  - The summary is structured into 6 main topics.
- **Input Prompt:**
  - The agent first prompts the user to upload a meeting transcript.

## Setup and Installations

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- Google ADK SDK (installed via Poetry)
- Google Cloud Project (for Vertex AI Gemini integration)

### Installation
1.  **Prerequisites:**

    For the Agent Engine deployment steps, you will need
    a Google Cloud Project. Once you have created your project,
    [install the Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
    Then run the following command to authenticate with your project:
    ```bash
    gcloud auth login
    ```
    You also need to enable certain APIs. Run the following command to enable
    the required APIs:
    ```bash
    gcloud services enable aiplatform.googleapis.com
    ```

2.  Clone the repository:

    ```bash
    git clone https://github.com/google/adk-samples.git
    cd adk-samples/python/agents/customer-service
    ```

    For the rest of this tutorial **ensure you remain in the `agents/customer-service` directory**.

3.  Install dependencies using Poetry:

- if you have not installed poetry before then run `pip install poetry` first. then you can create your virtual environment and install all dependencies using:

  ```bash
  poetry install
  ```

  To activate the virtual environment run:

  ```bash
  poetry env activate
  ```

4.  Set up Google Cloud credentials:

    - Ensure you have a Google Cloud project.
    - Make sure you have the Vertex AI API enabled in your project.
    - Set the `GOOGLE_GENAI_USE_VERTEXAI`, `GOOGLE_CLOUD_PROJECT`, and `GOOGLE_CLOUD_LOCATION` environment variables. You can set them in your `.env` file (modify and rename .env_sample file to .env) or directly in your shell. Alternatively you can edit [customer_service/config.py](./customer_service/config.py)

    ```bash
    export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_NAME_HERE
    export GOOGLE_GENAI_USE_VERTEXAI=1
    export GOOGLE_CLOUD_LOCATION=us-central1
    ```

## Running the Agent

You can run the agent using the ADK commant in your terminal.
from the root project directory:

1.  Run agent in CLI:

    ```bash
    adk run customer_service
    ```

2.  Run agent with ADK Web UI:
    ```bash
    adk web
    ```
    Select the customer_service from the dropdown

## Modifying the Agent's Instructions

The core behavior of the agent is defined by the instructions in the `customer_service/prompts.py` file. You can modify the agent's persona, its task, and its constraints by editing the `INSTRUCTION` variable in this file.

### 1. Locate the `INSTRUCTION` Variable

Open the file `customer_service/prompts.py`. Inside this file, you will find a Python variable named `INSTRUCTION`. It's a multi-line string that contains the core instructions for the agent.

### 2. Modify the `INSTRUCTION` String

To change the agent's behavior, you simply need to edit the text within the triple quotes (`"""..."""`) of the `INSTRUCTION` variable.

For example, if you wanted to change the agent's persona to be more formal, you could change the beginning of the instruction from:

```python
INSTRUCTION = """
You are the OC-Agent. Your task is to prepare a summary of the OC Morning Call meeting.

First, invite the user to upload the meeting transcript...
"""
```

to something like:

```python
INSTRUCTION = """
You are a professional assistant. Your primary function is to generate a formal summary of the OC Morning Call meeting.

Your first action should be to request the user to provide the meeting transcript...
"""
```

### 3. Redeploy the Agent

After you have saved your changes to the `prompts.py` file, the new instructions will not take effect until you redeploy the agent to the Agent Engine. You can do this by following the deployment steps outlined in the "Deployment on Google Agent Engine" section.

## Deployment on Google Agent Engine

To deploy the agent to the Google Agent Engine, you need to build the agent as a wheel file and then run the deployment script.

### 1. Build the Agent Wheel File

This command bundles the agent into a standardized `.whl` (wheel) file, which is required for deployment. The wheel file will be created in the `deployment` directory.

```bash
poetry build --format=wheel --output=deployment
```

### 2. Deploy the Agent to Agent Engine

The deployment script `deploy.py` is located in the `deployment` directory. It's important to run the script from within this directory to ensure all paths are resolved correctly.

Before running the deployment, make sure you have authenticated with Google Cloud:
```bash
gcloud auth login
gcloud auth application-default login
```

It is also crucial to ensure that the deployment script uses the correct Google Cloud project. You can force the script to use the correct project by setting the `GOOGLE_CLOUD_PROJECT` environment variable for the deployment command.

Navigate to the deployment directory and run the deployment command:

```bash
cd deployment
GOOGLE_CLOUD_PROJECT="your-gcp-project-id" poetry run python deploy.py
```

Replace `"your-gcp-project-id"` with your actual Google Cloud project ID.

The deployment process will take a few minutes. When it finishes, it will print the agent's unique **Resource Name**. It will look like:
`projects/your-gcp-project-id/locations/us-central1/reasoningEngines/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Copy this full resource name.** You will need it for the next steps.

### 3. Testing the Deployed Agent

You can test the deployed agent by creating a Python script and using the resource name you copied from the previous step.

Create a new Python file (e.g., `test_agent.py`) with the following content:

```python
import vertexai
from vertexai import agent_engines

# --- Your Configuration ---
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
AGENT_RESOURCE_NAME = "paste-your-agent-resource-name-here"
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
```

Replace `"your-gcp-project-id"` and `"paste-your-agent-resource-name-here"` with your actual project ID and agent resource name.

Run the test script:
```bash
poetry run python test_agent.py
```
You should see the agent's friendly greeting printed in your terminal.

## Connect to AgentSpace

After deploying the agent to the Agent Engine, you can register it as a tool in your AgentSpace application. This allows your user-facing agent to delegate tasks to your newly deployed customer service agent.

### 1. Grant IAM Permissions

Before you can register the agent, you need to grant the necessary permissions in the Google Cloud Console. The "Hub" agent (your AgentSpace app) needs permission to call the "Spoke" agent (your Reasoning Engine).

1.  Go to the **IAM & Admin** page in the Google Cloud Console.
2.  Click the **+ GRANT ACCESS** button.
3.  In the "New principals" box, find the service account for your AgentSpace app. It will be in the format: `service-<PROJECT_NUMBER>@gcp-sa-discoveryengine.iam.gserviceaccount.com`.
4.  Assign the **Vertex AI User** role to this service account.
5.  Click **Save**.

### 2. Register the Agent as a Tool

To register the agent, you will use a `curl` command. This command needs a temporary access token.

**Step 1: Get Your Access Token**

Run this command by itself first to get a fresh, temporary access token.

```bash
gcloud auth print-access-token
```
You will get a long string of characters as output. Copy this token for the next step.

**Step 2: Run the `curl` Command**

Now, use the following `curl` command. **Before you press Enter**, replace the placeholder `PASTE_YOUR_TOKEN_HERE` with the actual token you just copied. You also need to replace the placeholders for your project ID, engine ID and reasoning engine ID.

```bash
# Set your Project ID
export PROJECT_ID="your-gcp-project-id"

# Replace the placeholder and run the command
curl -X POST \
  -H "Authorization: Bearer PASTE_YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: ${PROJECT_ID}" \
  "https://discoveryengine.googleapis.com/v1alpha/projects/${PROJECT_ID}/locations/global/collections/default_collection/engines/your-engine-id/assistants/default_assistant/agents" \
  -d '{
    "displayName": "OC-Agent-YYYYMMDD",
    "description": "OC Agent for morning call summary",
    "icon": {
       "uri": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/support_agent/default/24px.svg"
     },
    "adk_agent_definition": {
      "tool_settings": {
        "tool_description": "A specialist agent that handles complex, real-time customer service tasks. Use this for any requests related to a customer shopping cart, modifying an order, checking product inventory, scheduling a service appointment, or getting personalized product recommendations."
      },
      "provisioned_reasoning_engine": {
        "reasoning_engine": "projects/your-gcp-project-id/locations/us-central1/reasoningEngines/your-reasoning-engine-id"
      }
    }
  }'
```

If successful, the command will return a JSON response describing the new agent connection it just created. You should then be able to see the "OC-Agent-YYYYMMDD" listed as an available tool in your AgentSpace configuration.

### 3. Updating the Agent Engine

For iterative development, you can update the deployed agent by pointing the AgentSpace agent to a new version of the Reasoning Engine. This is a blue/green deployment strategy that allows for instant rollback.

**Step 1: Deploy a New Reasoning Engine**

Follow the steps in the "Deployment on Google Agent Engine" section to deploy a new version of your agent. This will give you a new Reasoning Engine ID.

**Step 2: Update the AgentSpace Agent**

Use the following `curl` command to update the AgentSpace agent to point to the new Reasoning Engine. This is a `PATCH` request that updates the `reasoningEngine` field of the agent.

**Get Your Access Token:**
```bash
gcloud auth print-access-token
```

**Run the `curl` Command:**
```bash
# Set your Project ID
export PROJECT_ID="your-gcp-project-id"
export ENGINE_ID="your-agentspace-engine-id"
export ASSISTANT_ID="default_assistant"
export AGENT_ID="your-agent-id"
export NEW_ENGINE_ID="your-new-reasoning-engine-id"

# Replace the placeholder and run the command
curl -X PATCH \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: ${PROJECT_ID}" \
  "https://discoveryengine.googleapis.com/v1alpha/projects/${PROJECT_ID}/locations/global/collections/default_collection/engines/${ENGINE_ID}/assistants/${ASSISTANT_ID}/agents/${AGENT_ID}?updateMask=adkAgentDefinition.provisionedReasoningEngine.reasoningEngine" \
  -d 	'{ "adkAgentDefinition": { "provisionedReasoningEngine": { "reasoningEngine": "projects/${PROJECT_ID}/locations/us-central1/reasoningEngines/${NEW_ENGINE_ID}" } } }'
```

**Important:**
-   `your-gcp-project-id`: Your Google Cloud project ID.
-   `your-agentspace-engine-id`: The ID of your AgentSpace engine.
-   `your-agent-id`: The ID of the agent you want to update.
-   `your-new-reasoning-engine-id`: The ID of the new Reasoning Engine you deployed.

You will also need to include the `displayName`, `description` and `tool_description` in the payload to avoid errors.


## AgentSpace Agents

### Live Agent

The live version of the agent is available at the following URL:

[https://vertexaisearch.cloud.google.com/home/cid/7286c13e-bc26-4dd8-a058-82f2c75c1afd/r/agent/6840441290030617211](https://vertexaisearch.cloud.google.com/home/cid/7286c13e-bc26-4dd8-a058-82f2c75c1afd/r/agent/6840441290030617211)

### Test Agent

A test version of the agent is also available for development and testing purposes.

[https://vertexaisearch.cloud.google.com/home/cid/7286c13e-bc26-4dd8-a058-82f2c75c1afd/r/agent/6583307635341617033](https://vertexaisearch.cloud.google.com/home/cid/7286c13e-bc26-4dd8-a058-82f2c75c1afd/r/agent/6583307635341617033)

## Disclaimer

This agent sample is provided for illustrative purposes only and is not intended for production use. It serves as a basic example of an agent and a foundational starting point for individuals or teams to develop their own agents.

This sample has not been rigorously tested, may contain bugs or limitations, and does not include features or optimizations typically required for a production environment (e.g., robust error handling, security measures, scalability, performance considerations, comprehensive logging, or advanced configuration options).

Users are solely responsible for any further development, testing, security hardening, and deployment of agents based on this sample. We recommend thorough review, testing, and the implementation of appropriate safeguards before using any derived agent in a live or critical system.