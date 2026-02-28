"""
Core NLP logic for analyzing writing quality.
Detects clichés, weak claims, and measures originality.
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
import textstat

@dataclass
class AnalysisResult:
    overall_score: float
    originality_score: float
    evidence_score: float
    clarity_score: float
    voice_score: float
    clichés: List[Dict]
    weak_claims: List[Dict]
    suggestions: List[str]
    highlighted_text: str

class TextAnalyzer:
    # Common clichés in business/creative writing
    CLICHÉS = [
        r"\b(thinking outside the box|push the envelope|low hanging fruit|synergy|leverage)\b",
        r"\b(at the end of the day|moving forward|going forward|circle back|touch base)\b",
        r"\b(game changer|paradigm shift|best practice|thought leadership|deep dive)\b",
        r"\b(impactful|scalable|disruptive|innovative|agile|streamline)\b",
        r"\b(world class|cutting edge|state of the art|next generation|future ready)\b",
        r"\b(unlock.*potential|drive.*value|deliver.*results|maximize.*roi)\b",
        r"\b(it is what it is|think outside the box|hit the ground running)\b",
        r"\b(apples to apples|win-win|ballpark|elephant in the room|perfect storm)\b"
    ]

    # Weak claim indicators
    WEAK_PATTERNS = [
        r"\b(maybe|perhaps|might|could|possibly|potentially)\b",
        r"\b(some people say|it is said that|many believe|experts claim)\b",
        r"\b(obviously|clearly|undoubtedly|certainly|definitely)\b",
        r"\b(just|simply|only|merely|basically)\b",
        r"\b(very|really|quite|rather|pretty|fairly)\b\s+\w+",
        r"\b(i feel like|i think that|in my opinion|i believe)\b",
        r"\b(etc|and so on|and so forth|you know what i mean)\b"
    ]

    # Evidence indicators
    EVIDENCE_PATTERNS = [
        r"\b(data shows|research indicates|study found|according to)\b",
        r"\b(for example|for instance|specifically|namely|such as)\b",
        r"\b(digital|percent|\d+\s*(%|percent|million|billion))\b",
        r"\b(since|because|therefore|thus|consequently|as a result)\b",
        r"\b(in 20\d{2}|last year|over the past|recently published)\b"
    ]

    def __init__(self):
        self.cliché_patterns = [re.compile(p, re.IGNORECASE) for p in self.CLICHÉS]
        self.weak_patterns = [re.compile(p, re.IGNORECASE) for p in self.WEAK_PATTERNS]
        self.evidence_patterns = [re.compile(p, re.IGNORECASE) for p in self.EVIDENCE_PATTERNS]

    def analyze(self, text: str) -> AnalysisResult:
        if not text or len(text.strip()) < 20:
            return AnalysisResult(0, 0, 0, 0, 0, [], [], [], text)

        # Find issues
        clichés = self._find_clichés(text)
        weak_claims = self._find_weak_claims(text)

        # Calculate scores
        originality = self._calc_originality(text, clichés, weak_claims)
        evidence = self._calc_evidence(text)
        clarity = self._calc_clarity(text)
        voice = self._calc_voice(text, weak_claims)

        # Weighted overall score
        overall = (originality * 0.3 + evidence * 0.25 + clarity * 0.25 + voice * 0.2)

        # Generate suggestions
        suggestions = self._generate_suggestions(
            text, clichés, weak_claims, originality, evidence, clarity, voice
        )

        # Create highlighted version
        highlighted = self._highlight_text(text, clichés, weak_claims)

        return AnalysisResult(
            overall_score=round(overall, 1),
            originality_score=round(originality, 1),
            evidence_score=round(evidence, 1),
            clarity_score=round(clarity, 1),
            voice_score=round(voice, 1),
            clichés=clichés,
            weak_claims=weak_claims,
            suggestions=suggestions,
            highlighted_text=highlighted
        )

    def _find_clichés(self, text: str) -> List[Dict]:
        found = []
        for i, pattern in enumerate(self.cliché_patterns):
            for match in pattern.finditer(text):
                found.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'cliché',
                    'severity': 'high'
                })
        return found

    def _find_weak_claims(self, text: str) -> List[Dict]:
        found = []
        for pattern in self.weak_patterns:
            for match in pattern.finditer(text):
                found.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'weak_claim',
                    'severity': 'medium'
                })
        return found

    def _calc_originality(self, text: str, clichés: List, weak_claims: List) -> float:
        base_score = 100.0
        # Deduct for clichés
        base_score -= len(clichés) * 8
        # Deduct for weak/modifiers
        base_score -= len(weak_claims) * 3
        # Bonus for unique word ratio
        words = text.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        base_score += unique_ratio * 10
        # Length factor (very short = less original)
        if len(text) < 100:
            base_score *= 0.8
        return max(0, min(100, base_score))

    def _calc_evidence(self, text: str) -> float:
        score = 40.0  # Base
        for pattern in self.evidence_patterns:
            matches = len(pattern.findall(text))
            score += matches * 8
        # Check for statistics
        if re.search(r'\d+\s*(%|percent|million|billion|thousand)', text, re.IGNORECASE):
            score += 15
        # Check for citations/references
        if re.search(r'\[.*?\]|\(.*?\)|et al\.|\.pdf|http', text):
            score += 10
        return min(100, score)

    def _calc_clarity(self, text: str) -> float:
        try:
            # Readability scores (lower is easier)
            flesch = textstat.flesch_reading_ease(text)
            # Normalize to 0-100 (higher is better)
            normalized = max(0, min(100, flesch))
            # Penalty for very long sentences
            sentences = textstat.sentence_count(text)
            words = textstat.lexicon_count(text)
            avg_words_per_sentence = words / sentences if sentences > 0 else 0
            if avg_words_per_sentence > 25:
                normalized -= (avg_words_per_sentence - 25) * 2
            return max(0, min(100, normalized))
        except:
            return 70.0

    def _calc_voice(self, text: str, weak_claims: List) -> float:
        score = 80.0
        # Deduct for hedging language
        score -= len([w for w in weak_claims if w['type'] == 'weak_claim']) * 5
        # Bonus for active voice indicators
        if re.search(r'\b(we|i|our|my)\s+\w+ed\b', text, re.IGNORECASE):
            score += 10
        # Bonus for strong verbs
        strong_verbs = ['transform', 'disrupt', 'create', 'build', 'design', 'engineer', 'architect']
        for verb in strong_verbs:
            if re.search(rf'\b{verb}', text, re.IGNORECASE):
                score += 3
        return min(100, score)

    def _generate_suggestions(self, text: str, clichés: List, weak_claims: List, 
                             orig: float, evid: float, clar: float, voice: float) -> List[str]:
        suggestions = []

        if clichés:
            unique_clichés = list(set([c['text'] for c in clichés]))[:3]
            suggestions.append(f"Replace clichés like '{unique_clichés[0]}' with specific details")

        if evid < 60:
            suggestions.append("Add specific data, examples, or citations to strengthen claims")

        if clar < 60:
            suggestions.append("Break long sentences into shorter, punchier statements")

        if voice < 60:
            suggestions.append("Remove hedging words ('maybe', 'perhaps') to sound more confident")

        if orig < 50:
            suggestions.append("Add unexpected metaphors or personal anecdotes to stand out")

        if len(text.split()) < 50:
            suggestions.append("Expand with more specific details—shallow content averages out")

        return suggestions if suggestions else ["Great work! Your writing shows distinctive voice and depth."]

    def _highlight_text(self, text: str, clichés: List, weak_claims: List) -> str:
        """Create HTML highlighted version of text"""
        # Sort by position in reverse to avoid offset issues
        all_issues = sorted(clichés + weak_claims, key=lambda x: x['start'], reverse=True)

        result = text
        for issue in all_issues:
            start, end = issue['start'], issue['end']
            snippet = text[start:end]
            css_class = 'cliche-highlight' if issue['type'] == 'cliché' else 'weak-highlight'
            color = '#f43f5e' if issue['type'] == 'cliché' else '#f59e0b'
            replacement = f'<mark style="background: {color}40; color: {color}; padding: 2px 4px; border-radius: 4px; font-weight: 600;">{snippet}</mark>'
            result = result[:start] + replacement + result[end:]

        return result
