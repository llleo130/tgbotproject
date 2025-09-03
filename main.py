import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import threading
from flask import Flask

# Токен бота
API_TOKEN = '8214260739:AAF-99lkDfpMcjsx0ZE5n7tUgnwk1q7i7lY'

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Создаем Flask приложение для вебхука
app = Flask(__name__)

# Хранилище для выбора языка пользователей
user_language = {}

# Клавиатура выбора языка
def language_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇬🇧 English"))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
Привет! Добро пожаловать! 🇷🇺🇬🇧
Hello! Welcome! 🇬🇧🇷🇺

Пожалуйста, выберите язык / Please choose your language:
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=language_keyboard())

# Обработчик выбора языка
@bot.message_handler(func=lambda message: message.text in ["🇷🇺 Русский", "🇬🇧 English"])
def handle_language_choice(message):
    chat_id = message.chat.id
    
    if message.text == "🇷🇺 Русский":
        user_language[chat_id] = 'ru'
        response = "Отлично! Вы выбрали русский язык. 🇷🇺\n\nБот теперь готов к работе!"
        
        # Создаем основную клавиатуру для русского языка
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("ℹ️ Информация"), KeyboardButton("⚙️ Настройки"))
        markup.add(KeyboardButton("🔁 Сменить язык"))
        
    else:  # English
        user_language[chat_id] = 'en'
        response = "Great! You've chosen English. 🇬🇧\n\nThe bot is now ready!"
        
        # Создаем основную клавиатуру для английского языка
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("ℹ️ Info"), KeyboardButton("⚙️ Settings"))
        markup.add(KeyboardButton("🔁 Change language"))
    
    bot.send_message(chat_id, response, reply_markup=markup)

# Обработчик для основных команд на русском
@bot.message_handler(func=lambda message: message.text in ["ℹ️ Информация", "⚙️ Настройки", "🔁 Сменить язык"])
def handle_russian_commands(message):
    chat_id = message.chat.id
    
    if message.text == "ℹ️ Информация":
        bot.send_message(chat_id, "📚 Это информационное сообщение.\nБот работает стабильно! 🚀")
    
    elif message.text == "⚙️ Настройки":
        bot.send_message(chat_id, "⚙️ Раздел настроек в разработке...")
    
    elif message.text == "🔁 Сменить язык":
        bot.send_message(chat_id, "Выберите язык:", reply_markup=language_keyboard())

# Обработчик для основных команд на английском
@bot.message_handler(func=lambda message: message.text in ["ℹ️ Info", "⚙️ Settings", "🔁 Change language"])
def handle_english_commands(message):
    chat_id = message.chat.id
    
    if message.text == "ℹ️ Info":
        bot.send_message(chat_id, "📚 This is an information message.\nBot is working stable! 🚀")
    
    elif message.text == "⚙️ Settings":
        bot.send_message(chat_id, "⚙️ Settings section is under development...")
    
    elif message.text == "🔁 Change language":
        bot.send_message(chat_id, "Choose your language:", reply_markup=language_keyboard())

# Обработчик для всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    
    if chat_id in user_language:
        lang = user_language[chat_id]
        if lang == 'ru':
            bot.send_message(chat_id, "Я вас не понял. Используйте кнопки меню. 😊")
        else:
            bot.send_message(chat_id, "I didn't understand that. Please use the menu buttons. 😊")
    else:
        bot.send_message(chat_id, "Пожалуйста, сначала выберите язык / Please choose your language first:", 
                        reply_markup=language_keyboard())

# Вебхук для Flask (необязательно, но полезно для некоторых хостингов)
@app.route('/')
def home():
    return "Bot is running!"

# Функция для запуска бота
def run_bot():
    print("Бот запущен...")
    bot.infinity_polling()

# Запуск бота в отдельном потоке
if __name__ == "__main__":
    # Запускаем бота в фоновом режиме
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем Flask для веб-сервера
    print("Сервер запущен. Бот работает в фоне.")
    print("Теперь можно закрыть ноутбук - бот продолжит работать на сервере!")
    app.run(host='0.0.0.0', port=8080)