"""
Beautiful metric displays and score visualizations.
"""

import streamlit as st

def score_gauge(score: float, label: str, color: str = "#6366f1"):
    """Create a circular score gauge using HTML/CSS"""
    # Determine color based on score
    if score >= 80:
        color = "#10b981"  # Green
    elif score >= 60:
        color = "#6366f1"  # Indigo
    elif score >= 40:
        color = "#f59e0b"  # Orange
    else:
        color = "#f43f5e"  # Red

    html = f"""
    <div style="text-align: center; padding: 1rem;">
        <div style="
            width: 140px;
            height: 140px;
            border-radius: 50%;
            background: conic-gradient({color} {score * 3.6}deg, #1e293b 0deg);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            position: relative;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        ">
            <div style="
                width: 115px;
                height: 115px;
                background: #0f172a;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
            ">
                <span style="
                    font-size: 2.5rem;
                    font-weight: 800;
                    color: {color};
                    line-height: 1;
                ">{score:.0f}</span>
                <span style="
                    font-size: 0.75rem;
                    color: #94a3b8;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                    margin-top: 4px;
                ">score</span>
            </div>
        </div>
        <p style="
            margin-top: 0.75rem;
            font-size: 0.9rem;
            color: #e2e8f0;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">{label}</p>
    </div>
    """
    return html

def metric_card(title: str, value: str, delta: str = None, status: str = "neutral"):
    """Create a metric card with status indicator"""
    colors = {
        "good": "#10b981",
        "warning": "#f59e0b", 
        "bad": "#f43f5e",
        "neutral": "#6366f1"
    }

    color = colors.get(status, colors["neutral"])

    delta_html = f"""
        <span style="
            color: {color};
            font-size: 0.875rem;
            font-weight: 600;
        ">{delta}</span>
    """ if delta else ""

    html = f"""
    <div style="
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        border-left: 4px solid {color};
    ">
        <p style="
            color: #94a3b8;
            font-size: 0.875rem;
            margin: 0 0 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">{title}</p>
        <div style="display: flex; align-items: baseline; gap: 0.5rem;">
            <span style="
                font-size: 1.5rem;
                font-weight: 700;
                color: #f8fafc;
            ">{value}</span>
            {delta_html}
        </div>
    </div>
    """
    return html

def score_breakdown(originality: float, evidence: float, clarity: float, voice: float):
    """Display detailed score breakdown with progress bars"""

    def get_color(score):
        if score >= 80: return "#10b981"
        elif score >= 60: return "#6366f1"
        elif score >= 40: return "#f59e0b"
        return "#f43f5e"

    metrics = [
        ("Originality", originality, "Avoidance of clichés & uniqueness"),
        ("Evidence", evidence, "Data backing & specificity"),
        ("Clarity", clarity, "Readability & structure"),
        ("Voice", voice, "Confidence & personality")
    ]

    html = "<div style='space-y: 1rem;'>"

    for label, score, desc in metrics:
        color = get_color(score)
        html += f"""
        <div style="margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #e2e8f0; font-weight: 600;">{label}</span>
                <span style="color: {color}; font-weight: 700;">{score:.0f}/100</span>
            </div>
            <div style="
                width: 100%;
                height: 8px;
                background: #1e293b;
                border-radius: 4px;
                overflow: hidden;
            ">
                <div style="
                    width: {score}%;
                    height: 100%;
                    background: linear-gradient(90deg, {color} 0%, {color}dd 100%);
                    border-radius: 4px;
                    transition: width 1s ease-out;
                "></div>
            </div>
            <p style="
                color: #64748b;
                font-size: 0.8rem;
                margin: 0.25rem 0 0 0;
            ">{desc}</p>
        </div>
        """

    html += "</div>"
    return html

def overall_grade(score: float):
    """Calculate and display letter grade with interpretation"""
    if score >= 90:
        grade, label, color = "A", "Exceptional", "#10b981"
    elif score >= 80:
        grade, label, color = "B", "Strong", "#6366f1"
    elif score >= 70:
        grade, label, color = "C", "Average", "#f59e0b"
    elif score >= 60:
        grade, label, color = "D", "Below Average", "#f97316"
    else:
        grade, label, color = "F", "Convergent", "#f43f5e"

    return f"""
    <div style="
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    ">
        <div style="
            font-size: 4rem;
            font-weight: 800;
            color: {color};
            line-height: 1;
            margin-bottom: 0.5rem;
        ">{grade}</div>
        <div style="
            font-size: 1.25rem;
            color: #e2e8f0;
            font-weight: 600;
        ">{label}</div>
        <div style="
            color: #94a3b8;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        ">{score:.1f}/100 overall</div>
    </div>
    """
