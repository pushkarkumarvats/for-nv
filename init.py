import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# --- 1. Initialize FastAPI App ---
# This creates the main application object.
app = FastAPI(
    title="SaralAI Prototype",
    description="A prototype API for the Research Paper Simplifier.",
    version="1.0.0"
)

# --- 2. Define Request & Response Models (using Pydantic) ---
# This ensures that the data sent to and from the API is in the correct format.

class SimplifyRequest(BaseModel):
    content: str
    target_language: str # e.g., "en-hinglish", "en-only"

class ResponseData(BaseModel):
    original_chunk: str
    simplified_chunk: str
    key_points: List[str]

class SimplifyResponse(BaseModel):
    status: str
    data: ResponseData


# --- 3. Prompt Engineering: The "Secret Sauce" ---
# This dictionary holds the instructions we'll give to the AI for each language.
# Adding a new language is as easy as adding a new entry here.

PROMPT_TEMPLATES = {
    "en-hinglish": """
    You are 'SaralAI', a helpful assistant for Indian students. Your task is to explain the following complex academic text in simple, conversational Hinglish.
    - Use everyday English and simple Hindi words (like 'samajhna', 'zaroori', 'fayda').
    - Explain it like you are talking to a friend.
    - Keep it short and clear.
    - Also, provide 2-3 bullet points summarizing the main idea.
    
    Original Text: "{text}"
    """,
    "en-only": """
    You are 'SimplifyAI', an assistant that makes complex text easy to read.
    - Rephrase the following academic text using simple, clear English.
    - Avoid jargon and use shorter sentences.
    - Assume you're explaining this to a high school student.
    - Also, provide 2-3 bullet points summarizing the main idea.
    
    Original Text: "{text}"
    """,
    # In the future, we could add more languages here
    # "hi-pure": "..."
    # "ta-in": "..."
}


# --- 4. Mock AI/LLM Function ---
# In a real application, this function would make a network call to an LLM provider
# like Google Gemini or a self-hosted model.
# For this prototype, we'll simulate the response.

def get_ai_simplification(text: str, language: str) -> dict:
    """
    Simulates calling a Large Language Model (LLM) API.
    """
    print(f"--- Simulating AI call for language: {language} ---")
    
    if language not in PROMPT_TEMPLATES:
        return None # Language not supported

    # This is where we would format the prompt and send it to the LLM
    prompt = PROMPT_TEMPLATES[language].format(text=text)
    print("--- Generated Prompt for AI ---")
    print(prompt)
    print("-----------------------------\n")

    # --- MOCK RESPONSE ---
    # We'll return a hardcoded response based on the language for demonstration.
    if language == "en-hinglish":
        return {
            "simplified_text": "Is study ka main goal yeh samajhna tha ki cells ke andar 'apoptosis' (programmed cell death) process ke peeche molecular level par kya hota hai.",
            "key_points": [
                "Study ka main maqsad cells ke death process ko aasaani se samajhna tha.",
                "Unhone molecular mechanisms par focus kiya."
            ]
        }
    
    if language == "en-only":
        return {
            "simplified_text": "The main goal of this study was to understand the molecular process behind how cells die on purpose, a process called apoptosis.",
            "key_points": [
                "The study focused on understanding programmed cell death.",
                "It specifically investigated the mechanisms at a molecular level."
            ]
        }
    
    return None


# --- 5. API Endpoint ---
# This is the actual URL that the frontend will call.

@app.post("/api/v1/simplify", response_model=SimplifyResponse)
async def simplify_text(request: SimplifyRequest):
    """
    Receives complex text and returns a simplified version in the target language.
    """
    # Get the AI's response by calling our mock function
    ai_result = get_ai_simplification(request.content, request.target_language)

    if not ai_result:
        raise HTTPException(
            status_code=400, 
            detail=f"Language '{request.target_language}' not supported."
        )

    # Structure the final response according to our Pydantic model
    response_data = ResponseData(
        original_chunk=request.content,
        simplified_chunk=ai_result["simplified_text"],
        key_points=ai_result["key_points"]
    )

    return SimplifyResponse(status="success", data=response_data)


# --- To run this file ---
# 1. Save it as main.py
# 2. Open your terminal
# 3. Run the command: uvicorn main:app --reload

if __name__ == "__main__":
    # This allows you to run the app directly using "python main.py"
    # for simple testing, though 'uvicorn' is standard for development.
    uvicorn.run(app, host="0.0.0.0", port=8000)

