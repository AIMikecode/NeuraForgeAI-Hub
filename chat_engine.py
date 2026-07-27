#!/usr/bin/env python3
"""
💬 NEURAFORGEAI CORE - GEMINI CHAT ENGINE
Módulo de conversación inteligente con memoria y contexto del ecosistema.
Ubicación: core/chat_engine.py
"""

import os
import logging
import google.generativeai as genai

logger = logging.getLogger("GeminiChatEngine")

# Configuración de API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Memoria de sesiones de chat activa en memoria (Telegram ID -> Chat Session)
CHAT_SESSIONS = {}

SYSTEM_PROMPT = """
Eres la Inteligencia Artificial oficial de NeuraforgeAI.
Tu objetivo es asistir al usuario dentro de la App de Telegram y la WebApp.
Tienes acceso a los siguientes agentes del ecosistema:
1. Agente Monetízame: Tasación, renta y venta de activos físicos mediante fotos y GPS.
2. Agente Cash: Venta de bots, APKs optimizadas y licencias.
3. Agente Afiliados Cloud: Cashback y retorno de inversión en servidores AWS, GCP y Azure.
4. Agente Sabueso: Búsqueda de liquidez, pagos abandonados y airdrops crypto.

Responde de manera ejecutiva, clara, directa y motivadora. Muestra disponibilidad para procesar imágenes u órdenes.
"""

def obtener_o_crear_chat(telegram_id: str):
    """Recupera la sesión conversacional existente o inicia una nueva con Gemini."""
    if telegram_id not in CHAT_SESSIONS:
        # Usamos el modelo conversacional optimizado
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        CHAT_SESSIONS[telegram_id] = model.start_chat(history=[])
    return CHAT_SESSIONS[telegram_id]

async def responder_con_gemini(telegram_id: str, mensaje_usuario: str) -> str:
    """Procesa el mensaje del usuario en Telegram y devuelve la respuesta generada por Gemini."""
    try:
        chat = obtener_o_crear_chat(telegram_id)
        response = chat.send_message(mensaje_usuario)
        return response.text
    except Exception as e:
        logger.error(f"Error procesando chat con Gemini: {e}")
        return "⚠️ Tuve un pequeño parpadeo de red. ¿Podrías repetir tu consulta?"
