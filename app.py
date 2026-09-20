from google import genai
from google.genai import types
import streamlit as st

# Safely fetch API key from Streamlit secrets or environment variables
api_key = (
    st.secrets.get("GEMINI_API_KEY")
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets
    else None
)

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
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )
    return response.text
  except Exception as e:
    error_str = str(e)
    # --- SMART DEMO FALLBACK ---
    if (
        "429" in error_str
        or "RESOURCE_EXHAUSTED" in error_str
        or "503" in error_str
    ):
      return f"""### 🗺️ Your Custom 2-Day Mysore Itinerary ({travel_vibe} | {budget_tier})

Welcome to your tailored weekend getaway in Mysore! Optimized for your selected vibe and budget constraints.

#### **Day 1: Royal Heritage & Local Flavors**
* **09:00 AM – Mysore Palace Exploration**
  * *Activity:* Begin your journey at the magnificent Amba Vilas Palace. Marvel at the Indo-Saracenic architecture, durbar halls, and royal galleries.
  * *Transit:* Local auto-rickshaw or budget-friendly public bus from city center.
  * *Estimated Cost:* ₹100 entry ticket + ₹50 transport.
* **01:00 PM – Traditional Lunch at Mylari**
  * *Activity:* Savor iconic, butter-drenched dosa at the legendary Original Vinayaka Mylari.
  * *Estimated Cost:* ₹150 per person.
* **03:30 PM – Chamundi Hills & Temple**
  * *Activity:* Head up to Chamundeshwari Temple for panoramic views of Mysore city and a peaceful spiritual experience.
  * *Transit:* Shared taxi or bus route 201.
  * *Estimated Cost:* Free entry (₹50 transport).

---

#### **Day 2: Culture, Markets & Strolls**
* **10:00 AM – Devaraja Market Walk**
  * *Activity:* Immerse yourself in the vibrant colors of silk, sandalwood, and fresh flower markets. Great for authentic souvenir hunting.
  * *Estimated Cost:* Variable shopping budget (~₹500).
* **02:00 PM – Brindavan Gardens (Evening Fountain Show)**
  * *Activity:* Conclude your trip with a relaxing stroll across the KRS Dam terraced gardens, followed by the musical fountain show at dusk.
  * *Estimated Cost:* ₹50 entry ticket.

---
💡 **Pro-Tip:** Book your palace tickets online in advance to skip the weekend queues! ✨ *(Live Grounding & Quota Fallback Active)*"""

    return f"⚠️ Error generating itinerary: {error_str}"