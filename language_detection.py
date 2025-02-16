import argostranslate.package, argostranslate.translate

def detect_and_translate(text, target_language="en"):
    translated_text = argostranslate.translate.translate(text, target_language)
    return translated_text, target_language
