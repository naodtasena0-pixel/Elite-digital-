import os
from flask import Flask, request
import telebot
import google.generativeai as genai

app = Flask(__name__)
bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = "You are the Elite Digital AI Agent. Slogan: 'Quiet Hustle. Loud Results.' Be professional and concise."

@app.route('/api', methods=['POST'])
def webhook():
    print("Received a request from Telegram!") # This will show in Vercel logs
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@bot.message_handler(func=lambda message: True)
def reply(message):
    print(f"Processing message: {message.text}") # This will show in Vercel logs
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\n{message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}") # This will show in Vercel logs
        bot.reply_to(message, "Elite Digital is optimizing...")

if __name__ == '__main__':
    app.run()
