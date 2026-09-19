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
      "New Chat": [{
          "role": "assistant",
          "content": (
              "Hello! I am **TravelPilot**. Where would you like to travel"
              " next, and what kind of trip are you dreaming of?"
          ),
      }]
  }

if "current_chat" not in st.session_state:
  st.session_state.current_chat = "New Chat"

# Sidebar Setup (Clean & Collapsible UI)
with st.sidebar:
  st.header("💬 Conversations")

  if st.button("➕ New Chat", use_container_width=True):
    # Ensure unique names if multiple empty chats are created
    base_name = "New Chat"
    new_chat_name = base_name
    counter = 1
    while new_chat_name in st.session_state.chats:
      counter += 1
      new_chat_name = f"New Chat {counter}"

    st.session_state.chats[new_chat_name] = [{
        "role": "assistant",
        "content": (
            "Hello! I am **TravelPilot**. Where would you like to explore?"
        ),
    }]
    st.session_state.current_chat = new_chat_name
    st.rerun()

  # List past chats cleanly
  chat_names = list(st.session_state.chats.keys())
  for c_name in chat_names:
    display_label = f"📁 {c_name}"
    if c_name == st.session_state.current_chat:
      display_label = f"💬 ➔ {c_name}"

    if st.button(display_label, use_container_width=True):
      st.session_state.current_chat = c_name
      st.rerun()

  st.divider()

  with st.expander("⚙️ Trip Settings & Persona", expanded=True):
    travel_vibe = st.selectbox(
        "Travel Vibe",
        [
            "🎒 Backpacker / Budget",
            "🍷 Luxury & Leisure",
            "⚡ Extreme Adventure",
            "🏛️ Culture & History",
            "🍔 Foodie & Culinary Tour",
        ],
    )

    budget_tier = st.selectbox(
        "Budget Tier",
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
  # SMART AUTO-RENAME: If this is the first real user prompt, rename the chat title to match the input!
  if st.session_state.current_chat.startswith("New Chat"):
    # Clean up the prompt to make a nice title (take the first 25 characters)
    new_title = prompt.strip().title()
    if len(new_title) > 25:
      new_title = new_title[:22] + "..."

    # Avoid duplicate keys
    if new_title not in st.session_state.chats:
      st.session_state.chats[new_title] = st.session_state.chats.pop(
          st.session_state.current_chat
      )
      st.session_state.current_chat = new_title

  # Re-assign current messages reference after rename
  current_messages = st.session_state.chats[st.session_state.current_chat]

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