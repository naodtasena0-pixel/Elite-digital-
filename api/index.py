import os
from flask import Flask, request
import telebot
import google.generativeai as genai

app = Flask(__name__)
bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/api', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@bot.message_handler(func=lambda message: True)
def reply(message):
    prompt = f"You are the Elite Digital AI Agent. Slogan: 'Quiet Hustle. Loud Results.' Help this user: {message.text}"
    response = model.generate_content(prompt)
    bot.reply_to(message, response.text)
