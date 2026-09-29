import os
import telebot

# Aquí va la llave maestra (tu token de BotFather)
TOKEN = "8986905157:AAEDcbbSNomnClL07zc5U-ZnqquVJ_A1U78"
bot = telebot.TeleBot(TOKEN)

# Lo que hace el bot cuando le dices /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola Javiera! Soy tu calculadora de Mercado Libre. Escríbeme los datos de tu producto y te calcularé el margen.")

# Lo que hace el bot cuando le mandas cualquier texto
@bot.message_handler(func=lambda message: True)
def calcular_margen(message):
    texto_usuario = message.text
    # Aquí en el futuro pondremos la matemática exacta de comisiones y envíos
    respuesta = f"Recibí tus datos: '{texto_usuario}'. Pronto aquí aparecerá tu margen neto calculado automáticamente."
    bot.reply_to(message, respuesta)

# Esto enciende el bot
if __name__ == "__main__":
    print("El bot está andando...")
    bot.infinity_polling()