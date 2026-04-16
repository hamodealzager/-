---
name: learning-domain-research
description: Build end-to-end learning plans for any user-selected domain and continuously enrich answers with broad internet research. Use when users ask to learn a field/topic from scratch or intermediate level, request study roadmaps, want many curated resources, or need deep Q&A grounded in up-to-date web sources.
---

# Learning Domain Research

Provide a complete learning experience for any chosen domain by combining structured teaching with broad web research.

## Core Workflow

1. **Confirm learning target and profile**
   - Ask for: target domain, current level, available time, preferred language, and goal (job, exam, project, general knowledge).
   - If user gives limited details, infer a reasonable default and continue.

2. **Map the domain into a learning tree**
   - Break topic into:
     - Foundations
     - Core subdomains
     - Practical skills
     - Advanced/specialized paths
   - Represent as progressive levels (Beginner → Intermediate → Advanced).

3. **Perform broad web research for each major node**
   - Use internet search for every major subtopic.
   - Prioritize primary sources first (official docs, standards, university/open course pages, major books, reputable institutions).
   - Add secondary explainers only after primary sources.
   - Prefer recent sources for fast-changing topics.

4. **Build a practical study plan**
   - Produce a time-based plan (for example: 4/8/12 weeks based on user timeline).
   - Include weekly outcomes, daily tasks, and mini-projects.
   - Pair each module with 2–5 references (reading, video, exercises, datasets/tools).

5. **Deliver high-value teaching output**
   - Explain concepts in simple language first, then deeper technical detail.
   - Add examples, analogies, and common mistakes.
   - Include self-check quizzes and practice prompts.

6. **Maintain a research-backed Q&A loop**
   - For follow-up questions, search web again when freshness matters.
   - Compare multiple sources before finalizing answers.
   - Explicitly flag uncertainty and show best-supported conclusion.

## Output Template

Use this structure unless the user requests another format:

1. **Learning Goal Summary**
2. **Domain Roadmap (tiered tree)**
3. **Step-by-Step Curriculum**
4. **Top Curated Resources by Module**
5. **Hands-on Projects and Practice**
6. **Common Pitfalls**
7. **Progress Evaluation Checklist**
8. **Next Questions the Learner Should Ask**

## Research Quality Rules

- Search with varied query forms (overview, syllabus, best resources, official docs, roadmap, exercises).
- Cross-check important claims with at least two credible sources.
- Prefer direct links over generic mentions.
- Avoid over-reliance on one website.
- Distinguish stable facts from fast-changing information.

## Personalization Rules

- Adapt depth and pace to user level.
- If user is beginner, avoid jargon-first explanations.
- If user is advanced, prioritize depth, benchmarks, and cutting-edge material.
- Suggest low-cost/free options when budget is unknown.

## Reference File

- For reusable prompt/query patterns, read `references/research-playbook.md`.
