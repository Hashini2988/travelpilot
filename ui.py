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
    "Powered by Gemini 3.6 Flash — Generating dynamic, persona-driven travel"
    " experiences."
)
st.divider()

# --- MULTI-CHAT SESSION STATE INITIALIZATION ---
if "chats" not in st.session_state:
  st.session_state.chats = {
      "Chat 1": [{
          "role": "assistant",
          "content": (
              "Hello! I am **TravelPilot**. Where would you like to travel"
              " next, and what kind of trip are you dreaming of?"
          ),
      }]
  }

if "current_chat" not in st.session_state:
  st.session_state.current_chat = "Chat 1"

# Sidebar Setup (Chat History Manager + Trip Settings)
with st.sidebar:
  st.header("💬 Chat History")

  if st.button("➕ New Chat", use_container_width=True):
    new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat_name] = [{
        "role": "assistant",
        "content": (
            f"Hello! I am **TravelPilot**. Welcome to {new_chat_name}! Where"
            " would you like to explore?"
        ),
    }]
    st.session_state.current_chat = new_chat_name
    st.rerun()

  st.divider()

  st.subheader("Your Conversations")
  chat_names = list(st.session_state.chats.keys())
  for c_name in chat_names:
    if st.button(
        f"📁 {c_name}"
        if c_name != st.session_state.current_chat
        else f"💬 ➔ {c_name}",
        use_container_width=True,
    ):
      st.session_state.current_chat = c_name
      st.rerun()

  st.divider()
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
  if st.button("🗑️ Clear Current Chat", use_container_width=True):
    st.session_state.chats[st.session_state.current_chat] = [{
        "role": "assistant",
        "content": (
            "Hello! I am **TravelPilot**. Chat history cleared. Where would you"
            " like to go?"
        ),
    }]
    st.rerun()

# Retrieve messages for the currently selected chat session
current_messages = st.session_state.chats[st.session_state.current_chat]

# Render all messages in the active chat
for message in current_messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Handle User Input & Store in Active Chat Session
if prompt := st.chat_input(
    f"Message TravelPilot ({st.session_state.current_chat})..."
):
  current_messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner(
        f"Crafting custom {travel_vibe} itinerary for a {budget_tier} budget..."
    ):
      response_text = generate_travel_response(
          prompt=prompt, travel_vibe=travel_vibe, budget_tier=budget_tier
      )

      st.markdown(response_text)

      st.download_button(
          label="📥 Download Itinerary (Markdown)",
          data=response_text,
          file_name="travelpilot_itinerary.md",
          mime="text/markdown",
      )

      current_messages.append({"role": "assistant", "content": response_text})