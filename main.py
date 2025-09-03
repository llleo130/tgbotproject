import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os

# Токен бота
API_TOKEN = '8214260739:AAEfatPbnC7ZpcO2LckO7QM10EbgvGxemO0'

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Создаем Flask приложение
app = Flask(__name__)

# Хранилище для данных пользователей
user_data = {}

# Клавиатура выбора языка
def language_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇬🇧 English"))
    return markup

# Клавиатура выбора метода заработка
def earning_method_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        markup.add(KeyboardButton("🎁 NFT подарки"), KeyboardButton("💎 Telegram подарки"))
        markup.add(KeyboardButton("🔙 Назад"))
    else:
        markup.add(KeyboardButton("🎁 NFT Gifts"), KeyboardButton("💎 Telegram Gifts"))
        markup.add(KeyboardButton("🔙 Back"))
    return markup

# Клавиатура главного меню
def main_menu_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        markup.add(KeyboardButton("💰 Заработок"), KeyboardButton("📊 Статистика"))
        markup.add(KeyboardButton("🎓 Обучение"), KeyboardButton("🌐 Сменить язык"))
    else:
        markup.add(KeyboardButton("💰 Earn Money"), KeyboardButton("📊 Statistics"))
        markup.add(KeyboardButton("🎓 Tutorial"), KeyboardButton("🌐 Change Language"))
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
        user_data[chat_id] = {'lang': 'ru', 'balance': 0}
        response = "Отлично! Вы выбрали русский язык. 🇷🇺\n\nВыберите действие:"
        markup = main_menu_keyboard('ru')
    else:
        user_data[chat_id] = {'lang': 'en', 'balance': 0}
        response = "Great! You've chosen English. 🇬🇧\n\nChoose action:"
        markup = main_menu_keyboard('en')
    
    bot.send_message(chat_id, response, reply_markup=markup)

# Обработчик главного меню
@bot.message_handler(func=lambda message: message.text in [
    "💰 Заработок", "📊 Статистика", "🎓 Обучение", "🌐 Сменить язык",
    "💰 Earn Money", "📊 Statistics", "🎓 Tutorial", "🌐 Change Language"
])
def handle_main_menu(message):
    chat_id = message.chat.id
    lang = user_data.get(chat_id, {}).get('lang', 'ru')
    
    if message.text in ["💰 Заработок", "💰 Earn Money"]:
        response = "🎯 Выберите метод заработка:" if lang == 'ru' else "🎯 Choose earning method:"
        bot.send_message(chat_id, response, reply_markup=earning_method_keyboard(lang))
        
    elif message.text in ["📊 Статистика", "📊 Statistics"]:
        balance = user_data.get(chat_id, {}).get('balance', 0)
        response = f"📊 Ваш баланс: {balance}₽" if lang == 'ru' else f"📊 Your balance: ${balance}"
        bot.send_message(chat_id, response)
        
    elif message.text in ["🎓 Обучение", "🎓 Tutorial"]:
        send_tutorial(chat_id, lang)
        
    elif message.text in ["🌐 Сменить язык", "🌐 Change Language"]:
        response = "Выберите язык:" if lang == 'ru' else "Choose language:"
        bot.send_message(chat_id, response, reply_markup=language_keyboard())

# Обработчик методов заработка
@bot.message_handler(func=lambda message: message.text in [
    "🎁 NFT подарки", "💎 Telegram подарки", "🔙 Назад",
    "🎁 NFT Gifts", "💎 Telegram Gifts", "🔙 Back"
])
def handle_earning_methods(message):
    chat_id = message.chat.id
    lang = user_data.get(chat_id, {}).get('lang', 'ru')
    
    if message.text in ["🔙 Назад", "🔙 Back"]:
        response = "Главное меню:" if lang == 'ru' else "Main menu:"
        bot.send_message(chat_id, response, reply_markup=main_menu_keyboard(lang))
        
    elif message.text in ["🎁 NFT подарки", "🎁 NFT Gifts"]:
        send_nft_tutorial(chat_id, lang)
        
    elif message.text in ["💎 Telegram подарки", "💎 Telegram Gifts"]:
        send_telegram_tutorial(chat_id, lang)

# Обучение NFT
def send_nft_tutorial(chat_id, lang):
    if lang == 'ru':
        steps = [
            "🎯 NFT Заработок - Пошаговое руководство:\n\n1️⃣ Первый шаг:",
            "Зайдите на сайт diving.io и создайте фейковый аккаунт\nИспользуйте временную почту и случайные данные",
            "2️⃣ Второй шаг:\nНапишите 10-15 девушкам в день с предложением получить NFT подарок\nТекст: 'Привет! Хочешь получить эксклюзивный NFT в подарок? 🎁'",
            "3️⃣ Третий шаг:\nОбщайтесь 10-15 минут, создайте доверительные отношения",
            "4️⃣ Четвертый шаг:\nНачните мягко угрожать: 'Если не заберешь подарок в течение часа, аккаунт будет удален системой'",
            "5️⃣ Пятый шаг:\nКогда они согласятся, направьте их на платформу для 'получения подарка' (на самом деле - фишинг)",
            "⚠️ ВАЖНО: Используйте VPN и одноразовые аккаунты. Не нарушайте законы!"
        ]
    else:
        steps = [
            "🎯 NFT Earnings - Step by Step Guide:\n\n1️⃣ First step:",
            "Go to diving.io and create a fake account\nUse temporary email and random data",
            "2️⃣ Second step:\nWrite to 10-15 girls per day offering NFT gift\nText: 'Hi! Want to get an exclusive NFT gift? 🎁'",
            "3️⃣ Third step:\nChat for 10-15 minutes, build trust relationships",
            "4️⃣ Fourth step:\nStart soft threats: 'If you don't claim the gift within an hour, your account will be deleted by the system'",
            "5️⃣ Fifth step:\nWhen they agree, direct them to the 'gift claiming' platform (actually phishing)",
            "⚠️ IMPORTANT: Use VPN and disposable accounts. Don't break laws!"
        ]
    
    for step in steps:
        bot.send_message(chat_id, step)
        import time
        time.sleep(2)

# Обучение Telegram подаркам
def send_telegram_tutorial(chat_id, lang):
    if lang == 'ru':
        steps = [
            "💎 Telegram Подарки - Пошаговое руководство:\n\n1️⃣ Первый шаг:",
            "Создайте привлекательный фейковый аккаунт с красивой аватаркой\nКупите Premium на 1 месяц для доверия",
            "2️⃣ Второй шаг:\nИщите богатых пользователей в Premium чатах\nПишите: 'Привет! Тебе пришел подарок от Telegram 🎁'",
            "3️⃣ Третий шаг:\nОбщайтесь 5-10 минут, объясните что они выиграли бонус",
            "4️⃣ Четвертый шаг:\nСкажите: 'Чтобы получить подарок, нужно подтвердить аккаунт вот по этой ссылке...'",
            "5️⃣ Пятый шаг:\nИспользуйте фишинг страницу для сбора данных\nПосле получения данных - заблокируйте пользователя",
            "⚡ СОВЕТ: Меняйте аккаунты каждые 2-3 дня. Используйте разные подходы!"
        ]
    else:
        steps = [
            "💎 Telegram Gifts - Step by Step Guide:\n\n1️⃣ First step:",
            "Create attractive fake account with beautiful avatar\nBuy Premium for 1 month for trust",
            "2️⃣ Second step:\nLook for rich users in Premium chats\nWrite: 'Hi! You received a gift from Telegram 🎁'",
            "3️⃣ Third step:\nChat for 5-10 minutes, explain they won a bonus",
            "4️⃣ Fourth step:\nSay: 'To receive the gift, you need to verify your account via this link...'",
            "5️⃣ Fifth step:\nUse phishing page to collect data\nAfter getting data - block the user",
            "⚡ TIP: Change accounts every 2-3 days. Use different approaches!"
        ]
    
    for step in steps:
        bot.send_message(chat_id, step)
        import time
        time.sleep(2)

# Общее обучение
def send_tutorial(chat_id, lang):
    if lang == 'ru':
        text = """
🎓 ПОЛНОЕ ОБУЧЕНИЕ:

📌 Основные принципы:
• Используйте VPN (NordVPN, ExpressVPN)
• Создавайте фейковые аккаунты
• Меняйте подходы регулярно
• Не жадничайте - лучше много мелких жертв

📌 Безопасность:
• Никогда не используйте личные данные
• Очищайте кэш браузера
• Используйте антидетект браузеры
• Работайте через прокси

📌 Эффективные методы:
1. Массовая рассылка (100+ сообщений в день)
2. Целевой подход (богатые пользователи)
3. Социальная инженерия
4. Фишинг через 'официальные' предложения

⚠️ ВНИМАНИЕ: Это образовательная информация. Не нарушайте законы!
"""
    else:
        text = """
🎓 COMPLETE TUTORIAL:

📌 Basic principles:
• Use VPN (NordVPN, ExpressVPN)
• Create fake accounts
• Change approaches regularly
• Don't be greedy - better many small victims

📌 Security:
• Never use personal data
• Clear browser cache
• Use anti-detect browsers
• Work through proxies

📌 Effective methods:
1. Mass mailing (100+ messages per day)
2. Targeted approach (rich users)
3. Social engineering
4. Phishing through 'official' offers

⚠️ WARNING: This is educational information. Don't break laws!
"""
    
    bot.send_message(chat_id, text)

# Обработчик для всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        lang = user_data[chat_id]['lang']
        response = "Используйте кнопки меню 😊" if lang == 'ru' else "Use menu buttons 😊"
    else:
        response = "Пожалуйста, выберите язык / Please choose language:"
    bot.send_message(chat_id, response)

# Маршрут для Flask
@app.route('/')
def home():
    return "🤖 Telegram Bot is running on Scalingo!"

# Функция для запуска бота
def run_bot():
    print("🤖 Бот запускается...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# Запуск приложения
if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем Flask
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
