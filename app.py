import os
from google import genai
from google.genai import errors


def get_gemini_client(api_key_input: str = None):
  """Initializes and returns the Google Gen AI client securely."""
  api_key = api_key_input
  if not api_key:
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
    prompt: str, travel_vibe: str, budget_tier: str, api_key_input: str = None
) -> str:
  """Generates a structured, multi-day travel itinerary using Gemini 2.5 Flash."""
  try:
    client = get_gemini_client(api_key_input)

    system_instruction = (
        "You are TravelPilot, an expert AI travel architect. "
        f"The user's chosen travel persona/vibe is: {travel_vibe}. "
        f"The budget constraint is: {budget_tier}. "
        "You must structure your response clearly using Markdown headers for each Day (e.g., '### Day 1: Arrival & Exploration') "
        "and include specific local recommendations, estimated costs, and hidden gems."
    )

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
    return f"⚠️ Google GenAI API Error: {e.message}"
  except ValueError as ve:
    return f"🔑 {str(ve)}"
  except Exception as ex:
    return f"❌ An unexpected error occurred: {str(ex)}"