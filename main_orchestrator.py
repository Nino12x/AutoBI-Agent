```python
import os
import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# ==========================================
# 1. Configuration & LLM Setup
# ==========================================
# In a real environment, load from .env. Here we mock the config for demonstration.
config_list = [
    {
        "model": "gpt-4-turbo-preview", # Requesting high-tier model for complex reasoning
        "api_key": os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_PLACEHOLDER")
    }
]

llm_config = {
    "cache_seed": 42,
    "temperature": 0.2,
    "config_list": config_list,
    "timeout": 120,
}

print("Initializing AutoBI-Agent Multi-Agent Workflow...")

# ==========================================
# 2. Agent Definitions
# ==========================================

# Agent 1: The SQL & Data Extraction Expert
sql_agent = AssistantAgent(
    name="SQL_Expert",
    system_message="""You are a Senior Data Engineer. 
    Your task is to parse the user's business anomaly question, determine what data is needed, 
    and write the exact SQL queries to extract regional DAU (Daily Active Users) and error logs. 
    You do NOT analyze the data, you only provide the queries and mock the extraction status.""",
    llm_config=llm_config,
)

# Agent 2: The Code Analyzer & Anomaly Sandbox
code_analyzer = AssistantAgent(
    name="Code_Analyzer",
    system_message="""You are a Principal Data Scientist. 
    You receive data context from the SQL_Expert. 
    Your job is to write Python code (Pandas, Scikit-learn Isolation Forest) to find the root cause of the anomaly. 
    You must use Chain-of-Thought reasoning: first exclude normal holiday drops, then check regional disparities, then correlate with system error logs. 
    Explain your reasoning step-by-step.""",
    llm_config=llm_config,
)

# Agent 3: The Insight Report Generator
report_generator = AssistantAgent(
    name="Report_Generator",
    system_message="""You are a Chief Business Analyst. 
    You take the technical findings from the Code_Analyzer and translate them into a structured, 
    bullet-point executive summary. The report must include:
    1. The core issue.
    2. The root cause discovered via data.
    3. Actionable recommendations for the management team.""",
    llm_config=llm_config,
)

# User Proxy: Acts as the trigger and automated sandbox executor
user_proxy = UserProxyAgent(
    name="Admin_Trigger",
    system_message="A human admin or automated monitoring webhook that triggers the task.",
    code_execution_config={"last_n_messages": 2, "work_dir": "data_sandbox", "use_docker": False},
    human_input_mode="NEVER" # Fully automated pipeline
)

# ==========================================
# 3. Group Chat Orchestration
# ==========================================
groupchat = GroupChat(
    agents=[user_proxy, sql_agent, code_analyzer, report_generator], 
    messages=[], 
    max_round=6 # Ensure the workflow completes within a set number of interactions
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# ==========================================
# 4. Execution Trigger
# ==========================================
if __name__ == "__main__":
    task_prompt = """
    [ALERT] Regional DAU (Daily Active Users) dropped by 15% today compared to the 7-day moving average. 
    Please initiate the AutoBI workflow to find the root cause and generate an executive report.
    """
    
    print(f"\n[Task Initiated]: {task_prompt}")
    
    # Start the multi-agent chat
    # Note: In a live environment with an API key, this will trigger the actual LLM calls.
    try:
        user_proxy.initiate_chat(manager, message=task_prompt)
    except Exception as e:
        print("\n[System Warning] API Key not configured. Running mock execution trace for demonstration...")
        # Mocking the output for safe demonstration without API keys
        print("\nSQL_Expert: Wrote query to extract DAU grouped by region and joined with gateway error logs. Extraction successful.")
        print("Code_Analyzer: Executed anomaly_detect.py. Isolated drop to 'Region_A'. Correlated with a 300% spike in Network Timeout (Error 504) at 02:00 AM.")
        print("Report_Generator: Generated Executive Summary: The 15% DAU drop is isolated to Region A, caused by an API gateway timeout (Error 504). Recommend immediate rollback of the load balancer configuration.")