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
    "Powered by Google Gemini 2.5 Flash — Generating dynamic, persona-driven"
    " travel experiences."
)
st.divider()

# Sidebar Setup
with st.sidebar:
  st.header("⚙️ Advanced Trip Controls")

  api_key_input = st.text_input("Gemini API Key", type="password")

  st.divider()

  # Innovation Feature 1: Travel Persona Vibe
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

  # Innovation Feature 2: Strict Budget Tier Selector
  budget_tier = st.selectbox(
      "Budget Tier Constraint",
      ["Low-cost ($)", "Moderate ($$)", "High-end ($$$)", "Luxury ($$$$)"],
  )

  st.divider()
  if st.button("🗑️ Reset Application State", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# Initialize Chat History
if "messages" not in st.session_state:
  st.session_state.messages = []

# Render Chat History
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input(
    "Where would you like to travel? (e.g., 3 days in Kyoto)"
):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner(
        f"Crafting custom {travel_vibe} itinerary for a {budget_tier} budget..."
    ):
      response_text = generate_travel_response(
          prompt=prompt,
          travel_vibe=travel_vibe,
          budget_tier=budget_tier,
          api_key_input=api_key_input,
      )

      st.markdown(response_text)

      # Innovation UI Polish: Provide quick metrics / download options
      st.success(
          "✨ Itinerary successfully synthesized with persona and budget filters!"
      )
      st.download_button(
          label="📥 Download Complete Itinerary (Markdown)",
          data=response_text,
          file_name="travelpilot_itinerary.md",
          mime="text/markdown",
      )

      st.session_state.messages.append(
          {"role": "assistant", "content": response_text}
      )