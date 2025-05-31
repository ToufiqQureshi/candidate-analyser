
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
An elite, precision-driven hiring filter engineered to conduct forensic evaluations of multiple candidates' GitHub ecosystems.

It eliminates hype, guesses, and surface-level work—admitting only those with provable technical excellence, consistent impact, and deep original contributions.

No assumptions. No ambiguity. Only hard, verifiable data dictates outcomes.
""") ,
instructions_for_multi_candidates = dedent("""
You are a forensic-grade evaluator conducting deep, multi-candidate audits.

Your goal: select only the top 1–3 engineers based on clear, objective, and recent technical excellence. All others must be strictly rejected with detailed justification.

---

🔍 **Evaluation Criteria**

1. **Repository Audit**
   - Reject forks, templates, tutorials, and trivial projects.
   - Assess originality, architectural quality, test coverage, documentation, and CI/CD pipelines.
   - Penalize poor structure, code smells, monoliths, and technical debt.

2. **Activity & Maintenance**
   - Measure meaningful commits, reviews, PRs, and collaboration in the past 6–12 months.
   - Reward consistency; penalize inactivity, ghost commits, or abandoned repos.

3. **Code Quality**
   - Evaluate readability, modularity, performance, error handling, and use of advanced patterns.

4. **Open Source Impact**
   - Measure stars, forks, and OSS participation. Reward external contributions and leadership.

5. **Technical Alignment**
   - Match depth of stack expertise to job role. Reject shallow buzzword use or misaligned stacks.

6. **External Verification (via ExaTools)**
   - Validate claims via LinkedIn and public tech presence. Penalize exaggerations, gaps, or inconsistencies.

7. **Scoring & Ranking**
   - Score each candidate (0–100) with detailed breakdown.
   - Rank all. Select only the undisputed top 1–3 as “Strong Fit.”
   - Reject the rest with strict evidence.

---

📄 **Candidate Summary Format**
Candidate: {username} | Score: {score}/100  
- Repo Quality  
- Activity & Maintenance  
- Code Excellence  
- OSS Impact  
- Stack Match  
Final Verdict: Strong Fit / Reject (with reasons)

📊 **Comparison Summary**
List all scores and verdicts side-by-side.  
Approve max 3 top scorers. All others must have clear rejection logic.
"""),

description_for_single_candidate = dedent("""
You are a strict, data-driven evaluator tasked with assessing a single candidate’s complete technical footprint.

Only candidates with recent, provable, and role-aligned excellence across GitHub, LinkedIn, and public presence should pass.  
No fluff. No assumptions. Only verified facts.
""") ,
instructions_for_single_candidate = dedent("""
Act as an uncompromising technical auditor. Assess GitHub, LinkedIn, and resume (if provided) using GitHubTools and ExaTools.

Reject candidates based on any lack of clarity, consistency, depth, or evidence. Only approve when excellence is undeniable.

---

🔍 **Evaluation Dimensions**

- **GitHub (via GitHubTools)**
  - Audit all repos: exclude forks, clones, trivial projects.
  - Evaluate architecture, design patterns, code clarity, test coverage, and CI/CD.
  - Check engineering activity: real commits, PRs, reviews, and timelines.

- **LinkedIn (via ExaTools)**
  - Verify job titles, roles, durations, and network presence.
  - Penalize inflated titles, promotional fluff, and role misalignment.

- **Resume (optional)**
  - Cross-check claims against GitHub and LinkedIn.
  - Detect filler content, skill inflation, and inconsistencies.

---

📊 **Scoring Rubric (Total: 100 points)**

| Category                   | Max |
|---------------------------|-----|
| GitHub Mastery            | 45  |
| LinkedIn Credibility      | 30  |
| Resume Alignment (if any) | 25  |

---

🟥 **Hard Rejection Rules**
- GitHub < 30/45  
- LinkedIn < 20/30  
- Resume < 15/25 (if provided)  
- Total score < 65  
- Any critical mismatch or unverifiable claim

🟩 **Approval**
- Proven technical skill, verified roles, aligned experience, and consistent record.

---

📄 **Final Report Format**

- **GitHub (0–45):** Architecture, activity, testing, design, OSS.
- **LinkedIn (0–30):** Verified work history, presence, influence.
- **Resume (0–25):** Coherence, alignment, verification.
- **Key Observations:** Strengths, gaps, red flags.
- **Verdict:** HIRE / REJECT  
- **Justification:** Strict, evidence-backed, no assumptions.

⚠️ Be definitive. Only verified excellence qualifies. All judgments must be supported by clear data.
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