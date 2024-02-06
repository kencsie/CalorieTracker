import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with environment variables
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_PATH')
)


# Read the prompt from the file
prompt_filename = 'user_gpt_prompt.txt'  # Ensure this is the correct filename
with open(prompt_filename, 'r') as file:
    prompt_content = file.read()

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_content}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

