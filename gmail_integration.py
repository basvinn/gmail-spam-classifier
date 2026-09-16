"""
Gmail Integration Module - Connect to Gmail API and classify emails
Enhanced version with automatic spam movement
"""

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_python_client import discovery
from email.mime.text import MIMEText
import base64
import os
from spam_classifier import SpamClassifier, EmailProcessor


class GmailConnector:
    """Connect to Gmail API and fetch emails"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']  # Modified for write access
    
    def __init__(self, credentials_file='credentials.json'):
        """
        Initialize Gmail connector
        
        Args:
            credentials_file: Path to OAuth2 credentials JSON file
        """
        self.credentials_file = credentials_file
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load token if it exists
        if os.path.exists('token.pickle'):
            import pickle
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            import pickle
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = discovery.build('gmail', 'v1', credentials=creds)
    
    def get_emails(self, query='is:unread', max_results=10):
        """
        Fetch emails from Gmail
        
        Args:
            query: Gmail search query (default: unread emails)
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email data
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self.get_email_details(message['id'])
                emails.append(email_data)
            
            return emails
        
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
    
    def get_email_details(self, message_id):
        """
        Get detailed information about an email
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dictionary with email details
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            
            # Extract body
            body = self._get_message_body(message['payload'])
            
            return {
                'message_id': message_id,
                'subject': subject,
                'sender': sender,
                'body': body,
                'has_attachments': 'parts' in message['payload'],
                'raw_message': message
            }
        
        except Exception as e:
            print(f"Error getting email details: {e}")
            return {}
    
    def _get_message_body(self, payload):
        """Extract email body from payload"""
        try:
            if 'parts' in payload:
                parts = payload['parts']
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            return base64.urlsafe_b64decode(
                                part['body']['data']).decode('utf-8')
            elif 'body' in payload and 'data' in payload['body']:
                return base64.urlsafe_b64decode(
                    payload['body']['data']).decode('utf-8')
            return ''
        except Exception as e:
            print(f"Error extracting body: {e}")
            return ''
    
    def move_email_to_spam(self, message_id):
        """
        Move email to spam folder
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Boolean - True if successful
        """
        try:
            # Add SPAM label and remove INBOX label
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={
                    'addLabelIds': ['SPAM'],
                    'removeLabelIds': ['INBOX']
                }
            ).execute()
            return True
        except Exception as e:
            print(f"Error moving email to spam: {e}")
            return False
    
    def move_email_to_inbox(self, message_id):
        """
        Move email back to inbox from spam
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Boolean - True if successful
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={
                    'addLabelIds': ['INBOX'],
                    'removeLabelIds': ['SPAM']
                }
            ).execute()
            return True
        except Exception as e:
            print(f"Error moving email to inbox: {e}")
            return False
    
    def delete_email(self, message_id):
        """
        Permanently delete email
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Boolean - True if successful
        """
        try:
            self.service.users().messages().delete(
                userId='me',
                id=message_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting email: {e}")
            return False


class GmailSpamFilter:
    """Main class to filter Gmail emails for spam and move them"""
    
    def __init__(self, credentials_file='credentials.json'):
        """Initialize spam filter with Gmail connector"""
        self.gmail = GmailConnector(credentials_file)
        self.classifier = SpamClassifier()
    
    def check_inbox_for_spam(self, query='is:unread', max_results=10, auto_move=False, confidence_threshold=0.7):
        """
        Check inbox emails and classify them
        
        Args:
            query: Gmail search query
            max_results: Maximum emails to check
            auto_move: Automatically move spam to spam folder
            confidence_threshold: Confidence level to mark as spam (0-1)
            
        Returns:
            Dictionary with spam and legitimate emails
        """
        emails = self.gmail.get_emails(query, max_results)
        
        results = {
            'spam': [],
            'legitimate': [],
            'suspicious': [],
            'moved_to_spam': 0,
            'errors': 0
        }
        
        for email in emails:
            email_text = EmailProcessor.combine_email_text(email)
            classification = classifier.classify_email(email_text)
            
            email['classification'] = classification
            
            final_pred = classification.get('final_prediction', {})
            confidence = final_pred.get('confidence', 0)
            
            if final_pred.get('is_spam'):
                if confidence > confidence_threshold:
                    results['spam'].append(email)
                    
                    # Auto-move to spam if enabled
                    if auto_move:
                        success = self.gmail.move_email_to_spam(email['message_id'])
                        if success:
                            results['moved_to_spam'] += 1
                            print(f"✅ Moved to spam: {email['subject'][:50]}")
                        else:
                            results['errors'] += 1
                            print(f"❌ Failed to move: {email['subject'][:50]}")
                else:
                    results['suspicious'].append(email)
            else:
                results['legitimate'].append(email)
        
        return results
    
    def print_results(self, results):
        """Pretty print classification results"""
        print("\n" + "="*70)
        print("GMAIL SPAM FILTER RESULTS")
        print("="*70)
        
        print(f"\n✅ LEGITIMATE EMAILS ({len(results['legitimate'])})")
        print("-"*70)
        for email in results['legitimate']:
            self._print_email(email, 'LEGITIMATE')
        
        print(f"\n⚠️  SUSPICIOUS EMAILS ({len(results['suspicious'])})")
        print("-"*70)
        for email in results['suspicious']:
            self._print_email(email, 'SUSPICIOUS')
        
        print(f"\n🚨 SPAM EMAILS ({len(results['spam'])})")
        print("-"*70)
        for email in results['spam']:
            self._print_email(email, 'SPAM')
        
        # Show movement stats
        if 'moved_to_spam' in results and results['moved_to_spam'] > 0:
            print(f"\n📊 AUTO-MOVE STATS")
            print("-"*70)
            print(f"  ✅ Moved to spam: {results['moved_to_spam']}")
            if results.get('errors', 0) > 0:
                print(f"  ❌ Errors: {results['errors']}")
    
    def _print_email(self, email, category):
        """Print individual email info"""
        print(f"\n{category}")
        print(f"  Subject: {email['subject'][:60]}...")
        print(f"  From: {email['sender'][:50]}...")
        
        if 'classification' in email:
            final = email['classification'].get('final_prediction', {})
            print(f"  Confidence: {final.get('confidence', 0):.2%}")
    
    def batch_check_and_move(self, max_results=10, auto_move=True, confidence_threshold=0.7):
        """
        Convenience method to check inbox and automatically move spam
        
        Args:
            max_results: Maximum emails to process
            auto_move: Whether to move spam automatically
            confidence_threshold: Confidence threshold for spam classification
        """
        print(f"🔍 Checking top {max_results} emails...")
        results = self.check_inbox_for_spam(
            query='is:unread',
            max_results=max_results,
            auto_move=auto_move,
            confidence_threshold=confidence_threshold
        )
        
        self.print_results(results)
        
        return results
