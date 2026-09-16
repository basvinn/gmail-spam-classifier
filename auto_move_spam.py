"""
Auto Gmail Spam Filter Script
Monitors inbox and automatically moves spam emails to spam folder
Handles both existing and new emails
"""

from gmail_integration import GmailSpamFilter
import time
from datetime import datetime


def check_and_move_spam():
    """
    Check inbox for spam and automatically move to spam folder
    Works with both unread and new emails
    """
    print("="*70)
    print("GMAIL SPAM FILTER - AUTO MOVE TO SPAM")
    print("="*70)
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("This will:")
    print("  1. Read top 10 unread emails from your inbox")
    print("  2. Classify each email as SPAM or LEGITIMATE")
    print("  3. Automatically move SPAM emails to spam folder")
    print("  4. Show detailed results\n")
    
    try:
        # Initialize spam filter
        spam_filter = GmailSpamFilter('credentials.json')
        
        # Check inbox and automatically move spam
        # Parameters:
        # - max_results: Number of emails to check (top 10)
        # - auto_move: Enable automatic movement to spam
        # - confidence_threshold: Only move emails with >70% spam confidence
        results = spam_filter.batch_check_and_move(
            max_results=10,           # Check top 10 emails
            auto_move=True,           # Enable auto-move
            confidence_threshold=0.7  # 70% confidence threshold
        )
        
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"✅ Legitimate emails: {len(results['legitimate'])}")
        print(f"⚠️  Suspicious emails: {len(results['suspicious'])}")
        print(f"🚨 Spam emails: {len(results['spam'])}")
        print(f"📤 Moved to spam: {results.get('moved_to_spam', 0)}")
        if results.get('errors', 0) > 0:
            print(f"❌ Errors: {results['errors']}")
        print(f"\n✅ Process completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except FileNotFoundError:
        print("\n❌ ERROR: credentials.json not found!")
        print("\nTo use Gmail integration:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("2. Create a new project")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials (Desktop application)")
        print("5. Download the JSON file")
        print("6. Save it as 'credentials.json' in this directory")
        print("\nSee README.md for detailed instructions")
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Please check your credentials or Gmail API setup")


def monitor_continuous(interval_minutes=5):
    """
    Monitor inbox continuously and move spam
    
    Args:
        interval_minutes: Check inbox every N minutes
    """
    print("="*70)
    print("CONTINUOUS MONITORING MODE")
    print("="*70)
    print(f"Will check inbox every {interval_minutes} minutes")
    print("Press Ctrl+C to stop\n")
    
    try:
        spam_filter = GmailSpamFilter('credentials.json')
        check_count = 0
        
        while True:
            check_count += 1
            print(f"\n🔄 Check #{check_count} at {datetime.now().strftime('%H:%M:%S')}")
            print("-"*70)
            
            results = spam_filter.batch_check_and_move(
                max_results=10,
                auto_move=True,
                confidence_threshold=0.7
            )
            
            print(f"Summary: {len(results['legitimate'])} legit, " \
                  f"{len(results['spam'])} spam, " \
                  f"{results.get('moved_to_spam', 0)} moved")
            
            print(f"\n⏳ Next check in {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)
    
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped")
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_with_sample_emails():
    """Demo without Gmail - shows how classification works"""
    from spam_classifier import SpamClassifier, EmailProcessor
    
    print("="*70)
    print("DEMO - LOCAL CLASSIFICATION (No Gmail Required)")
    print("="*70)
    
    classifier = SpamClassifier()
    
    sample_emails = [
        {
            'subject': 'Meeting Tomorrow at 2 PM',
            'body': 'Hi John, let\'s meet tomorrow to discuss the project. Best regards, Sarah',
            'sender': 'sarah@company.com'
        },
        {
            'subject': '🎉 YOU WON $50,000!!! 🎉',
            'body': 'CONGRATULATIONS!!! You have been selected! Click here immediately to claim: http://bit.ly/prize NOW!!!',
            'sender': 'noreply@suspicious.ru'
        },
        {
            'subject': 'Verify Your PayPal Account',
            'body': 'Your account needs verification. Click to update payment information immediately or your account will be suspended.',
            'sender': 'verify@paypa1.tk'
        },
        {
            'subject': 'Project Update',
            'body': 'Here\'s the update on the Q4 project. Please review and provide feedback.',
            'sender': 'boss@company.com'
        },
    ]
    
    print("\nClassifying sample emails:\n")
    
    spam_count = 0
    legit_count = 0
    
    for i, email in enumerate(sample_emails, 1):
        print(f"Email #{i}")
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        
        email_text = EmailProcessor.combine_email_text(email)
        results = classifier.classify_email(email_text)
        final = results.get('final_prediction', {})
        
        is_spam = final.get('is_spam')
        confidence = final.get('confidence', 0)
        
        if is_spam:
            print(f"Result: 🚨 SPAM (Confidence: {confidence:.0%})")
            spam_count += 1
        else:
            print(f"Result: ✅ LEGITIMATE (Confidence: {(1-confidence):.0%})")
            legit_count += 1
        
        print("-"*70)
    
    print(f"\n📊 Summary: {legit_count} legitimate, {spam_count} spam")
    print("\nTo use with real Gmail emails:")
    print("  1. Set up credentials.json (see README.md)")
    print("  2. Run: python auto_move_spam.py --gmail")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--gmail':
            # Run with real Gmail
            check_and_move_spam()
        elif sys.argv[1] == '--monitor':
            # Continuous monitoring
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            monitor_continuous(interval)
        else:
            print("Usage:")
            print("  python auto_move_spam.py              # Demo with sample emails")
            print("  python auto_move_spam.py --gmail      # Check real Gmail inbox")
            print("  python auto_move_spam.py --monitor N  # Monitor every N minutes")
    else:
        # Demo mode (no Gmail required)
        demo_with_sample_emails()
