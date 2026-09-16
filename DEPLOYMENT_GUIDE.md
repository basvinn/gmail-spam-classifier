"""
HOW TO DEPLOY AND RUN THE SPAM CLASSIFIER
==========================================

3 WAYS TO RUN THIS APPLICATION:

1. DEVELOPMENT MODE (Run in VS Code) - Testing/Development
2. STANDALONE EXE (Windows) - Easy for non-developers
3. DEPLOYED SERVER (AWS/Heroku/etc) - Production 24/7

Choose based on your needs!
"""

print("""
================================================================================
OPTION 1: DEVELOPMENT MODE (Run in VS Code/Terminal)
================================================================================

WHEN TO USE:
├─ You're testing the code
├─ You want quick development
├─ You don't need it running 24/7
├─ You're learning how it works
└─ You can keep your computer on

HOW TO RUN:
──────────

Step 1: Open VS Code Terminal
   ├─ View → Terminal (Ctrl + `)
   └─ Or use Windows Command Prompt

Step 2: Navigate to project directory
   $ cd gmail-spam-classifier

Step 3: Install dependencies
   $ pip install -r requirements.txt

Step 4: Run the monitor
   $ python auto_move_spam.py --monitor 5

OUTPUT:
────────
🔄 Check #1 at 10:00:15
Checking top 10 emails...
Summary: 8 legit, 2 spam, 2 moved
⏳ Next check in 5 minutes...

[Continues running...]

TO STOP:
────────
Press Ctrl + C in terminal

PROS:
✅ Easy to start
✅ See output in real-time
✅ Good for testing
✅ Good for development

CONS:
❌ Only runs while terminal is open
❌ Stops if you close VS Code
❌ Stops if your computer sleeps
❌ Not suitable for always-on


================================================================================
OPTION 2: CREATE A STANDALONE EXE (Windows)
================================================================================

WHEN TO USE:
├─ You want to send to non-technical users
├─ You want a clickable executable
├─ You don't want to show terminal
├─ You want professional distribution
└─ Users don't need Python installed

HOW TO CREATE EXE:
──────────────────

Step 1: Install PyInstaller
   $ pip install pyinstaller

Step 2: Create wrapper script (run_monitor.py)
   Create file: run_monitor.py
   
   Content:
   ────────
   import subprocess
   import sys
   
   if __name__ == "__main__":
       subprocess.run([sys.executable, 'auto_move_spam.py', '--monitor', '5'])

Step 3: Convert to EXE
   $ pyinstaller --onefile --icon=icon.ico run_monitor.py

   (--onefile = creates single .exe file)
   (--icon = optional icon for the exe)

Step 4: Find your EXE
   ├─ Location: dist/run_monitor.exe
   └─ This is your standalone executable!

Step 5: Share the EXE
   ├─ Users can double-click it
   ├─ Monitor starts automatically
   ├─ No Python installation needed
   └─ No terminal visible


HOW USERS RUN IT:
─────────────────

1. Double-click: run_monitor.exe
2. Command prompt appears (if you want visible output)
3. Monitor starts checking Gmail
4. Spam gets moved automatically

TO STOP:
────────
Close the command prompt window
OR press Ctrl + C


DEPLOYMENT STEPS:
─────────────────

1. Create folder: GmailSpamFilter/
2. Add files:
   ├─ run_monitor.exe (created from PyInstaller)
   ├─ credentials.json (user's own)
   ├─ spam_classifier.py
   ├─ gmail_integration.py
   └─ README.txt (instructions)

3. Send folder to users
4. Users run: double-click run_monitor.exe


PROS:
✅ Professional distribution
✅ No Python needed
✅ Single .exe file
✅ Easy for end-users
✅ Can share with team

CONS:
❌ Only runs while open
❌ Stops if computer sleeps
❌ Requires credentials.json
❌ Still needs maintenance


EXAMPLE ADVANCED EXE (with GUI):
────────────────────────────────

Create a GUI window instead of terminal:

from tkinter import Tk, Label, Button
from auto_move_spam import check_and_move_spam

root = Tk()
root.title("Gmail Spam Filter")

Label(root, text="Gmail Spam Filter Monitor").pack()

def start_monitor():
    Label(root, text="Monitor running...").pack()
    check_and_move_spam()

Button(root, text="Start Monitor", command=start_monitor).pack()
Button(root, text="Exit", command=root.quit).pack()

root.mainloop()

Then convert to EXE with PyInstaller ↑


================================================================================
OPTION 3: DEPLOY TO CLOUD SERVER (AWS/Heroku/Google Cloud)
================================================================================

WHEN TO USE:
├─ You want 24/7 automatic spam filtering
├─ You need it always running
├─ You don't want to keep computer on
├─ You want professional deployment
├─ You need monitoring and logs
└─ Multiple users can benefit


3 POPULAR DEPLOYMENT OPTIONS:

A) HEROKU (Easiest - Free tier available)
────────────────────────────────────────

Step 1: Create Heroku account at heroku.com

Step 2: Install Heroku CLI
   $ npm install -g heroku
   $ heroku login

Step 3: Create Procfile
   Create file: Procfile
   
   Content:
   ────────
   worker: python auto_move_spam.py --monitor 5

Step 4: Create runtime.txt
   Create file: runtime.txt
   
   Content:
   ────────
   python-3.9.18

Step 5: Deploy to Heroku
   $ heroku create your-app-name
   $ git push heroku main
   $ heroku ps:scale worker=1

Step 6: View logs
   $ heroku logs --tail

PROS:
✅ Free tier available
✅ Always running
✅ Easy deployment
✅ Built-in logging
✅ Can scale easily

CONS:
❌ Free tier has limits (550 hours/month)
❌ Paid tier costs money (~$7/month)
❌ Requires Git knowledge


B) AWS (Amazon Web Services)
────────────────────────────

Step 1: Create AWS account

Step 2: Launch EC2 instance (Ubuntu Linux)
   Instance type: t2.micro (free tier)

Step 3: SSH into server
   $ ssh -i your-key.pem ubuntu@your-server-ip

Step 4: Install Python and dependencies
   $ sudo apt update
   $ sudo apt install python3-pip
   $ pip3 install -r requirements.txt

Step 5: Run as background service
   $ nohup python3 auto_move_spam.py --monitor 5 &

Step 6: Keep running after disconnect
   Use screen or tmux:
   $ screen
   $ python3 auto_move_spam.py --monitor 5
   $ [Ctrl+A then D to detach]

PROS:
✅ More control
✅ Free tier available (1 year)
✅ Highly scalable
✅ Professional setup
✅ Can add monitoring

CONS:
❌ More complex
❌ Requires Linux knowledge
❌ Paid after free tier
❌ Steeper learning curve


C) GOOGLE CLOUD (Similar to AWS)
────────────────────────────────

Step 1: Create Google Cloud account

Step 2: Create Cloud Run job or VM instance

Step 3: Upload code and dependencies

Step 4: Deploy and schedule

PROS:
✅ Good free tier
✅ Integrates with Gmail API
✅ Can schedule jobs
✅ Professional

CONS:
❌ Complex setup
❌ Requires learning
❌ Can be expensive


================================================================================
WINDOWS TASK SCHEDULER (Alternative - Always Running)
================================================================================

WHEN TO USE:
├─ You want always-on without cloud
├─ You'll keep computer running 24/7
├─ You want automatic startup
├─ You want scheduling
└─ Simple setup, no coding


HOW TO SET UP:
──────────────

Step 1: Create batch file (run_monitor.bat)
   Create file: run_monitor.bat
   
   Content:
   ────────
   @echo off
   cd C:\\path\\to\\gmail-spam-classifier
   python auto_move_spam.py --monitor 5
   pause

Step 2: Open Task Scheduler
   $ taskschd.msc

Step 3: Create Basic Task
   ├─ Name: "Gmail Spam Monitor"
   ├─ Description: "Automatically move spam emails"
   └─ Click: Create Task

Step 4: General Tab
   ├─ Check: "Run whether user is logged in or not"
   ├─ Check: "Run with highest privileges"
   └─ Select: Windows 10 or higher

Step 5: Triggers Tab
   ├─ Click: New
   ├─ Select: "At startup"
   ├─ Click: OK

Step 6: Actions Tab
   ├─ Click: New
   ├─ Action: "Start a program"
   ├─ Program: C:\\path\\to\\run_monitor.bat
   ├─ Click: OK

Step 7: Settings Tab
   ├─ Check: "Run task as soon as possible after a scheduled start is missed"
   ├─ Check: "If the running task does not end when requested, force it to stop"
   └─ Click: OK

Step 8: Finish and test
   ├─ The monitor should start automatically
   ├─ Runs on every startup
   ├─ Runs continuously in background


TO VIEW RUNNING:
─────────────────
$ tasklist | find "python"

TO STOP:
─────────
$ taskkill /IM python.exe /F

PROS:
✅ Always running after startup
✅ No cloud costs
✅ Keep on your own computer
✅ Simple setup
✅ Automatic restart

CONS:
❌ Computer must stay on
❌ Your computer = electricity costs
❌ Not as professional as cloud
❌ Less monitoring/logging


================================================================================
COMPARISON TABLE
================================================================================

                    VS Code     EXE         Task Sched.  Cloud
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Setup Time          5 min       20 min      15 min       1 hour+
Difficulty         Easy        Medium      Medium       Hard
Always Running      No          No          Yes          Yes
Cost                Free        Free        Electricity  $5-50/mo
Professional        No          Yes         Medium       Yes
Requires Computer   Yes         Yes         Yes          No
24/7 Availability   No          No          Yes          Yes
Easy to Share       No          Yes         Medium       Yes
Monitoring/Logs     No          No          Medium       Yes
Scaling             No          No          Limited      Easy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


================================================================================
RECOMMENDATION BY USE CASE
================================================================================

USE CASE 1: "I want to test the code"
RECOMMENDATION: Option 1 (VS Code)
├─ Run in terminal
├─ Watch output
├─ Test and debug
└─ Perfect for development


USE CASE 2: "I want to send to my friend"
RECOMMENDATION: Option 2 (EXE)
├─ Create .exe file
├─ Friend double-clicks it
├─ No Python needed
└─ Professional looking


USE CASE 3: "I want it running 24/7 on my PC"
RECOMMENDATION: Option 3B (Task Scheduler)
├─ Set up Task Scheduler
├─ Auto-runs on startup
├─ Always monitoring
└─ Simple and free


USE CASE 4: "I want professional always-on solution"
RECOMMENDATION: Option 3A (Heroku)
├─ Deploy to cloud
├─ Always running
├─ Professional logs
├─ Can share with team


USE CASE 5: "I want enterprise solution"
RECOMMENDATION: Option 3B/3C (AWS/Google Cloud)
├─ Full control
├─ Scalable
├─ Professional monitoring
└─ Enterprise support


================================================================================
STEP-BY-STEP GUIDE - QUICK START OPTIONS
================================================================================

QUICK START #1: Run in VS Code (Development)
──────────────────────────────────────────

$ cd gmail-spam-classifier
$ pip install -r requirements.txt
$ python auto_move_spam.py --monitor 5

✅ Done! Monitor is running.
Press Ctrl+C to stop.


QUICK START #2: Create Windows EXE
────────────────────────────────

$ pip install pyinstaller
$ pyinstaller --onefile auto_move_spam.py
$ dist\\auto_move_spam.exe

✅ EXE created! Share the .exe file.


QUICK START #3: Setup Task Scheduler
─────────────────────────────────

1. Create run_monitor.bat (see above)
2. Open Task Scheduler (taskschd.msc)
3. Create Basic Task → At Startup
4. Program: run_monitor.bat
5. Apply

✅ Done! Runs automatically on startup.


QUICK START #4: Deploy to Heroku
────────────────────────────────

$ heroku create your-app
$ git push heroku main
$ heroku ps:scale worker=1

✅ Done! Running 24/7 on cloud.


================================================================================
FINAL DECISION GUIDE
================================================================================

Choose based on your answer:

Q1: Do you need 24/7 operation?
├─ NO  → Use Option 1 or 2
└─ YES → Use Option 3

Q2: How much money to spend?
├─ $0   → Use Option 1, 2, or 3B (Task Scheduler)
├─ $5-10/month → Use Option 3A (Heroku)
└─ $10+/month  → Use Option 3C (AWS/Google Cloud)

Q3: Do you know Linux/Cloud?
├─ NO  → Use Option 1, 2, or 3B (Task Scheduler)
├─ SOME → Use Option 3A (Heroku)
└─ YES → Use Option 3B or 3C (AWS/Google Cloud)

Q4: Who will use it?
├─ Just me → Option 1 or 3B
├─ Friends → Option 2 (EXE)
└─ Company → Option 3A or 3C (Cloud)
""")

print("""
================================================================================
MY RECOMMENDATION FOR YOU
================================================================================

Since you're using VS Code and want to deploy:

STAGE 1: TESTING (Right Now)
────────────────────────────
Run in VS Code terminal:
$ python auto_move_spam.py --monitor 5

This lets you test everything works.


STAGE 2: PERSONAL USE (If for yourself)
─────────────────────────────────────────
Setup Windows Task Scheduler:
├─ Runs automatically on startup
├─ Runs 24/7 (as long as computer is on)
├─ No terminal window visible
├─ Free, simple, professional
└─ See instructions above for setup


STAGE 3: SHARE WITH OTHERS (If for team)
──────────────────────────────────────────
Create .EXE file:
├─ $ pip install pyinstaller
├─ $ pyinstaller --onefile auto_move_spam.py
├─ Share dist\\auto_move_spam.exe
├─ Others can run it without Python
└─ Professional and easy


STAGE 4: ENTERPRISE (If for business 24/7)
──────────────────────────────────────────
Deploy to Heroku:
├─ $ heroku create your-app
├─ $ git push heroku main
├─ Always running in cloud
├─ Professional monitoring
├─ Low cost ($5-7/month)
└─ Can share with team easily
""")
