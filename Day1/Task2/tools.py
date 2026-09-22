COMPANIES = {
    "Company A": 7.5,
    "Company B": 7.0,
    "Company C": 8.0
}


def check_company_eligibility(cgpa, backlog, attendance, company):
    if attendance < 75:
        return "Not eligible: attendance is below 75%."

    if backlog:
        return "Not eligible: active backlog."

    required = COMPANIES.get(company)

    if required is None:
        return "Unknown company."

    if cgpa >= required:
        return f"Eligible for {company}."

    return (
        f"Not eligible for {company}. "
        f"Required CGPA: {required}, student CGPA: {cgpa}."
    )


def get_eligible_companies(cgpa, backlog, attendance):
    if attendance < 75:
        return "No companies: attendance is below 75%."

    if backlog:
        return "No companies: student has an active backlog."

    eligible = [
        company
        for company, required in COMPANIES.items()
        if cgpa >= required
    ]

    return ", ".join(eligible) if eligible else "No eligible companies."


TOOL_FUNCTIONS = {
    "check_company_eligibility": check_company_eligibility,
    "get_eligible_companies": get_eligible_companies
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_company_eligibility",
            "description": "Check whether a student is eligible for a specific company.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cgpa": {"type": "number"},
                    "backlog": {"type": "boolean"},
                    "attendance": {"type": "number"},
                    "company": {
                        "type": "string",
                        "enum": ["Company A", "Company B", "Company C"]
                    }
                },
                "required": [
                    "cgpa",
                    "backlog",
                    "attendance",
                    "company"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_eligible_companies",
            "description": "Find all companies a student is eligible for.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cgpa": {"type": "number"},
                    "backlog": {"type": "boolean"},
                    "attendance": {"type": "number"}
                },
                "required": [
                    "cgpa",
                    "backlog",
                    "attendance"
                ]
            }
        }
    }
]