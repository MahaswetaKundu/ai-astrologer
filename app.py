# app.py
# Streamlit app: AI Astrologer (rule-based demo)
# Collects Name, Date, Time, Place and returns a simple reading + free-text Q&A.

import hashlib
import random
from dataclasses import dataclass
from datetime import datetime, date

from typing import Dict, List

import streamlit as st

# ----------------------------
# Astrology logic (rule-based)
# ----------------------------
min_date = date(1800, 1, 1)   # start limit
max_date = date(2200, 12, 31)

ZODIAC_RANGES = [
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21)),
]

TRAITS = {
    "Aries": {"element": "Fire", "strengths": ["Bold", "Driven", "Candid"], "growth": ["Patience", "Listening"]},
    "Taurus": {"element": "Earth", "strengths": ["Steady", "Loyal", "Practical"], "growth": ["Flexibility", "Letting go"]},
    "Gemini": {"element": "Air", "strengths": ["Curious", "Witty", "Adaptable"], "growth": ["Focus", "Consistency"]},
    "Cancer": {"element": "Water", "strengths": ["Nurturing", "Intuitive", "Protective"], "growth": ["Boundaries", "Directness"]},
    "Leo": {"element": "Fire", "strengths": ["Confident", "Warm", "Creative"], "growth": ["Humility", "Delegation"]},
    "Virgo": {"element": "Earth", "strengths": ["Analytical", "Helpful", "Refined"], "growth": ["Self-kindness", "Big-picture"]},
    "Libra": {"element": "Air", "strengths": ["Diplomatic", "Fair", "Charming"], "growth": ["Decisiveness", "Follow-through"]},
    "Scorpio": {"element": "Water", "strengths": ["Intense", "Loyal", "Transformative"], "growth": ["Trust", "Lightness"]},
    "Sagittarius": {"element": "Fire", "strengths": ["Optimistic", "Candid", "Adventurous"], "growth": ["Detail care", "Commitment"]},
    "Capricorn": {"element": "Earth", "strengths": ["Ambitious", "Disciplined", "Patient"], "growth": ["Playfulness", "Vulnerability"]},
    "Aquarius": {"element": "Air", "strengths": ["Original", "Humanitarian", "Independent"], "growth": ["Warmth", "Practicality"]},
    "Pisces": {"element": "Water", "strengths": ["Empathic", "Imaginative", "Gentle"], "growth": ["Boundaries", "Clarity"]},
}

@dataclass
class Profile:
    name: str
    sign: str
    element: str
    strengths: List[str]
    growth: List[str]
    today_vibe: str

def get_zodiac_sign(date_str: str) -> str:
    """Map YYYY-MM-DD to Western sun sign by date range."""
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    m, day = d.month, d.day
    for name, (sm, sd), (em, ed) in ZODIAC_RANGES:
        if (m == sm and day >= sd) or (m == em and day <= ed):
            return name
    return "Capricorn"

def seed_from_text(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)

def build_profile(name: str, date: str, time_str: str, place: str) -> Profile:
    sign = get_zodiac_sign(date)
    traits = TRAITS[sign]
    vibes = ["lucky", "reflective", "productive", "social", "romantic", "adventurous"]
    rnd = random.Random(seed_from_text(f"{name}|{date}|{time_str}|{place}"))
    return Profile(
        name=name.strip(),
        sign=sign,
        element=traits["element"],
        strengths=traits["strengths"],
        growth=traits["growth"],
        today_vibe=rnd.choice(vibes),
    )

def daily_outlook(profile: Profile) -> Dict[str, str]:
    rnd = random.Random(seed_from_text(f"{profile.name}|{profile.sign}|{profile.today_vibe}"))
    def pick(choices): return rnd.choice(choices)
    return {
        "career": pick([
            "Tackle the task you’ve been postponing—the momentum will snowball.",
            "A short conversation unlocks a big opportunity—speak up.",
            "Focus beats multitasking today; one deep work block will shine.",
            "Document your wins; they’ll be handy for reviews or pitching ideas.",
        ]),
        "love": pick([
            "Lead with honesty and a tiny act of kindness—warmth returns.",
            "Keep plans flexible; a spontaneous invite could delight you.",
            "Listening more than you speak improves harmony dramatically.",
            "Share a small personal story to deepen connection.",
        ]),
        "health": pick([
            "Hydration plus a 20-minute walk resets your energy.",
            "Stretch your neck/shoulders; screens have been sneaking tension in.",
            "Choose whole foods over packaged today; your focus will thank you.",
            "Early bedtime amplifies tomorrow’s productivity.",
        ]),
        "finance": pick([
            "Review one recurring expense—you may trim a small leak.",
            "Avoid impulsive purchases; sleep on non-essentials.",
            "Automate a tiny transfer to savings; consistency compounds.",
            "Compare prices before you commit; a bargain appears.",
        ]),
        "luck": pick([
            "Lucky color: something that makes you feel confident.",
            "A message from an old contact could be timely—check politely.",
            "Numbers that repeat today are your nudge to act.",
            "A detour reveals a pleasant surprise.",
        ]),
    }

def answer_question(question: str, profile: Profile) -> str:
    q = (question or "").lower()
    buckets = {
        "career": ["job", "career", "work", "promotion", "study", "college", "internship"],
        "money": ["money", "finance", "investment", "loan", "buy", "sell"],
        "love": ["love", "relationship", "marriage", "partner", "crush"],
        "health": ["health", "fitness", "diet", "stress", "sleep"],
        "travel": ["travel", "trip", "move", "relocate", "abroad", "visa"],
    }
    base = f"As a {profile.sign} ({profile.element} element), today’s theme is **{profile.today_vibe}**."
    tips = {
        "career": [
            "Prioritize a single high-impact task before noon.",
            "Have a crisp 2–3 line update ready for your manager or mentor.",
            "Say yes to collaborations that align with your long-term plan.",
        ],
        "money": [
            "Do a 10-minute budget review and cancel one low-value expense.",
            "Favor steady growth over high-risk moves today.",
            "If negotiating, anchor with data and be ready to walk away.",
        ],
        "love": [
            "State your needs kindly and ask one curious question in return.",
            "Shared activities build closeness—suggest something simple.",
            "Let actions match words; small consistency wins hearts.",
        ],
        "health": [
            "Micro-habit: 5 deep breaths whenever you unlock your phone.",
            "Add protein+fiber to your next meal for steady energy.",
            "A 15-minute walk outdoors clears mental fog.",
        ],
        "travel": [
            "Recheck documents and build a simple plan B.",
            "Choose comfort plus safety over speed today.",
            "Reach out to a local friend/contact for one insider tip.",
        ],
        "general": [
            "Reflect for 3 minutes, then take the smallest useful step.",
            "Clarity comes after action—start tiny.",
            "Protect your time blocks; say no gracefully.",
        ],
    }
    def choose(topic): return random.choice(tips[topic])
    if any(w in q for w in buckets["career"]): return f"{base} Career note: {choose('career')}"
    if any(w in q for w in buckets["money"]):  return f"{base} Finance note: {choose('money')}"
    if any(w in q for w in buckets["love"]):   return f"{base} Love note: {choose('love')}"
    if any(w in q for w in buckets["health"]): return f"{base} Health note: {choose('health')}"
    if any(w in q for w in buckets["travel"]): return f"{base} Travel note: {choose('travel')}"
    return f"{base} Guidance: {choose('general')}"

# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="AI Astrologer (Demo)", page_icon="🔮", layout="centered")
st.title("🔮 AI Astrologer")
st.caption("Educational demo • Rule-based reading (no real ephemeris).")

with st.form("birth_form"):
    name = st.text_input("Name", placeholder="Your full name")
    
    date = st.date_input("Date of Birth", min_value=min_date,
    max_value=max_date)
    time = st.time_input("Time of Birth")
    place = st.text_input("Place of Birth", placeholder="City, Country")
    submitted = st.form_submit_button("Generate Reading")

# After form submission, save profile in session
if submitted:
    if not name or not place or not date or not time:
        st.warning("Please fill all fields.")
    else:
        st.session_state.profile = build_profile(
            name, date.strftime("%Y-%m-%d"), time.strftime("%H:%M"), place
        )
        st.success("Profile generated! Scroll down to ask a question.")

# If profile exists, show results + Q&A
if "profile" in st.session_state:
    profile = st.session_state.profile
    outlook = daily_outlook(profile)

    st.subheader("Your Profile")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Sun Sign", profile.sign)
        st.metric("Element", profile.element)
    with c2:
        st.write("**Strengths**")
        st.write(", ".join(profile.strengths))
    with c3:
        st.write("**Growth Areas**")
        st.write(", ".join(profile.growth))

    st.subheader("Today’s Outlook")
    colA, colB = st.columns(2)
    with colA:
        st.write("**Career:**", outlook["career"])
        st.write("**Health:**", outlook["health"])
        st.write("**Luck:**", outlook["luck"])
    with colB:
        st.write("**Love:**", outlook["love"])
        st.write("**Finance:**", outlook["finance"])

    st.divider()
    st.subheader("Ask a Question")
    q = st.text_area("Type one free-text question", placeholder="e.g., Will I get a promotion this year?")
    if st.button("Get Answer"):
        ans = answer_question(q, profile)
        st.success(ans)
        st.caption("Note: For serious decisions, use practical research and professional advice.")
else:
    st.info("Fill the form and click **Generate Reading** to see your profile and outlook.")
