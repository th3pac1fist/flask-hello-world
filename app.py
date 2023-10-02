from flask import Flask, request, jsonify
import openai
import random
import os

app = Flask(__name__)

# Get the API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API with your API key
openai.api_key = openai_api_key

# Profiles dictionary
profiles = {
    "Aria": {
        "age": 28,
        "occupation": "Environmental Scientist",
        "hobbies": ["hiking", "reading science fiction", "photography"],
        "favorite_food": "Sushi",
        "favorite_music": "Indie rock",
        "interesting_fact": "Visited 30 countries before turning 25",
        "dream_destination": "Antarctica",
        "values": ["sustainability", "education", "family"],
        "looking_for": "Someone curious, loves nature, and values meaningful conversations.",
        "recent_book_read": "The Overstory by Richard Powers",
        "favorite_movie": "Into the Wild",
        "pet_peeves": ["littering", "not recycling", "loud chewing"],
        "life_goal": "To make a significant positive impact on the environment and inspire others to do the same."
    }
    # Add other profiles similarly
}

def generate_prompt(profile_name, profile):
    return f"""
    {profile_name}, a {profile['age']}-year-old {profile['occupation']}. 
    She enjoys {', '.join(profile['hobbies'][:-1])} and {profile['hobbies'][-1]}. 
    Her favorite food is {profile['favorite_food']} and she loves listening to {profile['favorite_music']}. 
    An interesting fact about her is that she {profile['interesting_fact']}. 
    She values {', '.join(profile['values'][:-1])} and {profile['values'][-1]}. 
    She's looking for {profile['looking_for']}. 
    The last book she read was {profile['recent_book_read']} and her favorite movie is {profile['favorite_movie']}. 
    Some of her pet peeves include {', '.join(profile['pet_peeves'][:-1])} and {profile['pet_peeves'][-1]}. 
    Her life goal is {profile['life_goal']}.
    """

@app.route('/chat_with_date', methods=['POST'])
def chat_with_date():
    user_message = request.json.get('message')
    current_date_name = random.choice(list(profiles.keys()))
    current_date_profile = profiles[current_date_name]
    current_prompt = generate_prompt(current_date_name, current_date_profile)
    
    messages = [{"role": "system", "content": current_prompt}]
    
    if user_message.lower() in ["next", "move on", "next date"]:
        return jsonify({"message": "Moving on to the next date..."})
        
    messages.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    ai_message = response.choices[0].message['content']
    tokens_used = response['usage']['total_tokens']
    
    return jsonify({
        "date_name": current_date_name,
        "ai_message": ai_message,
        "tokens_used": tokens_used
    })

if __name__ == "__main__":
    app.run(debug=True)
