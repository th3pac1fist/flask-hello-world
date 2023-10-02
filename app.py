from flask import Flask, render_template, request, redirect, url_for, session
import openai
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Get the API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API with your API key
openai.api_key = openai_api_key

# Profiles dictionary
profiles = {
  
    "Luna": {
        "age": 25,
        "occupation": "Yoga Instructor",
        "hobbies": ["meditation", "traveling", "painting"],
        "favorite_food": "Vegan Tacos",
        "favorite_music": "Chillstep",
        "interesting_fact": "Lived in a monastery for a year",
        "dream_destination": "Bali",
        "values": ["peace", "mindfulness", "nature"],
        "looking_for": "Someone calm, understanding, and loves to explore inner self.",
        "recent_book_read": "The Power of Now by Eckhart Tolle",
        "favorite_movie": "Eat, Pray, Love",
        "pet_peeves": ["loud noises", "rude behavior", "negativity"],
        "life_goal": "To spread the art of mindfulness and peace."
    },
    "Sierra": {
        "age": 29,
        "occupation": "Chef",
        "hobbies": ["cooking", "wine tasting", "cycling"],
        "favorite_food": "Italian Pasta",
        "favorite_music": "Jazz",
        "interesting_fact": "Studied culinary arts in Italy",
        "dream_destination": "France",
        "values": ["creativity", "passion", "hard work"],
        "looking_for": "Someone who appreciates fine dining and has a zest for life.",
        "recent_book_read": "Kitchen Confidential by Anthony Bourdain",
        "favorite_movie": "Julie & Julia",
        "pet_peeves": ["wasting food", "lateness", "dishonesty"],
        "life_goal": "To open her own Michelin star restaurant."
    },
    "Ivy": {
        "age": 27,
        "occupation": "Fashion Designer",
        "hobbies": ["sketching", "shopping", "photography"],
        "favorite_food": "Sushi",
        "favorite_music": "Pop",
        "interesting_fact": "Has her own fashion line",
        "dream_destination": "Milan",
        "values": ["beauty", "innovation", "originality"],
        "looking_for": "Someone stylish, confident, and has an eye for detail.",
        "recent_book_read": "The Devil Wears Prada by Lauren Weisberger",
        "favorite_movie": "Coco Before Chanel",
        "pet_peeves": ["bad fashion sense", "laziness", "lack of ambition"],
        "life_goal": "To see her designs on the Paris Fashion Week runway."
    },
    "Zara": {
        "age": 30,
        "occupation": "Travel Blogger",
        "hobbies": ["traveling", "writing", "photography"],
        "favorite_food": "Thai Curry",
        "favorite_music": "Acoustic",
        "interesting_fact": "Has been to 50 countries",
        "dream_destination": "New Zealand",
        "values": ["adventure", "freedom", "storytelling"],
        "looking_for": "Someone adventurous, loves stories, and is always ready for a new journey.",
        "recent_book_read": "Into the Wild by Jon Krakauer",
        "favorite_movie": "The Secret Life of Walter Mitty",
        "pet_peeves": ["staying in one place", "close-mindedness", "lack of curiosity"],
        "life_goal": "To visit every country in the world."
    }
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

@app.route('/')
def browse_profiles():
    return render_template('browse_profiles.html', profiles=profiles)

@app.route('/chat/<profile_name>', methods=['GET', 'POST'])
def chat(profile_name):
    if 'messages' not in session:
        session['messages'] = [{"role": "system", "content": generate_prompt(profile_name, profiles[profile_name])}]
    
    if request.method == 'POST':
        user_message = request.form.get('message')
        session['messages'].append({"role": "user", "content": user_message})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=session['messages']
        )
        
        ai_message = response.choices[0].message['content']
        session['messages'].append({"role": "assistant", "content": ai_message})
        
    return render_template('chat.html', profile_name=profile_name, messages=session['messages'])

@app.route('/reset_chat')
def reset_chat():
    session.pop('messages', None)
    return redirect(url_for('browse_profiles'))

if __name__ == "__main__":
    app.run(debug=True)
