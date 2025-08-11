# Cymbal Home & Garden Customer Service Agent

This project implements an AI-powered customer service agent for Cymbal Home & Garden, a big-box retailer specializing in home improvement, gardening, and related supplies. The agent is designed to provide excellent customer service, assist customers with product selection, manage orders, schedule services, and offer personalized recommendations.

## Overview

The Cymbal Home & Garden Customer Service Agent is designed to provide a seamless and personalized shopping experience for customers. It leverages Gemini to understand customer needs, offer tailored product recommendations, manage orders, and schedule services. The agent is designed to be friendly, empathetic, and highly efficient, ensuring that customers receive the best possible service.

## Agent Details

The key features of the Customer Service Agent include:

| Feature            | Description             |
| ------------------ | ----------------------- |
| _Interaction Type_ | Conversational          |
| _Complexity_       | Intermediate            |
| _Agent Type_       | Single Agent            |
| _Components_       | Tools, Multimodal, Live |
| _Vertical_         | Retail                  |

### Agent Architecture

![Customer Service Agent Workflow](customer_service_workflow.png)

The agent is built using a multi-modal architecture, combining text and video inputs to provide a rich and interactive experience. It mocks interactions with various tools and services, including a product catalog, inventory management, order processing, and appointment scheduling systems. The agent also utilizes a session management system to maintain context across interactions and personalize the customer experience.

It is important to notice that this agent is not integrated to an actual backend and the behaviour is based on mocked tools. If you would like to implement this agent with actual backend integration you will need to edit [customer_service/tools.py](./customer_service/tools/tools.py)

Because the tools are mocked you might notice that some requested changes will not be applied. For instance newly added item to cart will not show if later a user asks the agent to list all items.

### Key Features

- **Personalized Customer Assistance:**
  - Greets returning customers by name and acknowledges their purchase history.
  - Maintains a friendly, empathetic, and helpful tone.
- **Product Identification and Recommendation:**
  - Assists customers in identifying plants, even from vague descriptions.
  - Requests and utilizes visual aids (video) to accurately identify plants.
  - Provides tailored product recommendations based on identified plants, customer needs, and location (e.g., Las Vegas, NV).
  - Offers alternatives to items in the customer's cart if better options exist.
- **Order Management:**
  - Accesses and displays the contents of a customer's shopping cart.
  - Modifies the cart by adding and removing items based on recommendations and customer approval.
  - Informs customers about relevant sales and promotions.
- **Upselling and Service Promotion:**
  - Suggests relevant services, such as professional planting services.
  - Handles inquiries about pricing and discounts, including competitor offers.
  - Requests manager approval for discounts when necessary.
- **Appointment Scheduling:**
  - Schedules appointments for planting services (or other services).
  - Checks available time slots and presents them to the customer.
  - Confirms appointment details and sends a confirmation/calendar invite.
- **Customer Support and Engagement:**
  - Sends via sms or email plant care instructions relevant to the customer's purchases and location.
  - Offers a discount QR code for future in-store purchases to loyal customers.
- **Tool-Based Interactions:**
  - The agent interacts with the user using a set of tools.
  - The agent can use multiple tools in a single interaction.
  - The agent can use the tools to get information and to modify the user's transaction state.
- **Evaluation:**
  - The agent can be evaluated using a set of test cases.
  - The evaluation is based on the agent's ability to use the tools and to respond to the user's requests.

#### Agent State - Default customer information

The agent's session state is preloaded with sample customer data, simulating a real conversation. Ideally, this state should be loaded from a CRM system at the start of the conversation, using the user's information. This assumes that either the agent authenticates the user or the user is already logged in. If this behavior is expected to be modified edit the [get_customer(current_customer_id: str) in customer.py](./customer_service/entities/customer.py)

#### Tools

The agent has access to the following tools:

- `send_call_companion_link(phone_number: str) -> str`: Sends a link for video connection.
- `approve_discount(type: str, value: float, reason: str) -> str`: Approves a discount (within pre-defined limits).
- `sync_ask_for_approval(type: str, value: float, reason: str) -> str`: Requests discount approval from a manager.
- `update_salesforce_crm(customer_id: str, details: str) -> dict`: Updates customer records in Salesforce.
- `access_cart_information(customer_id: str) -> dict`: Retrieves the customer's cart contents.
- `modify_cart(customer_id: str, items_to_add: list, items_to_remove: list) -> dict`: Updates the customer's cart.
- `get_product_recommendations(plant_type: str, customer_id: str) -> dict`: Suggests suitable products.
- `check_product_availability(product_id: str, store_id: str) -> dict`: Checks product stock.
- `schedule_planting_service(customer_id: str, date: str, time_range: str, details: str) -> dict`: Books a planting service appointment.
- `get_available_planting_times(date: str) -> list`: Retrieves available time slots.
- `send_care_instructions(customer_id: str, plant_type: str, delivery_method: str) -> dict`: Sends plant care information.
- `generate_qr_code(customer_id: str, discount_value: float, discount_type: str, expiration_days: int) -> dict`: Creates a discount QR code.

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

1.  Clone the repository:

    ```bash
    git clone https://github.com/google/adk-samples.git
    cd adk-samples/python/agents/customer-service
    ```

    For the rest of this tutorial **ensure you remain in the `agents/customer-service` directory**.

2.  Install dependencies using Poetry:

- if you have not installed poetry before then run `pip install poetry` first. then you can create your virtual environment and install all dependencies using:

  ```bash
  poetry install
  ```

  To activate the virtual environment run:

  ```bash
  poetry env activate
  ```

3.  Set up Google Cloud credentials:

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

### Example Interaction

Here's a quick example of how a user might interact with the agent:

**User:**:
hi there

**Agent**:
Hey Alex, I see you've been a Cymbal Home & Garden customer for a couple of years now - we appreciate your business! I also see you have a few things in your cart already. How can I help you get your garden growing today?

**User**:
Yeah, so I'm a bit confused. I just bought some...uh...plants or flowers that I wanted to put in the backyard. They just say "sun loving annuals" on them. I totally spaced on picking up potting soil so I'm placing an order for pickup now. The problem is, I'm not sure if the potting soil and fertilizer I picked out are the right ones.

**Agent**:
I understand – it can be tricky when you're not quite sure what you've got! Let's figure this out together. Don't worry, we'll get your plants the right care. To best help you, would you be willing to share a quick video of the plants you've purchased? That will help me identify them and make sure you have the right supplies.

**User**:
Sure, how do I do that?

**Agent**:
I just texted you a link to the number in your profile. Just click on that, and it'll open a secure video connection.

```tool_code
print(send_call_companion_link(phone_number='+12065550123'))
```

```tool_outputs
{'status': 'success', 'message': 'Link sent to +12065550123'}
```

**User**:
Okay, I clicked the link...can you see this?

**Agent**:
Yes I can see you Alex! Can you go ahead and point the camera at your plants so I can inspect them?

**User**:
Yes of course!
...

## Evaluating the Agent

Evaluation tests assess the overall performance and capabilities of the agent in a holistic manner.

**Steps:**

1.  **Run Evaluation Tests:**

    ```bash
    pytest eval
    ```

    - This command executes all test files within the `eval` directory.

## Unit Tests

Unit tests focus on testing individual units or components of the code in isolation.

**Steps:**

1.  **Run Unit Tests:**

    ```bash
    pytest tests/unit
    ```

    - This command executes all test files within the `tests/unit` directory.

## Configuration

You can find further configuration parameters in [customer_service/config.py](./customer_service/config.py). This incudes parameters such as agent name, app name and llm model used by the agent.

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
    "displayName": "CJ Customer Service Agent",
    "description": "CJ Customer Service Agent",
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

If successful, the command will return a JSON response describing the new agent connection it just created. You should then be able to see the "CJ Customer Service Agent" listed as an available tool in your AgentSpace configuration.

## Disclaimer

This agent sample is provided for illustrative purposes only and is not intended for production use. It serves as a basic example of an agent and a foundational starting point for individuals or teams to develop their own agents.

This sample has not been rigorously tested, may contain bugs or limitations, and does not include features or optimizations typically required for a production environment (e.g., robust error handling, security measures, scalability, performance considerations, comprehensive logging, or advanced configuration options).

Users are solely responsible for any further development, testing, security hardening, and deployment of agents based on this sample. We recommend thorough review, testing, and the implementation of appropriate safeguards before using any derived agent in a live or critical system.
