import discord
from discord.ext import commands
import random

# Configuración del bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Listas originales
datos_climaticos = [
    "🌡️ La temperatura global promedio ha aumentado 1,1 °C desde la era preindustrial.",
    "🧊 Los glaciares se están derritiendo a un ritmo sin precedentes, contribuyendo al aumento del nivel del mar.",
    "🌍 Más del 90% del calentamiento global se almacena en los océanos.",
    "🌲 Se pierden aproximadamente 10 millones de hectáreas de bosque al año debido a la deforestación.",
    "🚗 El sector del transporte contribuye con el 14% de las emisiones globales de gases de efecto invernadero.",
    "🌊 Los niveles del mar han aumentado más de 20 cm desde 1880.",
    "🔥 Los eventos climáticos extremos, como huracanes y olas de calor, son más frecuentes debido al cambio climático."
]

posibles_soluciones = [
    "🌱 Reforestar: Plantar árboles para absorber CO₂.",
    "☀️ Energías renovables: Usar energía solar, eólica y otras fuentes limpias.",
    "🚲 Transporte sostenible: Usar bicicletas, caminar o vehículos eléctricos.",
    "🗑️ Reducir residuos: Reciclar y evitar plásticos de un solo uso.",
    "🍃 Consumo consciente: Comprar productos locales y sostenibles.",
    "💡 Eficiencia energética: Usar bombillas LED y apagar dispositivos no usados.",
    "🚿 Ahorro de agua: Reducir el tiempo en la ducha y reparar fugas."
]

# Variables para controlar los elementos restantes
datos_restantes = datos_climaticos[:]
soluciones_restantes = posibles_soluciones[:]

# Evento: cuando el bot se conecta
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# Comando: dato climático sin repetición
@bot.command()
async def datosrandom(ctx):
    global datos_restantes
    if not datos_restantes:  # Si la lista está vacía, se reinicia
        datos_restantes = datos_climaticos[:]
    dato = random.choice(datos_restantes)
    datos_restantes.remove(dato)  # Elimina el dato elegido
    await ctx.send(f"Aquí tienes un dato sobre el cambio climático:\n{dato}")

# Comando: solución sin repetición
@bot.command()
async def soluciones(ctx):
    global soluciones_restantes
    if not soluciones_restantes:  # Si la lista está vacía, se reinicia
        soluciones_restantes = posibles_soluciones[:]
    solucion = random.choice(soluciones_restantes)
    soluciones_restantes.remove(solucion)  # Elimina la solución elegida
    await ctx.send(f"Aquí tienes una solución al cambio climático:\n{solucion}")

# Comando: menú de ayuda
@bot.command()
async def menu(ctx):
    menu = (
        "**Menú de Comandos de EcologyBot** 🌱\n\n"
        "**!datosrandom** - Muestra un dato sobre el cambio climático 📢\n"
        "**!soluciones** - Muestra una solución al cambio climático 🎯 \n"
        "**!pregunta** - Te hace una pregunta del cambio climatico 🎟️ \n"
        "**!puntuacion** - Te muestra tu puntuacion obtenida 🏆 \n"
        "**!menu** - Muestra este menú de ayuda 📖\n"
    )
    await ctx.send(menu)

# Sistema de preguntas

preguntas_ecologicas = [
    {"pregunta": "¿Qué gas es el principal responsable del calentamiento global?", "respuesta": "Dióxido de carbono"},
    {"pregunta": "¿Cuál es la principal fuente de energía renovable?", "respuesta": "Solar"},
    {"pregunta": "¿Cuánto ha aumentado el nivel del mar desde 1880?", "respuesta": "Más de 20 cm"},
    {"pregunta": "¿Cuál es el país que más emite CO₂?", "respuesta": "China"},
    {"pregunta": "¿Cuántos grados ha aumentado la temperatura global desde la era preindustrial?", "respuesta": "1,1 °C"}
]

# Sistema de puntuación
puntuaciones = {}

# Comando: Iniciar trivia
@bot.command()
async def pregunta(ctx):
    pregunta = random.choice(preguntas_ecologicas)
    await ctx.send(f"🧠 CONTESTA: {pregunta['pregunta']}")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        respuesta = await bot.wait_for("message", check=check, timeout=15)
        if respuesta.content.lower() == pregunta["respuesta"].lower():
            usuario = str(ctx.author)
            puntuaciones[usuario] = puntuaciones.get(usuario, 0) + 1
            await ctx.send(f"✅ ¡Correcto, {usuario}! Tienes {puntuaciones[usuario]} puntos.")
        else:
            await ctx.send(f"❌ Incorrecto. La respuesta correcta es: {pregunta['respuesta']}")
    except:
        await ctx.send("⏰ Tiempo agotado. ¡Inténtalo de nuevo!")

# Comando: Mostrar clasificación
@bot.command()
async def puntuacion(ctx):
    if puntuaciones:
        clasificacion = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)
        mensaje = "**🏆 Puntuacion**\n"
        for idx, (usuario, puntos) in enumerate(clasificacion, start=1):
            mensaje += f"{idx}. {usuario}: {puntos} puntos\n"
        await ctx.send(mensaje)
    else:
        await ctx.send("⚠️ Aún no hay puntuaciones registradas.")

# Evento: Bot conectado
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


# Reemplaza "TU_TOKEN_AQUÍ" con el token de tu bot
bot.run("token aqui")
