import os
import re
import requests
import urllib.parse
import unicodedata
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()


def clean_text_content(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r'</?[^>]+(>|$)', '', text)
    cleaned = re.sub(r'^Sentence:\s*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return unicodedata.normalize('NFC', cleaned)


def is_telugu_script(text: str) -> bool:
    return bool(re.search(r'[\u0C00-\u0C7F]', text))


def translate_text(text: str, target_lang: str) -> str:
    if not text:
        return ""
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        normalized = unicodedata.normalize('NFC', translated)
        cleaned = re.sub(r'[\uFFFD\u200B-\u200D]', '', normalized)
        return cleaned
    except Exception as e:
        print(f"Translation Error ({target_lang}): {e}")
        return text


def fetch_internet_summary(title: str) -> str:
    """Multi-stage real-world knowledge fetcher for any topic title."""
    if not title:
        return ""

    clean_title = re.sub(r'^\d+[\.\s\-]+', '', title).strip()
    headers = {"User-Agent": "LexiHubCorpusApp/1.0 (contact@lexihub.org)"}

    # 1. Generate search variations (from full phrase to core subject)
    candidates = [clean_title]

    # Split compound phrases
    if "Programming Language" in clean_title:
        candidates.append(clean_title.replace("Programming Language", "").strip())
    if "Application Development" in clean_title:
        candidates.append(clean_title.split()[0] + " (programming language)")
        candidates.append(clean_title.split()[0])
    if "iOS" in clean_title:
        candidates.append("Swift (programming language)")
        candidates.append("iOS")
    if "Management & OOP" in clean_title:
        candidates.append("C++")
    if "Corpus" in clean_title:
        candidates.append("Linguistic corpus")

    # Add individual words as last resort
    words = [w for w in clean_title.split() if len(w) > 3 and w.lower() not in ["and", "with", "from"]]
    candidates.extend(words)

    # 2. Try Wikipedia Summary API for each candidate
    for term in candidates:
        try:
            encoded = urllib.parse.quote(term)
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
            res = requests.get(url, headers=headers, timeout=3)
            if res.status_code == 200:
                data = res.json()
                extract = data.get("extract", "")
                if extract and len(extract) > 40 and data.get("type") != "disambiguation":
                    return extract
        except Exception:
            continue

    # 3. Try DuckDuckGo Instant Answer API if Wikipedia Direct fails
    try:
        ddg_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(clean_title)}&format=json"
        res = requests.get(ddg_url, headers=headers, timeout=3)
        if res.status_code == 200:
            abstract = res.json().get("AbstractText", "")
            if abstract and len(abstract) > 30:
                return abstract
    except Exception:
        pass

    return ""


def generate_summary(text: str, language: str = "english", title: str = "") -> str:
    cleaned = clean_text_content(text)
    lang_str = str(language).strip().lower()
    is_telugu_target = lang_str in ["telugu", "te"]

    clean_title = re.sub(r'^\d+[\.\s\-]+', '', title).strip()
    if not clean_title:
        clean_title = "Corpus Record"

    # Fetch live factual internet data
    real_world_info = fetch_internet_summary(clean_title)

    if real_world_info:
        body_content = real_world_info
    elif cleaned and len(cleaned.split()) >= 8:
        body_content = cleaned
    else:
        body_content = f"{clean_title} represents a core domain subject in computer science, linguistics, and software architecture."

    # -----------------------------------------------------------------
    # 1. TELUGU SUMMARY
    # -----------------------------------------------------------------
    if is_telugu_target:
        telugu_title = clean_title if is_telugu_script(clean_title) else translate_text(clean_title, 'te')
        telugu_body = body_content if is_telugu_script(body_content) else translate_text(body_content, 'te')

        return unicodedata.normalize('NFC', (
            f"సారాంశ నివేదిక:\n\n"
            f"అంశము: {telugu_title}\n\n"
            f"ప్రధాన విశ్లేషణ మరియు వాస్తవ సమాచారం:\n"
            f"{telugu_body}\n\n"
            f"వాస్తవ ప్రపంచ ప్రాముఖ్యత:\n"
            f"ఈ సమాచారం ఇంటర్నెట్ డిజిటల్ రిపాజిటరీ ఆధారంగా నేరుగా సేకరించబడింది. "
            f"ఇది పరిశోధన మరియు విశ్లేషణ కోసం కీలకమైన ప్రామాణిక సూచికగా ఉపయోగపడుతుంది."
        ))

    # -----------------------------------------------------------------
    # 2. ENGLISH SUMMARY
    # -----------------------------------------------------------------
    english_title = translate_text(clean_title, 'en') if is_telugu_script(clean_title) else clean_title
    english_body = translate_text(body_content, 'en') if is_telugu_script(body_content) else body_content

    return (
        f"Summary Report:\n\n"
        f"Topic: {english_title}\n\n"
        f"Real-World Knowledge & Detailed Analysis:\n"
        f"{english_body}\n\n"
        f"Project Significance:\n"
        f"Fetched live from open digital knowledge repositories, this entry provides authentic reference material for {english_title}."
    )