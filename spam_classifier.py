"""
Gmail Spam Classifier - Classifies emails as spam or legitimate
Uses multiple approaches: rule-based, Naive Bayes, and keyword analysis
"""

import re
import json
from typing import Dict, List, Tuple
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os


class SpamClassifier:
    """Multi-method spam classifier for Gmail emails"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.spam_keywords = self._load_spam_keywords()
        self.rule_engine = RuleBasedDetector()
        self.ml_model = None
        
    def _load_spam_keywords(self) -> Dict[str, List[str]]:
        """Load common spam keywords and phrases"""
        return {
            'urgent': ['urgent', 'act now', 'immediate action', 'limited time', 'expire'],
            'money': ['free money', 'prize', 'claim reward', 'bonus', 'cash', 'financial gain'],
            'phishing': ['verify account', 'confirm identity', 'update payment', 'click here', 'verify now'],
            'numbers': ['999', '888', '1234', '00000'],
            'cps': ['viagra', 'casino', 'lottery', 'click here', 'buy now'],
            'urgency': ['congratulations', 'you won', 'you are selected'],
            'suspicious_links': ['bit.ly', 'tinyurl', 'short.link'],
        }
    
    def train_model(self, emails: List[Dict], labels: List[int]):
        """
        Train the ML model on labeled emails
        
        Args:
            emails: List of email texts
            labels: List of binary labels (0=legitimate, 1=spam)
        """
        self.ml_model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        self.ml_model.fit(emails, labels)
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        if self.ml_model:
            with open(filepath, 'wb') as f:
                pickle.dump(self.ml_model, f)
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.ml_model = pickle.load(f)
    
    def classify_email(self, email_text: str, use_ensemble: bool = True) -> Dict:
        """
        Classify an email as spam or legitimate
        
        Args:
            email_text: The email body/subject text
            use_ensemble: Use multiple methods for robust classification
            
        Returns:
            Dictionary with classification result and confidence scores
        """
        results = {}
        
        # Rule-based detection
        rule_score, rule_confidence = self.rule_engine.detect_spam(email_text)
        results['rule_based'] = {
            'is_spam': rule_score > 0.5,
            'score': rule_score,
            'confidence': rule_confidence
        }
        
        # Keyword-based detection
        keyword_score = self._keyword_detection(email_text)
        results['keyword_based'] = {
            'is_spam': keyword_score > 0.5,
            'score': keyword_score,
        }
        
        # ML-based detection
        if self.ml_model:
            ml_score = self._ml_detection(email_text)
            results['ml_based'] = {
                'is_spam': ml_score > 0.5,
                'score': ml_score,
            }
        
        # Ensemble decision
        if use_ensemble:
            final_decision = self._ensemble_decision(results)
            results['final_prediction'] = final_decision
        
        return results
    
    def _keyword_detection(self, email_text: str) -> float:
        """
        Detect spam using keyword analysis
        Returns score between 0 and 1
        """
        text_lower = email_text.lower()
        spam_indicators = 0
        total_checks = 0
        
        for category, keywords in self.spam_keywords.items():
            for keyword in keywords:
                total_checks += 1
                if keyword in text_lower:
                    spam_indicators += 1
        
        return spam_indicators / max(total_checks, 1)
    
    def _ml_detection(self, email_text: str) -> float:
        """Detect spam using ML model"""
        if not self.ml_model:
            return 0.5
        
        probability = self.ml_model.predict_proba([email_text])[0]
        return probability[1]  # Probability of being spam
    
    def _ensemble_decision(self, results: Dict) -> Dict:
        """Combine multiple detection methods"""
        scores = []
        
        for method in ['rule_based', 'keyword_based', 'ml_based']:
            if method in results:
                scores.append(results[method]['score'])
        
        if not scores:
            return {'is_spam': False, 'confidence': 0.0}
        
        avg_score = sum(scores) / len(scores)
        
        return {
            'is_spam': avg_score > 0.5,
            'confidence': avg_score,
            'method_count': len(scores)
        }


class RuleBasedDetector:
    """Rule-based spam detection using common patterns"""
    
    def __init__(self):
        self.spam_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for spam detection"""
        return {
            'multiple_exclamation': re.compile(r'!{3,}'),
            'suspicious_url': re.compile(r'(https?://[^\s]+[.](ru|tk|ml|ga|cf))'),
            'email_harvesting': re.compile(r'(verify|confirm|update).*?(account|payment|information)', re.IGNORECASE),
            'all_caps': re.compile(r'^[A-Z\s!]{10,}$'),
            'too_many_links': re.compile(r'https?://'),
            'excessive_spacing': re.compile(r'\s{10,}'),
            'suspicious_sender': re.compile(r'(noreply|no-reply|donotreply)', re.IGNORECASE),
        }
    
    def detect_spam(self, email_text: str) -> Tuple[float, Dict]:
        """
        Detect spam using rule-based patterns
        
        Returns:
            Tuple of (spam_score, confidence_breakdown)
        """
        score = 0
        total_rules = len(self.spam_patterns)
        triggered_rules = []
        
        # Check each pattern
        if self.spam_patterns['multiple_exclamation'].search(email_text):
            score += 0.2
            triggered_rules.append('multiple_exclamation')
        
        if self.spam_patterns['suspicious_url'].search(email_text):
            score += 0.3
            triggered_rules.append('suspicious_url')
        
        if self.spam_patterns['email_harvesting'].search(email_text):
            score += 0.3
            triggered_rules.append('email_harvesting')
        
        all_caps_blocks = self.spam_patterns['all_caps'].findall(email_text)
        if all_caps_blocks and len(all_caps_blocks) > 2:
            score += 0.2
            triggered_rules.append('all_caps')
        
        links = self.spam_patterns['too_many_links'].findall(email_text)
        if len(links) > 5:
            score += 0.2
            triggered_rules.append('too_many_links')
        
        if self.spam_patterns['excessive_spacing'].search(email_text):
            score += 0.1
            triggered_rules.append('excessive_spacing')
        
        # Normalize score
        normalized_score = min(score, 1.0)
        
        return normalized_score, {
            'triggered_rules': triggered_rules,
            'rule_count': len(triggered_rules),
            'total_rules': total_rules
        }


class EmailProcessor:
    """Process and extract features from Gmail emails"""
    
    @staticmethod
    def extract_email_features(email_data: Dict) -> Dict:
        """Extract relevant features from email"""
        return {
            'subject': email_data.get('subject', ''),
            'body': email_data.get('body', ''),
            'sender': email_data.get('sender', ''),
            'recipient': email_data.get('recipient', ''),
            'has_links': len(re.findall(r'https?://', email_data.get('body', ''))) > 0,
            'link_count': len(re.findall(r'https?://', email_data.get('body', ''))),
            'has_attachments': email_data.get('has_attachments', False),
        }
    
    @staticmethod
    def combine_email_text(email_data: Dict) -> str:
        """Combine email subject and body for analysis"""
        subject = email_data.get('subject', '')
        body = email_data.get('body', '')
        sender = email_data.get('sender', '')
        return f"{subject} {body} {sender}"


def demo_classification():
    """Demonstrate spam classification"""
    
    classifier = SpamClassifier()
    
    # Sample emails
    sample_emails = [
        {
            'subject': 'URGENT!!! Claim your FREE prize NOW!!!',
            'body': 'Congratulations! You won $1,000,000. Click here: bit.ly/fakeprice',
            'sender': 'noreply@suspicious.ru'
        },
        {
            'subject': 'Meeting Tomorrow at 2 PM',
            'body': 'Hi John, let\'s meet tomorrow to discuss the project. Best regards, Sarah',
            'sender': 'sarah@company.com'
        },
        {
            'subject': 'Verify Your Account',
            'body': 'Please verify your account information immediately: click here to update payment',
            'sender': 'support@fake-amazon.tk'
        },
    ]
    
    print("=" * 60)
    print("GMAIL SPAM CLASSIFIER DEMO")
    print("=" * 60)
    
    for i, email in enumerate(sample_emails, 1):
        email_text = EmailProcessor.combine_email_text(email)
        print(f"\nEmail #{i}")
        print(f"Subject: {email['subject']}")
        print(f"Sender: {email['sender']}")
        print("-" * 40)
        
        results = classifier.classify_email(email_text)
        
        print("Classification Results:")
        for method, result in results.items():
            if method != 'final_prediction':
                print(f"  {method}:")
                print(f"    - Is Spam: {result['is_spam']}")
                print(f"    - Score: {result['score']:.2f}")
        
        if 'final_prediction' in results:
            final = results['final_prediction']
            print(f"\n  FINAL PREDICTION: {'SPAM' if final['is_spam'] else 'LEGITIMATE'}")
            print(f"  Confidence: {final['confidence']:.2f}")


if __name__ == "__main__":
    demo_classification()
