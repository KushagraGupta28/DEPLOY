from flask import Flask, request, jsonify
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    user_info = request.json

    prompt = f"""Based on the following info:
    Name: {user_info.get('name')}
    Gender: {user_info.get('gender')}
    Favorite Color: {user_info.get('color')}
    Season: {user_info.get('season')}
    Suggest upperwear and bottomwear this person might like."""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    clothing_description = response.text.strip()

    matched_images = match_images_from_description(clothing_description)

    return jsonify({
        "description": clothing_description,
        "upperwear": matched_images["upperwear"],
        "bottomwear": matched_images["bottomwear"]
    })

def match_images_from_description(desc):
    # Your custom model goes here instead
    return {
        "upperwear": [
            "https://yourhost.com/upperwear/top1.jpg",
            "https://yourhost.com/upperwear/top2.jpg"
        ],
        "bottomwear": [
            "https://yourhost.com/bottomwear/bottom1.jpg",
            "https://yourhost.com/bottomwear/bottom2.jpg"
        ]
    }

@app.route('/')
def home():
    return "Backend API is running"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
