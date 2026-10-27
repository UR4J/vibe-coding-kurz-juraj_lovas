"""
Neohunter sourcing agent: the same ReAct loop as main.py, with recruitment tools.

The agent gets a job ID and has to work out the steps itself:
read the job -> search the candidate pool -> open the profiles -> rank -> draft outreach.
Nothing in the code tells it this order. That is the point of ReAct.

All candidates and jobs below are FICTIONAL. This repo is public:
never put real candidate or client data here.

Run:  uv run neohunter_agent.py
"""

from main import ReactAgent

# -----------------------------------------------------------------------------
# Fictional data (in real life: Recruit CRM API, LinkedIn Recruiter, Profesia...)
# -----------------------------------------------------------------------------
JOBS = {
    "J-101": {
        "title": "Senior Java Developer",
        "client": "Fintech klient (dôverné)",
        "location": "Bratislava, hybrid 2 dni v kancelárii",
        "must_have": ["Java", "Spring Boot", "5+ rokov praxe"],
        "nice_to_have": ["Kafka", "Kubernetes", "fintech"],
        "salary_max_eur_month": 5500,
        "language": "angličtina B2",
    },
    "J-102": {
        "title": "Regionálny manažér predaja",
        "client": "Retailová sieť (dôverné)",
        "location": "Nitra a okolie, veľa cestovania",
        "must_have": ["riadenie tímu 10+ ľudí", "retail alebo FMCG", "vodičský preukaz B"],
        "nice_to_have": ["P&L zodpovednosť", "otváranie nových predajní"],
        "salary_max_eur_month": 3800,
        "language": "slovenčina",
    },
}

CANDIDATES = {
    "C-01": {"name": "Martin K.", "headline": "Senior Java Developer", "location": "Bratislava",
             "skills": ["Java", "Spring Boot", "Kafka", "AWS"], "years": 7, "domain": "banking",
             "salary_expect_eur_month": 5200, "notice_months": 2, "open_to_move": "pasívny, otvorený"},
    "C-02": {"name": "Zuzana P.", "headline": "Backend Engineer (Java/Kotlin)", "location": "Brno (CZ)",
             "skills": ["Java", "Kotlin", "Spring Boot", "Kubernetes"], "years": 6, "domain": "e-commerce",
             "salary_expect_eur_month": 5800, "notice_months": 2, "open_to_move": "aktívne hľadá"},
    "C-03": {"name": "Peter L.", "headline": "Java Developer", "location": "Trnava",
             "skills": ["Java", "Spring", "SQL"], "years": 3, "domain": "telco",
             "salary_expect_eur_month": 3600, "notice_months": 1, "open_to_move": "aktívne hľadá"},
    "C-04": {"name": "Andrea M.", "headline": "Area Manager, retail", "location": "Nitra",
             "skills": ["riadenie tímu", "retail", "P&L", "vodičský preukaz B"], "years": 9, "team_size": 45,
             "domain": "potravinový retail", "salary_expect_eur_month": 3500, "notice_months": 3,
             "open_to_move": "pasívna, otvorená"},
    "C-05": {"name": "Tomáš V.", "headline": "Key Account Manager FMCG", "location": "Nitra",
             "skills": ["predaj", "FMCG", "vyjednávanie", "vodičský preukaz B"], "years": 8, "team_size": 0,
             "domain": "FMCG distribúcia", "salary_expect_eur_month": 3200, "notice_months": 2,
             "open_to_move": "aktívne hľadá"},
    "C-06": {"name": "Lucia H.", "headline": "Store Operations Manager", "location": "Trnava",
             "skills": ["riadenie tímu", "retail", "otváranie predajní", "vodičský preukaz B"], "years": 6,
             "team_size": 14, "domain": "drogéria", "salary_expect_eur_month": 3100, "notice_months": 2,
             "open_to_move": "pasívna"},
}


# -----------------------------------------------------------------------------
# Tool implementations
# -----------------------------------------------------------------------------
def get_job(job_id: str):
    """Return the job requirements."""
    return JOBS.get(job_id, {"error": f"Job {job_id} not found"})


def search_candidates(keyword: str):
    """Search candidates by a keyword in headline, skills or domain. Returns a short list only."""
    kw = keyword.lower()
    hits = []
    for cid, c in CANDIDATES.items():
        haystack = " ".join([c["headline"], c["domain"], *c["skills"]]).lower()
        if kw in haystack:
            hits.append({"candidate_id": cid, "name": c["name"], "headline": c["headline"], "location": c["location"]})
    return {"keyword": keyword, "results": hits}


def get_candidate(candidate_id: str):
    """Return the full candidate profile."""
    return CANDIDATES.get(candidate_id, {"error": f"Candidate {candidate_id} not found"})


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_job",
            "description": "Get the requirements of an open job: must-haves, nice-to-haves, location, salary cap.",
            "parameters": {
                "type": "object",
                "properties": {"job_id": {"type": "string", "description": "Job ID, e.g. J-101"}},
                "required": ["job_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_candidates",
            "description": (
                "Search the candidate pool by ONE keyword (skill, role or industry). "
                "Returns only ID, name, headline and location. Call several times with different keywords."
            ),
            "parameters": {
                "type": "object",
                "properties": {"keyword": {"type": "string", "description": "e.g. Java, retail, FMCG"}},
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_candidate",
            "description": "Get the full profile of one candidate: skills, years, team size, salary expectation, notice period.",
            "parameters": {
                "type": "object",
                "properties": {"candidate_id": {"type": "string", "description": "Candidate ID, e.g. C-04"}},
                "required": ["candidate_id"],
            },
        },
    },
]

FUNCTIONS = {
    "get_job": get_job,
    "search_candidates": search_candidates,
    "get_candidate": get_candidate,
}

SYSTEM_PROMPT = """You are a senior headhunter at Neohunter, a Slovak executive search firm.
Work only with data you get from the tools. Never invent candidates or facts.
Before you rank anyone, open their full profile with get_candidate.
Check every must-have and the salary cap. If a candidate misses a must-have, say so.
Answer in Slovak, short and structured."""


def main():
    agent = ReactAgent(tools=TOOLS, functions=FUNCTIONS)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Pozícia J-102. Nájdi 2 najvhodnejších kandidátov, ku každému 2 vety prečo "
                "a 1 riziko. Potom napíš úvodnú vetu LinkedIn oslovenia pre kandidáta č. 1 "
                "(vykanie, bez mena klienta)."
            ),
        },
    ]
    agent.run(messages)


if __name__ == "__main__":
    main()
