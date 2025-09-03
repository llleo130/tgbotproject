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
PAYMENT_AMOUNT = 200

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

# Проверка оплаты - всегда требует подтверждения через админа
def check_payment(user_id):
    # Всегда возвращаем False, чтобы пользователь писал админу
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
    premium = user_data[chat_id]['premium']
    
    if message.text in ["💰 Заработать", "💰 Earn Money"]:
        if premium:
            send_premium_earning_guide(chat_id, lang)
        else:
            send_free_earning_guide(chat_id, lang)
        
    elif message.text in ["💳 Купить 'Весь пак'", "💳 Buy 'Full Pack'"]:
        send_payment_instructions(chat_id, lang)
        
    elif message.text in ["📜 Политика", "📜 Policy"]:
        send_policy(chat_id, lang)
        
    elif message.text in ["🌐 Сменить язык", "🌐 Change Language"]:
        response = "Выберите язык:" if lang == 'ru' else "Choose language:"
        bot.send_message(chat_id, response, reply_markup=language_keyboard())

# Руководство по заработку (бесплатная версия)
def send_free_earning_guide(chat_id, lang):
    if lang == 'ru':
        text = f"""
🎯 БЕСПЛАТНОЕ РУКОВОДСТВО:

1️⃣ Создайте фейковый аккаунт в ботах для знакомств
2️⃣ Пишите девушкам комплименты
3️⃣ Ищите тех, у кого есть подарки в профиле

⚠️ ОГРАНИЧЕНИЯ БЕСПЛАТНОЙ ВЕРСИИ:
• Нет доступа к премиум-базам данных
• Ограниченное количество сообщений
• Без гарантии результата

💳 Для полного доступа купите «Весь пак» за {PAYMENT_AMOUNT} рублей!

📞 После оплаты напишите админу: @{ADMIN_TG}
"""
    else:
        text = f"""
🎯 FREE GUIDE:

1️⃣ Create a fake account in dating bots
2️⃣ Write compliments to girls
3️⃣ Look for those who have gifts in their profile

⚠️ FREE VERSION LIMITATIONS:
• No access to premium databases
• Limited number of messages
• No result guarantee

💳 Buy «Full Pack» for {PAYMENT_AMOUNT} rubles for full access!

📞 After payment write to admin: @{ADMIN_TG}
"""
    bot.send_message(chat_id, text)

# Руководство по заработку (премиум версия)
def send_premium_earning_guide(chat_id, lang):
    if lang == 'ru':
        text = f"""
🎯 ПРЕМИУМ РУКОВОДСТВО (ВЕСЬ ПАК):

💰 ВАШ ЗАРАБОТОК: 500-2000₽ в день

📋 ПОЛНЫЙ ПЛАН ДЕЙСТВИЙ:

1️⃣ СОЗДАНИЕ АККАУНТА:
• Перейдите: {DATING_BOT_LINK}
• Используйте фото пацана из Google (красивый парень)
• Имя: Максим, 24 года
• Био: "Ищу серьезные отношения 💍"

2️⃣ ПОИСК ЦЕЛЕЙ:
• База №1: @rich_girls_base
• База №2: @millionaire_dating
• База №3: @premium_girls_chat
• Ищите девушек с 💎 в нике

3️⃣ СООБЩЕНИЯ ДЛЯ РАЗНЫХ СИТУАЦИЙ:

💌 Первое сообщение:
"Привет! Ты очень красивая! 😊 Как твои дела?"

💬 Если отвечает:
"Рада, что ответила! У тебя такой стильный профиль, видно что с вкусом 💫"

🎯 Если видит подарки:
"Ого, у тебя столько подарков! Как тебе удается?"

4️⃣ ФИНАЛЬНЫЙ ЭТАП (СКАМ):
• После 10-15 минут общения
• "Кстати, я администратор системы, твой аккаунт могут удалить из-за подозрительной активности"
• "Перейди по ссылке для проверки: [фишинг ссылка]"
• После получения доступа - блокируем девушку

5️⃣ БЕЗОПАСНОСТЬ:
• Используйте: @hideipbot
• Меняйте аккаунты каждые 3 дня
• Никогда не переводите на свои карты

📊 ПРЕМИУМ БАЗЫ ДЛЯ РАБОТЫ:
• @rich_dating_rus
• @premium_dating_offical
• @gifts_collection
• @millionaires_dating

💎 ВАШ ДОХОД: 3-5 девушек в день = 1500-2500₽

📞 Поддержка: @{ADMIN_TG}
"""
    else:
        text = f"""
🎯 PREMIUM GUIDE (FULL PACK):

💰 YOUR EARNINGS: 500-2000₽ per day

📋 COMPLETE ACTION PLAN:

1️⃣ ACCOUNT CREATION:
• Go to: {DATING_BOT_LINK}
• Use guy photos from Google (handsome man)
• Name: Maxim, 24 years old
• Bio: "Looking for serious relationship 💍"

2️⃣ TARGET SEARCH:
• Database #1: @rich_girls_base
• Database #2: @millionaire_dating
• Database #3: @premium_girls_chat
• Look for girls with 💎 in nickname

3️⃣ MESSAGES FOR DIFFERENT SITUATIONS:

💌 First message:
"Hi! You're very beautiful! 😊 How are you?"

💬 If responds:
"Glad you answered! You have such a stylish profile, you can see you have taste 💫"

🎯 If sees gifts:
"Wow, you have so many gifts! How do you manage?"

4️⃣ FINAL STAGE (SCAM):
• After 10-15 minutes of communication
• "By the way, I'm a system administrator, your account may be deleted due to suspicious activity"
• "Follow the link to verify: [phishing link]"
• After gaining access - block the girl

5️⃣ SECURITY:
• Use: @hideipbot
• Change accounts every 3 days
• Never transfer to your cards

📊 PREMIUM DATABASES:
• @rich_dating_rus
• @premium_dating_offical
• @gifts_collection
• @millionaires_dating

💎 YOUR INCOME: 3-5 girls per day = 1500-2500₽

📞 Support: @{ADMIN_TG}
"""
    bot.send_message(chat_id, text)

# Инструкции по оплате
def send_payment_instructions(chat_id, lang):
    user_data[chat_id]['payment_pending'] = True
    
    if lang == 'ru':
        text = f"""
💳 ПОКУПКА «ВЕСЬ ПАК»

Стоимость: {PAYMENT_AMOUNT} рублей

📋 ИНСТРУКЦИЯ:
1. Перейдите по ссылке: {DONATION_ALERTS_URL}
2. Введите сумму: {PAYMENT_AMOUNT} рублей
3. Выберите удобный способ оплаты
4. Совершите платеж
5. Напишите админу: @{ADMIN_TG}

⚡ После оплаты вы получите:
• Полное руководство по скаму девушек
• Базы данных богатых девушек
• Шаблоны сообщений для обмана
• Инструкции по безопасности
• Поддержку 24/7

📞 ОБЯЗАТЕЛЬНО напишите админу после оплаты!
"""
    else:
        text = f"""
💳 PURCHASE «FULL PACK»

Price: {PAYMENT_AMOUNT} rubles

📋 INSTRUCTIONS:
1. Follow the link: {DONATION_ALERTS_URL}
2. Enter amount: {PAYMENT_AMOUNT} rubles
3. Choose convenient payment method
4. Make payment
5. Write to admin: @{ADMIN_TG}

⚡ After payment you will receive:
• Complete guide to scamming girls
• Databases of rich girls
• Message templates for deception
• Security instructions
• 24/7 support

📞 MANDATORY write to admin after payment!
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

💰 Система заработка описана как теоретическая модель для изучения механизмов социальной инженерии и кибербезопасности.

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

💰 The earning system is described as a theoretical model for studying social engineering mechanisms and cybersecurity.

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
        # Всегда просим написать админу
        if lang == 'ru':
            text = f"""
❌ Автопроверка оплаты не удалась!

📞 Напишите админу: @{ADMIN_TG}
Отправьте ему скриншот оплаты и ваш Telegram ID: {chat_id}

⚡ После ручной проверки вам откроют доступ к «Весь пак»!
"""
        else:
            text = f"""
❌ Automatic payment check failed!

📞 Write to admin: @{ADMIN_TG}
Send him payment screenshot and your Telegram ID: {chat_id}

⚡ After manual verification you will get access to «Full Pack»!
"""
        
        bot.send_message(chat_id, text)
        user_data[chat_id]['payment_pending'] = False
    else:
        response = "Сначала нажмите «Купить Весь пак»" if lang == 'ru' else "First click «Buy Full Pack»"
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
