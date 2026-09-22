COMPANIES = {
    "Company A": 7.5,
    "Company B": 7.0,
    "Company C": 8.0
}


def check_eligibility(cgpa, backlog, attendance, company):
    if attendance < 75:
        return "Not eligible: attendance is below 75%."

    if backlog:
        return "Not eligible: student has an active backlog."

    required_cgpa = COMPANIES[company]

    if cgpa >= required_cgpa:
        return f"Eligible for {company}."

    return f"Not eligible for {company}: CGPA requirement is {required_cgpa}."


if __name__ == "__main__":

    print("=== TASK 2: RULE-BASED WORKFLOW ===")

    tests = [
        (7.6, False, 80, "Company A"),
        (7.6, False, 80, "Company C"),
        (7.8, False, 80, "Company B"),
        (7.8, False, 80, "Company C")
    ]

    for cgpa, backlog, attendance, company in tests:
        print(
            f"\nStudent: CGPA={cgpa}, "
            f"Backlog={backlog}, Attendance={attendance}%"
        )
        print(check_eligibility(
            cgpa, backlog, attendance, company
        ))