"""
MONITOR FUNCTION EXPLANATION
How continuous email monitoring works
"""

"""
WHAT IS THE MONITOR FUNCTION?
==============================

The monitor_continuous() function checks your Gmail inbox repeatedly
at regular intervals and automatically moves spam emails to spam folder.

It runs continuously until you stop it (Ctrl+C).


HOW IT WORKS - STEP BY STEP
============================

1. START MONITORING
   └─ monitor_continuous(interval_minutes=5)
   
2. EVERY 5 MINUTES (or custom interval):
   ├─ Connect to Gmail API
   ├─ Fetch top 10 UNREAD emails
   ├─ Classify each email (SPAM or LEGITIMATE)
   ├─ Automatically move SPAM to spam folder
   ├─ Show results
   └─ Wait 5 minutes
   
3. REPEAT STEP 2
   └─ Continues indefinitely until you press Ctrl+C


DETAILED FLOW DIAGRAM
=====================

    Start Monitor
        ↓
    [LOOP - Repeats every N minutes]
        ↓
    Fetch TOP 10 UNREAD emails from inbox
        ↓
    For each email:
        ├─ Extract subject, body, sender
        ├─ Classify (3 methods):
        │   ├─ Rule-based (regex patterns)
        │   ├─ Keyword-based (spam words)
        │   └─ ML-based (trained model)
        ├─ Calculate confidence score
        ├─ If confidence > 70% AND is_spam = TRUE:
        │   ├─ Move to SPAM folder ✅
        │   ├─ Remove from INBOX
        │   └─ Count as moved
        └─ Else: Keep in INBOX
        ↓
    Show results:
        ├─ Legitimate count
        ├─ Spam count
        ├─ Moved count
        └─ Errors (if any)
        ↓
    Wait N minutes
        ↓
    [LOOP BACK TO FETCH]


EXAMPLE WORKFLOW
================

TIME: 10:00 AM
────────────────
Monitor started
Checking inbox...

Email 1: "Meeting at 3 PM"
  → Classification: LEGITIMATE ✅
  → Confidence: 95%
  → Action: STAYS IN INBOX

Email 2: "YOU WON $1,000,000!!!"
  → Classification: SPAM 🚨
  → Confidence: 98%
  → Action: MOVED TO SPAM ✅

Email 3: "Project update"
  → Classification: LEGITIMATE ✅
  → Confidence: 92%
  → Action: STAYS IN INBOX

Email 4: "Verify your account"
  → Classification: SPAM 🚨
  → Confidence: 87%
  → Action: MOVED TO SPAM ✅

Summary:
  ✅ Legitimate: 2
  🚨 Spam: 2
  📤 Moved to spam: 2
  ⏳ Next check in 5 minutes...


TIME: 10:05 AM
────────────────
Monitor running...
Checking inbox again...
[NEW EMAILS ARRIVE]

Email 1: "New message from boss"
  → Classification: LEGITIMATE ✅
  → Confidence: 96%
  → Action: STAYS IN INBOX

Email 2: "Click here for FREE MONEY"
  → Classification: SPAM 🚨
  → Confidence: 99%
  → Action: MOVED TO SPAM ✅

Summary:
  ✅ Legitimate: 1
  🚨 Spam: 1
  📤 Moved to spam: 1
  ⏳ Next check in 5 minutes...


KEY FEATURES
============

✅ HANDLES NEW EMAILS
   - Every check fetches the latest unread emails
   - New emails that arrive are automatically classified
   - Works with "is:unread" query

✅ AUTOMATIC MOVEMENT
   - Spam emails are automatically moved to spam folder
   - Removed from INBOX
   - Added to SPAM folder

✅ CONFIDENCE THRESHOLD
   - Only moves if confidence > 70% (configurable)
   - High-confidence spam is moved
   - Uncertain emails stay in inbox for review

✅ ERROR HANDLING
   - Shows connection errors
   - Reports failed movements
   - Continues even if one email fails

✅ DETAILED REPORTING
   - Shows each check's results
   - Running count of processed emails
   - Next check countdown


PARAMETERS EXPLAINED
====================

monitor_continuous(interval_minutes=5)

interval_minutes: int
  │
  └─ How often to check inbox (in minutes)
  
  Examples:
  ├─ 1  = Check every 1 minute  (frequent, uses more API calls)
  ├─ 5  = Check every 5 minutes (default, balanced)
  ├─ 10 = Check every 10 minutes (less frequent)
  └─ 60 = Check every hour (once per hour)


USAGE EXAMPLES
==============

Example 1: DEFAULT - Check every 5 minutes
──────────────────────────────────────────
from auto_move_spam import monitor_continuous

monitor_continuous()  # Defaults to 5 minutes


Example 2: CUSTOM INTERVAL - Check every 10 minutes
─────────────────────────────────────────────────────
monitor_continuous(interval_minutes=10)


Example 3: FREQUENT - Check every minute
───────────────────────────────────────────
monitor_continuous(interval_minutes=1)


Example 4: VIA COMMAND LINE - Check every 3 minutes
─────────────────────────────────────────────────────
python auto_move_spam.py --monitor 3


HANDLING NEW EMAILS
====================

How does it handle NEW emails that arrive?

Each time monitor checks (every N minutes):

1. Fetches top 10 UNREAD emails
   └─ This includes:
      ├─ Old unread emails from before
      ├─ Brand new emails just arrived
      └─ Emails never seen by the system

2. Classifies ALL of them
   └─ Even if classified before, re-checks

3. Moves SPAM to spam folder
   └─ New or old, if spam → moves to spam

Example Timeline:
─────────────────
10:00 AM - Monitor starts
          ├─ Finds 3 unread emails
          ├─ 1 is spam → moved
          └─ Next check at 10:05

10:02 AM - New email arrives
          └─ Monitor NOT running yet (waiting)

10:05 AM - Monitor checks again
          ├─ Finds 4 unread emails (original 2 + new 1)
          ├─ Processes all 4
          ├─ New spam email is caught and moved
          └─ Next check at 10:10

10:10 AM - Monitor checks again
          └─ Only finds legitimate unread
              (all spam already moved)


WHAT GETS CHECKED?
===================

Gmail Query: 'is:unread'

This fetches:
✅ Unread emails in INBOX
✅ New emails just arrived
✅ Old unread emails
❌ Already read emails (ignored)
❌ Emails in SPAM folder already (not checked again)

You can customize the query:
│
├─ 'is:unread' - Only unread
├─ 'is:unread is:inbox' - Unread in inbox only
├─ 'from:unknown@example.com' - From specific sender
└─ 'subject:urgent' - Specific subject keywords


MONITORING LOGS EXAMPLE
=======================

✅ Process started at 10:00:15

🔄 Check #1 at 10:00:15
──────────────────────
Checking top 10 emails...
✅ Moved to spam: RE: You won FREE MONEY
✅ Moved to spam: Verify your account NOW
Summary: 8 legit, 2 spam, 2 moved
⏳ Next check in 5 minutes...

🔄 Check #2 at 10:05:16
──────────────────────
Checking top 10 emails...
✅ Moved to spam: LIMITED TIME OFFER!!!
Summary: 9 legit, 1 spam, 1 moved
⏳ Next check in 5 minutes...

🔄 Check #3 at 10:10:17
──────────────────────
Checking top 10 emails...
Summary: 10 legit, 0 spam, 0 moved
⏳ Next check in 5 minutes...

[User presses Ctrl+C]
✅ Monitoring stopped


WHEN TO USE MONITOR
===================

✅ USE MONITOR IF:
  ├─ You want continuous spam filtering
  ├─ You get lots of spam regularly
  ├─ You want automated cleanup
  ├─ You want real-time spam detection
  └─ You'll leave computer running

❌ DON'T USE MONITOR IF:
  ├─ You only want one-time checking
  ├─ You can't keep computer running
  ├─ You want manual control (use check_and_move_spam instead)
  └─ You have limited API quota


API LIMITS TO KNOW
==================

Gmail API Rate Limits:
├─ Free tier: 1 million requests per day
├─ Each check = ~10-12 API calls (10 emails)
└─ 5-minute interval = 288 checks/day = 3,000-3,500 API calls/day

So you have plenty of room! Even with 1-minute intervals:
└─ 1,440 checks/day = 14,400-17,280 API calls/day
    (Still within the 1 million limit)


TROUBLESHOOTING MONITOR
=======================

Problem: Monitor keeps stopping
Solution: Check credentials.json exists
         └─ Delete token.pickle and re-authenticate

Problem: Spam not moving to folder
Solution: Check Gmail API has MODIFY scope
         └─ Delete token.pickle to re-authenticate with correct scope

Problem: Monitor uses too much data
Solution: Increase interval_minutes
         └─ monitor_continuous(interval_minutes=30)

Problem: Want to check only NEW emails
Solution: Modify query in gmail_integration.py
         └─ Change 'is:unread' to custom query


STOPPING THE MONITOR
====================

The monitor runs indefinitely until you stop it.

To stop:
  Press: Ctrl + C

Output when stopped:
  ^C
  ✅ Monitoring stopped

The script will then exit gracefully.
"""

# ============================================================================
# VISUAL COMPARISON
# ============================================================================

print("""
MONITOR VS ONE-TIME CHECK
==========================

ONE-TIME CHECK:
───────────────
python auto_move_spam.py --gmail
    ↓
Checks inbox once
    ↓
Moves spam
    ↓
Done - Program exits
    ↓
(Must run again manually later)


CONTINUOUS MONITOR:
───────────────────
python auto_move_spam.py --monitor 5
    ↓
Check #1: Checks inbox
    ↓
Waits 5 minutes
    ↓
Check #2: Checks inbox (NEW emails included)
    ↓
Waits 5 minutes
    ↓
Check #3: Checks inbox (NEW emails included)
    ↓
[Continues indefinitely...]
    ↓
User presses Ctrl+C to stop
    ↓
Done - Program exits


WHICH ONE TO USE?

✅ One-Time Check: python auto_move_spam.py --gmail
   └─ Run manually whenever you want
   └─ Good for quick cleanup
   └─ Good if you can't keep process running

✅ Continuous Monitor: python auto_move_spam.py --monitor 5
   └─ Runs automatically
   └─ Catches new spam as it arrives
   └─ Good if you leave computer running
   └─ Good for always-on servers
""")
