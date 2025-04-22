import os
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '7869555754:AAFlPNauYT35gvXBgplqQuMaFSnpwK0kZiM'
YANDEX_API_KEY = 'AQVN204JFosIF5HqPcN7JXOMpRhg-H1RBLThXHzr'
FOLDER_ID = 'b1g8pqllqmmp67h9j7lt'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Спросить YandexGPT")],
        [KeyboardButton("Получить рандомную шутку")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Привет! Выберите действие:', reply_markup=reply_markup)

def get_yandex_gpt_response(prompt: str) -> str:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Bearer {YANDEX_API_KEY}",
        "x-folder-id": FOLDER_ID,
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "10000"
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        return response_data['result']['alternatives'][0]['message']['text']
    except requests.exceptions.RequestException as e:
        error_msg = f"Ошибка при обращении к YandexGPT: {str(e)}"
        if hasattr(e, 'response') and e.response:
            error_msg += f"\nДетали ошибки: {e.response.text}"
        return error_msg

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    if user_message == "Спросить YandexGPT":
        await update.message.reply_text("Введите ваш вопрос:")
    elif user_message == "Получить рандомную шутку":
        joke = get_random_joke()
        await update.message.reply_text(joke)
    else:
        gpt_response = get_yandex_gpt_response(user_message)
        await update.message.reply_text(gpt_response)

def get_random_joke() -> str:
    jokes = [
        "Почему программисты не любят природу? Потому что там слишком много багов.",
        "Какой язык программирования самый оптимистичный? Python — он всегда в ожидании!",
        "Почему Java разработчики всегда путают Рождество и Хэллоуин? Потому что Oct 31 == Dec 25.",
        "Какой любимый напиток программиста? Java, конечно)",
        "Какой любимый танец программиста на Python? Импорт-танец!",
        "Как Python-программисты решают проблемы? Они просто 'импортируют' свои чувства!"
    ]
    import random
    return random.choice(jokes)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
