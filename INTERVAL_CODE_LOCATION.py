"""
WHERE THE INTERVAL CODE IS DEPLOYED
====================================

This explains where each part of the monitoring interval code lives
and how they work together.
"""

# ============================================================================
# FILE 1: auto_move_spam.py (THE MAIN MONITOR SCRIPT)
# ============================================================================
# Location: auto_move_spam.py
# Lines: ~105-140 (in the monitor_continuous function)

"""
def monitor_continuous(interval_minutes=5):
    '''
    Monitor inbox continuously and move spam
    
    Args:
        interval_minutes: Check inbox every N minutes
    '''
    print("="*70)
    print("CONTINUOUS MONITORING MODE")
    print("="*70)
    print(f"Will check inbox every {interval_minutes} minutes")
    print("Press Ctrl+C to stop\\n")
    
    try:
        spam_filter = GmailSpamFilter('credentials.json')
        check_count = 0
        
        while True:  # ← INFINITE LOOP (starts monitoring)
            check_count += 1
            print(f"\\n🔄 Check #{check_count} at {datetime.now().strftime('%H:%M:%S')}")
            print("-"*70)
            
            # CHECK INBOX
            results = spam_filter.batch_check_and_move(
                max_results=10,
                auto_move=True,
                confidence_threshold=0.7
            )
            
            print(f"Summary: {len(results['legitimate'])} legit, " \\
                  f"{len(results['spam'])} spam, " \\
                  f"{results.get('moved_to_spam', 0)} moved")
            
            # ↓ THIS IS THE INTERVAL CODE
            print(f"\\n⏳ Next check in {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)  # ← WAITS HERE
            # ↑ Converts minutes to seconds (5 * 60 = 300 seconds)
"""

# ============================================================================
# THE INTERVAL CODE - DETAILED BREAKDOWN
# ============================================================================

"""
CODE LOCATION & PARTS:
======================

FILE: auto_move_spam.py
FUNCTION: monitor_continuous()
LINE: ~139 (approximately)

THE ACTUAL INTERVAL CODE:
┌─────────────────────────────────────────┐
│ time.sleep(interval_minutes * 60)       │
└─────────────────────────────────────────┘

BREAKDOWN:
──────────
time.sleep()           ← Python function that pauses execution
interval_minutes       ← Parameter you pass in (default: 5)
* 60                   ← Converts MINUTES to SECONDS
                         (5 minutes × 60 seconds = 300 seconds)


EXAMPLES:
─────────
interval_minutes=1   → time.sleep(1 * 60)   → Waits 60 seconds
interval_minutes=5   → time.sleep(5 * 60)   → Waits 300 seconds (5 min)
interval_minutes=10  → time.sleep(10 * 60)  → Waits 600 seconds (10 min)
interval_minutes=60  → time.sleep(60 * 60)  → Waits 3600 seconds (1 hour)
"""

# ============================================================================
# FILE 2: gmail_integration.py (BATCH CHECK FUNCTION)
# ============================================================================
# Location: gmail_integration.py
# Method: GmailSpamFilter.batch_check_and_move()

"""
This is CALLED BY the monitor every N minutes:

def batch_check_and_move(self, max_results=10, auto_move=True, 
                         confidence_threshold=0.7):
    '''
    Convenience method to check inbox and automatically move spam
    '''
    print(f"🔍 Checking top {max_results} emails...")
    results = self.check_inbox_for_spam(
        query='is:unread',
        max_results=max_results,
        auto_move=auto_move,
        confidence_threshold=confidence_threshold
    )
    
    self.print_results(results)
    
    return results


EXECUTION FLOW:
───────────────
1. monitor_continuous() starts
2. EVERY N minutes:
   ├─ Calls spam_filter.batch_check_and_move()
   ├─ This fetches unread emails (including NEW ones)
   ├─ Classifies them
   ├─ Moves spam to spam folder
   ├─ Shows results
   └─ Returns control to monitor
3. time.sleep(interval_minutes * 60) pauses the loop
4. After pause, loop starts again (GOTO step 2)
"""

# ============================================================================
# COMPLETE CODE MAP
# ============================================================================

print("""
COMPLETE DEPLOYMENT MAP
=======================

┌─────────────────────────────────────────────────────────────┐
│ FILE: auto_move_spam.py                                     │
│                                                             │
│ if __name__ == "__main__":                                  │
│     if sys.argv[1] == '--monitor':                          │
│         interval = int(sys.argv[2]) if len(sys.argv) > 2   │
│                    else 5                                   │
│         monitor_continuous(interval)  ← ENTRY POINT        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ FUNCTION: monitor_continuous(interval_minutes=5)            │
│                                                             │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ while True:  (infinite loop)                           │ │
│ │    ├─ Check #1, #2, #3... (increments)               │ │
│ │    ├─ Calls: spam_filter.batch_check_and_move()      │ │
│ │    ├─ Shows results                                   │ │
│ │    └─ time.sleep(interval_minutes * 60) ← WAITS HERE │ │
│ │                                                        │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ FILE: gmail_integration.py                                  │
│ METHOD: batch_check_and_move()                              │
│                                                             │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Calls: self.check_inbox_for_spam()                     │ │
│ │   ├─ Fetches top 10 unread emails (NEW + OLD)         │ │
│ │   ├─ For each email:                                  │ │
│ │   │   ├─ Classify using SpamClassifier               │ │
│ │   │   └─ If spam: Move to spam folder                │ │
│ │   └─ Return results                                   │ │
│ │                                                        │ │
│ │ Calls: self.print_results()                           │ │
│ │   └─ Displays summary                                 │ │
│ │                                                        │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ FILE: spam_classifier.py                                    │
│ CLASS: SpamClassifier                                       │
│                                                             │
│ For each email:                                             │
│   ├─ Rule-based detection (regex patterns)                │
│   ├─ Keyword-based detection (spam words)                 │
│   └─ ML-based detection (trained model)                   │
│                                                             │
│ Returns: Classification result with confidence score       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    [BACK TO monitor_continuous]
                              ↓
                    PAUSE: time.sleep(300 seconds)
                              ↓
                    [LOOP REPEATS - Back to WHILE TRUE]
""")

# ============================================================================
# HOW TO RUN - COMMAND LINE
# ============================================================================

print("""
HOW TO RUN THE MONITOR
======================

COMMAND LINE USAGE:
───────────────────

1. DEFAULT (5 minutes interval):
   $ python auto_move_spam.py --monitor
   
   What happens:
   └─ Checks every 5 minutes (default)
   └─ interval = 5 (hardcoded default)

2. CUSTOM INTERVAL (your choice):
   $ python auto_move_spam.py --monitor 10
   
   What happens:
   └─ Checks every 10 minutes
   └─ interval = 10 (from command line argument)

3. PYTHON CODE:
   from auto_move_spam import monitor_continuous
   
   monitor_continuous()           # 5 minutes (default)
   monitor_continuous(10)         # 10 minutes
   monitor_continuous(1)          # 1 minute
   monitor_continuous(60)         # 1 hour

HOW COMMAND LINE ARGUMENT WORKS:
────────────────────────────────

$ python auto_move_spam.py --monitor 3

Execution:
└─ sys.argv[1] = '--monitor'
└─ sys.argv[2] = '3'
└─ interval = int(sys.argv[2]) = 3
└─ monitor_continuous(3)  ← Called with 3 minutes interval
""")

# ============================================================================
# CODE PATH WITH TIMING
# ============================================================================

print("""
TIMELINE EXAMPLE - 5 MINUTE INTERVAL
=====================================

10:00:00 - Program started
          └─ monitor_continuous(interval_minutes=5)
          └─ while True loop begins

10:00:01 - Check #1 starts
          ├─ Fetches 10 unread emails
          ├─ Classifies each
          ├─ Moves 2 spam emails
          └─ Shows results

10:00:05 - Check #1 ends, enters time.sleep()
          └─ time.sleep(5 * 60) = time.sleep(300)
          └─ Program PAUSES for 300 seconds

10:05:05 - Pause ends, loop continues
          └─ check_count = 2

10:05:06 - Check #2 starts
          ├─ NEW emails included in fetch!
          ├─ Fetches 10 unread emails (includes new arrivals)
          ├─ Classifies each
          ├─ Moves 1 spam email
          └─ Shows results

10:05:10 - Check #2 ends, enters time.sleep()
          └─ Pauses another 300 seconds

10:10:10 - Check #3 starts
          └─ [Process repeats...]

[This continues until user presses Ctrl+C]

KEY POINT: Each time loop runs, it fetches FRESH emails
           including ANY that arrived during the sleep period!
""")

# ============================================================================
# WHERE EACH PIECE LIVES
# ============================================================================

print("""
QUICK REFERENCE - WHERE IS WHAT?
=================================

INTERVAL LOGIC:
├─ File: auto_move_spam.py
├─ Function: monitor_continuous()
├─ Line: ~139
└─ Code: time.sleep(interval_minutes * 60)

INFINITE LOOP:
├─ File: auto_move_spam.py
├─ Function: monitor_continuous()
├─ Line: ~119
└─ Code: while True:

FETCH EMAILS:
├─ File: gmail_integration.py
├─ Function: check_inbox_for_spam()
├─ Uses: gmail.get_emails(query='is:unread', max_results=10)
└─ Returns: Fresh list of unread emails each time

CLASSIFY EMAILS:
├─ File: spam_classifier.py
├─ Class: SpamClassifier
└─ Method: classify_email()

MOVE SPAM:
├─ File: gmail_integration.py
├─ Function: move_email_to_spam()
└─ Gmail API: AddLabel SPAM, RemoveLabel INBOX

COMMAND LINE PARSING:
├─ File: auto_move_spam.py
├─ Lines: 188-200 (in __main__)
└─ Checks: sys.argv for --monitor flag


PARAMETER FLOW:
───────────────
Command Line
    ↓
$ python auto_move_spam.py --monitor 5
    ↓
sys.argv[2] = '5'
    ↓
interval = int('5') = 5
    ↓
monitor_continuous(interval=5)
    ↓
time.sleep(5 * 60) = time.sleep(300)
    ↓
Waits 300 seconds (5 minutes)
    ↓
Loop repeats
""")

# ============================================================================
# WHAT HAPPENS EACH ITERATION
# ============================================================================

print("""
DETAILED ITERATION BREAKDOWN
=============================

ITERATION #1
────────────
1. Print check header
2. Create results container
3. Call batch_check_and_move()
   ├─ Call check_inbox_for_spam()
   │  ├─ Fetch top 10 unread emails
   │  ├─ For each email:
   │  │  ├─ Combine text (subject + body + sender)
   │  │  ├─ Run classification (3 methods)
   │  │  ├─ Get confidence score
   │  │  └─ If spam & confidence > 0.7:
   │  │     └─ Move to spam folder
   │  └─ Return results
   └─ Print results summary
4. Print countdown message
5. Enter time.sleep(interval_minutes * 60)
   └─ CPU suspends, waits for timer
6. Timer expires
7. Loop continues to ITERATION #2


BETWEEN ITERATIONS
──────────────────
During time.sleep():
├─ Computer can do other things
├─ Gmail gets new emails
├─ Process is "paused"
└─ Waiting for interval to expire

What happens to NEW emails:
├─ They arrive in INBOX
├─ Monitor is sleeping (doesn't see them yet)
├─ When sleep ends, next iteration fetches them
└─ They get classified and moved if spam


ITERATION #2 (after sleep)
───────────────────────────
1. check_count increments (1 → 2)
2. Print check header with new timestamp
3. Same process as iteration #1
   └─ But with UPDATED email list (includes new emails!)
4. Repeat steps 4-7


THIS REPEATS FOREVER
────────────────────
└─ Until user presses Ctrl+C
└─ Then: KeyboardInterrupt exception caught
└─ Print: "✅ Monitoring stopped"
└─ Program exits gracefully
""")
