# Task 2 Analysis – College Placement Eligibility Assistant

## Scenario

This project uses private college placement eligibility data to compare a chatbot, rule-based workflow, and AI agent.

### Private Data

- Minimum CGPA: 7.0
- No active backlogs
- Minimum attendance: 75%

### Company Requirements

- Company A: CGPA >= 7.5
- Company B: CGPA >= 7.0
- Company C: CGPA >= 8.0

---

## 1. Chatbot

The chatbot uses an LLM to answer questions using the provided private placement information.

It is flexible in understanding natural-language questions but does not independently execute tools or perform a controlled decision process.

---

## 2. Rule-Based Workflow

The workflow uses predefined Python rules to check eligibility.

It produces deterministic results and is reliable for known input conditions, but changes to the rules require code changes.

---

## 3. AI Agent

The AI agent uses:

**LLM + Tools + Loop**

The agent decides when it needs eligibility information, selects the appropriate tool, receives the tool result, and then produces the final answer.

---

## Comparison

| Feature | Chatbot | Workflow | Agent |
|---|---|---|---|
| Flexibility | High | Low | High |
| Decision-making | LLM response | Fixed rules | Dynamic |
| Tool usage | No | Direct code | LLM-selected tools |
| Private-data access | Prompt-based | Direct | Through tools |
| Multi-step handling | Limited | Predefined | Dynamic |
| Automation | Medium | High | High |
| Reliability | Depends on LLM | High for defined rules | Depends on tools + LLM |

---

## Suitability

### Chatbot
Suitable for answering general questions about placement rules.

### Workflow
Suitable when placement rules are fixed and deterministic.

### Agent
Suitable when students ask varied questions and the system needs to select tools and perform multiple steps dynamically.

---

## Conclusion

The three approaches solve the same type of problem differently.

A chatbot mainly generates responses.

A workflow follows predefined rules.

An AI agent combines an LLM with tools and an execution loop to dynamically handle multi-step tasks.