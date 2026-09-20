from app import generate_travel_response
import sqlite3
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="TravelPilot | Intelligent Itinerary Architect",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- UNIQUE CUSTOM STYLING (Cohesive Dark Mode) ---
st.markdown("""
    <style>
    /* Main App Background & Text Colors */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Sleek Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    /* Chat Input Bar Alignment and Color */
    [data-testid="stChatInput"] {
        background-color: #1f2937;
        border-radius: 12px;
        border: 1px solid #374151;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #374151;
        border-color: #60a5fa;
        color: #60a5fa;
    }
    
    /* Expander Box Styling */
    .streamlit-expanderHeader {
        background-color: #1f2937;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)


# --- SQLITE DATABASE SETUP FOR PERMANENT STORAGE ---
def init_db():
  conn = sqlite3.connect("travelpilot.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_name TEXT,
            role TEXT,
            content TEXT
        )
    """)
  conn.commit()
  return conn, cursor


conn, cursor = init_db()


def load_chats_from_db():
  cursor.execute("SELECT DISTINCT chat_name FROM messages")
  chat_names = [row[0] for row in cursor.fetchall()]

  if not chat_names:
    cursor.execute(
        "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
        (
            "New Chat",
            "assistant",
            (
                "Hello! I am **TravelPilot**. Where would you like to travel"
                " next, and what kind of trip are you dreaming of?"
            ),
        ),
    )
    conn.commit()
    chat_names = ["New Chat"]

  chats = {}
  for name in chat_names:
    cursor.execute(
        "SELECT role, content FROM messages WHERE chat_name = ?", (name,)
    )
    rows = cursor.fetchall()
    chats[name] = [{"role": row[0], "content": row[1]} for row in rows]
  return chats


# App Header
st.title("✈️ TravelPilot: Intelligent Itinerary Architect")
st.caption(
    "Powered by Gemini 3.6 Flash with Live Search Grounding — Generating"
    " dynamic, persona-driven travel experiences."
)
st.divider()

# Load chats from SQLite database into session state
if "chats" not in st.session_state:
  st.session_state.chats = load_chats_from_db()

if "current_chat" not in st.session_state:
  st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# Sidebar Setup
with st.sidebar:
  st.header("💬 Conversations")

  if st.button("➕ New Chat", use_container_width=True):
    base_name = "New Chat"
    new_chat_name = base_name
    counter = 1
    while new_chat_name in st.session_state.chats:
      counter += 1
      new_chat_name = f"New Chat {counter}"

    initial_msg = (
        "Hello! I am **TravelPilot**. Where would you like to explore?"
    )
    cursor.execute(
        "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
        (new_chat_name, "assistant", initial_msg),
    )
    conn.commit()

    st.session_state.chats[new_chat_name] = [{
        "role": "assistant",
        "content": initial_msg,
    }]
    st.session_state.current_chat = new_chat_name
    st.rerun()

  # List past chats
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

  # --- PROMINENT DISRUPTION SIMULATOR ---
  st.header("⚡ Disruption Simulator")
  st.caption("Test real-time itinerary adaptation:")

  if st.button("🌧️ Rain Alert: Swap Outdoor Spots", use_container_width=True):
    disruption_prompt = (
        "It just started raining heavily! Please instantly modify today's"
        " outdoor activities to indoor alternatives nearby without changing"
        " the budget."
    )
    current_messages = st.session_state.chats[st.session_state.current_chat]
    current_messages.append({"role": "user", "content": disruption_prompt})
    cursor.execute(
        "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
        (st.session_state.current_chat, "user", disruption_prompt),
    )
    conn.commit()

    with st.spinner("Adapting itinerary for weather disruption..."):
      response_text = generate_travel_response(
          prompt=disruption_prompt,
          travel_vibe=travel_vibe,
          budget_tier=budget_tier,
      )
      cursor.execute(
          "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
          (st.session_state.current_chat, "assistant", response_text),
      )
      conn.commit()
      current_messages.append({"role": "assistant", "content": response_text})
    st.rerun()

  if st.button("✈️ Flight Delayed by 3 Hours", use_container_width=True):
    disruption_prompt = (
        "My flight was delayed by 3 hours. Adjust my Day 1 arrival schedule and"
        " morning activities accordingly."
    )
    current_messages = st.session_state.chats[st.session_state.current_chat]
    current_messages.append({"role": "user", "content": disruption_prompt})
    cursor.execute(
        "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
        (st.session_state.current_chat, "user", disruption_prompt),
    )
    conn.commit()

    with st.spinner("Adjusting schedule for flight delay..."):
      response_text = generate_travel_response(
          prompt=disruption_prompt,
          travel_vibe=travel_vibe,
          budget_tier=budget_tier,
      )
      cursor.execute(
          "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
          (st.session_state.current_chat, "assistant", response_text),
      )
      conn.commit()
      current_messages.append({"role": "assistant", "content": response_text})
    st.rerun()

  st.divider()

  if st.button("🗑️ Clear Current Chat", use_container_width=True):
    cursor.execute(
        "DELETE FROM messages WHERE chat_name = ?",
        (st.session_state.current_chat,),
    )
    clear_msg = (
        "Hello! I am **TravelPilot**. Chat history cleared. Where would you"
        " like to go?"
    )
    cursor.execute(
        "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
        (st.session_state.current_chat, "assistant", clear_msg),
    )
    conn.commit()
    st.session_state.chats[st.session_state.current_chat] = [{
        "role": "assistant",
        "content": clear_msg,
    }]
    st.rerun()

# Retrieve messages for the currently selected chat session
current_messages = st.session_state.chats[st.session_state.current_chat]

# Render all messages in the active chat
for message in current_messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Handle User Input & Store in SQLite Database
if prompt := st.chat_input(
    f"Message TravelPilot ({st.session_state.current_chat})..."
):
  old_chat_name = st.session_state.current_chat

  # SMART AUTO-RENAME: Rename chat title based on first prompt
  if old_chat_name.startswith("New Chat"):
    new_title = prompt.strip().title()
    if len(new_title) > 25:
      new_title = new_title[:22] + "..."

    if new_title not in st.session_state.chats:
      cursor.execute(
          "UPDATE messages SET chat_name = ? WHERE chat_name = ?",
          (new_title, old_chat_name),
      )
      conn.commit()
      st.session_state.chats[new_title] = st.session_state.chats.pop(
          old_chat_name
      )
      st.session_state.current_chat = new_title

  current_messages = st.session_state.chats[st.session_state.current_chat]

  # Save user message to database
  cursor.execute(
      "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
      (st.session_state.current_chat, "user", prompt),
  )
  conn.commit()

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

      # Save assistant response to database
      cursor.execute(
          "INSERT INTO messages (chat_name, role, content) VALUES (?, ?, ?)",
          (st.session_state.current_chat, "assistant", response_text),
      )
      conn.commit()

      current_messages.append({"role": "assistant", "content": response_text})