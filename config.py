"""
Personal Assistant Bot — Configuration
Loads credentials and settings from environment variables.
"""

import os

# ==================== BOT CREDENTIALS ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
PORT = int(os.getenv("PORT", 8080))

# ==================== STARTUP VALIDATION ====================
if not BOT_TOKEN:
    # We will log a warning or let it fail gracefully if token is missing
    # so that the user has a chance to set it before running
    pass
