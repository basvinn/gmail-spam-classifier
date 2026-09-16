"""
Complete example demonstrating how to use the spam classifier
Shows both standalone and Gmail-integrated usage
"""

from spam_classifier import SpamClassifier, EmailProcessor, demo_classification
from gmail_integration import GmailSpamFilter
import json


def example_1_basic_classification():
    """Example 1: Basic spam classification without Gmail"""
    print("\n" + "="*70)
    print("EXAMPLE 1: BASIC SPAM CLASSIFICATION")
    print("="*70)
    
    classifier = SpamClassifier()
    
    # Test emails
    test_emails = [
        {
            'subject': 'Meeting rescheduled to 3 PM',
            'body': 'Hi, the meeting has been moved to 3 PM. See you then!',
            'sender': 'john@company.com'
        },
        {
            'subject': '🎉 YOU WON $50,000!!! 🎉',
            'body': 'CONGRATULATIONS!!! Click here immediately: http://bit.ly/claim-prize NOW!!!',
            'sender': 'noreply@suspicious.ru'
        },
        {
            'subject': 'Verify your PayPal account',
            'body': 'Your account needs verification. Click to update payment information immediately.',
            'sender': 'verify@paypa1.tk'
        }
    ]
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n📨 Email {i}")
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        
        # Combine text for analysis
        email_text = EmailProcessor.combine_email_text(email)
        
        # Classify
        results = classifier.classify_email(email_text)
        
        # Display results
        final = results.get('final_prediction', {})
        classification = "🚨 SPAM" if final.get('is_spam') else "✅ LEGITIMATE"
        confidence = final.get('confidence', 0)
        
        print(f"Result: {classification}")
        print(f"Confidence: {confidence:.2%}")
        
        # Show which methods detected it
        print("Detection Methods:")
        for method in ['rule_based', 'keyword_based', 'ml_based']:
            if method in results:
                is_spam = results[method].get('is_spam')
                score = results[method].get('score', 0)
                method_name = method.replace('_', ' ').title()
                print(f"  - {method_name}: {'SPAM' if is_spam else 'LEGIT'} ({score:.2f})")


def example_2_model_training():
    """Example 2: Train the ML model with sample data"""
    print("\n" + "="*70)
    print("EXAMPLE 2: TRAINING THE ML MODEL")
    print("="*70)
    
    classifier = SpamClassifier()
    
    # Sample training data
    training_emails = [
        "Join our newsletter for daily updates",
        "Your order has been shipped",
        "CLICK HERE TO WIN FREE MONEY!!!",
        "Meeting scheduled for tomorrow",
        "Verify your account immediately",
        "Project proposal attached",
        "Limited time offer - ACT NOW!",
        "Thank you for your purchase",
    ]
    
    # Labels: 0 = legitimate, 1 = spam
    labels = [0, 0, 1, 0, 1, 0, 1, 0]
    
    print(f"\nTraining on {len(training_emails)} emails...")
    classifier.train_model(training_emails, labels)
    print("✅ Model trained successfully!")
    
    # Save model
    classifier.save_model('spam_model.pkl')
    print("✅ Model saved to spam_model.pkl")
    
    # Test on new email
    test_email = "EXCLUSIVE OFFER - Get rich quick! Buy now!!!"
    results = classifier.classify_email(test_email)
    final = results.get('final_prediction', {})
    
    print(f"\nTesting trained model on: '{test_email}'")
    print(f"Result: {'SPAM' if final.get('is_spam') else 'LEGITIMATE'}")
    print(f"Confidence: {final.get('confidence', 0):.2%}")


def example_3_gmail_integration():
    """Example 3: Check actual Gmail inbox (requires credentials)"""
    print("\n" + "="*70)
    print("EXAMPLE 3: GMAIL INTEGRATION")
    print("="*70)
    
    print("\nTo use this feature:")
    print("1. Download credentials from Google Cloud Console")
    print("2. Save as 'credentials.json' in this directory")
    print("3. The app will open a browser for authentication")
    print("\nNote: This requires Gmail API credentials setup")
    
    try:
        # Initialize filter
        spam_filter = GmailSpamFilter('credentials.json')
        
        # Check unread emails
        print("\nChecking unread emails...")
        results = spam_filter.check_inbox_for_spam(
            query='is:unread',
            max_results=10
        )
        
        # Display results
        spam_filter.print_results(results)
        
    except FileNotFoundError:
        print("❌ credentials.json not found")
        print("   Please set up Gmail API credentials first (see README.md)")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_batch_processing():
    """Example 4: Process multiple emails and save results"""
    print("\n" + "="*70)
    print("EXAMPLE 4: BATCH PROCESSING")
    print("="*70)
    
    classifier = SpamClassifier()
    
    emails = [
        {'subject': 'Daily standup', 'body': 'Let\'s sync up', 'sender': 'team@company.com'},
        {'subject': 'Prize winner!', 'body': 'YOU WON!!!', 'sender': 'spam@fake.ru'},
    ]
    
    results_list = []
    
    for email in emails:
        email_text = EmailProcessor.combine_email_text(email)
        classification = classifier.classify_email(email_text)
        
        results_list.append({
            'email': email,
            'classification': classification
        })
    
    # Save results to JSON
    with open('classification_results.json', 'w') as f:
        # Convert for JSON serialization
        json_results = []
        for r in results_list:
            json_results.append({
                'email': r['email'],
                'is_spam': r['classification'].get('final_prediction', {}).get('is_spam'),
                'confidence': r['classification'].get('final_prediction', {}).get('confidence')
            })
        json.dump(json_results, f, indent=2)
    
    print("✅ Results saved to classification_results.json")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("GMAIL SPAM CLASSIFIER - COMPLETE EXAMPLES")
    print("="*70)
    
    # Run examples
    example_1_basic_classification()
    example_2_model_training()
    example_4_batch_processing()
    
    print("\n" + "="*70)
    print("For Gmail integration example, run:")
    print("  python examples.py --gmail")
    print("="*70)


if __name__ == "__main__":
    import sys
    
    if '--gmail' in sys.argv:
        example_3_gmail_integration()
    else:
        main()
        example_3_gmail_integration()
