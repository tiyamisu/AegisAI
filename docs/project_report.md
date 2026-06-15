# AegisAI — AI-Powered Human Trafficking Prevention and Victim Assistance Chatbot
## Complete Project Report

**Course**: Introduction to Artificial Intelligence
**Degree**: B.Tech (Computer Science and Engineering) — 2nd Year
**Project Title**: AegisAI — AI-Powered Human Trafficking Prevention and Victim Assistance Chatbot
**Version**: 1.0

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Description](#3-problem-description)
4. [Requirement Analysis](#4-requirement-analysis)
5. [System Architecture](#5-system-architecture)
6. [Knowledge Base Design](#6-knowledge-base-design)
7. [Expert System Design](#7-expert-system-design)
8. [Implementation](#8-implementation)
9. [Testing](#9-testing)
10. [Benefits](#10-benefits)
11. [Limitations](#11-limitations)
12. [Future Scope](#12-future-scope)
13. [Conclusion](#13-conclusion)
14. [References](#14-references)

---

## 1. Abstract

Human trafficking is a severe violation of human rights affecting millions of people globally, with India ranking among the most affected nations. Victims, family members, and concerned citizens often lack access to timely, reliable, and confidential guidance. AegisAI is an AI-powered chatbot and expert system designed to address this gap by providing interactive, accessible, and intelligent assistance in the domain of human trafficking prevention and victim support.

The system employs a **Rule-Based Expert System** with **Forward-Chaining Inference** to perform dynamic risk assessment, classify situational danger levels, and generate context-sensitive responses. A **Weighted Indicator Scam Analyzer** evaluates job offer descriptions for trafficking recruitment patterns using 110 NLP-driven indicators across 12 categories. The knowledge base contains **105 structured entries** spanning 13 thematic categories, covering everything from trafficking basics and warning signs to legal rights and emergency procedures.

Built entirely in Python using Object-Oriented Programming and a modular architecture, AegisAI features a modern dark-themed Tkinter graphical interface and a command-line mode. The system achieved a **50/50 (100%) test pass rate** across unit, integration, and user acceptance tests, demonstrating functional reliability and correctness across all core modules.

---

## 2. Introduction

### 2.1 Background

Human trafficking is defined by the United Nations as the recruitment, transportation, transfer, harbouring, or receipt of persons by means of threat, force, coercion, deception, or abuse of power for the purpose of exploitation. It is one of the world's most serious crimes. According to the International Labour Organization (ILO), approximately **40.3 million people** are victims of modern slavery globally, with forced labour accounting for 24.9 million and forced marriages for 15.4 million.

In India, the National Crime Records Bureau (NCRB) reports over 6,000 trafficking cases annually, though actual numbers are believed to be significantly higher due to underreporting. Victims include men, women, and children trafficked for sexual exploitation, forced labour, bonded labour, domestic servitude, and organ trafficking.

### 2.2 Motivation

Despite the severity of the problem, victims and at-risk individuals face multiple barriers:

- **Lack of awareness** — Many victims do not recognise they are being trafficked
- **Fear and isolation** — Traffickers deliberately isolate victims from support networks
- **Inaccessible resources** — Legal aid and NGO contacts are not widely known
- **Language and literacy barriers** — Formal resources are not always accessible
- **Stigma** — Victims may fear judgment when seeking help

An AI-powered chatbot can overcome these barriers by providing **anonymous, always-available, jargon-free guidance** in a conversational format.

### 2.3 Project Objectives

AegisAI aims to:

1. Educate users about human trafficking — types, signs, and statistics
2. Perform intelligent, interactive risk assessment using expert system inference
3. Detect and flag suspicious job offers and recruitment scams
4. Provide emergency guidance, helpline contacts, and escape strategies
5. Explain reporting procedures and legal rights
6. Connect users to verified NGOs and support organisations

### 2.4 Scope

AegisAI targets five user groups:

| User Group | Description |
|---|---|
| **Potential victims** | Individuals in or approaching dangerous situations |
| **Family members** | Concerned relatives of missing or at-risk persons |
| **Concerned citizens** | Bystanders who suspect trafficking |
| **NGO workers** | Professionals needing quick reference resources |
| **Students** | Learners seeking awareness about the issue |

---

## 3. Problem Description

### 3.1 The Human Trafficking Crisis

Human trafficking operates as the second-largest criminal industry globally after drug trafficking, generating an estimated **USD 150 billion** annually. In India:

| Metric | Figure |
|---|---|
| Annual registered trafficking cases | ~6,500 |
| Estimated actual victims (annual) | ~300,000+ |
| Child victims (% of total) | ~40% |
| Female victims (% of total) | ~70% |
| States with highest trafficking | West Bengal, Rajasthan, Odisha, Maharashtra |
| Common recruitment method | Fraudulent job offers (>60% of cases) |

### 3.2 Key Problem Statements

**Problem 1 — Awareness Gap**
A large proportion of trafficking victims are recruited through deceptive job offers. Many victims, especially from rural areas with limited education, cannot identify red flags. An AI system that analyses a job offer text and flags trafficking indicators directly addresses this gap.

**Problem 2 — Risk Recognition**
Individuals already in a dangerous situation often do not recognise it as trafficking. An interactive questionnaire driven by expert system rules helps them objectively assess their situation.

**Problem 3 — Resource Access**
Emergency helplines, NGO contacts, legal aid organisations, and reporting procedures are not widely known. An always-available chatbot centralises this information.

**Problem 4 — Reporting Barriers**
The formal complaint process is unfamiliar to most citizens. Step-by-step guidance reduces the intimidation of approaching authorities.

### 3.3 Existing Solutions and Gaps

| Existing Resource | Limitation |
|---|---|
| NHRC Helpline (14433) | Phone-only, not 24/7 interactive |
| Childline (1098) | Limited to children, not a knowledge resource |
| NGO websites | Passive information, no interactivity |
| Government portals | Complex navigation, legal jargon |
| General chatbots | Not specialised for the trafficking domain |

**AegisAI fills this gap** by combining an expert knowledge base, an intelligent inference engine, and a conversational interface specifically designed for the trafficking prevention domain.

---

## 4. Requirement Analysis

### 4.1 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR01 | Educational content on trafficking types, signs, and statistics | High |
| FR02 | Interactive risk assessment (15-question questionnaire) | High |
| FR03 | Risk classification: LOW / MEDIUM / HIGH / CRITICAL | High |
| FR04 | Analyse job offer text for scam indicators | High |
| FR05 | Emergency guidance and helpline contacts | Critical |
| FR06 | Reporting procedures (police, NHRC, cybercrime portal) | High |
| FR07 | Legal rights and victim protections | Medium |
| FR08 | NGO and rehabilitation resource directory | Medium |
| FR09 | Conversational natural language input | High |
| FR10 | Session state management across conversation | High |
| FR11 | Graphical user interface | Medium |
| FR12 | CLI mode for accessibility | Low |
| FR13 | Session reset on user request | Low |

### 4.2 Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR01 | Response time | < 1 second per query |
| NFR02 | Availability | Always-on (offline capable) |
| NFR03 | Privacy | No data storage, no network requests |
| NFR04 | Portability | Windows, Linux, macOS |
| NFR05 | Reliability | 100% test pass rate |
| NFR06 | Usability | Accessible to non-technical users |
| NFR07 | Maintainability | Modular OOP design |

### 4.3 AI Methodology Requirements

| Requirement | Choice | Justification |
|---|---|---|
| AI Paradigm | Rule-Based Expert System | Transparent, auditable, no training data required |
| Inference Method | Forward Chaining | Reasons from known facts to new conclusions |
| Knowledge Representation | IF-THEN Production Rules | Industry standard for expert systems |
| Risk Scoring | Weighted indicator scoring | Quantifiable, explainable output |
| NLP Approach | Keyword and pattern matching | Lightweight, no external ML dependencies |

### 4.4 Target User Stories

```
AS A potential victim,
  I WANT TO assess my situation confidentially
  SO THAT I know if I need help and how to get it.

AS A concerned family member,
  I WANT TO know the warning signs
  SO THAT I can protect my child or relative.

AS AN NGO worker,
  I WANT TO quickly access NGO contacts and legal info
  SO THAT I can guide survivors I work with.

AS A student,
  I WANT TO learn about human trafficking
  SO THAT I can be aware and help prevent it.
```

---

## 5. System Architecture

### 5.1 High-Level Architecture Diagram

```
+---------------------------------------------------------------+
|                      USER INTERFACES                          |
|                                                               |
|   +-------------------------+   +-------------------------+   |
|   |        gui.py           |   |   main.py --cli         |   |
|   |    (Tkinter GUI)        |   |   (Terminal Mode)       |   |
|   +----------+--------------+   +----------+--------------+   |
+--------------|-------------------------------|-----------------|
               |                               |
               v                               v
+-----------------------------------------------------------------+
|                   chatbot.py  (Core Orchestrator)               |
|                                                                 |
|      Intent Classifier  -->  Dispatcher  -->  Response Builder  |
|      Session State Manager (SessionState dataclass)             |
+------+----------+----------+----------+-----------------------+-+
       |          |          |          |
       v          v          v          v
+----------+ +----------+ +----------+ +----------+
|knowledge | |expert_   | |risk_asse | |scam_     |
|_base.py  | |system.py | |ssment.py | |detector  |
+----------+ +----------+ +----------+ +----------+
       |          |          |          |
       v          v          v          v
+----------+ +----------+ +----------+ +----------+
|data/     | |engine/   | |engine/   | |modules/  |
|knowledge | |expert_   | |expert_   | |scam_     |
|_base.py  | |system.py | |system.py | |analyzer  |
|(105 KB)  | |(52 rules)| |(15 Qs)   | |(110 ind) |
+----------+ +----------+ +----------+ +----------+
```

### 5.2 Module Descriptions

| Module | File | Responsibility |
|---|---|---|
| **KnowledgeBaseManager** | `knowledge_base.py` | KB loading, keyword/category/intent search, emergency lookup |
| **ExpertSystemEngine** | `expert_system.py` | Fact assertion, forward-chaining inference, risk classification |
| **RiskAssessmentModule** | `risk_assessment.py` | Questionnaire FSM, answer collection, score aggregation |
| **ScamDetector** | `scam_detector.py` | Job text NLP analysis, weighted scoring, report generation |
| **ChatBot** | `chatbot.py` | Intent classification, session state, module orchestration |
| **AegisAIApp** | `gui.py` | Tkinter GUI, chat bubbles, sidebar navigation, emergency UI |
| **Entry Point** | `main.py` | Mode selection (GUI / CLI / test), argument parsing |

### 5.3 Data Flow

```
User Input
    |
    v
ChatBot.process(input)
    |
    +--[Assessment active]--> RiskAssessmentModule.submit_answer()
    |                                  |
    |                                  v
    |                         ExpertSystemEngine.run_inference()
    |                                  |
    |                                  v
    |                         AssessmentResult (risk_level, actions)
    |
    +--[Job text pending]----> ScamDetector.analyze(text)
    |                                  |
    |                                  v
    |                         DetectionResult (level, flags, report)
    |
    +--[Normal query]---------> classify_intent(input)
                                       |
                                       v
                               KnowledgeBaseManager.query(input)
                                       |
                                       v
                               ChatResponse (text, risk_level, flags)
```

### 5.4 Design Patterns Used

| Pattern | Applied In | Purpose |
|---|---|---|
| **Facade** | `chatbot.py` | Single interface over 4 sub-modules |
| **Strategy** | Intent handlers | Each intent has a dedicated handler method |
| **State Machine** | `risk_assessment.py` | Assessment lifecycle (NOT_STARTED → IN_PROGRESS → COMPLETED) |
| **Dataclass Factory** | `SessionState` | Immutable-style fresh session state creation |
| **Observer / Callback** | `gui.py` threading | Background thread posts updates to main thread via `root.after()` |

---

## 6. Knowledge Base Design

### 6.1 Entry Schema

Each knowledge base entry is a Python dictionary with the following schema:

```python
{
    "id":           "KB001",             # Unique identifier
    "category":     "category_name",    # One of 13 categories
    "intent":       "specific_intent",  # Intent within category
    "keywords":     ["kw1", "kw2"],     # Matching keyword list
    "user_queries": ["Q1", "Q2"],       # Example user questions
    "response":     "Full response...", # Chatbot answer text
    "priority":     1,                  # 1=emergency, 2=high, 3=normal
    "tags":         ["tag1", "tag2"],   # Supplementary metadata
}
```

### 6.2 Categories and Entry Counts

| # | Category Key | Entries | Primary Topics |
|---|---|---|---|
| 1 | `human_trafficking_basics` | 10 | Definition, IPC 370, types, statistics |
| 2 | `warning_signs` | 9 | Control, deception, isolation, document seizure |
| 3 | `recruitment_scams` | 10 | Fake jobs, overseas fraud, modeling scams |
| 4 | `child_trafficking` | 8 | POCSO, Childline 1098, online child safety |
| 5 | `forced_labour` | 6 | Bonded labour, debt bondage, ILO standards |
| 6 | `online_grooming` | 7 | Social media, catfishing, sextortion |
| 7 | `victim_support` | 7 | Counselling, rehabilitation, survivor support |
| 8 | `emergency_assistance` | 8 | Escape plans, silent signals, shelter homes |
| 9 | `reporting_procedures` | 7 | FIR filing, NHRC, cybercrime.gov.in |
| 10 | `legal_rights` | 9 | ITPA, POCSO, IPC 370, victim compensation |
| 11 | `safety_measures` | 8 | Job verification, travel safety, online safety |
| 12 | `ngo_support` | 5 | IJM, ECPAT, Prerana, Shakti Vahini |
| 13 | `faqs` | 11 | Common questions and misconceptions |
| **Total** | | **105** | |

### 6.3 Three-Stage Query Pipeline

```
Stage 1: Emergency Keyword Detection
  - 7 emergency trigger words (danger, trapped, help me, etc.)
  - Immediately returns emergency_assistance response
  - Bypasses normal scoring

Stage 2: Keyword Scoring
  - score = matched_keywords / total_entry_keywords
  - All entries scored and sorted descending
  - Top-N results returned with confidence

Stage 3: Fallback
  - If max_score < threshold (0.10), return standard fallback menu
  - Invites user to browse categories
```

### 6.4 Performance Indexing

Two indices pre-built at load time for O(1) lookup:

| Index | Structure | Contents |
|---|---|---|
| `KEYWORD_INDEX` | `{keyword: [entry_id, ...]}` | 653 keywords across all entries |
| `CATEGORY_INDEX` | `{category: [entry_id, ...]}` | 13 category buckets |

---

## 7. Expert System Design

### 7.1 Component Architecture

| Component | Role |
|---|---|
| **Working Memory (WM)** | Stores all session facts — user flags, inferred conclusions, risk score |
| **Rule Base** | 52 IF-THEN production rules organised into 9 priority groups |
| **Inference Engine** | Forward-chaining algorithm with fixpoint termination |
| **Conflict Resolution** | Priority ordering — lowest number fires first |

### 7.2 Working Memory Facts

```python
# User-asserted facts (set by questionnaire answers)
"user_in_immediate_danger"    # bool — immediate life-threatening situation
"user_is_minor"               # bool — victim is under 18
"documents_confiscated"       # bool — ID/passport taken away
"freedom_restricted"          # bool — movement controlled
"threats_received"            # bool — threatened with force/violence
"wages_withheld"              # bool — not paid or wages stolen
"debt_bondage_present"        # bool — impossible debt imposed
"physical_abuse_present"      # bool — physically harmed
"isolated_from_family"        # bool — cut off from support network
"sexual_exploitation"         # bool — sexual coercion present
"cross_border_movement"       # bool — crossed state/national border
"online_contact_suspicious"   # bool — online recruiter involved

# Inferred facts (set by inference engine rules)
"risk_level"                  # str: LOW / MEDIUM / HIGH / CRITICAL
"risk_score"                  # int: accumulated weighted score
"trafficking_type_suspected"  # str: e.g. LABOUR_TRAFFICKING
"urgency"                     # int: 1-5 (ROUTINE to EMERGENCY)
"show_emergency_contacts"     # bool: display flag
"show_escape_plan"            # bool: display flag
"show_legal_aid_info"         # bool: display flag
"show_child_protection_info"  # bool: display flag
```

### 7.3 Rule Base Summary (52 Rules)

| Section | Rule IDs | Description |
|---|---|---|
| Emergency Detection | R001–R005 | Immediate danger → CRITICAL + EMERGENCY urgency |
| Control & Coercion | R006–R015 | Scoring for each control indicator |
| Recruitment Scams | R016–R021 | Job fraud + overseas posting patterns |
| Risk Classification | R022–R025 | Score thresholds → risk level assignment |
| Low Risk Rules | R026–R030 | Safe scenario — educational guidance |
| Medium Risk Rules | R031–R036 | Caution scenario — helpline + job check |
| High Risk Rules | R037–R042 | Danger scenario — emergency contacts + legal aid |
| Critical Risk Rules | R043–R047 | Emergency scenario — escape plan + immediate call |
| Resource Recommendations | R048–R052 | Post-assessment info routing |

### 7.4 Sample Production Rules

```
R001: IF   user_in_immediate_danger = TRUE
      THEN risk_level       ← CRITICAL
           urgency          ← EMERGENCY (5)
           risk_score       += 100
           show_emergency_contacts ← TRUE
           show_escape_plan        ← TRUE
      Priority: 1  (fires first)

R010: IF   debt_bondage_present = TRUE
      THEN risk_score                  += 20
           trafficking_type_suspected  ← BONDED_LABOUR
           show_bonded_labour_rights   ← TRUE
      Priority: 10

R025: IF   risk_assessment_complete = TRUE
       AND risk_score >= 100
      THEN risk_level             ← CRITICAL
           show_emergency_guidance ← TRUE
           urgency                 ← EMERGENCY
      Priority: 25

R043: IF   risk_level = CRITICAL
       AND user_is_minor = TRUE
      THEN show_child_protection_info ← TRUE
           show_childline_priority    ← TRUE
      Priority: 43
```

### 7.5 Risk Classification Table

| Score Range | Risk Level | Urgency Level | Primary Bot Response |
|---|---|---|---|
| 0 – 20 | 🟢 LOW | ROUTINE (1) | Educational resources, safety tips |
| 21 – 50 | 🟡 MEDIUM | ADVISORY (2) | Helplines, caution advice, job scam check |
| 51 – 99 | 🔴 HIGH | URGENT (4) | Emergency contacts, legal aid, escape plan |
| 100+ | 🚨 CRITICAL | EMERGENCY (5) | Call 100 / 1098 NOW, immediate escape guide |

### 7.6 Forward-Chaining Inference Algorithm

```
ALGORITHM ForwardChain(WorkingMemory WM, RuleBase RB)
  INPUT  : WM  -- initial set of user-asserted facts
  OUTPUT : WM  -- enriched with all inferred conclusions

  cycle ← 0
  REPEAT
    fired_any ← FALSE
    FOR EACH rule R in RB sorted ascending by priority:
      IF (R.fired = FALSE) AND (R.condition(WM) = TRUE):
        R.action(WM)       // assert new facts into working memory
        R.fired ← TRUE
        fired_any ← TRUE
    cycle ← cycle + 1
  UNTIL (fired_any = FALSE) OR (cycle ≥ MAX_CYCLES)

  RETURN WM

Termination guarantee: Fixpoint — algorithm halts when no rule
fires in a complete pass through the rule base (or safety cap hit).
```

### 7.7 Risk Assessment Questionnaire (Branching)

```
RQ01  Freedom restricted?        --Yes--> RQ01a: Threats used to control?
RQ02  Deception used?            --Yes--> RQ02a: Conditions differ from promise?
RQ03  Documents confiscated?
RQ04  Wages withheld?            --Yes--> RQ04a: Debt bondage present?
RQ05  Physical abuse present?
RQ06  Isolated from family?
RQ07  Sexual exploitation?
RQ08  In immediate danger?
RQ09  Transported here?          --Yes--> RQ09a: Crossed border?
RQ10  Online contact involved?
RQ11  Children in same situation?

Total: 11 root questions + 4 conditional follow-ups = 15 questions
```

---

## 8. Implementation

### 8.1 Technology Stack

| Component | Technology | Justification |
|---|---|---|
| Core Language | Python 3.8+ | Cross-platform, readable, standard for AI courses |
| GUI Framework | Tkinter (stdlib) | No installation required, cross-platform |
| Testing Framework | unittest (stdlib) | Standard Python testing library |
| OOP Constructs | dataclasses, Enum | Clean, type-safe data modelling |
| NLP Engine | re, string (stdlib) | Zero-dependency pattern matching |
| **External Dependencies** | **None** | Runs on bare Python installation |

### 8.2 Complete File Structure

```
AegisAI/
|
|-- main.py              Entry point: GUI, CLI, and --test mode
|-- chatbot.py           Core orchestrator: intent, session, dispatch
|-- knowledge_base.py    KB API layer: query, categories, emergency
|-- expert_system.py     Expert system API: facts, inference, results
|-- risk_assessment.py   Questionnaire FSM: question flow, scoring
|-- scam_detector.py     Scam detector API: analyze, report, Q&A mode
|-- gui.py               Tkinter GUI: dark theme, chat bubbles, sidebar
|-- requirements.txt     Dependency list (colorama optional)
|
|-- data/
|   |-- knowledge_base.py   105 KB entries (13 categories)
|   `-- __init__.py
|
|-- engine/
|   |-- expert_system.py    52 IF-THEN rules + inference engine
|   `-- __init__.py
|
|-- modules/
|   |-- scam_analyzer.py    110 scam indicators + weighted scoring
|   `-- __init__.py
|
|-- tests/
|   |-- test_suite.py       50 tests: Unit + Integration + UAT
|   `-- __init__.py
|
`-- docs/
    `-- project_report.md   This document
```

### 8.3 Key Implementation Highlights

#### A — Intent Classification (`chatbot.py`)

Three-tier classifier (priority order):

```python
1. Exact match:      "menu", "1"–"15" → direct Intent mapping
2. Pattern match:    22 intent × keyword lists, priority-ordered
3. KB fallback:      confidence threshold = 0.2
```

#### B — Session State Machine (`risk_assessment.py`)

```
                  start()
NOT_STARTED  ──────────────────►  WAITING_INPUT
                                       │
                                  submit_answer()
                                       │
                            ┌──────────┴──────────┐
                    [more Qs left]         [queue exhausted]
                            │                      │
                      WAITING_INPUT           COMPLETED
                            │
                         abort()
                            │
                        ABORTED
```

#### C — Scam Scoring Formula (`modules/scam_analyzer.py`)

```
suspicion_pct = min((raw_score / REFERENCE_CAP) × 100,  100.0)

REFERENCE_CAP = 60  (calibrated against a typical scam advertisement)

Level thresholds:
  0  – 15%   →  SAFE
  16 – 35%   →  LOW_RISK
  36 – 55%   →  MODERATE_RISK
  56 – 75%   →  HIGH_RISK
  76% – 100% →  VERY_HIGH
```

#### D — GUI Threading (`gui.py`)

All chatbot processing runs in a **daemon background thread** to keep the UI responsive:

```python
def _on_send(self):
    thread = threading.Thread(
        target=self._process_in_thread, daemon=True
    )
    thread.start()

def _process_in_thread(self, user_text):
    response = self._bot.process(user_text)           # runs in background
    self._root.after(0, lambda: self._handle_response(response))  # back to main
```

### 8.4 OOP Class Hierarchy

```
ChatBot
├── KnowledgeBaseManager    query(), get_emergency_response(), get_stats()
├── ExpertSystemEngine      assert_fact(), run_inference(), quick_assess()
│   └── _CoreSession        (engine/expert_system.py — inner engine)
├── RiskAssessmentModule    start(), submit_answer(), get_result()
│   └── ExpertSystemEngine
└── ScamDetector            analyze(), analyze_from_qa(), format_report()
    └── _CoreAnalyzer       (modules/scam_analyzer.py — inner engine)

AegisAIApp   (Tkinter GUI root)
└── ChatBot
```

---

## 9. Testing

### 9.1 Testing Strategy

AegisAI uses a three-tier testing approach aligned with industry best practices:

| Tier | Test IDs | Count | What is Tested |
|---|---|---|---|
| **Unit Testing** | TC01–TC41 | 41 | Individual methods in each module |
| **Integration Testing** | TC42–TC46 | 5 | Data flow between modules |
| **User Acceptance Testing** | TC47–TC50 | 4 | Complete real-world user scenarios |
| **TOTAL** | TC01–TC50 | **50** | Full system coverage |

### 9.2 Final Test Results

| Group | Module | Tests | Passed | Failed | Pass Rate |
|---|---|---|---|---|---|
| A | Knowledge Base Manager | 10 | 10 | 0 | **100%** |
| B | Expert System Engine | 8 | 8 | 0 | **100%** |
| C | Risk Assessment Module | 8 | 8 | 0 | **100%** |
| D | Scam Detector | 8 | 8 | 0 | **100%** |
| E | ChatBot Engine | 7 | 7 | 0 | **100%** |
| F | Integration Tests | 5 | 5 | 0 | **100%** |
| G | User Acceptance Tests | 4 | 4 | 0 | **100%** |
| **GRAND TOTAL** | | **50** | **50** | **0** | **100%** |

### 9.3 Complete Test Case Table

| TC# | Test Description | Input / Scenario | Expected Result | Status |
|---|---|---|---|---|
| TC01 | KB loads without error | Module import | No exception raised | PASS |
| TC02 | KB has entries | total_entries() | count >= 0 | PASS |
| TC03 | query() returns list | Any string | List type | PASS |
| TC04 | Trafficking basics query | "what is human trafficking" | Non-empty string | PASS |
| TC05 | Emergency response is string | get_emergency_response() | len > 20 | PASS |
| TC06 | Emergency contains helpline | Emergency response text | Contains 100/1098/112 | PASS |
| TC07 | Fallback is string | get_fallback() | len > 10 | PASS |
| TC08 | Category query returns list | "emergency_assistance" | List type | PASS |
| TC09 | Stats returns dict | get_stats() | Dict with expected keys | PASS |
| TC10 | List categories | list_categories() | Contains "emergency" | PASS |
| TC11 | New session resets state | new_session() | last_result = None | PASS |
| TC12 | Assert fact no crash | fact = True | No exception | PASS |
| TC13 | Immediate danger → HIGH+ | danger=True | HIGH or CRITICAL | PASS |
| TC14 | No flags → LOW | {} empty dict | LOW or UNKNOWN | PASS |
| TC15 | Multiple flags → HIGH+ | 5 control flags True | HIGH or CRITICAL | PASS |
| TC16 | Result has required fields | quick_assess({danger:True}) | All fields populated | PASS |
| TC17 | Sexual exploitation escalates | exploit=True | MEDIUM or higher | PASS |
| TC18 | Format banner returns string | quick_assess() result | Contains "RISK" | PASS |
| TC19 | Initial state NOT_STARTED | Module created | NOT_STARTED state | PASS |
| TC20 | start() activates session | start() called | is_active() = True | PASS |
| TC21 | abort() deactivates | start() then abort() | is_active() = False | PASS |
| TC22 | First question after start | start() called | question != None | PASS |
| TC23 | Answer advances question | submit_answer(False) | Next question differs | PASS |
| TC24 | Yes increments yes_count | submit_answer(True) | yes_count > 0 | PASS |
| TC25 | All No → LOW risk | All answers = False | LOW or UNKNOWN | PASS |
| TC26 | Progress pct valid range | During assessment | 0.0 ≤ pct ≤ 100.0 | PASS |
| TC27 | ScamDetector loads | Module import | No exception | PASS |
| TC28 | Empty input no crash | analyze("") | Result != None | PASS |
| TC29 | Legit job → not HIGH+ | Legitimate software job text | NOT HIGH_RISK/VERY_HIGH | PASS |
| TC30 | Trafficking scam → HIGH+ | Classic scam advertisement | HIGH_RISK or VERY_HIGH | PASS |
| TC31 | Result has required fields | analyze("sample text") | All fields present | PASS |
| TC32 | Report format is string | format_report(result) | len > 20 | PASS |
| TC33 | Pct always 0–100 | 3 diverse inputs | 0 ≤ pct ≤ 100 each | PASS |
| TC34 | Q&A mode analysis works | 5 Yes answers dict | NOT SAFE level | PASS |
| TC35 | ChatBot initialises | ChatBot() created | No exception | PASS |
| TC36 | Greeting returns response | "hello" | len > 10, is string | PASS |
| TC37 | Emergency sets flag | "emergency" | is_emergency = True | PASS |
| TC38 | Welcome message content | get_welcome_message() | Contains "AegisAI" + features | PASS |
| TC39 | Risk assessment activates | "risk assessment" | "assessment" in response | PASS |
| TC40 | Empty input handled | "" (empty string) | No exception raised | PASS |
| TC41 | Job analysis triggers | "check job offer" | Job keywords in response | PASS |
| TC42 | Full assessment flow E2E | Assessment → all No | Risk level assigned | PASS |
| TC43 | Job analysis E2E | Trigger → scam text | Non-empty response text | PASS |
| TC44 | KB and expert consistent | "I need help now" | Helpline numbers present | PASS |
| TC45 | Session reset clears state | Multi-step + reset() | risk=UNKNOWN, count=0 | PASS |
| TC46 | Scam detector integrates | Trigger → scam text | len(response) > 50 | PASS |
| TC47 (UAT) | Victim in immediate danger | 3 emergency phrases | Emergency response + flag | PASS |
| TC48 (UAT) | Student learning | 3 educational queries | Informative, no emergency | PASS |
| TC49 (UAT) | NGO reporting guidance | Reporting query | Reporting keywords present | PASS |
| TC50 (UAT) | Job seeker suspicious offer | Trigger + suspicious job | Warning/danger response | PASS |

### 9.4 How to Run the Tests

```bash
# All 50 tests — standalone colour runner
python tests/test_suite.py

# With pytest (if installed)
python -m pytest tests/test_suite.py -v

# Module self-tests only
python main.py --test
```

---

## 10. Benefits

### 10.1 Social Impact

| Benefit | Description |
|---|---|
| **24/7 Availability** | Assistance at any time — no waiting, no appointments |
| **Anonymous Access** | No login, no data stored — victims feel safe to use it |
| **Plain Language** | Conversational interface — no legal jargon or complex navigation |
| **Centralised Resource** | One tool: education + risk check + scam detection + emergency + legal |
| **Empowering Information** | Users gain knowledge and tools to protect themselves and others |
| **Offline Operation** | Works without internet — usable in low-connectivity rural areas |

### 10.2 Technical Benefits

| Benefit | Description |
|---|---|
| **Transparent AI** | Every decision is rule-based and fully explainable |
| **No External Dependencies** | Pure Python stdlib — trivial to install and deploy |
| **Modular OOP Design** | Each module independently replaceable and testable |
| **Extensible KB** | New knowledge added without touching application code |
| **Scalable Rule Base** | New expert rules added without disrupting existing inference |
| **Verified Correctness** | 100% test pass rate across 50 independent test cases |

### 10.3 Academic Contribution

The project demonstrates the practical application of key AI course concepts:

| AI Concept | Application in AegisAI |
|---|---|
| Expert Systems | Core reasoning engine with 52 production rules |
| Forward Chaining | Dynamic inference from user facts to risk conclusions |
| Knowledge Representation | IF-THEN rules + structured KB schema |
| NLP | Pattern matching for intent classification and scam detection |
| Finite State Machines | Session lifecycle management (NOT_STARTED → COMPLETED) |
| Weighted Scoring | Multi-factor decision making with transparent score formula |
| Search and Matching | Keyword index lookup for KB retrieval |

---

## 11. Limitations

| # | Limitation | Impact | Proposed Mitigation |
|---|---|---|---|
| L01 | English-only interface | Excludes non-English speakers | Future: multilingual KB translation |
| L02 | Keyword-based NLP, no ML | May miss paraphrased queries | Expanded synonym lists; future BERT layer |
| L03 | Static knowledge base | Cannot auto-update with new cases | Scheduled manual KB reviews |
| L04 | No user authentication | Cannot track returning users | Privacy-by-design — intentional choice |
| L05 | Text input only | Cannot process images or audio | Future: OCR, voice-to-text integration |
| L06 | No live data feeds | Cannot show real-time news or alerts | Future: API integration with government portals |
| L07 | Rule-based limits | Cannot generalise to completely unseen patterns | Future: hybrid rule + ML approach |
| L08 | Tkinter GUI | Less polished than modern web apps | Future: web or mobile frontend |
| L09 | Windows CLI encoding | Special chars require UTF-8 flag | Documented workaround provided |

---

## 12. Future Scope

### 12.1 Short-Term Enhancements (3–6 months)

1. **Multilingual Support** — Hindi, Bengali, Tamil, Telugu KB translation layers
2. **Voice Interface** — Speech-to-text input using `speech_recognition` library
3. **Web Interface** — Flask/FastAPI backend with React or Vue.js frontend
4. **PDF Safety Report** — Exportable personalised safety plan after assessment
5. **Expanded KB** — Scale from 105 to 500+ entries with state-specific data

### 12.2 Medium-Term Enhancements (6–12 months)

1. **Machine Learning Intent Layer** — BERT/DistilBERT for improved NLP accuracy
2. **Mobile Application** — Android/iOS app using Flutter or React Native
3. **Real-Time Alerts** — Integration with police missing person databases
4. **Live NGO Directory** — API integration with registered NGO databases
5. **Encrypted Case References** — Local follow-up tracking without storing PII

### 12.3 Long-Term Vision (1–2 years)

1. **Federated Learning** — Train NLP model on anonymised case data (privacy-safe)
2. **Image Analysis** — OCR + CV to detect trafficking indicators in scanned job ads
3. **Social Media Monitoring** — Public-post flagging for trafficking-related content
4. **Government API Integration** — Direct FIR filing via NCRB/eCitizen portal
5. **AI-Moderated Survivor Network** — Peer support chat with AI safety guardrails

---

## 13. Conclusion

AegisAI demonstrates that Artificial Intelligence — specifically Rule-Based Expert Systems with Forward-Chaining Inference — can be meaningfully applied to address one of the most serious human rights violations of our time.

The project delivers a complete, fully verified implementation that:

- **Educates** through 105 structured knowledge base entries across 13 categories
- **Assesses** individual risk using a 52-rule inference engine with dynamic forward chaining
- **Detects** recruitment scams through 110 weighted NLP indicators
- **Guides** victims and citizens with actionable, contextually appropriate responses
- **Connects** users to emergency helplines, legal resources, and NGO support

The system achieves a **100% test pass rate (50/50 tests)** across unit, integration, and user acceptance levels — demonstrating production-quality reliability for an academic project.

The modular OOP architecture ensures that knowledge, rules, and modules can be extended independently, making AegisAI a maintainable and scalable foundation for future development.

Most importantly, every design decision in AegisAI is made with the safety and dignity of real human beings at its core — from the anonymous session model to the non-judgmental conversational tone, from the emergency flash indicator to offline availability. AegisAI is not just a software project; it is a social responsibility tool built with the hope that it might, in some way, help protect vulnerable lives.

---

## 14. References

### 14.1 Artificial Intelligence and Computer Science

1. Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson Education. *(Expert Systems — Chapter 8; Forward Chaining — Chapter 7)*

2. Giarratano, J. & Riley, G. (2005). *Expert Systems: Principles and Programming* (4th ed.). Thomson Course Technology.

3. Jurafsky, D. & Martin, J. H. (2023). *Speech and Language Processing* (3rd draft). Stanford University. Retrieved from https://web.stanford.edu/~jurafsky/slp3/

4. Jackson, P. (1998). *Introduction to Expert Systems* (3rd ed.). Addison Wesley Longman.

5. Nilsson, N. J. (1998). *Artificial Intelligence: A New Synthesis*. Morgan Kaufmann Publishers.

### 14.2 Human Trafficking — Global Reports

6. International Labour Organization (2022). *Global Estimates of Modern Slavery: Forced Labour and Forced Marriage*. ILO, Geneva.

7. United Nations Office on Drugs and Crime (2022). *Global Report on Trafficking in Persons 2022*. United Nations, Vienna.

8. National Crime Records Bureau (2022). *Crime in India 2022 — Statistical Tables*. Ministry of Home Affairs, Government of India, New Delhi.

### 14.3 Indian Government and Policy

9. Ministry of Home Affairs, India (2020). *Standard Operating Procedure (SOP) for Prevention, Rescue, and Rehabilitation of Trafficked Victims*. Government of India.

10. National Human Rights Commission (2018). *A Handbook for Law Enforcement Agencies on Anti-Human Trafficking*. NHRC, New Delhi.

### 14.4 Legislation

11. Government of India (2012). *The Protection of Children from Sexual Offences (POCSO) Act, 2012*. Ministry of Women and Child Development.

12. Government of India (2013). *The Criminal Law (Amendment) Act, 2013* — Section 370 and 370A Indian Penal Code (Trafficking of Persons).

13. Government of India (1956, amended 2008). *The Immoral Traffic (Prevention) Act, 1956 — Amendment 2008* (ITPA).

### 14.5 Online Resources

14. National Human Rights Commission India. https://nhrc.nic.in

15. Childline India Foundation. https://www.childlineindia.org *(Helpline: 1098)*

16. Ministry of Home Affairs — Cyber Crime Portal. https://cybercrime.gov.in *(Helpline: 1930)*

17. Ministry of External Affairs — Emigrate Portal. https://emigrate.gov.in *(Overseas job verification)*

18. Python Software Foundation. (2024). *Python 3 Documentation — tkinter, unittest, dataclasses*. https://docs.python.org/3/

---

> **Confidentiality Note**: AegisAI stores no personal user data. All conversations are session-local and erased on exit.
>
> **Emergency Contacts**: Police — 100 | Childline — 1098 | National Emergency — 112 | Women's Helpline — 1091

---

*Report prepared for academic submission.*
*AegisAI Project | Introduction to Artificial Intelligence | B.Tech CSE — 2nd Year*
