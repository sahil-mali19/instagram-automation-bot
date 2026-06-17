"""
reply_engine.py — Intelligent Reply Generation
Author: Sahil Mali | MSc BA&C, Strathclyde

Matches incoming message text to the best reply template using:
  1. Exact keyword matching
  2. Partial/substring matching
  3. Priority scoring (longer keyword = more specific = higher priority)
  4. Fallback to default reply
"""

import re
import logging
from typing import Tuple
from config import Config

log = logging.getLogger('ReplyEngine')


class ReplyEngine:
    """
    Keyword-based intelligent reply engine.

    Processes raw message text → cleans it → matches keywords →
    returns the best matching reply + category label.
    """

    # Category labels mapped to keywords (for analytics logging)
    CATEGORIES = {
        'pricing'      : ['price', 'cost', 'how much', 'rate', 'fee', 'charge'],
        'order'        : ['order', 'buy', 'purchase', 'get one', 'want to buy'],
        'availability' : ['available', 'open', 'time', 'hours', 'when'],
        'shipping'     : ['delivery', 'shipping', 'ship', 'dispatch', 'send'],
        'collaboration': ['collab', 'collaborate', 'partnership', 'sponsor', 'work together'],
        'returns'      : ['return', 'refund', 'exchange', 'cancel'],
        'greeting'     : ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
        'appreciation' : ['thank', 'thanks', 'appreciate', 'great service'],
    }

    def __init__(self, config: Config):
        self.cfg = config
        # Sort keywords by length descending — longer = more specific = higher priority
        self._keyword_map = sorted(
            self.cfg.REPLIES.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        log.info(f"ReplyEngine loaded {len(self._keyword_map)} keyword templates")

    def _clean(self, text: str) -> str:
        """Normalise text for matching: lowercase, strip punctuation."""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)   # Remove punctuation
        text = re.sub(r'\s+', ' ', text)        # Collapse whitespace
        return text

    def _categorise(self, text: str) -> str:
        """Return the highest-matching category label for a message."""
        cleaned = self._clean(text)
        for category, keywords in self.CATEGORIES.items():
            for kw in keywords:
                if kw in cleaned:
                    return category
        return 'general'

    def generate_reply(self, message_text: str) -> Tuple[str, str]:
        """
        Match message text to best reply template.

        Args:
            message_text: Raw incoming DM text

        Returns:
            Tuple of (reply_text, category_label)
        """
        if not message_text or not message_text.strip():
            return self.cfg.DEFAULT_REPLY, 'empty'

        cleaned = self._clean(message_text)
        category = self._categorise(message_text)

        # Match keywords (sorted by length = priority)
        for keyword, reply in self._keyword_map:
            if keyword in cleaned:
                log.debug(f"Matched keyword '{keyword}' → category '{category}'")
                return reply, category

        # No match — use default
        log.debug(f"No keyword match for: '{cleaned[:50]}' — using default reply")
        return self.cfg.DEFAULT_REPLY, 'unmatched'

    def get_stats(self) -> dict:
        """Return engine configuration stats."""
        return {
            'total_keywords'  : len(self._keyword_map),
            'total_categories': len(self.CATEGORIES),
            'keywords'        : [k for k, _ in self._keyword_map],
        }


# ── Quick Test ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cfg = Config()
    engine = ReplyEngine(cfg)

    test_messages = [
        "Hi! What are your prices?",
        "I want to place an order please",
        "How long does delivery take?",
        "Can we collaborate on something?",
        "What is your refund policy?",
        "Hey there!",
        "Thank you so much for your help!",
        "Random message that won't match anything specific",
    ]

    print("\n🧪 ReplyEngine Test Results:")
    print("=" * 65)
    for msg in test_messages:
        reply, cat = engine.generate_reply(msg)
        print(f"\n📩 Input   : '{msg}'")
        print(f"   Category: {cat}")
        print(f"   Reply   : '{reply[:70]}...'")
