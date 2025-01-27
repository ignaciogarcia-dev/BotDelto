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


