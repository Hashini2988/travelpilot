import os
from google import genai
from google.genai import types

# Initialize the Gemini client using environment variables (Streamlit secrets)
client = genai.Client()


def generate_travel_response(prompt: str, travel_vibe: str, budget_tier: str):
  system_instruction = (
      f"You are TravelPilot, an expert AI travel architect. The user wants a custom itinerary."
      f"Selected Travel Persona/Vibe: {travel_vibe}."
      f"Strict Budget Tier Constraint: {budget_tier}."
      f"Tailor all recommendations, local transit, food spots, and activities strictly to this vibe and budget."
      f"Provide a structured, multi-day itinerary with estimated cost breakdowns in local currency and practical pro-tips."
  )

  try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        ),
    )
    return response.text
  except Exception as e:
    return f"⚠️ Error generating itinerary: {str(e)}"