import ZeroCalendarBot.bot_support as bot_support
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from loggers import telegrambot_logger

USE_PRIVATE_CHAT = True
ACTIVATE_CHAT_ID_REQUEST = False

# Telegram BOT Vars
bot_support.load_env_vars()
BOT_TOKEN = bot_support.get_bot_token()

if not USE_PRIVATE_CHAT:
    GROUP_ID = bot_support.get_group_id()
else:
    GROUP_ID = bot_support.get_debug_chat_id()

print(GROUP_ID)

# Start bot
telegram_bot_app = Application.builder().token(token=BOT_TOKEN).build()

# =========================================================
#                       COMMANDS
# =========================================================

# async def help_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Hello! This function is disabled, cya!")

if ACTIVATE_CHAT_ID_REQUEST:
    async def chatid_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Chat ID: {update.effective_chat.id}")

# =========================================================
#                       CRAFT RESPONSES
# =========================================================

if ACTIVATE_CHAT_ID_REQUEST:
    def handle_response(text : str) -> str:
        text = text.lower()

        if 'helo' in text:
            return "helo"
        return "Polite people say helo"

# =========================================================
#                       SEND MESSAGES
# =========================================================

if ACTIVATE_CHAT_ID_REQUEST:
    async def handle_message(update : Update, context: ContextTypes.DEFAULT_TYPE):
        message_type : str = update.message.chat.type # Group or nah?
        text : str = update.message.text # Incoming message from user

        print(f"User {update.message.chat.id} in {message_type}: {text}")

async def send_message_in_ZeroCalendar_group_chat( text : str):
    telegrambot_logger.info(f'SENT MESSAGE -> "{repr(text)}"')
    await telegram_bot_app.bot.send_message(
        chat_id=GROUP_ID,
        text=text,
        parse_mode="Markdown"
    )

# =========================================================
#                       LOG ERRORS
# =========================================================

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = f"Update {update} caused error {context.error}"
    print(s)
    telegrambot_logger.error(repr(s))


# =========================================================
#                      STARTUP LOGIC
# =========================================================


def main():
    try:
        s = "-----------------< TELEGRAM BOT STARTED >-----------------"
        print(s)
        telegrambot_logger.info(s)

        # Commands
        if ACTIVATE_CHAT_ID_REQUEST:
            telegram_bot_app.add_handler(CommandHandler('chatid', chatid_command))
        # telegram_bot_app.add_handler(CommandHandler('help', help_command))

            # Messages
            telegram_bot_app.add_handler(MessageHandler(filters.TEXT, handle_message))

        # Errors
        telegram_bot_app.add_error_handler(error)

        if ACTIVATE_CHAT_ID_REQUEST:
            print("ACTIVATE_CHAT_ID_REQUEST IS ON: Polling")
            telegrambot_logger.warning("ACTIVATE_CHAT_ID_REQUEST IS ON, POLLING")
            telegram_bot_app.run_polling(poll_interval=5) # Check updates every 5 seconds
        elif USE_PRIVATE_CHAT:
            import asyncio
            # If no polling, but bot in debug mode, just keep alive
            s = "Bot started WITHOUT polling but with keepalive: sleeping forever"
            telegrambot_logger.warning(s)
            print(s)
            asyncio.get_event_loop().run_forever()

    except Exception as e:
        telegrambot_logger.critical(repr(str(e)))


# ====================================
#           LOG PROCESS DEATH
# ====================================


def handle_exit_sigint():
    s = "-------!!!-------< TELEGRAM BOT SHUTTING DOWN (ctrl+c) >-------!!!-------"
    telegrambot_logger.warning(s)
    print(s)

    # Here should go any fancy logic for safe death handling. Nothing for now :)

def handle_exit_sigterm():
    s = "-------!!!-------< TELEGRAM BOT SHUTTING DOWN (systemctl or kill) >-------!!!-------"
    telegrambot_logger.warning(s)
    print(s)

    # Here should go any fancy logic for safe death handling. Nothing for now :)