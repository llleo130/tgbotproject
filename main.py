import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
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

# Клавиатура главного меню
def main_menu_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        markup.add(KeyboardButton("💰 Заработать"), KeyboardButton("⭐ Мои звезды"))
        markup.add(KeyboardButton("🎓 Обучение"), KeyboardButton("🌐 Сменить язык"))
    else:
        markup.add(KeyboardButton("💰 Earn Money"), KeyboardButton("⭐ My Stars"))
        markup.add(KeyboardButton("🎓 Tutorial"), KeyboardButton("🌐 Change Language"))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
Привет! Добро пожаловать в систему заработка! 🇷🇺🇬🇧
Hello! Welcome to the earning system! 🇬🇧🇷🇺

Пожалуйста, выберите язык / Please choose your language:
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=language_keyboard())

# Обработчик выбора языка
@bot.message_handler(func=lambda message: message.text in ["🇷🇺 Русский", "🇬🇧 English"])
def handle_language_choice(message):
    chat_id = message.chat.id
    
    if message.text == "🇷🇺 Русский":
        user_data[chat_id] = {'lang': 'ru', 'stars': 0, 'balance': 0}
        response = "✅ Отлично! Вы выбрали русский язык.\n\nВыберите действие:"
        markup = main_menu_keyboard('ru')
    else:
        user_data[chat_id] = {'lang': 'en', 'stars': 0, 'balance': 0}
        response = "✅ Great! You've chosen English.\n\nChoose action:"
        markup = main_menu_keyboard('en')
    
    bot.send_message(chat_id, response, reply_markup=markup)

# Обработчик главного меню
@bot.message_handler(func=lambda message: message.text in [
    "💰 Заработать", "⭐ Мои звезды", "🎓 Обучение", "🌐 Сменить язык",
    "💰 Earn Money", "⭐ My Stars", "🎓 Tutorial", "🌐 Change Language"
])
def handle_main_menu(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["💰 Заработать", "💰 Earn Money"]:
        send_earning_guide(chat_id, lang)
        
    elif message.text in ["⭐ Мои звезды", "⭐ My Stars"]:
        stars = user_data[chat_id]['stars']
        if lang == 'ru':
            response = f"⭐ У вас {stars} звезд\n\nДля отправки подарка нужно 15 звезд 💎"
        else:
            response = f"⭐ You have {stars} stars\n\nYou need 15 stars to send a gift 💎"
        bot.send_message(chat_id, response)
        
    elif message.text in ["🎓 Обучение", "🎓 Tutorial"]:
        send_tutorial(chat_id, lang)
        
    elif message.text in ["🌐 Сменить язык", "🌐 Change Language"]:
        response = "Выберите язык:" if lang == 'ru' else "Choose language:"
        bot.send_message(chat_id, response, reply_markup=language_keyboard())

# Руководство по заработку
def send_earning_guide(chat_id, lang):
    if lang == 'ru':
        steps = [
            "🎯 ПОШАГОВОЕ РУКОВОДСТВО ПО ЗАРАБОТКУ:\n\n1️⃣ ПЕРВЫЙ ШАГ:",
            "📝 Создайте фейковый аккаунт в боте для знакомств:\n• Используйте привлекательное фото\n• Придумайте интересную биографию\n• Укажите случайные данные\n• Используйте временную почту",
            
            "2️⃣ ВТОРОЙ ШАГ:\n💌 Напишите 10-15 девушкам в день:\n\nТекст сообщения:\n\"Привет! Ты очень красивая! 😊 Хочешь пообщаться?\"",
            
            "3️⃣ ТРЕТИЙ ШАГ:\n🔍 Проверьте профиль девушки:\n• Есть ли у нее Telegram Premium?\n• Есть ли NFT в профиле?\n• Активна ли она?",
            
            "4️⃣ ЧЕТВЕРТЫЙ ШАГ:\n⚡ Если у девушки есть подарки:\n\nТекст угрозы:\n\"Я администратор системы. Твой аккаунт будет удален через 1 час из-за нарушения правил. Чтобы избежать этого, перейди по ссылке и подтверди аккаунт...\"",
            
            "5️⃣ ПЯТЫЙ ШАГ:\n🎁 После получения доступа:\n• Заблокируйте девушку\n• Переведите подарки на свой основной аккаунт\n• Очистите историю действий",
            
            "💎 ВАЖНО: Для отправки подарка нужно 15 звезд! Звезды можно получить за активность в системе."
        ]
    else:
        steps = [
            "🎯 STEP-BY-STEP EARNING GUIDE:\n\n1️⃣ FIRST STEP:",
            "📝 Create a fake account in a dating bot:\n• Use an attractive photo\n• Create an interesting biography\n• Provide random data\n• Use temporary email",
            
            "2️⃣ SECOND STEP:\n💌 Write to 10-15 girls per day:\n\nMessage text:\n\"Hi! You're very beautiful! 😊 Want to chat?\"",
            
            "3️⃣ THIRD STEP:\n🔍 Check the girl's profile:\n• Does she have Telegram Premium?\n• Does she have NFT in her profile?\n• Is she active?",
            
            "4️⃣ FOURTH STEP:\n⚡ If the girl has gifts:\n\nThreat text:\n\"I am the system administrator. Your account will be deleted in 1 hour due to rule violations. To avoid this, follow the link and verify your account...\"",
            
            "5️⃣ FIFTH STEP:\n🎁 After gaining access:\n• Block the girl\n• Transfer gifts to your main account\n• Clear activity history",
            
            "💎 IMPORTANT: You need 15 stars to send a gift! Stars can be earned through system activity."
        ]
    
    for step in steps:
        bot.send_message(chat_id, step)
        import time
        time.sleep(2)

# Обучение безопасности
def send_tutorial(chat_id, lang):
    if lang == 'ru':
        text = """
🔒 ОБУЧЕНИЕ БЕЗОПАСНОСТИ:

🛡️ Основные правила:
• Всегда используйте VPN (NordVPN, ExpressVPN)
• Создавайте новые аккаунты каждые 3 дня
• Никогда не используйте личные данные
• Очищайте кэш браузера после каждой сессии

📱 Рекомендуемые инструменты:
• Антидетект браузеры
• Временные номера телефонов
• Одноразовые email адреса
• Прокси серверы

⚡ Эффективные стратегии:
1. Массовая рассылка (100+ сообщений в день)
2. Целевой подход к Premium пользователям
3. Социальная инженерия
4. Фишинг через "официальные" уведомления

⭐ ЗВЕЗДНАЯ СИСТЕМА:
• 1 звезда = 1 день активности
• 15 звезд = возможность отправить подарок
• Звезды сбрасываются после отправки подарка

⚠️ ВНИМАНИЕ: Это образовательная информация. 
Не нарушайте законы вашей страны!
"""
    else:
        text = """
🔒 SECURITY TUTORIAL:

🛡️ Basic rules:
• Always use VPN (NordVPN, ExpressVPN)
• Create new accounts every 3 days
• Never use personal data
• Clear browser cache after each session

📱 Recommended tools:
• Anti-detect browsers
• Temporary phone numbers
• Disposable email addresses
• Proxy servers

⚡ Effective strategies:
1. Mass mailing (100+ messages per day)
2. Targeted approach to Premium users
3. Social engineering
4. Phishing through "official" notifications

⭐ STAR SYSTEM:
• 1 star = 1 day of activity
• 15 stars = ability to send a gift
• Stars reset after sending a gift

⚠️ WARNING: This is educational information. 
Do not break the laws of your country!
"""
    
    bot.send_message(chat_id, text)

# Обработчик для всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        lang = user_data[chat_id]['lang']
        response = "Используйте кнопки меню для навигации 😊" if lang == 'ru' else "Use menu buttons for navigation 😊"
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
