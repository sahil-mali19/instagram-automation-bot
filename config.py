"""
config.py — Bot Configuration
Author: Sahil Mali | MSc BA&C, Strathclyde

Loads credentials from .env file. Copy .env.example → .env and fill in.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── Instagram Credentials (load from .env) ───────────────────────────
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', 'your_username')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', 'your_password')

    # ── File Paths ────────────────────────────────────────────────────────
    SESSION_FILE        = 'config/session.json'
    PROCESSED_CACHE_FILE= 'logs/processed_ids.json'
    LOG_FILE            = 'logs/bot.log'

    # ── Polling ───────────────────────────────────────────────────────────
    POLL_INTERVAL       = 30       # seconds between message checks

    # ── Human-like delay range before sending reply (seconds) ────────────
    MIN_REPLY_DELAY     = 3.0
    MAX_REPLY_DELAY     = 9.0

    # ── Reply Templates (edit these for your business) ────────────────────
    REPLIES = {
        # Pricing / Cost queries
        'price': (
            "Hi! Thanks for reaching out 😊 Our pricing depends on the specific "
            "service or product you're interested in. Could you share more details "
            "so I can give you an accurate quote? I'll get back to you shortly!"
        ),
        'cost': (
            "Hey! Thank you for your message. Our rates vary by package — "
            "I'd love to help you find the best option. Could you tell me a bit "
            "more about what you're looking for?"
        ),
        'how much': (
            "Thanks for asking! Pricing starts from £X depending on your requirements. "
            "DM me your details and I'll send you a personalised quote 🙌"
        ),

        # Order / Purchase queries
        'order': (
            "Great news — we'd love to have you as a customer! 🎉 "
            "To place an order, please visit [your link] or reply here "
            "with the items you'd like and I'll process it for you."
        ),
        'buy': (
            "Awesome, let's get that sorted for you! Please visit [your link] "
            "or let me know exactly what you'd like and I'll help you out right away 💪"
        ),
        'purchase': (
            "Thanks for your interest! You can purchase via [your link]. "
            "Need any help choosing the right product? Just ask!"
        ),

        # Availability / Timing queries
        'available': (
            "Hi there! Yes, we're currently available and taking new enquiries. "
            "What can I help you with today? 😊"
        ),
        'open': (
            "We're open Monday–Friday, 9am–6pm. "
            "Feel free to message anytime — I check DMs regularly and aim to "
            "respond within a few minutes during business hours!"
        ),
        'time': (
            "Our business hours are Mon–Fri, 9am–6pm. "
            "We also respond to DMs on weekends when possible. How can I help?"
        ),

        # Delivery / Shipping
        'delivery': (
            "Standard delivery typically takes 3–5 working days within the UK. "
            "Express (1–2 days) is also available. International shipping available "
            "— timeframes vary by destination. Any other questions?"
        ),
        'shipping': (
            "We ship UK-wide and internationally! 📦 UK delivery: 3–5 days. "
            "International: 7–14 days depending on location. "
            "All orders are tracked — you'll receive a tracking link via email."
        ),

        # Collaboration / Partnership
        'collab': (
            "We love collaborating with creators and businesses! 🤝 "
            "Please share your Instagram handle, audience size, and what you have "
            "in mind — I'll review and get back to you within 24 hours."
        ),
        'collaborate': (
            "Exciting! We're always open to meaningful collaborations. "
            "Send over your media kit or a brief about your idea and "
            "we'll take it from there 🙌"
        ),
        'partnership': (
            "Thank you for thinking of us for a partnership! "
            "Please share more details about your proposal — "
            "we review all partnership requests carefully and respond within 48 hours."
        ),

        # Returns / Refunds
        'return': (
            "We have a 30-day hassle-free return policy. "
            "To start a return, please reply with your order number and reason. "
            "We'll arrange collection and process your refund within 5–7 business days."
        ),
        'refund': (
            "Refunds are processed within 5–7 business days to your original "
            "payment method. Please send your order number and I'll look into it "
            "right away for you!"
        ),

        # General greetings
        'hello': (
            "Hey! 👋 Great to hear from you! How can I help you today? "
            "Feel free to ask about products, pricing, orders, or anything else 😊"
        ),
        'hi': (
            "Hi there! Thanks for reaching out! 😊 What can I help you with today?"
        ),
        'hey': (
            "Hey! 👋 What can I do for you today? I'm here to help!"
        ),

        # Thank you
        'thank': (
            "You're very welcome! 😊 Is there anything else I can help you with? "
            "We really appreciate your support!"
        ),
        'thanks': (
            "No problem at all! Happy to help 🙌 Anything else you need?"
        ),
    }

    # ── Default fallback reply ────────────────────────────────────────────
    DEFAULT_REPLY = (
        "Hi! Thanks so much for your message! 😊 "
        "I'll get back to you as soon as possible — usually within a few minutes. "
        "In the meantime, feel free to check out our profile for more information!"
    )

    # ── Business info for enriched replies ───────────────────────────────
    BUSINESS_NAME = "Your Business Name"
    WEBSITE_URL   = "https://yourwebsite.com"
    SUPPORT_EMAIL = "support@yourbusiness.com"
