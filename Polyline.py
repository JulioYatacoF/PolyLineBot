import requests
import time
import pytz
import asyncio
import nest_asyncio
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, JobQueue


nest_asyncio.apply()  # 🔧 Permite usar asyncio en Codespaces/Replit sin errores
# Configuración del bot de Telegram
BOT_TOKEN = "7208203072:AAGluX7aLNCl_VtbSE4v4-r7bIaGLNjjp2I"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Configurar zona horaria manualmente
timezone = pytz.timezone("America/Lima")  # Cambia según tu país
scheduler = AsyncIOScheduler(timezone=timezone)

# Menú principal con llamada a la acción
MENU_OPCIONES = """
Hola, te saludamos de POLYLINE SAC. Selecciona la información que deseas:

1. Proyectos en venta
2. Proyecto Benavides 1
3. Proyecto Benavides 2
4. Proyecto Pueblo Libre 1
5. Agendar visita (virtual o presencial) 📅
6. Pedir más información 📩
7. Salir
"""

# Datos de los proyectos en venta
PROYECTOS_VENTA = """
Proyectos en venta:

1. Casa de Playa Golf 1
   - 3 dormitorios
   - 2 estacionamientos
   - 120 m²
   - Jardín privado

2. Casa de Playa Golf 2
   - 7 dormitorios
   - 7 baños
   - Piscina privada
   - 250 m²

3. Casa de Playa Golf 4
   - Áreas verdes y terrazas en 3 niveles

4. Casa de Playa Golf 5
   - 6 dormitorios
   - Piscina panorámica
   - Terraza de 100m²

5. Casa en Playa Lagunas
   - 4 dormitorios
   - Jacuzzi
   - Piscina
   - Acabados de lujo

6. Casa de Playa
   - 5 dormitorios
   - Amplias terrazas
   - Piscina privada

7. Casa de Playa Mykonos 1
   - 3 dormitorios
   - Piscina privada
   - Estacionamiento

8. Casa de Playa Mykonos 2
   - 5 dormitorios
   - 6 baños
   - Piscina
   - Terraza con vista al mar

9. Casa de Surco
   - 4 dormitorios
   - Sala con doble altura
   - Piscina
   - Jardines
"""

# Datos de los proyectos
PROYECTO_BENAVIDES_1 = """
Proyecto Benavides 1:

1. Departamento 101 - DUPLEX
   - 3 Dormitorios
   - 2 Baños
   - 113.32 m²

2. Departamento 201
   - 3 Dormitorios
   - 2 Baños
   - 103.81 m²

3. Departamento 202
   - 2 Dormitorios
   - 2 Baños
   - 75.40 m²

4. Departamento 301 - DUPLEX
   - 3 Dormitorios
   - 2 Baños
   - 113.32 m²

5. Departamento 303
   - 2 Dormitorios (Estudio)
   - 75.40 m²

6. Departamento 601
   - 3 Dormitorios
   - 2 Baños
   - 100 m²

7. Departamento 602
   - 3 Dormitorios
   - 2 Baños
   - 213.06 m²

8. Departamento 603
   - 3 Dormitorios
   - 2 Baños
   - 100 m²
"""

PROYECTO_PUEBLO_LIBRE_1 = """
Proyecto Pueblo Libre 1:

1. Departamento 201
   - 3 Dormitorios
   - 63.05 m²

2. Departamento 202
   - 2 Dormitorios
   - 51.38 m²

3. Departamento 203
   - 2 Dormitorios
   - 51.38 m²

4. Departamento 204
   - 3 Dormitorios
   - 63.05 m²

5. Departamento 205
   - 3 Dormitorios
   - 57.83 m²

6. Departamento 401
   - 3 Dormitorios
   - 63.05 m²

7. Departamento 402
   - 2 Dormitorios
   - 51.38 m²

8. Departamento 403
   - 2 Dormitorios
   - 51.38 m²

9. Departamento 404
   - 3 Dormitorios
   - 63.05 m²

10. Departamento 406
    - 2 Dormitorios
    - 48.78 m²

11. Departamento 502
    - 2 Dormitorios
    - 51.38 m²
"""

SALUDOS = ["hola", "buenos días", "buenas tardes", "buenas noches", "hey", "qué tal"]

async def start(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = "principal"
    await update.message.reply_text(MENU_OPCIONES)

async def handle_message(update: Update, context: CallbackContext) -> None:
    texto = update.message.text.strip().lower()
    
    if texto in SALUDOS or not texto.isdigit():
        await update.message.reply_text(MENU_OPCIONES)
        return
    
    opcion = int(texto) if texto.isdigit() else 0
    menu = context.user_data.get("menu", "principal")
    
    if menu == "principal":
        if opcion == 1:
            context.user_data["menu"] = "proyectos_venta"
            await update.message.reply_text(PROYECTOS_VENTA)
        elif opcion == 2:
            context.user_data["menu"] = "benavides_1"
            await update.message.reply_text(PROYECTO_BENAVIDES_1)
        elif opcion == 3:
            await update.message.reply_text(
                "Esta opción aún no está disponible, gracias por comunicarse con nosotros.\n"
                "Para más información, visita: https://polylinesac.netlify.app"
            )
        elif opcion == 4:
            context.user_data["menu"] = "pueblo_libre_1"
            await update.message.reply_text(PROYECTO_PUEBLO_LIBRE_1)
        elif opcion == 5:
            await update.message.reply_text("Para agendar su cita, visite: https://polylinesac.netlify.app/contact/agenda%20una%20reunión")
        elif opcion == 6:
            await update.message.reply_text("Para más información, visite: https://polylinesac.netlify.app/contact/información")
        elif opcion == 7:
            await update.message.reply_text("Gracias por contactarnos. ¡Hasta luego!")
        else:
            await update.message.reply_text("Por favor selecciona una opción válida.")
    elif menu in ["proyectos_venta", "benavides_1", "pueblo_libre_1"]:
        await update.message.reply_text(
            "Has seleccionado un proyecto en venta.\n\n"
            "Para agendar su cita puede entrar a este enlace: https://polylinesac.netlify.app/contact/agenda%20una%20reunión\n"
            "Para más información: https://polylinesac.netlify.app/contact/información"
        )
        context.user_data["menu"] = "principal"

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    job_queue = JobQueue()
    job_queue.set_application(app)  # Asociamos JobQueue con la app
    await job_queue.start()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":

   asyncio.get_event_loop().run_until_complete(main())