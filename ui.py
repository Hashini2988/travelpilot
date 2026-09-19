from app import generate_travel_response
import streamlit as st

# 1. Page Configuration & Styling
st.set_page_config(
    page_title="TravelPilot | AI Travel Assistant",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# App Header
st.title("✈️ TravelPilot")
st.caption(
    "Your intelligent, AI-powered travel companion for customized itineraries"
    " and trip planning."
)
st.divider()

# 2. Sidebar Setup & Controls
with st.sidebar:
  st.header("⚙️ Trip Settings")

  # API Key Input (useful if local secrets aren't set)
  api_key_input = st.text_input(
      "Gemini API Key",
      type="password",
      help=(
          "Enter your Gemini API key here if running locally without environment"
          " secrets."
      ),
  )

  st.divider()

  # Innovation Vibe / Persona Selector
  travel_vibe = st.selectbox(
      "Select Travel Persona / Vibe",
      [
          "🎒 Backpacker / Budget",
          "🍷 Luxury & Leisure",
          "⚡ Extreme Adventure",
          "🏛️ Culture & History",
          "🍔 Foodie & Culinary Tour",
      ],
      help="This dynamically changes how TravelPilot customizes your itinerary!",
  )

  st.divider()
  st.markdown("### About TravelPilot")
  st.info(
      "TravelPilot uses Google Gemini and custom context to generate tailored"
      " itineraries instantly. Built for seamless travel discovery."
  )

  if st.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# 3. Chat Session State Initialization
if "messages" not in st.session_state:
  st.session_state.messages = [
      {
          "role": "assistant",
          "content": (
              "Hello! I am **TravelPilot**. Where would you like to travel"
              " next, and what kind of trip are you dreaming of?"
          ),
      }
  ]

# 4. Render Conversation History
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# 5. Handle User Input & AI Generation
if prompt := st.chat_input(
    "e.g., Plan a 3-day weekend trip to Tokyo for food tasting..."
):
  # Append user message
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Generate Assistant Response
  with st.chat_message("assistant"):
    with st.spinner(f"Crafting your {travel_vibe} itinerary..."):
      # Call backend generation function with prompt, selected vibe, and optional key
      response_text = generate_travel_response(
          prompt=prompt, travel_vibe=travel_vibe, api_key_input=api_key_input
      )

      st.markdown(response_text)
      st.session_state.messages.append(
          {"role": "assistant", "content": response_text}
      )