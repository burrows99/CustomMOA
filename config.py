import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Environment Variables
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# User Prompt
USER_PROMPT = "What are 3 fun things to do in SF?"

# Reference Models
REFERENCE_MODELS = [
    "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "Qwen/Qwen2.5-72B-Instruct-Turbo",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "microsoft/WizardLM-2-8x22B"
]

# Aggregator Model
AGGREGATOR_MODEL = "Qwen/Qwen2.5-72B-Instruct-Turbo"

# Aggregator System Prompt
AGGREGATOR_SYSTEM_PROMPT = """
You have been provided with a set of responses from various open-source models to the latest user query. 
Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided, recognizing that some of it may be biased or incorrect. 
Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. 
Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models:
"""