import json
import urllib.request
import urllib.error

# Put your actual Google AI Studio API key inside the quotes below:
API_KEY = "PUT_YOUR_API_KEY_HERE"

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

if __name__ == "__main__":
    print("--- TravelPilot Agent Initialized (Zero-Install Mode) ---")
    
    query1 = "What should I do tomorrow morning and what is the cost?"
    print(f"\nUser: {query1}")
    print(f"TravelPilot: {ask_travel_agent(query1)}")
    
    query2 = "Simulate that TeamLab Planets is closed today due to maintenance. What is my backup option?"
    print(f"\nUser: {query2}")
    print(f"TravelPilot: {ask_travel_agent(query2)}")