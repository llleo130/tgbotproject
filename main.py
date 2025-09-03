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
PAYMENT_AMOUNT_USD = 5  # Примерно 200 рублей в долларах

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

# Руководство по заработку (бесплатная версия) - ОЧЕНЬ ПОДРОБНОЕ
def send_free_earning_guide(chat_id, lang):
    if lang == 'ru':
        # Русская версия (оставляем как было)
        parts = [
            """
🎯 БЕСПЛАТНОЕ РУКОВОДСТВО ПО ЗАРАБОТКУ NFT/TELEGRAM ПОДАРКОВ

📖 ОГЛАВЛЕНИЕ:
1. Создание идеального фейкового аккаунта
2. Поиск целей для заработка
3. Психология общения с девушками
4. Шаблоны сообщений для разных ситуаций
5. Безопасность и анонимность
6. Ограничения бесплатной версии
""",
            """
1️⃣ СОЗДАНИЕ ИДЕАЛЬНОГО ФЕЙКОВОГО АККАУНТА

🌟 ВАЖНО: Аккаунт должен выглядеть максимально естественно!

📝 ДАННЫЕ ДЛЯ АККАУНТА:
• Имя: Максим, 24 года
• Город: Москва/Санкт-Петербург
• Профессия: Предприниматель/IT-специалист
• Интересы: Путешествия, спорт, искусство

🖼️ ФОТОГРАФИИ:
• 3-5 качественных фото из Google
• Фото в разных ракурсах (портрет, в полный рост)
• Избегайте фото со знаменитостями
• Фото должны быть в высоком разрешении

📱 НАСТРОЙКА АККАУНТА:
• Включите верификацию двухэтапную
• Добавьте номер виртуального телефона
• Настройте приватность профиля
• Заполните все поля био
""",
            """
2️⃣ ПОИСК ЦЕЛЕЙ ДЛЯ ЗАРАБОТКА

🎯 КРИТЕРИИ ЦЕЛЕВЫХ ДЕВУШЕК:
• Наличие Telegram Premium (звездочка в профиле)
• NFT в аватарке или username
• Дорогие подарки в профиле
• Активность в премиум-чатах
• Красивые фото в профиле

🔍 ГДЕ ИСКАТЬ:
• Чаты знакомств с фильтром по Premium
• Тематические группы по NFT
• Чаты с дорогими подарками
• Группы по интересам (путешествия, luxury)

📊 ПРИОРИТЕТЫ ПОИСКА:
1. Девушки с 10+ подарками
2. Активные в последние 24 часа
3. С открытым профилем
4. Из крупных городов
""",
            """
3️⃣ ПСИХОЛОГИЯ ОБЩЕНИЯ С ДЕВУШКАМИ

🧠 ОСНОВНЫЕ ПРИНЦИПЫ:
• Создайте эмоциональную связь
• Проявляйте искренний интерес
• Не торопите события
• Используйте комплименты уместно

💬 ЭТАПЫ ОБЩЕНИА:
1. Знакомство (первые 5 сообщений)
2. Установление контакта (15-20 сообщений)
3. Создание доверия (30-60 минут общения)
4. Финальная стадия (переход к "проблеме")

😊 ЭМОЦИОНАЛЬНЫЕ ТРИГГЕРЫ:
• Лесть (комплименты внешности)
• Интерес к личности (вопросы о хобби)
• Общие темы (путешествия, музыка)
• Юмор (легкие шутки)
""",
            """
4️⃣ ШАБЛОНЫ СООБЩЕНИЙ ДЛЯ РАЗНЫХ СИТУАЦИЙ

💌 ПЕРВОЕ СООБЩЕНИЕ:
"Привет! Твоя улыбка на фото просто завораживает! 😊 Как твой день проходит?"

💬 ОТВЕТ НА ВОПРОС "ЧЕМ ЗАНИМАЕШЬСЯ?":
"Занимаюсь IT-проектами, создаю свои стартапы. А ты чем увлекаешься? Вижу, у тебя отличный вкус!"

🎯 ЕСЛИ ВИДИТЕ ПОДАРКИ:
"Ого, у тебя столько крутых подарков! Видимо, у тебя много поклонников) Как выбираешь, кому отвечать?"

🔄 ЕСЛИ ДЕВУШКА МАЛО ПИШЕТ:
"Похоже, ты сегодня занята) Может, продолжим вечером? Хочу узнать о тебе больше!"

❓ ЕСЛИ СПРАШИВАЕТ О ВСТРЕЧЕ:
"С удовольствием, но сначала хочу получше узнать тебя здесь. Расскажи о своих мечтах!"
""",
            """
5️⃣ БЕЗОПАСНОСТЬ И АНОНИМНОСТИ

🛡️ ОСНОВНЫЕ ПРАВИЛА:
• Никогда не используйте личные данные
• Меняйте аккаунты каждые 3-4 дня
• Используйте разные фото для каждого аккаунта
• Очищайте кэш после каждой сессии

🔧 ИНСТРУМЕНТЫ ДЛЯ БЕЗОПАСНОСТИ:
• VPN (NordVPN, ExpressVPN)
• Антидетект браузеры
• Временные номера телефонов
• Виртуальные карты

⚠️ КРАСНЫЕ ФЛАГИ:
• Девушки просят видео звонок сразу
• Подозрительные вопросы о работе
• Просьбы перейти в другие мессенджеры
• Агрессивное поведение
""",
            """
6️⃣ ОГРАНИЧЕНИЯ БЕСПЛАТНОЙ ВЕРСИИ

🚫 ЧЕГО НЕТ В БЕСПЛАТНОЙ ВЕРСИИ:
• Доступа к закрытым базам данных
• Автоматического поиска целей
• Готовых фишинг-ссылок
• Шаблонов для угроз и давления
• Инструкций по выводу средств
• Поддержки 24/7

📊 РЕАЛЬНЫЕ РЕЗУЛЬТАТЫ БЕСПЛАТНО:
• 1-2 успешные операции в неделю
• Доход: 500-1000 рублей в неделю
• Высокий риск блокировок
• Много ручной работы

💎 ЧТО ДАЕТ ПРЕМИУМ «ВЕСЬ ПАК»:
• Доход: 1500-2500 рублей в ДЕНЬ
• Автоматизированный поиск
• Готовые системы для работы
• Полная безопасность
• Поддержка и обучение
"""
        ]
        
        for part in parts:
            bot.send_message(chat_id, part)
            time.sleep(3)
            
        final_text = f"""
🔥 ВАЖНО: Бесплатная версия подходит только для обучения основам!

💳 Для реального заработка необходим «Весь пак» за {PAYMENT_AMOUNT_RUB} рублей

⚡ В премиум версии:
• Пошаговые видео инструкции
• Готовые скрипты общения
• Автоматические шаблоны
• Закрытые базы данных
• Техническая поддержка

📞 После оплаты напишите админу: @{ADMIN_TG}
"""
        bot.send_message(chat_id, final_text)
        
    else:
        # English version - ПОЛНАЯ ВЕРСИЯ
        parts = [
            """
🎯 FREE GUIDE TO EARN NFT/TELEGRAM GIFTS

📖 TABLE OF CONTENTS:
1. Creating the perfect fake account
2. Finding targets for earnings
3. Psychology of communication with girls
4. Message templates for different situations
5. Security and anonymity
6. Free version limitations
""",
            """
1️⃣ CREATING THE PERFECT FAKE ACCOUNT

🌟 IMPORTANT: The account should look as natural as possible!

📝 ACCOUNT DATA:
• Name: Alex, 25 years old
• City: New York/London
• Profession: Entrepreneur/IT specialist
• Interests: Travel, sports, art

🖼️ PHOTOS:
• 3-5 high-quality photos from Google
• Photos from different angles (portrait, full-length)
• Avoid photos with celebrities
• Photos should be high resolution

📱 ACCOUNT SETUP:
• Enable two-step verification
• Add virtual phone number
• Set up profile privacy
• Fill in all bio fields

🔧 RECOMMENDED TOOLS:
• Temp-mail.org for email
• TextNow for virtual number
• Google Images for photos
""",
            """
2️⃣ FINDING TARGETS FOR EARNINGS

🎯 TARGET GIRLS CRITERIA:
• Telegram Premium (star in profile)
• NFT in avatar or username
• Expensive gifts in profile
• Activity in premium chats
• Beautiful photos in profile

🔍 WHERE TO SEARCH:
• Dating chats with Premium filter
• NFT thematic groups
• Chats with expensive gifts
• Interest groups (travel, luxury)

📊 SEARCH PRIORITIES:
1. Girls with 10+ gifts
2. Active in last 24 hours
3. With open profile
4. From big cities
""",
            """
3️⃣ PSYCHOLOGY OF COMMUNICATION WITH GIRLS

🧠 BASIC PRINCIPLES:
• Create emotional connection
• Show genuine interest
• Don't rush events
• Use compliments appropriately

💬 COMMUNICATION STAGES:
1. Introduction (first 5 messages)
2. Contact establishment (15-20 messages)
3. Trust building (30-60 minutes communication)
4. Final stage (transition to "problem")

😊 EMOTIONAL TRIGGERS:
• Flattery (appearance compliments)
• Interest in personality (hobby questions)
• Common topics (travel, music)
• Humor (light jokes)
""",
            """
4️⃣ MESSAGE TEMPLATES FOR DIFFERENT SITUATIONS

💌 FIRST MESSAGE:
"Hi! Your smile in the photo is just mesmerizing! 😊 How's your day going?"

💬 ANSWER TO "WHAT DO YOU DO?":
"I work on IT projects, creating my startups. What are you passionate about? I can see you have great taste!"

🎯 IF YOU SEE GIFTS:
"Wow, you have so many cool gifts! You must have many admirers) How do you choose who to answer?"

🔄 IF GIRL WRITES LITTLE:
"Seems like you're busy today) Maybe we continue in the evening? I want to know more about you!"

❓ IF ASKS ABOUT MEETING:
"With pleasure, but first I want to get to know you better here. Tell me about your dreams!"
""",
            """
5️⃣ SECURITY AND ANONYMITY

🛡️ BASIC RULES:
• Never use personal data
• Change accounts every 3-4 days
• Use different photos for each account
• Clear cache after each session

🔧 SECURITY TOOLS:
• VPN (NordVPN, ExpressVPN)
• Anti-detect browsers
• Temporary phone numbers
• Virtual cards

⚠️ RED FLAGS:
• Girls ask for video call immediately
• Suspicious questions about work
• Requests to switch to other messengers
• Aggressive behavior
""",
            """
6️⃣ FREE VERSION LIMITATIONS

🚫 WHAT'S NOT IN FREE VERSION:
• Access to closed databases
• Automatic target search
• Ready phishing links
• Threat and pressure templates
• Withdrawal instructions
• 24/7 support

📊 REAL FREE RESULTS:
• 1-2 successful operations per week
• Income: $10-20 per week
• High risk of bans
• Lots of manual work

💎 WHAT PREMIUM "FULL PACK" GIVES:
• Income: $30-50 per DAY
• Automated search
• Ready working systems
• Complete security
• Support and training
"""
        ]
        
        for part in parts:
            bot.send_message(chat_id, part)
            time.sleep(3)
            
        final_text = f"""
🔥 IMPORTANT: Free version is only for learning basics!

💳 For real earnings you need «Full Pack» for ${PAYMENT_AMOUNT_USD}

⚡ In premium version:
• Step-by-step video instructions
• Ready communication scripts
• Automatic templates
• Closed databases
• Technical support

📞 After payment write to admin: @{ADMIN_TG}
"""
        bot.send_message(chat_id, final_text)

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

💰 YOUR EARNINGS: $30-50 per day

📋 COMPLETE ACTION PLAN:

1️⃣ ACCOUNT CREATION:
• Go to: {DATING_BOT_LINK}
• Use guy photos from Google (handsome man)
• Name: Alex, 25 years old
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

💎 YOUR INCOME: 3-5 girls per day = $40-70

📞 Support: @{ADMIN_TG}
"""
    bot.send_message(chat_id, text)

# Инструкции по оплате
def send_payment_instructions(chat_id, lang):
    user_data[chat_id]['payment_pending'] = True
    
    if lang == 'ru':
        text = f"""
💳 ПОКУПКА «ВЕСЬ ПАК»

Стоимость: {PAYMENT_AMOUNT_RUB} рублей

📋 ИНСТРУКЦИЯ:
1. Перейдите по ссылке: {DONATION_ALERTS_URL}
2. Введите сумму: {PAYMENT_AMOUNT_RUB} рублей
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

Price: ${PAYMENT_AMOUNT_USD}

📋 INSTRUCTIONS:
1. Follow the link: {DONATION_ALERTS_URL}
2. Enter amount: {PAYMENT_AMOUNT_RUB} rubles (approx ${PAYMENT_AMOUNT_USD})
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
