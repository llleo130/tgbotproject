import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading
import os
import requests
import time

# Токен бота
API_TOKEN = '8214260739:AAEfatPbnC7ZpcO2LckO7QM10EbgvGxemO0'

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Создаем Flask приложение
app = Flask(__name__)

# Хранилище для данных пользователей
user_data = {}

# DonationAlerts настройки
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

# Проверка оплаты (заглушка - в реальности нужно API DonationAlerts)
def check_payment(user_id):
    # В реальном боте здесь будет проверка через API DonationAlerts
    # Сейчас просто симуляция - 50% шанс что оплата прошла
    time.sleep(2)
    return True  # Заглушка - всегда успех

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
        text = """
🎯 БЕСПЛАТНОЕ РУКОВОДСТВО:

1️⃣ Создайте фейковый аккаунт в ботах для знакомств
2️⃣ Пишите девушкам комплименты
3️⃣ Ищите тех, у кого есть подарки в профиле

⚠️ ОГРАНИЧЕНИЯ БЕСПЛАТНОЙ ВЕРСИИ:
• Нет доступа к премиум-базам данных
• Ограниченное количество сообщений
• Без гарантии результата

💳 Для полного доступа купите «Весь пак» за 200 рублей!
"""
    else:
        text = """
🎯 FREE GUIDE:

1️⃣ Create a fake account in dating bots
2️⃣ Write compliments to girls
3️⃣ Look for those who have gifts in their profile

⚠️ FREE VERSION LIMITATIONS:
• No access to premium databases
• Limited number of messages
• No result guarantee

💳 Buy «Full Pack» for 200 rubles for full access!
"""
    bot.send_message(chat_id, text)

# Руководство по заработку (премиум версия)
def send_premium_earning_guide(chat_id, lang):
    if lang == 'ru':
        text = """
🎯 ПРЕМИУМ РУКОВОДСТВО (ВЕСЬ ПАК):

💰 ВАШ ЗАРАБОТОК: 500-2000₽ в день

📋 ПОЛНЫЙ ПЛАН ДЕЙСТВИЙ:

1️⃣ СОЗДАНИЕ АККАУНТА:
• Скачайте бота: @datingbot
• Используйте фото из Google (красивая девушка)
• Имя: Анастасия, 22 года
• Био: "Ищу интересное общение 😊"

2️⃣ ПОИСК ЦЕЛЕЙ:
• Перейдите в: @rich_girls_chat
• Ищите девушек с 💎 в нике
• Проверяйте кто онлайн (@onlinecheckbot)

3️⃣ СООБЩЕНИЯ ДЛЯ РАЗНЫХ СИТУАЦИЙ:

💌 Первое сообщение:
"Привет! Ты очень красивая! 😊 Как твои дела?"

💬 Если отвечает:
"Рада, что ответила! У тебя такой стильный профиль, видно что с вкусом 💫"

🎯 Если видит подарки:
"Ого, у тебя столько подарков! Как тебе удается?"

4️⃣ ФИНАЛЬНЫЙ ЭТАП:
• После 10-15 минут общения
• "Кстати, я администратор системы, твой аккаунт могут удалить из-за подозрительной активности"
• "Перейди по ссылке для проверки: [ваша фишинг ссылка]"

5️⃣ БЕЗОПАСНОСТЬ:
• Используйте: @hideipbot
• Меняйте аккаунты каждые 3 дня
• Никогда не переводите на свои карты

📊 БАЗЫ ДЛЯ РАБОТЫ:
• @premium_dating
• @rich_dating
• @gifts_chat
• @millionaires_chat

💎 ВАШ ДОХОД: 3-5 аккаунтов в день = 1500-2500₽
"""
    else:
        text = """
🎯 PREMIUM GUIDE (FULL PACK):

💰 YOUR EARNINGS: 500-2000₽ per day

📋 COMPLETE ACTION PLAN:

1️⃣ ACCOUNT CREATION:
• Download bot: @datingbot
• Use photos from Google (beautiful girl)
• Name: Anastasia, 22 years old
• Bio: "Looking for interesting communication 😊"

2️⃣ TARGET SEARCH:
• Go to: @rich_girls_chat
• Look for girls with 💎 in nickname
• Check who's online (@onlinecheckbot)

3️⃣ MESSAGES FOR DIFFERENT SITUATIONS:

💌 First message:
"Hi! You're very beautiful! 😊 How are you?"

💬 If responds:
"Glad you answered! You have such a stylish profile, you can see you have taste 💫"

🎯 If sees gifts:
"Wow, you have so many gifts! How do you manage?"

4️⃣ FINAL STAGE:
• After 10-15 minutes of communication
• "By the way, I'm a system administrator, your account may be deleted due to suspicious activity"
• "Follow the link to verify: [your phishing link]"

5️⃣ SECURITY:
• Use: @hideipbot
• Change accounts every 3 days
• Never transfer to your cards

📊 DATABASES FOR WORK:
• @premium_dating
• @rich_dating
• @gifts_chat
• @millionaires_chat

💎 YOUR INCOME: 3-5 accounts per day = 1500-2500₽
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
5. Вернитесь в бот и отправьте скриншот оплаты

⚡ После проверки вы получите:
• Полное руководство по заработку
• Базы данных богатых девушек
• Шаблоны сообщений
• Инструкции по безопасности
• Поддержку 24/7

⏳ Проверка оплаты занимает до 5 минут
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
5. Return to bot and send payment screenshot

⚡ After verification you will receive:
• Complete earning guide
• Databases of rich girls
• Message templates
• Security instructions
• 24/7 support

⏳ Payment verification takes up to 5 minutes
"""
    
    bot.send_message(chat_id, text)

# Политика конфиденциальности
def send_policy(chat_id, lang):
    if lang == 'ru':
        text = """
📜 ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ

⚠️ ВАЖНОЕ УВЕДОМЛЕНИЕ:

Создатель данного бота не призывает и не заставляет пользователей зарабатывать деньги нелегальным способом. Вся представленная информация предназначена исключительно в образовательных целях.

Пользователь самостоятельно несет ответственность за свои действия и их последствия. Мы не одобряем и не поддерживаем незаконную деятельность.

💰 Система заработка описана как теоретическая модель для изучения механизмов социальной инженерии и кибербезопасности.

🔒 Ваши данные: Мы не храним персональную информацию и данные платежей.

Вы используете бот на свой собственный риск.
"""
    else:
        text = """
📜 PRIVACY POLICY

⚠️ IMPORTANT NOTICE:

The creator of this bot does not encourage or force users to earn money illegally. All information provided is for educational purposes only.

The user is solely responsible for their actions and their consequences. We do not approve or support illegal activities.

💰 The earning system is described as a theoretical model for studying social engineering mechanisms and cybersecurity.

🔒 Your data: We do not store personal information and payment data.

You use the bot at your own risk.
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
        # Симуляция проверки оплаты
        bot.send_message(chat_id, "⏳ Проверяем оплату..." if lang == 'ru' else "⏳ Checking payment...")
        
        if check_payment(chat_id):
            user_data[chat_id]['premium'] = True
            user_data[chat_id]['payment_pending'] = False
            
            success_text = "✅ Оплата подтверждена! Теперь у вас есть доступ к «Весь пак»!" if lang == 'ru' else "✅ Payment confirmed! Now you have access to «Full Pack»!"
            bot.send_message(chat_id, success_text)
            
            # Отправляем премиум контент
            send_premium_earning_guide(chat_id, lang)
        else:
            error_text = "❌ Оплата не найдена. Попробуйте еще раз или обратитесь в поддержку." if lang == 'ru' else "❌ Payment not found. Try again or contact support."
            bot.send_message(chat_id, error_text)
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
