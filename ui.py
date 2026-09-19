from app import generate_travel_response
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="TravelPilot | AI Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App Header
st.title("✈️ TravelPilot: Intelligent Itinerary Architect")
st.caption(
    "Powered by Google Gemini 3.6 Flash — Generating dynamic, persona-driven"
    " travel experiences."
)
st.divider()

# Sidebar Setup (Clean & Frictionless)
with st.sidebar:
  st.header("⚙️ Trip Settings")

  travel_vibe = st.selectbox(
      "Select Travel Persona / Vibe",
      [
          "🎒 Backpacker / Budget",
          "🍷 Luxury & Leisure",
          "⚡ Extreme Adventure",
          "🏛️ Culture & History",
          "🍔 Foodie & Culinary Tour",
      ],
  )

  budget_tier = st.selectbox(
      "Budget Tier Constraint",
      ["Low-cost ($)", "Moderate ($$)", "High-end ($$$)", "Luxury ($$$$)"],
  )

  st.divider()

  st.markdown("### About TravelPilot")
  st.info(
      "TravelPilot uses Google Gemini and custom context to generate tailored"
      " itineraries instantly. Built for seamless travel discovery."
  )

  st.divider()
  if st.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# Initialize Chat History storage in session state
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": (
          "Hello! I am **TravelPilot**. Where would you like to travel next,"
          " and what kind of trip are you dreaming of?"
      ),
  }]

# Render all previous chat history messages from storage
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Handle User Input & Store New Messages
if prompt := st.chat_input(
    "e.g., Plan a 1-day nature trip in Bangalore within 5000..."
):
  # Append and display user message
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Generate and display assistant response
  with st.chat_message("assistant"):
    with st.spinner(
        f"Crafting custom {travel_vibe} itinerary for a {budget_tier} budget..."
    ):
      response_text = generate_travel_response(
          prompt=prompt, travel_vibe=travel_vibe, budget_tier=budget_tier
      )

      st.markdown(response_text)

      st.download_button(
          label="📥 Download Complete Itinerary (Markdown)",
          data=response_text,
          file_name="travelpilot_itinerary.md",
          mime="text/markdown",
      )

      # Append assistant response to chat history storage
      st.session_state.messages.append(
          {"role": "assistant", "content": response_text}
      )