import json
import urllib.request
import urllib.error
import streamlit as st

API_KEY = "PUT_YOUR_API_KEY_HERE"  # Replace with your actual key

st.set_page_config(page_title="TravelPilot Agent", layout="wide")

def load_itinerary():
    with open("trip_data.json", "r") as f:
        return json.load(f)

def ask_travel_agent(prompt):
    itinerary = load_itinerary()
    system_instruction = f"""
    You are TravelPilot, an intelligent trip planning and disruption management agent. 
    Here is the current trip itinerary state in JSON:
    {json.dumps(itinerary)}
    
    Answer the user's question accurately based on this data. If they want to simulate a disruption 
    or change an activity, explain how you are optimizing the plan.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser Question: {prompt}"}]}]
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text']
    except urllib.error.HTTPError as e:
        return f"API Error: {e.read().decode('utf-8')}"

st.title("✈️ TravelPilot: Intelligent Trip Planning & Disruption Agent")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📅 Live Itinerary Dashboard")
    itinerary = load_itinerary()
    st.write(f"**Trip:** {itinerary['trip_name']}")
    st.write(f"**Destination:** {itinerary['destination']}")
    st.write(f"**Total Budget:** ${itinerary['total_budget']} {itinerary['currency']}")
    
    for day in itinerary['days']:
        st.markdown(f"### Day {day['day']} ({day['date']})")
        for act in day['activities']:
            st.info(f"**{act['time']}** - {act['name']} ({act['category']})\n\n📍 *{act['location']}* | 💰 ${act['cost']} | Status: `{act['status']}`")

with col2:
    st.subheader("🤖 TravelPilot Assistant Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your trip or simulate a disruption..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("TravelPilot is analyzing and re-optimizing schedule..."):
                response = ask_travel_agent(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("🚨 Simulate: TeamLab Planets Closed"):
        sim_prompt = "Simulate that TeamLab Planets is closed today due to maintenance. Provide a backup option."
        with st.spinner("Re-optimizing itinerary..."):
            response = ask_travel_agent(sim_prompt)
            st.success(response)