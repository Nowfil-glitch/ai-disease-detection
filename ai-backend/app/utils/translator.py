from deep_translator import GoogleTranslator
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class TranslationService:
    """Multi-language translation service"""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'english',
            'hi': 'hindi',
            'es': 'spanish',
            'fr': 'french',
            'de': 'german',
            'zh-CN': 'chinese (simplified)',
            'ar': 'arabic',
            'pt': 'portuguese',
            'te': 'telugu'
        }
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'hi', 'es')
            
        Returns:
            Translated text
        """
        try:
            if target_lang == 'en':
                return text
            
            translator = GoogleTranslator(source='en', target=target_lang)
            translated = translator.translate(text)
            return translated
            
        except Exception as e:
            logger.error(f"Translation error for {target_lang}: {str(e)}")
            return text  # Fallback to original text
    
    def translate_multiple(self, text: str, languages: list = None) -> Dict[str, str]:
        """
        Translate text to multiple languages
        
        Args:
            text: Text to translate
            languages: List of language codes (default: ['en', 'hi', 'es', 'fr'])
            
        Returns:
            Dictionary of language code to translated text
        """
        if languages is None:
            languages = ['en', 'hi', 'es', 'fr', 'te']
        
        translations = {}
        
        for lang in languages:
            translations[lang] = self.translate_text(text, lang)
        
        return translations
    
    def translate_diagnosis(self, diagnosis: str, description: str, recommendation: str) -> Dict[str, str]:
        """
        Translate full diagnosis message to multiple languages
        
        Args:
            diagnosis: Disease name
            description: Disease description
            recommendation: Recommended action
            
        Returns:
            Dictionary of translated full messages
        """
        # Construct full message
        full_message = f"{diagnosis} detected. {description} {recommendation}"
        
        # Translate to multiple languages
        translations = self.translate_multiple(
            full_message,
            languages=['en', 'hi', 'es', 'fr', 'te']
        )
        
        return translations


translator_service = TranslationService()
