"""Offline Argos translation adapter; model installation is an explicit separate step."""
def translate(text):
    try: import argostranslate.translate
    except ImportError as e: raise RuntimeError('install requirements-translation.txt and an offline English-to-Spanish Argos model, or supply a non-English excerpt') from e
    available=argostranslate.translate.get_installed_languages()
    src=next((x for x in available if x.code=='en'),None);dst=next((x for x in available if x.code=='es'),None)
    if not src or not dst: raise RuntimeError('install an offline English-to-Spanish Argos model, or supply a non-English excerpt')
    try: return src.get_translation(dst).translate(text)
    except Exception as e: raise RuntimeError('offline English-to-Spanish translation unavailable') from e
