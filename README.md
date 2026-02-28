# ⚡ Dnt Be Average

**Break the content convergence. Score your writing against the average.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dnt-be-average.streamlit.app/)

## The Problem

Large Language Models predict the most probable next word. Mathematically, this creates a convergence toward the mean:

```
Average(Average(Average(...))) → Global Mean
```

The result? The internet is slowly collapsing into a single, lukewarm voice. Original thought is becoming statistically rare.

## The Solution

**Dnt Be Average** is a writing analyzer that scores your content on four dimensions that resist convergence:

- **🎨 Originality** - Avoidance of clichés and generic phrases
- **📊 Evidence** - Specific data, examples, and citations  
- **📖 Clarity** - Readable structure without unnecessary complexity
- **🎤 Voice** - Confidence and distinctive personality

## Features

- ⚡ **Instant Analysis** - Paste text and get scores in seconds
- 🎯 **Cliché Detection** - Identifies overused business/writing tropes
- 🔍 **Weak Claim Flagging** - Catches hedging and vague language
- 💡 **Actionable Suggestions** - Specific improvements, not just scores
- 🎨 **Beautiful UI** - Dark mode glassmorphism design
- 🔒 **Privacy First** - No text is stored or sent to external APIs

## Installation

```bash
git clone https://github.com/yourusername/dnt-be-average.git
cd dnt-be-average
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. **Paste your text** (LinkedIn post, email, essay, article)
2. **Click Analyze** to get your scores
3. **Review the highlighted text** to see clichés and weak claims
4. **Follow suggestions** to improve your writing

## Scoring Guide

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Exceptional - Truly distinctive writing |
| 80-89 | B | Strong - Above average with clear voice |
| 70-79 | C | Average - Converging toward the mean |
| 60-69 | D | Below Average - Heavy on clichés |
| <60 | F | Convergent - Generic AI-like content |

## Technology

- **Frontend**: Streamlit with custom CSS
- **Analysis**: Pattern matching + Readability metrics
- **Design**: Glassmorphism, dark mode, responsive layout
- **Deployment**: Streamlit Cloud / GitHub Pages

## Contributing

This is an open tool to help fight content homogenization. Contributions welcome:

- Add new cliché patterns
- Improve scoring algorithms
- Enhance UI/UX
- Add language support

## License

MIT License - Free to use, modify, and distribute.

---

**Remember**: The algorithms reward the average. Your audience deserves the deviation.
