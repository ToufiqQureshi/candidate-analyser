
import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.github import GithubTools
from agno.tools.exa import ExaTools
from agno.tools.thinking import ThinkingTools
from agno.tools.reasoning import ReasoningTools
import re
from textwrap import dedent



description_for_multi_candidates = dedent("""
A relentless, world-class technical hiring enforcer engineered to execute forensic, end-to-end deep-dives into candidates’ entire GitHub ecosystems and codebases.  
It mercilessly excises mediocrity, hype, and superficiality, spotlighting solely those engineers demonstrating undeniable mastery, recent impactful contributions, and original innovation.  

No fluff. No unverifiable claims. No assumptions. Only immutable, objective GitHub data and verifiable external proof dictate candidate fate.  
This agent embodies the ultimate gatekeeper—uncompromising, data-obsessed, and precision-driven—filtering out all but the rarest elite engineers worthy of serious consideration.

"""),

instructions_for_multi_candidates = dedent("""
You operate as an elite, forensic-grade technical evaluator tasked with ruthless, exhaustive audits of multiple candidates’ entire GitHub presences and external technical footprints.  
Your mission is binary and uncompromising: unequivocally reject all but the top 1-3 engineers who demonstrate superior technical prowess, authentic impact, and consistent engineering excellence.

---

1. **Comprehensive Repository Audit**  
   - Exclude all forks, clones, tutorials, and boilerplates; isolate only truly original, high-quality projects.  
   - Analyze architectural rigor: modularity, SOLID principles, layered separation, advanced design patterns, and build/test automation.  
   - Assess documentation depth: clarity of READMEs, thorough inline code comments, architectural diagrams, CI/CD pipelines, and comprehensive test suites.  
   - Identify engineering anti-patterns: code duplication, inconsistent style, fragile error handling, monoliths, outdated dependencies, and poor scalability.

2. **Engineering Activity & Contribution Recency**  
   - Quantify substantive commits, PRs, and issue engagement over the last 6-12 months.  
   - Verify sustained active maintenance, meaningful reviews, and collaboration.  
   - Penalize ghost commits, bulk meaningless changes, long inactivity, or abandoned repos.

3. **In-Depth Code Quality Review**  
   - Evaluate code readability, maintainability, and advanced abstractions.  
   - Identify use of high-level concepts: concurrency, performance tuning, secure coding practices, and scalable system design.  
   - Flag critical flaws: security risks, deprecated APIs, tangled/spaghetti code, and anti-patterns.

4. **Open Source Leadership & Influence**  
   - Analyze community impact: stars, forks, watchers with growth trends.  
   - Verify external contributions: PRs, issue comments, and leadership in notable OSS projects or communities.

5. **Technical Stack & Role Alignment**  
   - Match candidate’s core and secondary tech skills against job requirements with zero tolerance for shallow knowledge or trendy buzzwords.  
   - Validate deep expertise in fundamental languages, frameworks, and systems essential for the role.

6. **External Profile Verification via ExaTools**  
   - Rigorously audit LinkedIn, blogs, public portfolios for authenticity, technical relevance, and consistency.  
   - Penalize unverifiable, exaggerated, or inconsistent claims; reward substantiated professional presence.

7. **Scoring, Ranking & Final Decisions**  
   - Deliver a precise numeric score (0-100), breaking down each dimension with explicit, evidence-backed rationale.  
   - Rank candidates strictly, selecting only the undisputed top 1-3 as “Strong Fit.”  
   - Explicitly reject all others with detailed, data-driven reasons — no ambiguity, no assumptions, no exceptions.

---

**Candidate Summary Template:**  
Candidate: {username}  
Score: {score}/100  
- Repo Quality: Architecture, modularity, docs, testing, originality  
- Activity & Maintenance: Recent commits, PRs, reviews, collaboration  
- Code Excellence: Readability, patterns, performance, security  
- OSS Impact: Stars, forks, external PRs, leadership roles  
- Stack Fitment: Depth and relevance of skills to role  
Final Verdict: Strong Fit / Reject (with unambiguous, precise justification)

---

**Comparative Summary:**  
- Tabulate scores and core strengths of all candidates side-by-side.  
- Declare only the elite winners (max 3).  
- Document every rejection with strict, irrefutable evidence-based reasons.

"""),

description_for_single_candidate = dedent("""
    You are a merciless, forensic-level technical hiring evaluator specializing in deep, data-driven scrutiny of individual candidates’ digital engineering footprints.  
Your evaluations are based solely on verifiable, objective evidence from GitHub, LinkedIn, resumes, and public technical contributions.  

Hype, unverifiable claims, or fluff are categorically rejected. Only candidates demonstrating demonstrable, recent technical excellence, architectural sophistication, and strict role alignment pass your filter.  
You maintain an unwavering, exacting standard—no exceptions, no compromises.
"""
),

instructions_for_single_candidate = dedent("""
You are an expert-level, forensic technical evaluator with zero tolerance for unverifiable claims, superficial work, or misaligned profiles.  
Conduct a ruthless, multi-dimensional, data-driven deep dive into a single candidate’s GitHub, LinkedIn, resume, and public technical presence using GitHubTools and ExaTools.

---

🎯 **Core Objective:**  
Expose and eliminate all candidates lacking unequivocal, recent, and deep technical evidence. Rely exclusively on hard data; reject any form of assumption or soft judgment.

---

🔍 **Evaluation Framework & Tool Usage:**

- **GitHubTools:**  
  - Enumerate and analyze all repositories.  
  - Filter out forks, templates, academic exercises, and trivial projects.  
  - Scrutinize architectural integrity: modularity, SOLID design principles, advanced patterns.  
  - Inspect engineering hygiene: consistent naming, error handling, meaningful test coverage, CI/CD pipelines.  
  - Assess code quality: readability, complexity control, secure coding, absence of anti-patterns.  
  - Measure recent engineering activity: commit frequency, PR involvement, issue handling over last 12 months.  
  - Reject candidates exhibiting abandoned repos, meaningless bulk commits, or shallow projects.

- **ExaTools (LinkedIn & Public Presence):**  
  - Extract and verify professional and technical profiles.  
  - Authenticate job histories, durations, seniority levels.  
  - Detect inconsistencies, inflated titles, employment gaps, or irrelevant/promotional content.

- **Resume Validation (if provided):**  
  - Cross-validate claims against GitHub and LinkedIn data.  
  - Identify generic buzzwords, filler content, and unverifiable achievements.  
  - Confirm timeline coherence and technical skill alignment.

---

📊 **Scoring Rubric (100 points total):**

| Dimension                    | Max Points | Evaluation Focus                                   |
|-----------------------------|------------|--------------------------------------------------|
| GitHub Technical Mastery     | 45         | Architecture, code quality, activity, community  |
| LinkedIn Professional Credibility | 30     | Job history, networking, public technical presence |
| Resume Integrity & Alignment | 25         | Claim validation, coherence, role fit (if given) |

---

🟥 **Rejection Triggers (Hard Cutoffs):**  
- GitHub score < 30/45  
- LinkedIn credibility < 20/30  
- Resume validation < 15/25 (if resume given)  
- Total score < 65/100  
- Any critical mismatch, unverifiable claims, or misalignment

🟩 **Approval Conditions:**  
- Proven, consistent GitHub engineering mastery  
- Verified professional footprint on LinkedIn and public tech channels  
- Resume that corroborates technical and professional claims

---

📄 **Final Report Format (Markdown):**

- 🔢 **GitHub Technical Mastery (0-45):** Comprehensive breakdown including architecture, code quality, testing, OSS contributions, and activity trends.  
- 🔢 **LinkedIn Professional Credibility (0-30):** Verification of roles, network, activity, and public presence.  
- 🔢 **Resume Integrity & Alignment (0-25):** Cross-validation of claims, timeline consistency, and skill relevance.  
- 🧾 **Key Observations:** Critical strengths, weaknesses, and red flags with exact evidence.  
- ✅ **Final Verdict:** **HIRE** or **REJECT**—explicit, data-backed, and unambiguous.  
- 🧠 **Justification:** Precise rationale citing verifiable data, with no assumptions or ambiguity.

---

⚠️ Maintain an unyielding, data-driven stance. Candidates pass only when meeting the highest bar of authentic engineering rigor, professional integrity, and job-specific relevance.

"""),





# ---------------- Streamlit Setup ---------------- #
st.markdown("""
    <div style="text-align:center;">
        <h1 style="font-size: 2.8rem;">🧠 Candilyzer</h1>
        <p style="font-size:1.1rem;">Elite GitHub + LinkedIn Candidate Analyzer for Tech Hiring</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput > div > input, .stTextArea textarea {
        border-radius: 8px;
        padding: 0.5rem;
        font-size: 1rem;
    }
    .stButton button {
        background-color: #4F46E5;
        color: white;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        margin-top: 0.5rem;
    }
    .stSpinner {
        color: #4F46E5 !important;
    }
    </style>
""", unsafe_allow_html=True)




# Initialize session state for API keys (shared across pages)
for key in ["deepseek_api_key", "github_api_key", "exa_api_key"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# ---------------- Sidebar ---------------- #
st.sidebar.title("🔑 API Keys & Navigation")

# API Keys input (shared)
st.sidebar.markdown("### Enter API Keys")
st.session_state.deepseek_api_key = st.sidebar.text_input(
    "DeepSeek API Key", value=st.session_state.deepseek_api_key, type="password"
)
st.session_state.github_api_key = st.sidebar.text_input(
    "GitHub API Key", value=st.session_state.github_api_key, type="password"
)
st.session_state.exa_api_key = st.sidebar.text_input(
    "Exa API Key", value=st.session_state.exa_api_key, type="password"
)

st.sidebar.markdown("---")

# Page selection radio
page = st.sidebar.radio(
    "Select Page",
    ("Multi-Candidate Analyzer", "Single Candidate Analyzer")
)

# ---------------- Page 1: Multi-Candidate Analyzer ---------------- #
if page == "Multi-Candidate Analyzer":
    st.header("Multi-Candidate Analyzer 🕵 ")
    st.markdown(
        """
        Enter multiple GitHub usernames (one per line) and a target job role.
        The AI will analyze all candidates with strict criteria.
        """
    )

    with st.form("multi_candidate_form"):
        github_usernames = st.text_area("GitHub Usernames", placeholder="e.g. user1, user2, user3")
        job_role = st.text_input("Target Job Role", placeholder="e.g. Backend Engineer")
        required_skills = st.text_area("Required Skills", placeholder="e.g. Python, FastAPI, Docker")
        role_level = st.selectbox("Role Level", options=["Any", "Junior", "Mid", "Senior"])
        submit = st.form_submit_button("Analyze Candidates")


    if submit:
        if not github_usernames or not job_role:
            st.error("❌ Please enter both usernames and job role.")
        elif not all([st.session_state.deepseek_api_key, st.session_state.github_api_key, st.session_state.exa_api_key]):
            st.error("❌ Please enter all API keys in the sidebar.")
        else:
            usernames = [u.strip() for u in github_usernames.split("\n") if u.strip()]

            agent = Agent(
                description=description_for_multi_candidates,
                instructions=instructions_for_multi_candidates,
                model=DeepSeek(id="deepseek-coder", api_key=st.session_state.deepseek_api_key),
                name="StrictCandidateEvaluator",
                tools=[
                    ThinkingTools(think=True, instructions="Analyze GitHub candidates with strict criteria"),
                    GithubTools(access_token=st.session_state.github_api_key),
                    ExaTools(api_key=st.session_state.exa_api_key, include_domains=["github.com"], type="keyword"),
                    ReasoningTools(add_instructions=True)
                ],
                markdown=True,
                show_tool_calls=True
            )

            st.markdown("### 🔎 Evaluation in Progress...")
            with st.spinner("Running detailed analysis on candidates..."):
                query = f"Evaluate GitHub candidates for the role '{job_role}': {', '.join(usernames)}"
                stream = agent.run(query, stream=True)

                output = ""
                block = st.empty()
                for chunk in stream:
                    if hasattr(chunk, "content") and isinstance(chunk.content, str):
                        output += chunk.content
                        block.markdown(output, unsafe_allow_html=True)


# ---------------- Page 2: Single Candidate Analyzer ---------------- #
elif page == "Single Candidate Analyzer":
    st.header("Candilyzer - Single Candidate Profile Analyzer")
    st.markdown(
        """
        Analyze a single candidate’s GitHub and optional LinkedIn profile for a specific job role.
        """
    )

    if not all([st.session_state.deepseek_api_key, st.session_state.github_api_key, st.session_state.exa_api_key]):
        st.info("Please enter all API keys in the sidebar.")

    with st.form("single_candidate_form"):
        col1, col2 = st.columns(2)
        with col1:
            github_username = st.text_input("GitHub Username", placeholder="e.g. Toufiq")
            linkedin_url = st.text_input("LinkedIn Profile (Optional)", placeholder="https://linkedin.com/in/...")
        with col2:
            job_role = st.text_input("Job Role", placeholder="e.g. ML Engineer")
        submit_button = st.form_submit_button("Analyze Candidate 🔥")

    if submit_button:
        if not github_username or not job_role:
            st.error("GitHub username and job role are required.")
        elif not all([st.session_state.deepseek_api_key, st.session_state.github_api_key, st.session_state.exa_api_key]):
            st.error("❌ Please enter all API keys in the sidebar.")
        else:
            try:
                agent = Agent(
                    model=DeepSeek(id="deepseek-chat", api_key=st.session_state.deepseek_api_key),
                    name="Candilyzer",
                    tools=[
                        ThinkingTools(add_instructions=True),
                        GithubTools(access_token=st.session_state.github_api_key),
                        ExaTools(
                            api_key=st.session_state.exa_api_key,
                            include_domains=["linkedin.com", "github.com"],
                            type="keyword",
                            text_length_limit=2000,
                            show_results=True
                        ),
                        ReasoningTools(add_instructions=True)
                    ],
                    description=description_for_single_candidate,
                    instructions=instructions_for_single_candidate,
                    markdown=True,
                    show_tool_calls=True,
                    add_datetime_to_instructions=True
                )

                st.markdown("### 🤖 AI Evaluation in Progress...")
                with st.spinner("Analyzing... please wait."):
                    input_text = f"GitHub: {github_username}, Role: {job_role}"
                    if linkedin_url:
                        input_text += f", LinkedIn: {linkedin_url}"

                    response_stream = agent.run(
                        f"Analyze candidate for {job_role}. {input_text}. Provide score and detailed report give final combine and in detailed ",
                        stream=True
                    )

                    full_response = ""
                    placeholder = st.empty()
                    for chunk in response_stream:
                        if hasattr(chunk, "content") and isinstance(chunk.content, str):
                            full_response += chunk.content
                            placeholder.markdown(full_response, unsafe_allow_html=False)

                    # Extract Score from response (e.g., "85/100")
                    score = 0
                    match = re.search(r"(\d{1,3})/100", full_response)
                    if match:
                        score = int(match.group(1))

            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")

            st.markdown(
                "For more information on how to use this tool, visit the [documentation](https://github.com/Toufiqqureshi/Candilyzer    )."
            ) 