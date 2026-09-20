from google import genai
from google.genai import types

api_key = st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") else None
client = genai.Client(api_key=api_key) if api_key else genai.Client()


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
            tools=[
                types.Tool(google_search=types.GoogleSearch())
            ],  # Fixed SDK tool schema configuration
        ),
    )
    return response.text
  except Exception as e:
    error_str = str(e)
    if "503" in error_str or "UNAVAILABLE" in error_str:
      return (
          "⚠️ **Google Gemini API is currently experiencing temporary high"
          " demand (503 Service Unavailable).** \n\nPlease wait a few seconds and"
          " click send again."
      )
    return f"⚠️ Error generating itinerary: {error_str}"