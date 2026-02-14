
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load env
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
api_endpoint = os.environ.get("GEMINI_API_ENDPOINT")

print(f"API Key: {api_key[:5]}...{api_key[-5:] if api_key else ''}")
print(f"Endpoint: {api_endpoint}")

if api_endpoint:
    genai.configure(api_key=api_key, transport='rest', client_options={'api_endpoint': api_endpoint})
else:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-3-pro-image')

prompt = "Create a clean, hand-drawn line art illustration for a tech blog article. Title: GLM-5.0. Content: AI agentic engineering."

try:
    print("Sending request...")
    response = model.generate_content(prompt)
    print("\n--- Response Object ---")
    print(response)
    
    if hasattr(response, 'parts'):
        print(f"\nParts count: {len(response.parts)}")
        for i, part in enumerate(response.parts):
            print(f"Part {i}:")
            if hasattr(part, 'inline_data'):
                print(f"  inline_data mime_type: {part.inline_data.mime_type}")
                print(f"  inline_data data length: {len(part.inline_data.data)}")
            else:
                print("  No inline_data")
            
            if hasattr(part, 'text'):
                print(f"  text: {part.text[:100]}...")

    if hasattr(response, 'prompt_feedback'):
        print(f"\nPrompt Feedback: {response.prompt_feedback}")

    if hasattr(response, 'candidates'):
        print(f"\nCandidates: {response.candidates}")

except Exception as e:
    print(f"\nError: {e}")
