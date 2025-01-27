import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from openai import OpenAI

load_dotenv()

# API
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
OPEN_WEATHER_URL = os.getenv('OPEN_WEATHER_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')    
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Contador
contador_usuario = {}

client = OpenAI(api_key=OPENAI_API_KEY)

# Comandos 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    contador_usuario[user_id] = contador_usuario.get(user_id, 0) + 1

    await update.message.reply_text(
        "Bienvenid@! Usa los comandos:\n"
        "/clima - Para conocer el clima y obtener una recomendación de qué ropa usar\n"
        "/contador - Para ver el contador de interacciones\n"
        "Escribe el comando que deseas usar."
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    contador_usuario[user_id] = contador_usuario.get(user_id, 0) + 1 

    await update.message.reply_text(
        "Usa los comandos:\n"
        "/clima - Para conocer el clima y obtener una recomendación de qué ropa usar\n"
        "/contador - Para ver el contador de interacciones\n"
        "Escribe el comando que deseas usar."
    )

async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    contador_usuario[user_id] = contador_usuario.get(user_id, 0) + 1  

    await update.message.reply_text("Escribe el nombre de la ciudad para obtener el clima:")

async def contador(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    count = contador_usuario.get(user_id, 0)
    await update.message.reply_text(f"Contador: {count}")



# Función IA
async def obtener_sugerencia_ia(temperatura, humedad, descripcion):
    try:
        prompt = (
            f"Con base en los siguientes datos climáticos:\n"
            f"Temperatura: {temperatura}°C\n"
            f"Humedad: {humedad}%\n"
            f"Descripción del clima: {descripcion}\n"
            f"¿Qué recomendaciones de ropa sugerís? No más de 100 caracteres y comenzá la respuesta con 'Recomiendo usar...'"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"



# Respuesta clima y ia
async def mensaje_clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    contador_usuario[user_id] = contador_usuario.get(user_id, 0) + 1 

    city_name = update.message.text
    complete_url = f"{OPEN_WEATHER_URL}appid={OPEN_WEATHER_API_KEY}&q={city_name}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        temperatura = main["temp"]
        humedad = main["humidity"]
        weather = data["weather"]
        descripcion = weather[0]["description"]
        
        sugerencia_ia = await obtener_sugerencia_ia(temperatura, humedad, descripcion)
        
        await update.message.reply_text(
            f"El clima en {city_name} es el siguiente:\n"
            f"Temperatura: {temperatura}°C\n"
            f"Humedad: {humedad}%\n"
            f"Descripción: {descripcion}\n\n"
            f"Sugerencia de IA: {sugerencia_ia}"
        )
    else:
        await update.message.reply_text("Ciudad no encontrada.")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
      
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clima", clima))
    application.add_handler(CommandHandler("contador", contador))
    application.add_handler(CommandHandler("ayuda", ayuda))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_clima))

    application.run_polling()

if __name__ == '__main__':
    main()
