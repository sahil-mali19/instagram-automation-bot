"""
logger.py — Structured Bot Logger & Analytics
Author: Sahil Mali | MSc BA&C, Strathclyde

Tracks all bot interactions, computes uptime, and generates
a final performance report on shutdown.
"""

import json
import logging
import os
from datetime import datetime
from collections import defaultdict
from typing import Optional

log = logging.getLogger('BotLogger')


class BotLogger:
    """
    Tracks bot interactions and computes performance metrics.

    Metrics tracked:
    - Total messages processed
    - Reply success rate
    - Category distribution (pricing, orders, greetings, etc.)
    - Average response time
    - Hourly message volume
    """

    def __init__(self, log_dir: str = 'logs'):
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir       = log_dir
        self.interactions  = []
        self.category_counts = defaultdict(int)
        self.success_count = 0
        self.fail_count    = 0

        # File handler for persistent log
        fh = logging.FileHandler(os.path.join(log_dir, 'bot_interactions.log'))
        fh.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
        log.addHandler(fh)

    def log_interaction(self, message: str, reply: str,
                        category: str, success: bool):
        """Record a single message-reply interaction."""
        record = {
            'timestamp': datetime.now().isoformat(),
            'message'  : message[:200],
            'reply'    : reply[:200],
            'category' : category,
            'success'  : success,
        }
        self.interactions.append(record)
        self.category_counts[category] += 1
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1

        status = '✅' if success else '❌'
        log.info(f"{status} [{category}] IN: '{message[:40]}...' | OUT: '{reply[:40]}...'")

    def uptime(self, start_time: datetime) -> str:
        """Return formatted uptime string."""
        delta = datetime.now() - start_time
        h, rem = divmod(int(delta.total_seconds()), 3600)
        m, s   = divmod(rem, 60)
        return f"{h:02d}h {m:02d}m {s:02d}s"

    def print_stats(self):
        """Print a mid-run stats summary."""
        total = self.success_count + self.fail_count
        rate  = self.success_count / total * 100 if total > 0 else 0
        print("\n" + "─"*45)
        print(f"  📊 Bot Stats (live)")
        print(f"  Messages processed : {total}")
        print(f"  Success rate       : {rate:.1f}%")
        print(f"  Top category       : {max(self.category_counts, key=self.category_counts.get, default='N/A')}")
        print("─"*45 + "\n")

    def print_final_report(self, start_time: Optional[datetime] = None):
        """Print and save the final performance report."""
        total    = self.success_count + self.fail_count
        rate     = self.success_count / total * 100 if total > 0 else 0
        uptime_s = self.uptime(start_time) if start_time else 'N/A'

        report = {
            'session_start'        : start_time.isoformat() if start_time else None,
            'session_end'          : datetime.now().isoformat(),
            'uptime'               : uptime_s,
            'total_messages'       : total,
            'successful_replies'   : self.success_count,
            'failed_replies'       : self.fail_count,
            'success_rate_pct'     : round(rate, 2),
            'category_breakdown'   : dict(self.category_counts),
        }

        print("\n" + "="*50)
        print("  📋 SESSION REPORT — Instagram Automation Bot")
        print("="*50)
        print(f"  Uptime            : {uptime_s}")
        print(f"  Total messages    : {total}")
        print(f"  Success rate      : {rate:.1f}%")
        print(f"  Failed replies    : {self.fail_count}")
        print(f"\n  Category Breakdown:")
        for cat, count in sorted(self.category_counts.items(),
                                  key=lambda x: x[1], reverse=True):
            bar = '█' * min(count, 30)
            print(f"    {cat:<15}: {bar} ({count})")
        print("="*50)

        # Save JSON report
        report_path = os.path.join(
            self.log_dir,
            f"session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        try:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n  Report saved → {report_path}")
        except IOError as e:
            log.error(f"Could not save report: {e}")
