"""
Personal Assistant Bot — Main Entry Point
Handles account generation and OTP verification.
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

from config import BOT_TOKEN, WEBHOOK_URL, PORT
from utils import validate_totp_secret, generate_totp, get_totp_remaining_seconds
from generator import generate_accounts

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcoming message with instructions."""
    welcome_text = (
        "🤖 <b>Personal Assistant Bot</b>\n\n"
        "Welcome! I have two utility features designed to make registration flows easy:\n\n"
        "1️⃣ <b>🎲 Account Generator</b>\n"
        "Send any number between <b>1 and 30</b> (e.g. <code>15</code>) and I will generate "
        "that many random account details. The outputs are fully formatted in <code>click-to-copy</code> code blocks!\n\n"
        "2️⃣ <b>🔑 OTP Verification (2FA)</b>\n"
        "Send a 2-Step Verification secret key (e.g. from Google's Authenticator setup) "
        "and I will generate the 6-digit OTP code with a <b>🔄 Refresh</b> button.\n\n"
        "<i>Simply type a number or paste a secret key to start!</i>"
    )
    await update.message.reply_text(welcome_text, parse_mode="HTML")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route text inputs to either Account Generator or OTP Verification."""
    text = update.message.text.strip()
    chat_id = update.effective_chat.id

    # 1. Check if the user entered a number (Account Generator)
    if text.isdigit():
        count = int(text)
        if count < 1 or count > 30:
            await update.message.reply_text(
                "⚠️ <b>Invalid Quantity</b>\n\nPlease enter a number between <b>1 and 30</b>.",
                parse_mode="HTML"
            )
            return

        # Generate accounts
        await update.message.reply_text(f"⏳ Generating {count} accounts on the fly...")
        accounts = generate_accounts(count)

        if not accounts:
            await update.message.reply_text("⚠️ Account generation failed. Please try again.")
            return

        # We batch accounts in groups of 10 to prevent hitting Telegram's 4096-character limit per message
        batch_size = 10
        for i in range(0, len(accounts), batch_size):
            batch = accounts[i:i + batch_size]
            msg_lines = []
            
            for idx, acc in enumerate(batch, start=i + 1):
                gender_label = "Male" if acc["gender"] == "M" else "Female"
                msg_lines.append(
                    f"📦 <b>Account {idx}</b>\n"
                    f"👤 <b>First Name:</b> <code>{acc['first_name']}</code>\n"
                    f"👤 <b>Last Name:</b>  <code>{acc['last_name']}</code>\n"
                    f"🎂 <b>DOB:</b>        <code>{acc['dob']}</code>\n"
                    f"⚧️ <b>Gender:</b>     <code>{gender_label}</code>\n"
                    f"📧 <b>Email:</b>      <code>{acc['email']}</code>\n"
                    f"🔑 <b>Password:</b>   <code>{acc['password']}</code>\n"
                    f"━━━━━━━━━━━━━━━━━━━━"
                )
            
            message_text = "\n\n".join(msg_lines)
            await context.bot.send_message(chat_id, message_text, parse_mode="HTML")
        return

    # 2. Check if the user entered a 2FA secret key (OTP Verification)
    is_valid_secret, result = validate_totp_secret(text)
    if is_valid_secret:
        secret = result
        otp = generate_totp(secret)
        remaining = get_totp_remaining_seconds()

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh OTP", callback_data="refresh_otp")]
        ])

        msg = await update.message.reply_text(
            f"🔑 <b>Your 2FA Code</b>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"  📟  <code>{otp}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"⏱ Valid for <b>{remaining}s</b>\n\n"
            f"💡 Paste code into the verification page.",
            reply_markup=kb, parse_mode="HTML"
        )
        
        # Store the secret in context.user_data keyed by this message ID to handle refreshes securely
        context.user_data[f"otp_secret_{msg.message_id}"] = secret
        return

    # 3. Fallback for unrecognized text
    fallback_text = (
        "❓ <b>Unrecognized Input</b>\n\n"
        "I didn't understand that message. Please send:\n"
        "• A number from <b>1 to 30</b> to generate accounts.\n"
        "• A valid <b>2FA secret key</b> to get an OTP.\n\n"
        "Send /start to show instructions."
    )
    await update.message.reply_text(fallback_text, parse_mode="HTML")


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the '🔄 Refresh OTP' button clicks."""
    q = update.callback_query
    await q.answer()

    if q.data == "refresh_otp":
        message_id = q.message.message_id
        secret = context.user_data.get(f"otp_secret_{message_id}")

        if not secret:
            await q.edit_message_text(
                "⚠️ <b>Session Expired</b>\n\nThe 2FA session expired. Please send the secret key again.",
                parse_mode="HTML"
            )
            return

        otp = generate_totp(secret)
        remaining = get_totp_remaining_seconds()

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh OTP", callback_data="refresh_otp")]
        ])

        # Safely edit message to show the refreshed code
        try:
            await q.edit_message_text(
                f"🔑 <b>Your 2FA Code (Refreshed)</b>\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"  📟  <code>{otp}</code>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⏱ Valid for <b>{remaining}s</b>\n\n"
                f"💡 Paste code into the verification page.",
                reply_markup=kb, parse_mode="HTML"
            )
        except Exception as e:
            # Under some circumstances edit_message_text fails if contents are identical
            # (e.g. if code was refreshed within the same 30s window and output is identical)
            logger.warning(f"Failed to edit message: {e}")


def main():
    """Start the bot."""
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN environment variable is not set!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # Add Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback_query))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ── Webhook vs Polling ──
    webhook_url = WEBHOOK_URL
    if webhook_url:
        full_webhook = f"{webhook_url}/webhook/{BOT_TOKEN}"
        print(f"🌐 Running in WEBHOOK mode on port {PORT}")
        print(f"   Webhook: {full_webhook}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=f"webhook/{BOT_TOKEN}",
            webhook_url=full_webhook,
        )
    else:
        print("🔄 Running in POLLING mode (local development)")
        app.run_polling()


if __name__ == "__main__":
    main()
