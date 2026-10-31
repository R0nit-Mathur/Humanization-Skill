#!/usr/bin/env python3
"""
quick_audit.py — Fast CLI audit tool for AI markers and plagiarism risks.
Part of the ai-content-fixer skill.

Usage:
    python3 quick_audit.py file.txt
    python3 quick_audit.py file.txt --json
    cat draft.txt | python3 quick_audit.py -
"""

import sys
import os
import re
import json

# Top high-signal AI markers
AI_WORDS = [
    "delve", "delves", "delving", "leverage", "leveraging", "robust",
    "nuanced", "nuances", "tapestry", "landscape", "crucial", "pivotal",
    "underscore", "underscores", "underscoring", "testament", "navigate",
    "foster", "fosters", "fostering", "enhance", "enhances", "enhancing",
    "comprehensive", "multifaceted", "intricacies", "interplay", "garner",
    "showcase", "showcases", "showcasing", "enduring", "vibrant", "embark",
    "embarks", "embarking", "harness", "spearhead", "bolster", "synergy",
    "holistic", "paradigm", "seamless", "seamlessly", "innovative",
    "groundbreaking", "transformative", "game-changing", "unlock", "empower",
    "streamline", "elevate", "realm", "essentially", "certainly", "utilize",
    "facilitate", "cultivate", "encompass", "paramount", "indispensable",
    "profound", "meticulous", "resonate"
]

AI_PHRASES = [
    "in today's fast-paced world",
    "in the ever-evolving landscape",
    "it is important to note",
    "it is worth noting",
    "plays a crucial role",
    "plays a pivotal role",
    "a testament to",
    "delve into",
    "navigate the complexities",
    "the realm of",
    "the tapestry of",
    "foster a sense of",
    "underscore the importance",
    "not only",
    "but also",
    "at the end of the day",
    "when it comes to",
    "a wide range of",
    "a myriad of",
    "a plethora of",
    "shed light on",
    "pave the way",
    "bridge the gap",
    "push the boundaries",
    "unlock the potential",
    "harness the power",
    "seamlessly integrate",
    "robust framework",
    "holistic approach",
    "paradigm shift",
    "in an era of",
    "as we move forward",
    "the key takeaway",
    "here's a breakdown",
    "below is",
    "stands as a",
    "serves as a",
    "in order to",
    "due to the fact that",
    "at this point in time",
    "i hope this email finds you well",
    "please do not hesitate to reach out",
    "let that sink in",
    "read that again"
]

TRANSITIONS = [
    "furthermore", "moreover", "additionally", "consequently",
    "in conclusion", "in summary"
]

def analyze_text(text: str) -> dict:
    lower_text = text.lower()
    words = re.findall(r"[A-Za-z0-9]+(?:['\u2019-][A-Za-z0-9]+)*", text)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    word_count = len(words)
    sentence_count = len(sentences)

    sent_lengths = [len(re.findall(r"[A-Za-z0-9]+", s)) for s in sentences]
    avg_sent_len = sum(sent_lengths) / len(sent_lengths) if sent_lengths else 0
    variance = sum((x - avg_sent_len) ** 2 for x in sent_lengths) / len(sent_lengths) if sent_lengths else 0
    std_dev = variance ** 0.5
    cv = (std_dev / avg_sent_len) if avg_sent_len else 0

    # Counts
    found_words = {}
    for w in AI_WORDS:
        pattern = r"\b" + re.escape(w) + r"\b"
        matches = len(re.findall(pattern, lower_text))
        if matches > 0:
            found_words[w] = matches

    found_phrases = {}
    for p in AI_PHRASES:
        pattern = r"(?<!\w)" + re.escape(p) + r"(?!\w)"
        matches = len(re.findall(pattern, lower_text))
        if matches > 0:
            found_phrases[p] = matches

    found_transitions = {}
    for t in TRANSITIONS:
        pattern = r"\b" + re.escape(t) + r"\b"
        matches = len(re.findall(pattern, lower_text))
        if matches > 0:
            found_transitions[t] = matches

    em_dashes = text.count("—") + text.count("--")
    em_dash_rate = (em_dashes / word_count * 1000) if word_count else 0

    # Risk score calculation (0 - 100)
    risk_score = 0
    reasons = []

    if cv < 0.35 and sentence_count >= 5:
        risk_score += 30
        reasons.append(f"Uniform sentence rhythm (CV = {cv:.2f}, target is > 0.45)")
    elif cv < 0.45 and sentence_count >= 5:
        risk_score += 15
        reasons.append(f"Moderate rhythm uniformity (CV = {cv:.2f})")

    word_hits_total = sum(found_words.values())
    if word_hits_total > 5:
        risk_score += 30
        reasons.append(f"High concentration of AI vocabulary ({word_hits_total} hits)")
    elif word_hits_total > 0:
        risk_score += min(word_hits_total * 5, 20)
        reasons.append(f"AI vocabulary detected ({word_hits_total} hits)")

    phrase_hits_total = sum(found_phrases.values())
    if phrase_hits_total > 0:
        risk_score += min(phrase_hits_total * 10, 30)
        reasons.append(f"AI stock phrases detected ({phrase_hits_total} hits)")

    trans_hits_total = sum(found_transitions.values())
    if trans_hits_total > 2:
        risk_score += 15
        reasons.append(f"Excessive formal AI transitions ({trans_hits_total} hits)")

    if em_dash_rate > 6:
        risk_score += 15
        reasons.append(f"Excessive em dashes ({em_dash_rate:.1f} per 1k words, target is < 3)")

    risk_score = min(risk_score, 100)

    return {
        "stats": {
            "words": word_count,
            "sentences": sentence_count,
            "paragraphs": len(paragraphs),
            "avg_sentence_length": round(avg_sent_len, 1),
            "sentence_length_cv": round(cv, 2),
            "em_dash_count": em_dashes,
            "em_dash_rate_per_1k": round(em_dash_rate, 1)
        },
        "ai_risk_score": risk_score,
        "risk_level": "HIGH" if risk_score >= 60 else "MODERATE" if risk_score >= 30 else "LOW",
        "flags": {
            "ai_vocabulary": found_words,
            "ai_phrases": found_phrases,
            "transitions": found_transitions,
            "risk_reasons": reasons
        }
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 quick_audit.py <file.txt> [--json]")
        sys.exit(1)

    target = sys.argv[1]
    is_json = "--json" in sys.argv

    if target == "-":
        content = sys.stdin.read()
    else:
        if not os.path.exists(target):
            print(f"Error: File {target} not found.")
            sys.exit(1)
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()

    result = analyze_text(content)

    if is_json:
        print(json.dumps(result, indent=2))
        return

    stats = result["stats"]
    flags = result["flags"]

    print("\n" + "="*50)
    print(f" AI CONTENT AUDIT REPORT: {target}")
    print("="*50)
    print(f" Words: {stats['words']} | Sentences: {stats['sentences']} | Paragraphs: {stats['paragraphs']}")
    print(f" Avg Sentence Length: {stats['avg_sentence_length']} words | Rhythm CV: {stats['sentence_length_cv']} (Target: >0.45)")
    print(f" Em Dashes: {stats['em_dash_count']} ({stats['em_dash_rate_per_1k']}/1k words)")
    print("-"*50)
    print(f" AI DETECTION RISK: {result['risk_level']} ({result['ai_risk_score']}/100)")
    print("-"*50)

    if flags["risk_reasons"]:
        print(" Key Findings:")
        for r in flags["risk_reasons"]:
            print(f"  • {r}")

    if flags["ai_vocabulary"]:
        print("\n Flagged Vocabulary:")
        for w, c in flags["ai_vocabulary"].items():
            print(f"  - '{w}': {c} occurrence(s)")

    if flags["ai_phrases"]:
        print("\n Flagged Stock Phrases:")
        for p, c in flags["ai_phrases"].items():
            print(f"  - \"{p}\": {c} occurrence(s)")

    if flags["transitions"]:
        print("\n Flagged Transitions:")
        for t, c in flags["transitions"].items():
            print(f"  - \"{t}\": {c} occurrence(s)")

    print("="*50)
    if result["ai_risk_score"] > 25:
        print(" ACTION REQUIRED: Run ai-content-fixer pipeline to eliminate flags.")
    else:
        print(" CLEAN: Text shows natural human variation and low AI signature.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()

