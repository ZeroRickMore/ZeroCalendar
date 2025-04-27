import ZeroCalendarBot.bot_support as bot_support
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from loggers import telegrambot_logger
from sys import exit

# =========================================================
#                       COMMANDS
# =========================================================

# async def help_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Hello! This function is disabled, cya!")

# async def start_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(f"Group ID: {update.effective_chat.id} MARY OMOSESSUALE DIROMPENTE")

# =========================================================
#                       CRAFT RESPONSES
# =========================================================

# def handle_response(text : str) -> str:
#     text = text.lower()

#     if 'helo' in text:
#         return "helo"
#     return "Polite people say helo"

# =========================================================
#                       SEND MESSAGES
# =========================================================

# async def handle_message(update : Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type : str = update.message.chat.type # Group or nah?
#     text : str = update.message.text # Incoming message from user

#     print(f"User {update.message.chat.id} in {message_type}: {text}")

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

        # Telegram BOT Vars
        bot_support.load_env_vars()
        BOT_TOKEN = bot_support.get_bot_token()

        global GROUP_ID
        GROUP_ID = bot_support.get_group_id()

        # Start bot
        global telegram_bot_app
        telegram_bot_app = Application.builder().token(token=BOT_TOKEN).build()

        # Commands
        # telegram_bot_app.add_handler(CommandHandler('start', start_command))
        # telegram_bot_app.add_handler(CommandHandler('help', help_command))

        # Messages
        # telegram_bot_app.add_handler(MessageHandler(filters.TEXT, handle_message))

        # Errors
        telegram_bot_app.add_error_handler(error)

        # print("Polling")
        # telegram_bot_app.run_polling(poll_interval=5) # Check updates every 5 seconds

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
    exit(0)

def handle_exit_sigterm():
    s = "-------!!!-------< TELEGRAM BOT SHUTTING DOWN (systemctl or kill) >-------!!!-------"
    telegrambot_logger.warning(s)
    print(s)

    # Here should go any fancy logic for safe death handling. Nothing for now :)
    exit(0)



if __name__ == '__main__':
    main()