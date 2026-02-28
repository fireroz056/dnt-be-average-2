"""
Dnt Be Average - Professional Writing Analyzer
A Streamlit app that scores writing quality and fights content convergence.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from utils.text_processor import TextAnalyzer
from components.metrics import score_gauge, score_breakdown, overall_grade

# Page configuration
st.set_page_config(
    page_title="Dnt Be Average | Writing Quality Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "custom.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = TextAnalyzer()
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
        <div style="padding: 1rem 0; border-bottom: 1px solid rgba(148, 163, 184, 0.2); margin-bottom: 1rem;">
            <h1 style="margin: 0; font-size: 1.5rem; background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">⚡ Dnt Be Average</h1>
            <p style="color: #64748b; font-size: 0.875rem; margin: 0.5rem 0 0 0;">Break the convergence</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")
    page = st.radio("", ["📝 Analyze", "📚 Examples", "ℹ️ About"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### Settings")

    analysis_mode = st.selectbox(
        "Analysis Mode",
        ["Standard", "Strict (Academic)", "Creative", "Business"],
        help="Adjusts sensitivity for different writing contexts"
    )

    show_highlighting = st.toggle("Highlight Issues", value=True, 
                                  help="Show problematic text in red/orange")

    auto_analyze = st.toggle("Auto-analyze", value=False,
                             help="Analyze as you type (may be slower)")

    st.markdown("---")
    st.markdown("<div style='color: #64748b; font-size: 0.75rem;'>v2.0 • Built with Streamlit</div>", unsafe_allow_html=True)

# Main Content Area
if page == "📝 Analyze":
    # Hero Section
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("""
            <h1 class="main-header" style="margin-bottom: 0.5rem;">
                Escape the<br>
                <span style="background: linear-gradient(135deg, #f43f5e 0%, #f59e0b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Average</span>
            </h1>
            <p class="sub-header">
                LLMs converge to the mean. Your writing shouldn't. 
                <br>Get scored on originality, evidence, clarity, and voice.
            </p>
        """, unsafe_allow_html=True)

    with col2:
        # Quick stats or quote
        st.markdown("""
            <div style="
                background: rgba(30, 41, 59, 0.6);
                border-radius: 12px;
                padding: 1rem;
                border: 1px solid rgba(99, 102, 241, 0.3);
            ">
                <p style="color: #94a3b8; font-size: 0.875rem; margin: 0 0 0.5rem 0; font-style: italic;">
                    "Mathematically, repeated averaging converges toward the mean. Original thought becomes statistically rare."
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Input Section
    input_col, results_col = st.columns([1, 1], gap="large")

    with input_col:
        st.markdown("### 📝 Your Text")

        # Toolbar
        toolbar_cols = st.columns([1, 1, 1, 2])
        with toolbar_cols[0]:
            if st.button("🎲 Load Example", use_container_width=True):
                examples = [
                    "We need to leverage our core competencies to create synergy and move the needle on this game-changing initiative.",
                    "The data shows that 73% of users abandoned the checkout process at the payment step, suggesting a friction point we need to address.",
                    "I think that maybe we should probably consider looking into possibly implementing some sort of solution at some point."
                ]
                import random
                st.session_state.text_input = random.choice(examples)
                st.rerun()

        with toolbar_cols[1]:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.text_input = ""
                st.session_state.analysis_result = None
                st.rerun()

        with toolbar_cols[2]:
            if st.button("📋 Paste", use_container_width=True):
                # In real app, this would use pyperclip
                pass

        # Text Area
        text_input = st.text_area(
            "Paste your writing here...",
            value=st.session_state.text_input,
            height=400,
            placeholder="Paste your LinkedIn post, email, essay, or article here. We'll detect clichés, weak claims, and give you an originality score...",
            label_visibility="collapsed"
        )

        st.session_state.text_input = text_input

        # Character count
        char_count = len(text_input)
        word_count = len(text_input.split()) if text_input else 0

        st.markdown(f"""
            <div style="display: flex; gap: 1rem; color: #64748b; font-size: 0.875rem; margin-top: 0.5rem;">
                <span>{word_count} words</span>
                <span>•</span>
                <span>{char_count} characters</span>
            </div>
        """, unsafe_allow_html=True)

        # Analyze Button
        analyze_disabled = len(text_input.strip()) < 20
        if analyze_disabled:
            st.warning("⚠️ Enter at least 20 characters to analyze")

        if st.button("⚡ Analyze Writing", type="primary", disabled=analyze_disabled, use_container_width=True):
            with st.spinner("🔍 Analyzing your text..."):
                st.session_state.analysis_result = st.session_state.analyzer.analyze(text_input)

    # Results Section
    with results_col:
        if st.session_state.analysis_result:
            result = st.session_state.analysis_result

            st.markdown("### 📊 Analysis Results")

            # Overall Grade Card
            st.markdown(overall_grade(result.overall_score), unsafe_allow_html=True)

            st.markdown("---")

            # Score Breakdown
            st.markdown("#### Score Breakdown")
            st.markdown(score_breakdown(
                result.originality_score,
                result.evidence_score,
                result.clarity_score,
                result.voice_score
            ), unsafe_allow_html=True)

        else:
            # Empty state
            st.markdown("""
                <div style="
                    background: rgba(30, 41, 59, 0.4);
                    border: 2px dashed rgba(148, 163, 184, 0.2);
                    border-radius: 16px;
                    padding: 3rem 2rem;
                    text-align: center;
                    color: #64748b;
                ">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">Results will appear here</p>
                    <p style="font-size: 0.875rem;">Enter your text and click Analyze to see your scores</p>
                </div>
            """, unsafe_allow_html=True)

    # Detailed Results (Full Width)
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result

        st.markdown("---")
        st.markdown("### 🔍 Detailed Analysis")

        tabs = st.tabs(["🚨 Issues Found", "💡 Suggestions", "📄 Highlighted Text"])

        with tabs[0]:
            issues_col1, issues_col2 = st.columns(2)

            with issues_col1:
                st.markdown("#### Clichés Detected")
                if result.clichés:
                    unique_clichés = list(set([c['text'] for c in result.clichés]))[:10]
                    for cliché in unique_clichés:
                        st.markdown(f"""
                            <span class="cliche-tag">{cliché}</span>
                        """, unsafe_allow_html=True)
                    if len(result.clichés) > 10:
                        st.caption(f"...and {len(result.clichés) - 10} more")
                else:
                    st.success("✅ No clichés detected! Great job.")

            with issues_col2:
                st.markdown("#### Weak Claims")
                if result.weak_claims:
                    unique_weak = list(set([w['text'] for w in result.weak_claims]))[:10]
                    for claim in unique_weak:
                        st.markdown(f"""
                            <div style="
                                background: rgba(245, 158, 11, 0.1);
                                border-left: 3px solid #f59e0b;
                                padding: 0.5rem 0.75rem;
                                margin: 0.25rem 0;
                                border-radius: 0 8px 8px 0;
                                color: #fbbf24;
                                font-size: 0.9rem;
                            ">{claim}</div>
                        """, unsafe_allow_html=True)
                    if len(result.weak_claims) > 10:
                        st.caption(f"...and {len(result.weak_claims) - 10} more")
                else:
                    st.success("✅ Strong confident language detected!")

        with tabs[1]:
            st.markdown("#### Improvement Suggestions")
            for i, suggestion in enumerate(result.suggestions, 1):
                st.markdown(f"""
                    <div class="suggestion-item" style="
                        background: rgba(6, 182, 212, 0.1);
                        border-left: 3px solid #06b6d4;
                        padding: 0.75rem 1rem;
                        margin: 0.5rem 0;
                        border-radius: 0 8px 8px 0;
                        color: #22d3ee;
                    ">
                        <strong>{i}.</strong> {suggestion}
                    </div>
                """, unsafe_allow_html=True)

        with tabs[2]:
            if show_highlighting and (result.clichés or result.weak_claims):
                st.markdown("#### Text with Highlights")
                st.markdown("<span style='color: #f43f5e;'>■</span> Clichés | <span style='color: #f59e0b;'>■</span> Weak Claims", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style="
                        background: #1e293b;
                        border-radius: 12px;
                        padding: 1.5rem;
                        line-height: 1.8;
                        font-size: 1rem;
                        color: #e2e8f0;
                    ">
                        {result.highlighted_text}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Enable 'Highlight Issues' in the sidebar to see problematic text highlighted.")

        # Export Options
        st.markdown("---")
        export_col1, export_col2, export_col3 = st.columns([1, 1, 2])

        with export_col1:
            report_data = f"""
DNT BE AVERAGE - ANALYSIS REPORT
================================
Overall Score: {result.overall_score}/100
Originality: {result.originality_score}/100
Evidence: {result.evidence_score}/100
Clarity: {result.clarity_score}/100
Voice: {result.voice_score}/100

Issues Found:
- Clichés: {len(result.clichés)}
- Weak Claims: {len(result.weak_claims)}

Suggestions:
{chr(10).join(['• ' + s for s in result.suggestions])}

Analyzed Text:
{text_input[:500]}...
            """
            st.download_button(
                label="📥 Download Report",
                data=report_data,
                file_name="writing_analysis.txt",
                mime="text/plain",
                use_container_width=True
            )

elif page == "📚 Examples":
    st.markdown("""
        <h1 class="main-header">Example Analyses</h1>
        <p class="sub-header">See how different writing styles score</p>
    """, unsafe_allow_html=True)

    examples = [
        {
            "title": "Corporate Jargon",
            "text": "We need to leverage our core competencies to create synergy and move the needle on this game-changing initiative that will disrupt the industry.",
            "expected": "Low Originality"
        },
        {
            "title": "Data-Driven",
            "text": "Our Q3 analysis reveals that 73% of users abandoned the checkout process at the payment step (n=1,240). This suggests a friction point costing approximately $2.4M in annual revenue.",
            "expected": "High Evidence"
        },
        {
            "title": "Hedging Language",
            "text": "I think that maybe we should probably consider looking into possibly implementing some sort of solution at some point in the future, if that's okay.",
            "expected": "Low Voice"
        }
    ]

    for ex in examples:
        with st.expander(f"{ex['title']} ({ex['expected']})"):
            st.markdown(f"**Text:** {ex['text']}")
            if st.button(f"Analyze this example", key=f"btn_{ex['title']}"):
                st.session_state.text_input = ex['text']
                st.session_state.analysis_result = st.session_state.analyzer.analyze(ex['text'])
                st.rerun()

elif page == "ℹ️ About":
    st.markdown("""
        <h1 class="main-header">About Dnt Be Average</h1>
        <div style="max-width: 800px;">
            <h3 style="color: #6366f1;">The Problem</h3>
            <p style="color: #cbd5e1; line-height: 1.7;">
                Large Language Models are trained on billions of texts and predict the most probable next word. 
                Mathematically, this creates a convergence toward the mean. When everyone uses AI-generated content, 
                the world drifts toward an "average of averages"—where original thought becomes statistically rare.
            </p>

            <h3 style="color: #6366f1; margin-top: 2rem;">The Solution</h3>
            <p style="color: #cbd5e1; line-height: 1.7;">
                This tool scores your writing on four dimensions that resist convergence:
            </p>
            <ul style="color: #cbd5e1; line-height: 1.8;">
                <li><strong>Originality:</strong> Avoidance of clichés and generic phrases</li>
                <li><strong>Evidence:</strong> Specific data, examples, and citations</li>
                <li><strong>Clarity:</strong> Readable structure without unnecessary complexity</li>
                <li><strong>Voice:</strong> Confidence and distinctive personality</li>
            </ul>

            <h3 style="color: #6366f1; margin-top: 2rem;">Methodology</h3>
            <p style="color: #cbd5e1; line-height: 1.7;">
                The analyzer uses pattern matching for cliché detection, readability metrics for clarity, 
                and linguistic analysis for voice strength. It runs entirely in your browser (no text is stored 
                on any server) and is built with Python and Streamlit.
            </p>
        </div>
    """, unsafe_allow_html=True)
