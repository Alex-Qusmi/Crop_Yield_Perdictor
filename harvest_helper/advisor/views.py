from django.shortcuts import render
import json
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Configure the Gemini API client
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")
response = model.generate_content("Say hello in JSON format")
print(response.text)

@require_POST
def get_recommendation(request):
    try:
        # 1. Parse incoming data
        data = json.loads(request.body)

        # 2. Build the prompt dynamically
        location_str = f"District: {data.get('district')}"
        if data.get('latitude'):
            location_str = f"Latitude: {data.get('latitude')}, Longitude: {data.get('longitude')} (in {data.get('district')} district)"

        weather_str = data.get('weatherString', 'Weather data not provided.')

        nutrient_str = "Nutrient levels not provided."
        if data.get('nitrogen') or data.get('phosphorus') or data.get('potassium'):
            nutrient_str = f"N: {data.get('nitrogen') or 'N/A'} kg/ha, P: {data.get('phosphorus') or 'N/A'} kg/ha, K: {data.get('potassium') or 'N/A'} kg/ha."

        # 3. Create the AI prompt
        prompt = f"""
        Act as a world-class agronomist and market expert for the Himalayan region of Uttarakhand, India.
        A farmer has provided this data:
        - **Location:** {location_str}
        - **Soil Type:** {data.get('soilType')}
        - **Soil pH:** {data.get('soilPh')}
        - **Soil Nutrients:** {nutrient_str}
        - **Weather:** {weather_str}
        - **Farmer Notes:** {data.get('notes') or 'None'}

        Based only on this data, generate a detailed JSON report (valid JSON only) following this schema:

        {{
            "fullReport": "Here is your personalized report ...",
            "recommendations": [
                {{
                    "cropName": "Name of the crop",
                    "rationale": "Why it suits this soil and climate",
                    "growingGuide": "Detailed steps with practical tips (in Markdown)",
                    "marketStrategy": "Advice to sell at high value (in Markdown)"
                }},
                ... exactly 3 recommendations ...
            ]
        }}
        """

        # 4. Use the latest Gemini 2.5 model
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        # 5. Generate structured JSON content
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )

        # 6. Parse and return JSON safely
        ai_json = json.loads(response.text)
        return JsonResponse(ai_json)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# --- NEW AI CHATBOT VIEW ---
@require_POST
def ai_chat_helper(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # ✅ Define the "ChatGPT-style" personality
        model = genai.GenerativeModel(
            "models/gemini-2.5-flash",
            system_instruction=(
                "You are **Harvest Helper**, a friendly AI agronomist from Uttarakhand. "
                "You answer like ChatGPT — short, clear, structured, and emotionally warm. "
                "Each reply must be beautifully formatted in Markdown, with emojis, headings, and clean spacing. "
                "Use simple language, step-by-step explanations, and highlight key points. "
                "Always give concise, to-the-point answers — never overly long essays. "
                "If asked a farming or gardening question, explain with love and motivation. "
                "End with a cheerful encouragement like: '🌱 You’ve got this, happy farming!' "
                "If asked off-topic, politely say you can only assist with crops, soil, and weather."
            )
        )

        # ✅ Stream and combine the answer
        response_stream = model.generate_content(user_message, stream=True)
        full_text = ""
        for chunk in response_stream:
            if chunk.text:
                full_text += chunk.text
        response_stream.resolve()

        return JsonResponse({'response': full_text})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
