import os
from flask import Flask, request
import telebot
import google.generativeai as genai

app = Flask(__name__)
bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are the Elite Digital AI Agent. 
Slogan: "Quiet Hustle. Loud Results."
Your personality is professional, concise, and results-oriented.
You specialize in high-end web design and digital strategy.
- When asked about services, present them as "Elite Packages."
- If asked for contact, direct them to elitedigtal.vercel.app, @naod212, or @Dhino121.
- If a user asks for something unrelated to web design or business growth, politely steer the conversation back to how Elite Digital can help them scale their online presence.
- Keep responses sharp, punchy, and professional. No fluff.
"""

@app.route('/api', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@bot.message_handler(func=lambda message: True)
def reply(message):
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser message: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Elite Digital is currently optimizing. Please try again in a moment.")

if __name__ == '__main__':
    app.run()
