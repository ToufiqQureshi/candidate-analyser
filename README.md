<h1 align="center">🧠 Candilyzer</h1>
<p align="center">
  <strong>AI-Powered Candidate Analyzer for GitHub & LinkedIn</strong><br>
  <em>Strict, expert-level screening for tech candidates</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Built%20With-Streamlit-%23FF4B4B?style=for-the-badge">
  <img src="https://img.shields.io/badge/AI%20Model-DeepSeek-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/Agno-Agent%20Framework-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-success?style=for-the-badge">
</p>

---

## 🔍 What is Candilyzer?

**Candilyzer** is an advanced, AI-powered app that strictly analyzes technical candidates based on their **GitHub** and **LinkedIn** profiles. Designed like a tough hiring manager, it gives you detailed evaluations, skill assessments, and a final decision — all with zero assumptions.

---

## ⚡ Features

✅ **Multi-Candidate Analyzer**  
Analyze *multiple* GitHub users side-by-side for any job role.

✅ **Single Candidate Profiler**  
Deep analysis of one candidate's GitHub + optional LinkedIn profile.

✅ **Strict Scoring System**  
Each candidate is scored out of 100 with a clear final verdict.

✅ **Professional-Grade Reports**  
No fluff. Only data-backed, AI-generated expert-level assessments.

✅ **Powered by Agents**  
Uses Agno’s agent framework with DeepSeek + GitHubTools + ExaTools.

---

## 🧰 Tech Stack

| Component         | Tool/Library                   |
|------------------|--------------------------------|
| UI               | 🧼 Streamlit                   |
| AI Model         | 🧠 DeepSeek                    |
| Agent Framework  | 🧠 Agno Agents                 |
| GitHub Analysis  | 🛠️ GitHubTools                |
| LinkedIn Parsing | 🔎 ExaTools                   |
| Reasoning Engine | 🧩 ReasoningTools + ThinkingTools |

---

## 🚀 How to Run Locally

### 1. Clone the Repository


git clone https://github.com/Toufiqqureshi/Candilyzer.git
cd Candilyzer
** 2. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt


3. Get API Keys
You'll need the following keys:

🔑 DeepSeek API Key → Get from DeepSeek.com

🔑 GitHub API Key → Generate here (https://github.com/settings/tokens).

🔑 Exa API Key → Get from [exa](Exa.ai).

4. ```
Launch App
Copy
Edit
streamlit run Main.py
```


##🖥️ How to Use
*🔁 Multi-Candidate Analyzer
*Paste GitHub usernames (one per line)

Enter target Job Role (e.g. Backend Engineer)

Click Analyze Candidates

🔎 Single Candidate Analyzer
Enter GitHub username

Optionally, add LinkedIn profile link

Enter Job Role (e.g. ML Engineer)

Click Analyze Candidate 🔥

📊 Evaluation Logic
Candilyzer uses no assumptions and follows strict rules:

📁 GitHub Repos → code quality, structure, frequency

🧑‍💻 Commits → consistency, activity, skills shown

💼 LinkedIn → job titles, descriptions, keywords (via Exa)

🎯 Job Fit → match with required skills & experience

🧠 AI Reasoning → Final combined judgment with score


🧪 Powered by Agno Agents
Candilyzer builds a smart agent with:

```python
Copy
Edit
Agent(
  model=DeepSeek(...),
  tools=[
    GithubTools(...),
    ExaTools(...),
    ThinkingTools(...),
    ReasoningTools(...)
  ]
)
```

##This agent:

Thinks before evaluating (🧠)

Gathers accurate GitHub + LinkedIn info (🔍)

Reasons like an expert hiring manager (📈)

Provides a final score with strict justification (✅❌)



📄 License
This project is licensed under the MIT License.
Feel free to use, fork, and improve it.

💬 Questions / Feedback
Have suggestions or found a bug?
Open an issue or start a discussion → GitHub Discussions

🔗 Links
🔗 Agno Documentation

🔗 DeepSeek

🔗 Exa Search

📂 GitHubTools Docs

💡 Candilyzer is your AI hiring expert. Use it to save time, reduce bias, and get straight to the point.

