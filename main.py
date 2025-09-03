import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading
import os
import time
from datetime import datetime

# Токен бота
API_TOKEN = '8214260739:AAEfatPbnC7ZpcO2LckO7QM10EbgvGxemO0'

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Создаем Flask приложение
app = Flask(__name__)

# Контакты и ссылки
ADMIN_TG = "xricexx"
DONATION_ALERTS_URL = "https://www.donationalerts.com/r/lites_man"
PAYMENT_AMOUNT = 200

# Хранилище для данных пользователей
user_data = {}

# Функции для логирования пользователей
def log_user(user_id, username, first_name, last_name, action="joined"):
    """Записывает пользователя в txt файл"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    user_info = f"[{timestamp}] ID: {user_id}"
    if username:
        user_info += f" | @{username}"
    if first_name:
        user_info += f" | Name: {first_name}"
    if last_name:
        user_info += f" {last_name}"
    user_info += f" | Action: {action}"
    
    with open('users.txt', 'a', encoding='utf-8') as f:
        f.write(user_info + '\n')
    
    return True

def get_total_users():
    """Считает общее количество пользователей"""
    if not os.path.exists('users.txt'):
        return 0
    
    with open('users.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    user_ids = set()
    for line in lines:
        if 'ID:' in line:
            parts = line.split('ID:')
            if len(parts) > 1:
                user_id = parts[1].split()[0].strip()
                user_ids.add(user_id)
    
    return len(user_ids)

def get_recent_users(limit=10):
    """Возвращает последних пользователей"""
    if not os.path.exists('users.txt'):
        return []
    
    with open('users.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    return lines[-limit:] if lines else []

# Клавиатура выбора языка
def language_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇬🇧 English"))
    return markup

# Клавиатура главного меню
def main_menu_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        markup.add(KeyboardButton("💰 Заработать"), KeyboardButton("💳 Купить 'Весь пак'"))
        markup.add(KeyboardButton("📊 Статистика"), KeyboardButton("📜 Политика"))
        markup.add(KeyboardButton("🌐 Сменить язык"))
    else:
        markup.add(KeyboardButton("💰 Earn Money"), KeyboardButton("💳 Buy 'Full Pack'"))
        markup.add(KeyboardButton("📊 Statistics"), KeyboardButton("📜 Policy"))
        markup.add(KeyboardButton("🌐 Change Language"))
    return markup

# Клавиатура выбора типа заработка
def earning_type_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        markup.add(KeyboardButton("⚖️ Легальный"), KeyboardButton("⚡ Нелегальный"))
        markup.add(KeyboardButton("🔙 Назад"))
    else:
        markup.add(KeyboardButton("⚖️ Legal"), KeyboardButton("⚡ Illegal"))
        markup.add(KeyboardButton("🔙 Back"))
    return markup

# Клавиатура легальных методов
def legal_methods_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        markup.add(KeyboardButton("🔄 NFT перепродажа"), KeyboardButton("📊 Крипто арбитраж"))
        markup.add(KeyboardButton("🔙 Назад"))
    else:
        markup.add(KeyboardButton("🔄 NFT resale"), KeyboardButton("📊 Crypto arbitrage"))
        markup.add(KeyboardButton("🔙 Back"))
    return markup

# Клавиатура выбора пакета
def package_type_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        markup.add(KeyboardButton("⚖️ Легальный пак"), KeyboardButton("⚡ Нелегальный пак"))
        markup.add(KeyboardButton("🔙 Назад"))
    else:
        markup.add(KeyboardButton("⚖️ Legal pack"), KeyboardButton("⚡ Illegal pack"))
        markup.add(KeyboardButton("🔙 Back"))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    log_user(user_id, username, first_name, last_name, "started bot")
    
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
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    if message.text == "🇷🇺 Русский":
        user_data[chat_id] = {'lang': 'ru', 'premium': False}
        response = "✅ Отлично! Вы выбрали русский язык.\n\nВыберите действие:"
        markup = main_menu_keyboard('ru')
        log_user(user_id, username, first_name, last_name, "chose Russian")
    else:
        user_data[chat_id] = {'lang': 'en', 'premium': False}
        response = "✅ Great! You've chosen English.\n\nChoose action:"
        markup = main_menu_keyboard('en')
        log_user(user_id, username, first_name, last_name, "chose English")
    
    bot.send_message(chat_id, response, reply_markup=markup)

# Обработчик команды /stats (для админа)
@bot.message_handler(commands=['stats'])
def show_stats(message):
    user_id = message.from_user.id
    
    # Замени 123456789 на свой Telegram ID
    if user_id != 123456789:
        lang = user_data.get(message.chat.id, {}).get('lang', 'ru')
        response = "❌ Эта команда только для админа" if lang == 'ru' else "❌ This command is for admin only"
        bot.send_message(message.chat.id, response)
        return
    
    total_users = get_total_users()
    recent_users = get_recent_users(5)
    
    stats_text = f"📊 Статистика бота:\n\n"
    stats_text += f"👥 Всего пользователей: {total_users}\n"
    stats_text += f"🕒 Последние 5 записей:\n\n"
    
    for user in recent_users:
        stats_text += f"• {user}"
    
    bot.send_message(message.chat.id, stats_text)

# Обработчик главного меню
@bot.message_handler(func=lambda message: message.text in [
    "💰 Заработать", "💳 Купить 'Весь пак'", "📊 Статистика", "📜 Политика", "🌐 Сменить язык",
    "💰 Earn Money", "💳 Buy 'Full Pack'", "📊 Statistics", "📜 Policy", "🌐 Change Language"
])
def handle_main_menu(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["💰 Заработать", "💰 Earn Money"]:
        response = "Выберите тип заработка:" if lang == 'ru' else "Choose earning type:"
        bot.send_message(chat_id, response, reply_markup=earning_type_keyboard(lang))
        log_user(user_id, username, first_name, last_name, "clicked earn money")
        
    elif message.text in ["💳 Купить 'Весь пак'", "💳 Buy 'Full Pack'"]:
        response = "Выберите тип пакета:" if lang == 'ru' else "Choose package type:"
        bot.send_message(chat_id, response, reply_markup=package_type_keyboard(lang))
        log_user(user_id, username, first_name, last_name, "clicked buy package")
        
    elif message.text in ["📊 Статистика", "📊 Statistics"]:
        total_users = get_total_users()
        if lang == 'ru':
            text = f"📊 Статистика бота:\n\n👥 Всего пользователей: {total_users}"
        else:
            text = f"📊 Bot statistics:\n\n👥 Total users: {total_users}"
        bot.send_message(chat_id, text)
        log_user(user_id, username, first_name, last_name, "viewed statistics")
        
    elif message.text in ["📜 Политика", "📜 Policy"]:
        if lang == 'ru':
            text = f"""
📜 ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ

Создатель бота (@{ADMIN_TG}) не несет ответственности за ваши действия.

Вся информация предоставлена в образовательных целях.
"""
        else:
            text = f"""
📜 PRIVACY POLICY

Bot creator (@{ADMIN_TG}) is not responsible for your actions.

All information is provided for educational purposes.
"""
        bot.send_message(chat_id, text)
        log_user(user_id, username, first_name, last_name, "viewed policy")
        
    elif message.text in ["🌐 Сменить язык", "🌐 Change Language"]:
        response = "Выберите язык:" if lang == 'ru' else "Choose language:"
        bot.send_message(chat_id, response, reply_markup=language_keyboard())
        log_user(user_id, username, first_name, last_name, "changed language")

# Обработчик выбора типа заработка
@bot.message_handler(func=lambda message: message.text in [
    "⚖️ Легальный", "⚡ Нелегальный", "🔙 Назад",
    "⚖️ Legal", "⚡ Illegal", "🔙 Back"
])
def handle_earning_type(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["🔙 Назад", "🔙 Back"]:
        response = "Главное меню:" if lang == 'ru' else "Main menu:"
        bot.send_message(chat_id, response, reply_markup=main_menu_keyboard(lang))
        log_user(user_id, username, first_name, last_name, "went back to main menu")
        
    elif message.text in ["⚖️ Легальный", "⚖️ Legal"]:
        response = "Выберите легальный метод:" if lang == 'ru' else "Choose legal method:"
        bot.send_message(chat_id, response, reply_markup=legal_methods_keyboard(lang))
        log_user(user_id, username, first_name, last_name, "chose legal earning")
        
    elif message.text in ["⚡ Нелегальный", "⚡ Illegal"]:
        if lang == 'ru':
            text = """
⚡ НЕЛЕГАЛЬНЫЙ МЕТОД ЗАРАБОТКА

💰 ВАШ ЗАРАБОТОК: 1500-2500₽ в день

📋 КРАТКОЕ РУКОВОДСТВО:

1️⃣ СОЗДАНИЕ АККАУНТА:
• Используйте фейковые данные
• Качественные фото из Google
• Придумайте легенду

2️⃣ ПОИСК ЦЕЛЕЙ:
• Девушки с Telegram Premium
• NFT в профиле
• Дорогие подарки

3️⃣ ОБЩЕНИЕ:
• Комплименты внешности
• Создание доверия
• Поиск уязвимостей

⚠️ ОГРАНИЧЕНИЯ БЕСПЛАТНОЙ ВЕРСИИ:
• Нет доступ к базам данных
• Без готовых шаблонов
• Высокие риски

💳 Для полного доступа купите «Нелегальный пак»!
"""
        else:
            text = """
⚡ ILLEGAL EARNING METHOD

💰 YOUR EARNINGS: $30-50 per day

📋 QUICK GUIDE:

1️⃣ ACCOUNT CREATION:
• Use fake data
• Quality photos from Google
• Create a legend

2️⃣ TARGET SEARCH:
• Girls with Telegram Premium
• NFT in profile
• Expensive gifts

3️⃣ COMMUNICATION:
• Appearance compliments
• Trust building
• Vulnerability search

⚠️ FREE VERSION LIMITATIONS:
• No database access
• No ready templates
• High risks

💳 Buy «Illegal Pack» for full access!
"""
        bot.send_message(chat_id, text)
        log_user(user_id, username, first_name, last_name, "chose illegal earning")

# Обработчик легальных методов
@bot.message_handler(func=lambda message: message.text in [
    "🔄 NFT перепродажа", "📊 Крипто арбитраж", "🔙 Назад",
    "🔄 NFT resale", "📊 Crypto arbitrage", "🔙 Back"
])
def handle_legal_methods(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["🔙 Назад", "🔙 Back"]:
        response = "Выберите тип заработка:" if lang == 'ru' else "Choose earning type:"
        bot.send_message(chat_id, response, reply_markup=earning_type_keyboard(lang))
        log_user(user_id, username, first_name, last_name, "went back to earning type")
        
    elif message.text in ["🔄 NFT перепродажа", "🔄 NFT resale"]:
        if lang == 'ru':
            text = """
🔄 NFT ПЕРЕПРОДАЖА - ЛЕГАЛЬНЫЙ МЕТОД

💰 Доход: 500-2000₽ в день

📋 КАК РАБОТАЕТ:
1. Покупаете NFT по низкой цене
2. Ждете повышения стоимости
3. Продаете по высокой цене
4. Получаете прибыль

🎯 ПЛАТФОРМЫ ДЛЯ ТОРГОВЛИ:
• OpenSea
• Rarible
• Magic Eden
• Binance NFT

📊 СТРАТЕГИИ:
• Покупать новые коллекции
• Следить за трендами
• Использовать аналитические инструменты
• Диверсифицировать портфель

⚡ СТАРТОВЫЙ КАПИТАЛ: от 1000₽
"""
        else:
            text = """
🔄 NFT RESALE - LEGAL METHOD

💰 Income: $10-40 per day

📋 HOW IT WORKS:
1. Buy NFT at low price
2. Wait for price increase
3. Sell at high price
4. Get profit

🎯 TRADING PLATFORMS:
• OpenSea
• Rarible
• Magic Eden
• Binance NFT

📊 STRATEGIES:
• Buy new collections
• Follow trends
• Use analytical tools
• Diversify portfolio

⚡ STARTING CAPITAL: from $20
"""
        bot.send_message(chat_id, text)
        log_user(user_id, username, first_name, last_name, "viewed NFT resale")
        
    elif message.text in ["📊 Крипто арбитраж", "📊 Crypto arbitrage"]:
        if lang == 'ru':
            text = """
📊 КРИПТО АРБИТРАЖ - ЛЕГАЛЬНЫЙ МЕТОД

💰 Доход: 300-1500₽ в день

📋 СУТЬ МЕТОДА:
Покупка криптовалюты на одной бирже по низкой цене
и мгновенная продажа на другой бирже по высокой цене

🎯 БИРЖИ ДЛЯ АРБИТРАЖА:
• Binance
• Bybit
• KuCoin
• Huobi
• OKX

⚡ АВТОМАТИЗАЦИЯ:
• Используйте ботов для арбитража
• Настройте API ключи
• Мониторьте разницы цен
• Быстрые переводы между биржами
"""
        else:
            text = """
📊 CRYPTO ARBITRAGE - LEGAL METHOD

💰 Income: $6-30 per day

📋 METHOD ESSENCE:
Buying cryptocurrency on one exchange at low price
and instant selling on another exchange at high price

🎯 ARBITRAGE EXCHANGES:
• Binance
• Bybit
• KuCoin
• Huobi
• OKX

⚡ AUTOMATION:
• Use arbitrage bots
• Set up API keys
• Monitor price differences
• Fast transfers between exchanges
"""
        bot.send_message(chat_id, text)
        log_user(user_id, username, first_name, last_name, "viewed crypto arbitrage")

# Обработчик выбора пакета
@bot.message_handler(func=lambda message: message.text in [
    "⚖️ Легальный пак", "⚡ Нелегальный пак", "🔙 Назад",
    "⚖️ Legal pack", "⚡ Illegal pack", "🔙 Back"
])
def handle_package_type(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["🔙 Назад", "🔙 Back"]:
        response = "Главное меню:" if lang == 'ru' else "Main menu:"
        bot.send_message(chat_id, response, reply_markup=main_menu_keyboard(lang))
        log_user(user_id, username, first_name, last_name, "went back to main menu")
        
    elif message.text in ["⚖️ Легальный пак", "⚖️ Legal pack"]:
        if lang == 'ru':
            text = f"""
💳 ЛЕГАЛЬНЫЙ ПАКЕТ - {PAYMENT_AMOUNT}₽

🎯 ЧТО ВХОДИТ:
• Полные инструкции по NFT перепродаже
• Крипто арбитраж стратегии
• Автоматические торговые боты
• Доступ к аналитическим инструментам
• Обучение risk management

📊 ОЖИДАЕМЫЙ ДОХОД:
• 500-2000₽ в день
• 15 000-60 000₽ в месяц
• Полная легальность
• Низкие риски

💰 СТАРТОВЫЙ КАПИТАЛ: от 5000₽

📋 ИНСТРУКЦИЯ ПО ОПЛАТЕ:
1. Перейдите: {DONATION_ALERTS_URL}
2. Сумма: {PAYMENT_AMOUNT}₽
3. Напишите админу: @{ADMIN_TG}
"""
        else:
            text = f"""
💳 LEGAL PACK - {PAYMENT_AMOUNT}₽

🎯 WHAT'S INCLUDED:
• Complete NFT resale instructions
• Crypto arbitrage strategies
• Automatic trading bots
• Access to analytical tools
• Risk management training

📊 EXPECTED INCOME:
• $10-40 per day
• $300-1200 per month
• Complete legality
• Low risks

💰 STARTING CAPITAL: from $100

📋 PAYMENT INSTRUCTIONS:
1. Go to: {DONATION_ALERTS_URL}
2. Amount: {PAYMENT_AMOUNT}₽
3. Write to admin: @{ADMIN_TG}
"""
        bot.send_message(chat_id, text)
        log_user(user_id, username, first_name, last_name, "viewed legal pack")
        
    elif message.text in ["⚡ Нелегальный пак", "⚡ Illegal pack"]:
        if lang == 'ru':
            text = f"""
💳 НЕЛЕГАЛЬНЫЙ ПАКЕТ - {PAYMENT_AMOUNT}₽

🎯 ЧТО ВХОДИТ:
• Полное руководство по скаму девушек
• Базы данных богатых девушек
• Шаблоны сообщений для обмана
• Фишинг ссылки и методы
• Инструкции по безопасности
• Схемы вывода средств

📊 ОЖИДАЕМЫЙ ДОХОД:
• 1500-2500₽ в день
• 45 000-75 000₽ в месяц
• Высокие риски
• Нелегальная деятельность

⚠️ ПРЕДУПРЕЖДЕНИЕ:
Этот метод нарушает законы. Вы действуете на свой страх и риск.

📋 ИНСТРУКЦИЯ ПО ОПЛАТЕ:
1. Перейдите: {DONATION_ALERTS_URL}
2. Сумма: {PAYMENT_AMOUNT}₽
3. Напишите админу: @{ADMIN_TG}
"""
        else:
            text = f"""
💳 ILLEGAL PACK - {PAYMENT_AMOUNT}₽

🎯 WHAT'S INCLUDED:
• Complete guide to scamming girls
• Databases of rich girls
• Message templates for deception
• Phishing links and methods
• Security instructions
• Money withdrawal schemes

📊 EXPECTED INCOME:
• $30-50 per day
• $900-1500 per month
• High risks
• Illegal activity

⚠️ WARNING:
This method violates laws. You act at your own risk.

📋 PAYMENT INSTRUCTIONS:
1. Go to: {DONATION_ALERTS_URL}
2. Amount: {PAYMENT_AMOUNT}₽
3. Write to admin: @{ADMIN_TG}
"""
        bot.send_message(chat_id, text)
        log_user(user_id, username, first_name, last_name, "viewed illegal pack")

# Обработчик для всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    log_user(user_id, username, first_name, last_name, "sent message")
    
    if chat_id in user_data:
        lang = user_data[chat_id]['lang']
        response = "Используйте кнопки меню для навигации 😊" if lang == 'ru' else "Use menu buttons for navigation 😊"
    else:
        response = "Пожалуйста, выберите язык / Please choose language:"
    bot.send_message(chat_id, response)

# Маршрут для Flask
@app.route('/')
def home():
    return "🤖 Telegram Bot is running!"

@app.route('/stats')
def web_stats():
    total_users = get_total_users()
    return f"Total users: {total_users}"

# Функция для запуска бота
def run_bot():
    print("🤖 Бот запускается...")
    print(f"📁 Файл users.txt будет создан в: {os.path.abspath('users.txt')}")
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
    print(f"🌐 Web server started on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
