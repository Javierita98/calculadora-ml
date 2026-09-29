import telebot

TOKEN = "8986905157:AAEDcbbSNomnClL07zc5U-ZnqquVJ_A1U78"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bienvenida = (
        "¡Hola Javiera! 🤖🇨🇱\n\n"
        "Asistente de Mercado Libre y Estrategia Comercial (Versión Blindada 🛡️).\n\n"
        "<b>Componentes fijos incluidos siempre:</b>\n"
        "• Comisión máxima de Mercado Libre (13%)\n"
        "• Insumos de empaque ($300 fijos)\n"
        "• Envíos Santiago (Estándar ~$4.000 / Flex ~$6.000)\n\n"
        "<b>¿Cómo usarme?</b>\n"
        "Escribe 3 datos separados por comas:\n"
        "<code>Nombre del producto, costo total pagado, precio de venta competencia</code>\n\n"
        "<i>Ejemplo:</i>\n"
        "<code>Audífonos Sony, 20000, 35000</code>"
    )
    bot.reply_to(message, bienvenida, parse_mode="HTML")

@bot.message_handler(func=lambda message: True)
def analizar_comercial_blindado(message):
    try:
        texto = message.text.strip()
        partes = [p.strip() for p in texto.split(",")]
        
        if len(partes) == 3:
            nombre_producto = partes[0]
            costo_total = float(partes[1].replace("$", "").replace(".", ""))
            precio_venta_real = float(partes[2].replace("$", "").replace(".", ""))
            
            # 1. Comisión máxima de Mercado Libre (13% fijo)
            comision_ml = precio_venta_real * 0.13    
            
            # 2. Costos logísticos y operativos fijos (Siempre van)
            costo_envio_santiago = 4000  # Envío normal/gratis Santiago
            costo_flex = 6000            # Envío Flex Santiago
            costo_empaque = 300          # Scotch, etiquetas y embalaje prorrateado
            
            # Escenario Santiago (Envío Estándar / Gratis)
            gastos_stgo = costo_total + costo_envio_santiago + costo_empaque + comision_ml
            ganancia_stgo = precio_venta_real - gastos_stgo
            margen_stgo = (ganancia_stgo / precio_venta_real) * 100 if precio_venta_real > 0 else 0

            # Escenario Santiago (Envío FLEX)
            gastos_flex = costo_total + costo_flex + costo_empaque + comision_ml
            ganancia_flex = precio_venta_real - gastos_flex
            margen_flex = (ganancia_flex / precio_venta_real) * 100 if precio_venta_real > 0 else 0

            # Alerta visual estricta según el margen
            alerta = "🟢 Margen Saludable"
            if margen_stgo < 0:
                alerta = "🔴 ¡ALERTA ROJA! Estás vendiendo a pérdida"
            elif margen_stgo < 25:
                alerta = "🔴 ¡Cuidado! Margen muy bajo (<25%)"
            elif margen_stgo < 35:
                alerta = "🟡 Margen Moderado"

            # Respuesta estructurada y limpia
            respuesta = (
                f"🎯 <b>ANÁLISIS COMERCIAL: {nombre_producto.upper()}</b>\n"
                f"<i>{alerta}</i>\n\n"
                f"🏷️ <b>Tu costo total pagado:</b> ${costo_total:,.0f}\n"
                f"📦 <i>Insumos/Empaque fijos:</i> ${costo_empaque}\n"
                f"🛒 <b>Precio competencia:</b> <b>${precio_venta_real:,.0f}</b>\n"
                f"📉 Comisión ML máxima (13%): ${comision_ml:,.0f}\n\n"
                "🇨🇱 <b>MÁRGENES REALES EN SANTIAGO:</b>\n"
                f"📦 <i>Envío Estándar/Gratis (~${costo_envio_santiago:,.0f}):</i>\n"
                f"   • Ganancia Neta: <b>${ganancia_stgo:,.0f}</b> | Margen: <b>{margen_stgo:.2f}%</b>\n\n"
                f"⚡ <i>Envío FLEX / En el día (~${costo_flex:,.0f}):</i>\n"
                f"   • Ganancia Neta: <b>${ganancia_flex:,.0f}</b> | Margen: <b>{margen_flex:.2f}%</b>\n\n"
                "🌍 <i>Regiones:</i> Margen completo (envío por pagar del comprador)."
            )
            bot.reply_to(message, respuesta, parse_mode="HTML")
            return
            
        else:
            bot.reply_to(message, "⚠️ Formato incorrecto. Debes enviar 3 datos:\n<code>Producto, costo, precio competencia</code>", parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, "⚠️ Error en los números ingresados. Usa solo números para el costo y precio.", parse_mode="HTML")

print("Bot comercial blindado y activo...")
bot.infinity_polling()
