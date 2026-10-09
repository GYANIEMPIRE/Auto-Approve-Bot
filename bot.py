
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    ChatJoinRequestHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

VIDEO_LINK = "https://t.me/c/4327455535/4"
APK_FILE_ID = os.getenv("APK_FILE_ID", "").strip()
VOICE_FILE_ID = os.getenv("VOICE_FILE_ID", "").strip()

WELCOME = (
    " HELLO BABY🥰\n\n"
    "AAPKI REQUEST JALDI HI APPROVE HO JAYEGI ✅\n\n"
    "SETUP VIDEO & HACK APK NEECHE DIYA GAYA HAI VIDEO 
    DEKHO AUR PANEL KO USE KARO BABY👇"
)


async def handle_join_request(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    request = update.chat_join_request

    if request is None:
        return

    # Sirf configured channel ki requests handle karo.
    if str(request.chat.id) != -1004327455535:
        return

    user_chat_id = request.user_chat_id

    # Telegram ke temporary private-message access ka use karo.
    try:
        await context.bot.send_message(
            chat_id=user_chat_id,
            text=WELCOME,
        )

        # Video link seedhe message mein, bina button.
        await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"🎬 SETUP VIDEO\n{https://t.me/c/4327455535/4}",
        )

        # APK upload karne ke baad uska file_id Config Vars mein rakho.
        if APK_FILE_ID:
            await context.bot.send_document(
                chat_id=user_chat_id,
                document=APK_FILE_ID,
                caption="📥 APK FILE",
            )

        # Voice note baad mein add kar sakte ho.
        if VOICE_FILE_ID:
            await context.bot.send_voice(
                chat_id=user_chat_id,
                voice=VOICE_FILE_ID,
            )

    except Exception:
        logging.exception(
            "User ko message bhejne mein problem hui."
        )

    # Request ko automatically approve karo.
    try:
        await context.bot.approve_chat_join_request(
            chat_id=request.chat.id,
            user_id=request.from_user.id,
        )
        logging.info("Join request approved.")

    except Exception:
        logging.exception("Request approve nahi hui.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        ChatJoinRequestHandler(handle_join_request)
    )

    logging.info("Auto Approve Bot started.")
    app.run_polling(
        allowed_updates=["chat_join_request"]
    )


if __name__ == "__main__":
    main()
