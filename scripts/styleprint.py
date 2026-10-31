#!/usr/bin/env python3
"""
StylePrint — a dependency-free stylometric feature extractor.

This is the reference implementation for the measurement layer of PALIMPSEST.
It is deliberately small and auditable: no spaCy, no transformers, no network.
Production should add POS tagging, NER, dependency parsing, and a proper
word-frequency table; this module gives you the shape of the feature vector
and a reproducible baseline.

Usage:
    python styleprint.py draft.txt
    python styleprint.py draft.txt --json
    python styleprint.py a.txt b.txt --compare
    cat draft.txt | python styleprint.py -

The output is a JSON object:
    {
      "text": {"chars": ..., "words": ..., "sentences": ..., "paragraphs": ...},
      "features": {...},
      "diagnostics": {...}
    }

All rates are per 1,000 tokens unless stated otherwise.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from dataclasses import dataclass, field
from typing import Sequence

# ---------------------------------------------------------------------------
# Tokenization
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['\u2019-][A-Za-z0-9]+)*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])[\"'\u201d\u2019)]*\s+|\n{2,}")
ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "vs", "etc", "e.g",
    "i.e", "fig", "al", "inc", "ltd", "co", "corp", "dept", "univ", "approx",
    "a.m", "p.m", "u.s", "u.k", "ph.d", "b.c", "a.d",
}

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "than", "so", "because",
    "as", "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to",
    "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
    "further", "once", "here", "there", "when", "where", "why", "how", "all",
    "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "too", "very", "can", "will",
    "just", "should", "now", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "would",
    "could", "ought", "i", "you", "he", "she", "it", "we", "they", "me", "him",
    "her", "us", "them", "my", "your", "his", "its", "our", "their", "this",
    "that", "these", "those", "am", "were", "may", "might", "must", "shall",
}

HEDGES = {
    "might", "may", "could", "perhaps", "possibly", "probably", "seems",
    "seem", "appears", "appear", "suggest", "suggests", "suggested", "arguably",
    "somewhat", "rather", "fairly", "relatively", "tend", "tends", "tended",
    "often", "sometimes", "generally", "typically", "likely", "unlikely",
    "approximately", "roughly", "about", "around", "in principle", "in theory",
    "to some extent", "more or less", "presumably", "apparently",
}

BOOSTERS = {
    "clearly", "obviously", "undoubtedly", "certainly", "definitely",
    "absolutely", "strongly", "significantly", "substantially", "crucially",
    "essentially", "fundamentally", "indeed", "of course", "without doubt",
    "must", "always", "never", "proves", "prove", "demonstrates", "confirms",
}

DISCOURSE_MARKERS = {
    "however", "moreover", "furthermore", "additionally", "consequently",
    "therefore", "thus", "hence", "nevertheless", "nonetheless", "meanwhile",
    "similarly", "likewise", "conversely", "overall", "in conclusion",
    "in summary", "to sum up", "firstly", "secondly", "finally", "in addition",
    "on the other hand", "as a result", "for example", "for instance",
    "in other words", "that is", "in fact", "of course", "after all",
}

TEMPLATE_PHRASES = (
    "in today's fast-paced world",
    "in the ever-evolving landscape",
    "it is important to note",
    "it is worth noting",
    "it is crucial to",
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
    "on one hand",
    "on the other hand",
    "in an era of",
    "as we move forward",
    "the key takeaway",
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
    "game changer",
    "cutting-edge",
    "state-of-the-art",
    "leveraging",
)

FIRST_PERSON = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves"}
SECOND_PERSON = {"you", "your", "yours", "yourself", "yourselves"}

CONTRACTION_RE = re.compile(r"\b\w+(?:n't|'re|'ve|'ll|'d|'m|'s)\b", re.IGNORECASE)

PUNCTUATION = {
    "comma": ",",
    "semicolon": ";",
    "colon": ":",
    "dash": "\u2014",  # em dash
    "en_dash": "\u2013",
    "paren_open": "(",
    "question": "?",
    "exclamation": "!",
}

VOWEL_GROUP_RE = re.compile(r"[aeiouy]+", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def sentences(text: str) -> list[str]:
    raw = SENTENCE_SPLIT_RE.split(text.strip())
    out: list[str] = []
    for part in raw:
        part = part.strip()
        if not part:
            continue
        # Re-join sentences that were split after a known abbreviation.
        joined = False
        if out:
            last_words = out[-1].split()
            if last_words:
                tail = last_words[-1].rstrip(".").lower()
                if tail in ABBREVIATIONS:
                    out[-1] = out[-1] + " " + part
                    joined = True
        if not joined:
            out.append(part)
    return [s for s in out if words(s)]


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def syllables(word: str) -> int:
    word = word.lower()
    groups = VOWEL_GROUP_RE.findall(word)
    n = len(groups)
    if word.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stdev(values: Sequence[float]) -> float:
    return statistics.stdev(values) if len(values) > 1 else 0.0


def skewness(values: Sequence[float]) -> float:
    n = len(values)
    if n < 3:
        return 0.0
    m = mean(values)
    s = stdev(values)
    if s == 0:
        return 0.0
    return sum(((v - m) / s) ** 3 for v in values) * n / ((n - 1) * (n - 2))


def kurtosis(values: Sequence[float]) -> float:
    n = len(values)
    if n < 4:
        return 0.0
    m = mean(values)
    s = stdev(values)
    if s == 0:
        return 0.0
    return sum(((v - m) / s) ** 4 for v in values) / n - 3.0


def percentile(values: Sequence[float], q: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - pos) + xs[hi] * (pos - lo)


def count_phrase(text_lower: str, phrase: str) -> int:
    # Word-boundary-ish matching that works for multi-word phrases.
    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    return len(re.findall(pattern, text_lower))


def rate(count: int, n_words: int) -> float:
    return (count / n_words * 1000.0) if n_words else 0.0


def mattr(tokens: Sequence[str], window: int = 50) -> float:
    n = len(tokens)
    if n == 0:
        return 0.0
    if n <= window:
        return len(set(tokens)) / n
    total = 0.0
    for i in range(n - window + 1):
        total += len(set(tokens[i:i + window])) / window
    return total / (n - window + 1)


def flesch(text: str) -> float:
    ws = words(text)
    ss = sentences(text)
    if not ws or not ss:
        return 0.0
    syl = sum(syllables(w) for w in ws)
    return 206.835 - 1.015 * (len(ws) / len(ss)) - 84.6 * (syl / len(ws))


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------


@dataclass
class TextStats:
    chars: int
    words: int
    sentences: int
    paragraphs: int
    syllables: int


@dataclass
class Features:
    # Rhythm
    mean_sentence_length: float = 0.0
    sd_sentence_length: float = 0.0
    cv_sentence_length: float = 0.0
    skew_sentence_length: float = 0.0
    kurtosis_sentence_length: float = 0.0
    p10_sentence_length: float = 0.0
    p90_sentence_length: float = 0.0
    short_sentence_pct: float = 0.0
    long_sentence_pct: float = 0.0
    # Lexical
    ttr: float = 0.0
    mattr_50: float = 0.0
    content_word_ratio: float = 0.0
    rare_word_rate: float = 0.0
    # Punctuation (per 1k words)
    comma_rate: float = 0.0
    semicolon_rate: float = 0.0
    colon_rate: float = 0.0
    em_dash_rate: float = 0.0
    en_dash_rate: float = 0.0
    paren_rate: float = 0.0
    question_rate: float = 0.0
    exclamation_rate: float = 0.0
    contraction_rate: float = 0.0
    # Stance
    first_person_rate: float = 0.0
    second_person_rate: float = 0.0
    hedge_rate: float = 0.0
    booster_rate: float = 0.0
    hedge_booster_ratio: float = 0.0
    # Discourse
    discourse_marker_rate: float = 0.0
    template_rate: float = 0.0
    paragraph_length_cv: float = 0.0
    repeated_opener_rate: float = 0.0
    # Specificity proxies
    entity_proxy_rate: float = 0.0
    number_rate: float = 0.0
    # Readability
    flesch_reading_ease: float = 0.0
    # Diagnostics
    template_hits: dict[str, int] = field(default_factory=dict)


def extract(text: str) -> dict:
    toks = words(text)
    sents = sentences(text)
    paras = paragraphs(text)
    n = len(toks)
    lower = text.lower()

    sent_lengths = [len(words(s)) for s in sents]
    para_lengths = [len(words(p)) for p in paras]

    content = [t for t in toks if t.lower() not in STOPWORDS]
    content_ratio = len(content) / n if n else 0.0

    # A crude rarity proxy: words longer than 8 chars and not in stopwords.
    # Production should use a real frequency table (wordfreq / SUBTLEX).
    rare = [t for t in content if len(t) > 8]
    rare_rate = len(rare) / n * 1000.0 if n else 0.0

    uniq = len(set(t.lower() for t in toks))
    ttr = uniq / n if n else 0.0

    hedge_count = sum(1 for t in toks if t.lower() in HEDGES)
    # Multi-word hedges
    for phrase in ("in principle", "in theory", "to some extent", "more or less"):
        hedge_count += count_phrase(lower, phrase)
    booster_count = sum(1 for t in toks if t.lower() in BOOSTERS)
    for phrase in ("of course", "without doubt"):
        booster_count += count_phrase(lower, phrase)

    discourse_count = sum(1 for t in toks if t.lower() in DISCOURSE_MARKERS)
    for phrase in DISCOURSE_MARKERS:
        if " " in phrase:
            discourse_count += count_phrase(lower, phrase)

    template_hits: dict[str, int] = {}
    for phrase in TEMPLATE_PHRASES:
        c = count_phrase(lower, phrase)
        if c:
            template_hits[phrase] = c
    template_count = sum(template_hits.values())

    # Repeated sentence openers (first two words), a cheap templating signal.
    openers = [" ".join(words(s)[:2]).lower() for s in sents if len(words(s)) >= 2]
    repeated_openers = len(openers) - len(set(openers))
    repeated_opener_rate = repeated_openers / len(openers) * 1000.0 if openers else 0.0

    # Entity proxy: capitalized tokens not at sentence start, not all-caps stopwords.
    entity_proxy = 0
    for s in sents:
        ws = s.split()
        for w in ws[1:]:
            clean = w.strip("\"'(),.;:!?")
            if clean and clean[0].isupper() and clean.lower() not in STOPWORDS:
                entity_proxy += 1
    number_count = len(re.findall(r"\b\d[\d,./%-]*\b", text))

    p_counts = {k: text.count(v) for k, v in PUNCTUATION.items()}
    contraction_count = len(CONTRACTION_RE.findall(text))

    f = Features(
        mean_sentence_length=mean(sent_lengths),
        sd_sentence_length=stdev(sent_lengths),
        cv_sentence_length=(stdev(sent_lengths) / mean(sent_lengths)) if mean(sent_lengths) else 0.0,
        skew_sentence_length=skewness(sent_lengths),
        kurtosis_sentence_length=kurtosis(sent_lengths),
        p10_sentence_length=percentile(sent_lengths, 0.10),
        p90_sentence_length=percentile(sent_lengths, 0.90),
        short_sentence_pct=(sum(1 for x in sent_lengths if x < 8) / len(sent_lengths) * 100.0) if sent_lengths else 0.0,
        long_sentence_pct=(sum(1 for x in sent_lengths if x > 30) / len(sent_lengths) * 100.0) if sent_lengths else 0.0,
        ttr=ttr,
        mattr_50=mattr([t.lower() for t in toks], 50),
        content_word_ratio=content_ratio,
        rare_word_rate=rare_rate,
        comma_rate=rate(p_counts["comma"], n),
        semicolon_rate=rate(p_counts["semicolon"], n),
        colon_rate=rate(p_counts["colon"], n),
        em_dash_rate=rate(p_counts["dash"], n),
        en_dash_rate=rate(p_counts["en_dash"], n),
        paren_rate=rate(p_counts["paren_open"], n),
        question_rate=rate(p_counts["question"], n),
        exclamation_rate=rate(p_counts["exclamation"], n),
        contraction_rate=rate(contraction_count, n),
        first_person_rate=rate(sum(1 for t in toks if t.lower() in FIRST_PERSON), n),
        second_person_rate=rate(sum(1 for t in toks if t.lower() in SECOND_PERSON), n),
        hedge_rate=rate(hedge_count, n),
        booster_rate=rate(booster_count, n),
        hedge_booster_ratio=(hedge_count / booster_count) if booster_count else float(hedge_count),
        discourse_marker_rate=rate(discourse_count, n),
        template_rate=rate(template_count, n),
        paragraph_length_cv=(stdev(para_lengths) / mean(para_lengths)) if mean(para_lengths) else 0.0,
        repeated_opener_rate=repeated_opener_rate,
        entity_proxy_rate=rate(entity_proxy, n),
        number_rate=rate(number_count, n),
        flesch_reading_ease=flesch(text),
        template_hits=template_hits,
    )

    stats = TextStats(
        chars=len(text),
        words=n,
        sentences=len(sents),
        paragraphs=len(paras),
        syllables=sum(syllables(w) for w in toks),
    )

    diagnostics = {
        "min_words_recommended": 150,
        "meets_min_words": n >= 150,
        "notes": [],
    }
    if n < 150:
        diagnostics["notes"].append("Short text: rates are noisy; treat as directional only.")
    if len(sents) < 20:
        diagnostics["notes"].append("Fewer than 20 sentences: sentence-rhythm metrics are unstable.")
    if len(paras) < 3:
        diagnostics["notes"].append("Fewer than 3 paragraphs: paragraph-variance metrics are unstable.")
    if not any(t in lower for t in (" the ", " and ", " of ")):
        diagnostics["notes"].append("Text may not be English; feature priors are English-specific.")

    return {
        "text": stats.__dict__,
        "features": f.__dict__,
        "diagnostics": diagnostics,
    }


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------


def compare(a: dict, b: dict, label_a: str = "A", label_b: str = "B") -> dict:
    fa, fb = a["features"], b["features"]
    keys = [k for k in fa if isinstance(fa[k], (int, float))]
    rows = []
    for k in keys:
        va, vb = float(fa[k]), float(fb[k])
        delta = vb - va
        pct = (delta / abs(va) * 100.0) if va else None
        rows.append({"feature": k, "a": va, "b": vb, "delta": delta, "pct_change": pct})
    return {"label_a": label_a, "label_b": label_b, "rows": rows}


def print_human(result: dict, name: str = "text") -> None:
    t, f, d = result["text"], result["features"], result["diagnostics"]
    print(f"\n== {name} ==")
    print(f"{t['words']} words · {t['sentences']} sentences · {t['paragraphs']} paragraphs")
    print(f"Sentence length: mean {f['mean_sentence_length']:.1f}, "
          f"CV {f['cv_sentence_length']:.2f}, "
          f"short {f['short_sentence_pct']:.1f}%, long {f['long_sentence_pct']:.1f}%")
    print(f"Lexical: MATTR-50 {f['mattr_50']:.3f}, TTR {f['ttr']:.3f}, "
          f"content ratio {f['content_word_ratio']:.3f}, rare-word rate {f['rare_word_rate']:.1f}/1k")
    print(f"Punctuation /1k: comma {f['comma_rate']:.1f}, semicolon {f['semicolon_rate']:.1f}, "
          f"colon {f['colon_rate']:.1f}, em-dash {f['em_dash_rate']:.1f}, paren {f['paren_rate']:.1f}")
    print(f"Stance /1k: first-person {f['first_person_rate']:.1f}, hedge {f['hedge_rate']:.1f}, "
          f"booster {f['booster_rate']:.1f}, discourse markers {f['discourse_marker_rate']:.1f}")
    print(f"Templates /1k: {f['template_rate']:.1f}  (hits: {f['template_hits'] or 'none'})")
    print(f"Readability (Flesch): {f['flesch_reading_ease']:.1f}")
    for note in d["notes"]:
        print(f"! {note}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="StylePrint stylometric feature extractor")
    parser.add_argument("paths", nargs="+", help="Text file(s), or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="Emit JSON (single file or compare)")
    parser.add_argument("--compare", action="store_true", help="Compare exactly two files")
    args = parser.parse_args(argv)

    if args.compare and len(args.paths) != 2:
        parser.error("--compare requires exactly two paths")

    texts = [read_text(p) for p in args.paths]
    results = [extract(t) for t in texts]

    if args.compare:
        out = compare(results[0], results[1], args.paths[0], args.paths[1])
        if args.json:
            print(json.dumps(out, indent=2, ensure_ascii=False))
        else:
            print(f"\n== Compare: {args.paths[0]} -> {args.paths[1]} ==")
            for row in out["rows"]:
                pct = f"{row['pct_change']:+.1f}%" if row["pct_change"] is not None else "n/a"
                print(f"{row['feature']:<28} {row['a']:>10.3f} -> {row['b']:>10.3f}  ({pct})")
        return 0

    if args.json:
        payload = results[0] if len(results) == 1 else {
            p: r for p, r in zip(args.paths, results)
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    for p, r in zip(args.paths, results):
        print_human(r, p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
