import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading
import os
import time

# Токен бота
API_TOKEN = '8214260739:AAEfatPbnC7ZpcO2LckO7QM10EbgvGxemO0'

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Создаем Flask приложение
app = Flask(__name__)

# Хранилище для данных пользователей
user_data = {}

# Контакты и ссылки
ADMIN_TG = "xricexx"
DATING_BOT_LINK = "https://t.me/divingbot"
DONATION_ALERTS_URL = "https://www.donationalerts.com/r/lites_man"
PAYMENT_AMOUNT_RUB = 200
PAYMENT_AMOUNT_USD = 5

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
        markup.add(KeyboardButton("📜 Политика"), KeyboardButton("🌐 Сменить язык"))
    else:
        markup.add(KeyboardButton("💰 Earn Money"), KeyboardButton("💳 Buy 'Full Pack'"))
        markup.add(KeyboardButton("📜 Policy"), KeyboardButton("🌐 Change Language"))
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

# Проверка оплаты
def check_payment(user_id):
    return False

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
        user_data[chat_id] = {'lang': 'ru', 'premium': False, 'payment_pending': False}
        response = "✅ Отлично! Вы выбрали русский язык.\n\nВыберите действие:"
        markup = main_menu_keyboard('ru')
    else:
        user_data[chat_id] = {'lang': 'en', 'premium': False, 'payment_pending': False}
        response = "✅ Great! You've chosen English.\n\nChoose action:"
        markup = main_menu_keyboard('en')
    
    bot.send_message(chat_id, response, reply_markup=markup)

# Обработчик главного меню
@bot.message_handler(func=lambda message: message.text in [
    "💰 Заработать", "💳 Купить 'Весь пак'", "📜 Политика", "🌐 Сменить язык",
    "💰 Earn Money", "💳 Buy 'Full Pack'", "📜 Policy", "🌐 Change Language"
])
def handle_main_menu(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["💰 Заработать", "💰 Earn Money"]:
        response = "Выберите тип заработка:" if lang == 'ru' else "Choose earning type:"
        bot.send_message(chat_id, response, reply_markup=earning_type_keyboard(lang))
        
    elif message.text in ["💳 Купить 'Весь пак'", "💳 Buy 'Full Pack'"]:
        response = "Выберите тип пакета:" if lang == 'ru' else "Choose package type:"
        bot.send_message(chat_id, response, reply_markup=package_type_keyboard(lang))
        
    elif message.text in ["📜 Политика", "📜 Policy"]:
        send_policy(chat_id, lang)
        
    elif message.text in ["🌐 Сменить язык", "🌐 Change Language"]:
        response = "Выберите язык:" if lang == 'ru' else "Choose language:"
        bot.send_message(chat_id, response, reply_markup=language_keyboard())

# Обработчик выбора типа заработка
@bot.message_handler(func=lambda message: message.text in [
    "⚖️ Легальный", "⚡ Нелегальный", "🔙 Назад",
    "⚖️ Legal", "⚡ Illegal", "🔙 Back"
])
def handle_earning_type(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["🔙 Назад", "🔙 Back"]:
        response = "Главное меню:" if lang == 'ru' else "Main menu:"
        bot.send_message(chat_id, response, reply_markup=main_menu_keyboard(lang))
        
    elif message.text in ["⚖️ Легальный", "⚖️ Legal"]:
        response = "Выберите легальный метод:" if lang == 'ru' else "Choose legal method:"
        bot.send_message(chat_id, response, reply_markup=legal_methods_keyboard(lang))
        
    elif message.text in ["⚡ Нелегальный", "⚡ Illegal"]:
        send_free_earning_guide(chat_id, lang)

# Обработчик легальных методов
@bot.message_handler(func=lambda message: message.text in [
    "🔄 NFT перепродажа", "📊 Крипто арбитраж", "🔙 Назад",
    "🔄 NFT resale", "📊 Crypto arbitrage", "🔙 Back"
])
def handle_legal_methods(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["🔙 Назад", "🔙 Back"]:
        response = "Выберите тип заработка:" if lang == 'ru' else "Choose earning type:"
        bot.send_message(chat_id, response, reply_markup=earning_type_keyboard(lang))
        
    elif message.text in ["🔄 NFT перепродажа", "🔄 NFT resale"]:
        send_nft_resale_guide(chat_id, lang)
        
    elif message.text in ["📊 Крипто арбитраж", "📊 Crypto arbitrage"]:
        send_crypto_arbitrage_guide(chat_id, lang)

# Обработчик выбора пакета
@bot.message_handler(func=lambda message: message.text in [
    "⚖️ Легальный пак", "⚡ Нелегальный пак", "🔙 Назад",
    "⚖️ Legal pack", "⚡ Illegal pack", "🔙 Back"
])
def handle_package_type(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, выберите язык / Please choose language:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if message.text in ["🔙 Назад", "🔙 Back"]:
        response = "Главное меню:" if lang == 'ru' else "Main menu:"
        bot.send_message(chat_id, response, reply_markup=main_menu_keyboard(lang))
        
    elif message.text in ["⚖️ Легальный пак", "⚖️ Legal pack"]:
        send_legal_package_info(chat_id, lang)
        
    elif message.text in ["⚡ Нелегальный пак", "⚡ Illegal pack"]:
        send_illegal_package_info(chat_id, lang)

# Руководство по NFT перепродаже
def send_nft_resale_guide(chat_id, lang):
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

💡 СОВЕТЫ:
• Начинайте с небольших сумм
• Изучайте whitepaper проектов
• Следите за соцсетями создателей
• Используйте stop-loss ордера
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

💡 TIPS:
• Start with small amounts
• Study project whitepapers
• Follow creators' social media
• Use stop-loss orders
"""
    bot.send_message(chat_id, text)

# Руководство по крипто арбитражу
def send_crypto_arbitrage_guide(chat_id, lang):
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

📈 ВИДЫ АРБИТРАЖА:
• Пространственный (между биржами)
• Временной (разное время)
• Статистический (алгоритмический)

💡 СТАРТОВЫЕ УСЛОВИЯ:
• Капитал: от 5000₽
• Знание английского
• Опыт торговли
• Быстрый интернет
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

📈 ARBITRAGE TYPES:
• Spatial (between exchanges)
• Temporal (different times)
• Statistical (algorithmic)

💡 STARTING CONDITIONS:
• Capital: from $100
• English knowledge
• Trading experience
• Fast internet
"""
    bot.send_message(chat_id, text)

# Информация о легальном пакете
def send_legal_package_info(chat_id, lang):
    user_data[chat_id]['payment_pending'] = True
    user_data[chat_id]['package_type'] = 'legal'
    
    if lang == 'ru':
        text = f"""
💳 ЛЕГАЛЬНЫЙ ПАКЕТ - {PAYMENT_AMOUNT_RUB}₽

🎯 ЧТО ВХОДИТ:
• Полные инструкции по NFT перепродаже
• Крипто арбитраж стратегии
• Автоматические торговые боты
• Доступ к аналитическим инструментам
• Обучение risk management
• Юридические консультации

📊 ОЖИДАЕМЫЙ ДОХОД:
• 500-2000₽ в день
• 15 000-60 000₽ в месяц
• Полная легальность
• Низкие риски

💰 СТАРТОВЫЙ КАПИТАЛ: от 5000₽

📋 ИНСТРУКЦИЯ ПО ОПЛАТЕ:
1. Перейдите: {DONATION_ALERTS_URL}
2. Сумма: {PAYMENT_AMOUNT_RUB}₽
3. Напишите админу: @{ADMIN_TG}

⚡ После оплаты получите:
• PDF руководства
• Видео уроки
• Доступ к чату
• Поддержку 24/7
"""
    else:
        text = f"""
💳 LEGAL PACK - ${PAYMENT_AMOUNT_USD}

🎯 WHAT'S INCLUDED:
• Complete NFT resale instructions
• Crypto arbitrage strategies
• Automatic trading bots
• Access to analytical tools
• Risk management training
• Legal consultations

📊 EXPECTED INCOME:
• $10-40 per day
• $300-1200 per month
• Complete legality
• Low risks

💰 STARTING CAPITAL: from $100

📋 PAYMENT INSTRUCTIONS:
1. Go to: {DONATION_ALERTS_URL}
2. Amount: {PAYMENT_AMOUNT_RUB}₽ (approx ${PAYMENT_AMOUNT_USD})
3. Write to admin: @{ADMIN_TG}

⚡ After payment get:
• PDF guides
• Video lessons
• Chat access
• 24/7 support
"""
    bot.send_message(chat_id, text)

# Информация о нелегальном пакете
def send_illegal_package_info(chat_id, lang):
    user_data[chat_id]['payment_pending'] = True
    user_data[chat_id]['package_type'] = 'illegal'
    
    if lang == 'ru':
        text = f"""
💳 НЕЛЕГАЛЬНЫЙ ПАКЕТ - {PAYMENT_AMOUNT_RUB}₽

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
2. Сумма: {PAYMENT_AMOUNT_RUB}₽
3. Напишите админу: @{ADMIN_TG}

⚡ После оплаты получите:
• Полные инструкции
• Базы данных
• Шаблоны сообщений
• Поддержку 24/7
"""
    else:
        text = f"""
💳 ILLEGAL PACK - ${PAYMENT_AMOUNT_USD}

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
2. Amount: {PAYMENT_AMOUNT_RUB}₽ (approx ${PAYMENT_AMOUNT_USD})
3. Write to admin: @{ADMIN_TG}

⚡ After payment get:
• Complete instructions
• Databases
• Message templates
• 24/7 support
"""
    bot.send_message(chat_id, text)

# Руководство по заработку (нелегальная версия)
def send_free_earning_guide(chat_id, lang):
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

# Политика конфиденциальности
def send_policy(chat_id, lang):
    if lang == 'ru':
        text = f"""
📜 ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ

⚠️ ВАЖНОЕ УВЕДОМЛЕНИЕ:

Создатель данного бота (@{ADMIN_TG}) не призывает и не заставляет пользователей зарабатывать деньги нелегальным способом. Вся представленная информация предназначена исключительно в образовательных целях.

Пользователь самостоятельно несет ответственность за свои действия и их последствия. Мы не одобряем и не поддерживаем незаконную деятельность.

🔒 Ваши данные: Мы не храним персональную информацию и данные платежей.

Вы используете бот на свой собственный риск.

📞 Контакты: @{ADMIN_TG}
"""
    else:
        text = f"""
📜 PRIVACY POLICY

⚠️ IMPORTANT NOTICE:

The creator of this bot (@{ADMIN_TG}) does not encourage or force users to earn money illegally. All information provided is for educational purposes only.

The user is solely responsible for their actions and their consequences. We do not approve or support illegal activities.

🔒 Your data: We do not store personal information and payment data.

You use the bot at your own risk.

📞 Contacts: @{ADMIN_TG}
"""
    bot.send_message(chat_id, text)

# Обработчик скриншотов оплаты
@bot.message_handler(content_types=['photo'])
def handle_payment_screenshot(message):
    chat_id = message.chat.id
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "Пожалуйста, сначала выберите язык / Please choose language first:", reply_markup=language_keyboard())
        return
        
    lang = user_data[chat_id]['lang']
    
    if user_data[chat_id]['payment_pending']:
        package_type = user_data[chat_id].get('package_type', 'illegal')
        
        if lang == 'ru':
            text = f"""
❌ Автопроверка оплаты не удалась!

📞 Напишите админу: @{ADMIN_TG}
Отправьте скриншот оплаты и ваш ID: {chat_id}

📦 Выбранный пакет: {'Легальный' if package_type == 'legal' else 'Нелегальный'}

⚡ После проверки получите доступ!
"""
        else:
            text = f"""
❌ Automatic payment check failed!

📞 Write to admin: @{ADMIN_TG}
Send payment screenshot and your ID: {chat_id}

📦 Selected package: {'Legal' if package_type == 'legal' else 'Illegal'}

⚡ Get access after verification!
"""
        
        bot.send_message(chat_id, text)
        user_data[chat_id]['payment_pending'] = False
    else:
        response = "Сначала выберите пакет" if lang == 'ru' else "First choose package"
        bot.send_message(chat_id, response)

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
