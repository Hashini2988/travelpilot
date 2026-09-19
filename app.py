import os
from google import genai
from google.genai import errors


def get_gemini_client(api_key_input: str = None):
  """Initializes and returns the Google Gen AI client securely."""
  # Priority: 1. Passed user input, 2. Streamlit secrets, 3. Environment variable
  api_key = None

  if api_key_input:
    api_key = api_key_input
  else:
    try:
      import streamlit as st

      if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
      pass

  if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY")

  if not api_key:
    raise ValueError(
        "Gemini API key not found. Please provide it in the sidebar or set your"
        " environment secrets."
    )

  return genai.Client(api_key=api_key)


def generate_travel_response(
    prompt: str, travel_vibe: str, api_key_input: str = None
) -> str:
  """Generates a structured travel itinerary using Gemini 2.5 Flash."""
  try:
    client = get_gemini_client(api_key_input)

    system_instruction = (
        "You are TravelPilot, an expert, enthusiastic, and knowledgeable AI"
        " travel assistant. Your goal is to provide detailed, well-structured,"
        " and engaging itineraries, local tips, and budgeting breakdowns."
        f" The user has selected the following travel style/persona: {travel_vibe}."
        " Tailor all recommendations strictly to match this vibe."
    )

    # Using the recommended gemini-2.5-flash model for fast and smart responses
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "system_instruction": system_instruction,
            "temperature": 0.7,
        },
    )

    return response.text

  except errors.APIError as e:
    return (
        f"⚠️ Google GenAI API Error: {e.message}"
        " (Please check if your API key is valid.)"
    )
  except ValueError as ve:
    return f"🔑 {str(ve)}"
  except Exception as ex:
    return (
        f"❌ An unexpected error occurred: {str(ex)}. Please verify your setup."
    )