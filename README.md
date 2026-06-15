<div align="center">

<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/CustomTkinter-5.2%2B-F59E0B?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-Persistence-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Tests-50%20Passing-10B981?style=for-the-badge"/>

# 🛡️ AegisAI
### AI-Powered Human Trafficking Prevention & Victim Assistance Platform

*A rule-based expert system desktop application built for awareness, risk assessment, scam detection, and emergency guidance — designed as a university final year project.*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Expert System Design](#-expert-system-design)
- [Database Schema](#-database-schema)
- [Test Suite](#-test-suite)
- [Design System](#-design-system)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

**AegisAI** is a desktop chatbot application designed to combat human trafficking through AI-assisted awareness, real-time risk evaluation, and victim support. Built entirely in Python using a **rule-based forward-chaining expert system**, it operates fully offline — ensuring the privacy of potentially vulnerable users.

The platform simulates a knowledgeable assistant that can:
- Educate users on the signs, types, and realities of human trafficking
- Run a guided 15-question risk assessment and produce a detailed report
- Detect red flags in suspicious job offers using 110+ scam indicators
- Provide emergency helplines and step-by-step escape guidance

> **Academic Context:** This project was developed as a final-year university project, demonstrating applied AI techniques including expert systems, forward chaining inference, and knowledge base management.

---

## ✨ Features

### 🤖 AI Chat Assistant
- Natural language intent classification using keyword-pattern matching
- Conversational responses drawn from a structured knowledge base (105 entries)
- Context-aware replies with topic suggestions
- Animated typing indicator and auto-scrolling message history
- Quick-action chips for common queries
- Full chat history persisted across sessions (SQLite)

### 🛡️ Risk Assessment Wizard
- **15-question guided wizard** across **6 thematic steps**:
  1. Personal Safety
  2. Work Situation
  3. Recruitment & Travel
  4. Financial Control
  5. Online Safety
  6. Relationships
- Live risk gauge that updates after every answer
- Final report with: risk score, percentage, personalised summary, and recommendations
- Results classified into 5 levels: Unknown → Low → Medium → High → Critical

### 🔍 Scam Job Offer Analyzer
- Paste any job advertisement or recruitment message
- Detects 110+ red-flag indicators (unrealistic salary, document confiscation, vague location, etc.)
- Returns: suspicion percentage, level classification, red-flag chips, and advice
- Recent scan history log with one-click reload

### 📚 Awareness Center
- 13 browsable topic cards covering:
  - Trafficking Basics, Warning Signs, Recruitment Scams
  - Child Trafficking, Forced Labour, Online Grooming
  - Victim Support, Legal Rights, NGO Support, FAQs, and more
- Dynamic content loaded from the knowledge base

### 🆘 Emergency Help Page
- 8 emergency helplines (Police 100, National 112, Childline 1098, Women's Helpline 1091, etc.)
- Click-to-copy phone numbers
- 7-step safe escape plan with visual step-number badges

### 📁 Resources & Guidance
- 4 expandable accordion sections:
  - ⚖️ Legal Rights (IPC 370, POCSO, ITPA, Victim Compensation)
  - 📝 How to Report (FIR, NHRC, Cybercrime Portal, CWC)
  - 🏥 NGO Support (IJM, Prerana, Shakti Vahini, ECPAT)
  - 🔒 Online Safety (Job verification, social media, travel tips)

---

## 🖼️ Screenshots

> The application uses a warm **Navy + Amber** professional theme.

| Dashboard + Chat | Risk Assessment Wizard |
|---|---|
| Compact hero section + stat cards + embedded AI chat | 6-step guided wizard with live risk gauge |

| Scam Analyzer | Emergency Help |
|---|---|
| Paste-and-analyze job offer scanner | High-visibility helplines + escape plan |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   AegisAI Application               │
│                                                     │
│  ┌──────────┬──────────────────────────────────┐   │
│  │ SIDEBAR  │        CONTENT AREA              │   │
│  │  190px   │    (Dynamic Page Frames)         │   │
│  │          │                                  │   │
│  │ • Nav    │  Dashboard / Awareness /         │   │
│  │   Items  │  Assessment / Scam Analyzer /    │   │
│  │ • Brand  │  Emergency / Resources           │   │
│  └──────────┴──────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐   │
│  │         HEADER  (52px)                       │   │
│  │  🛡️ AegisAI  ›  [Page]  [Risk Badge] [SOS]  │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Design Patterns Used

| Pattern | Where Used |
|---|---|
| **Singleton** | `SessionService` — global application state |
| **Observer** | `on_risk_change()`, `on_navigate()` callbacks |
| **Strategy** | `IntentService` — swappable intent classifiers |
| **Factory** | Page instantiation in `app_window.py` |
| **Repository** | `DatabaseService` — all SQLite access |
| **MVC** | Models (`models/`), Services (controllers), Pages (views) |

### Data Flow

```
User Input
    │
    ▼
IntentService (keyword classification)
    │
    ├──► ChatService ──► KBManager (knowledge base lookup)
    │                         │
    │                         ▼
    │                    RuleEngine (52 rules, forward chaining)
    │                         │
    │                         ▼
    │                    ExpertSystem (inference + conclusions)
    │
    ├──► AssessmentService ──► 15 questions ──► AssessmentResult
    │
    └──► ScamService ──► 110 indicators ──► DetectionResult

All results ──► SessionService (state) ──► DatabaseService (SQLite)
                      │
                      ▼
                Header Badge / Risk Gauge / UI Update
```

---

## 📁 Project Structure

```
AegisAI/
│
├── main.py                    # Entry point (--test / --debug flags)
├── requirements.txt           # Python dependencies
├── .gitignore
│
├── models/                    # Pure data classes (no logic)
│   ├── assessment.py          # RiskLevel enum, AssessmentQuestion, AssessmentResult
│   ├── message.py             # ChatMessage, MessageRole
│   ├── scam.py                # DetectionResult, SuspicionLevel
│   └── session.py             # AppSession state dataclass
│
├── knowledge/                 # Knowledge representation layer
│   ├── kb_manager.py          # KBManager — loads & queries 105 KB entries
│   └── rule_engine.py         # RuleEngine — wraps ExpertSystem, exposes query API
│
├── engine/                    # Core AI inference engine
│   └── expert_system.py       # Forward-chaining rule engine (52 rules, 15 questions)
│
├── services/                  # Business logic / application layer
│   ├── session_service.py     # Singleton state hub + observer callbacks
│   ├── chat_service.py        # Processes chat messages, routes to KB/engine
│   ├── assessment_service.py  # Wizard flow: start → answer → result
│   ├── scam_service.py        # Scam detection + history retrieval
│   ├── intent_service.py      # NLP intent classification (Strategy pattern)
│   └── database_service.py    # SQLite CRUD (sessions, chat, assessments, scams)
│
├── ui/                        # Presentation layer (CustomTkinter)
│   ├── theme.py               # Design tokens: colors, fonts, spacing
│   ├── app_window.py          # Root window, layout, page routing
│   ├── components/
│   │   ├── sidebar.py         # Navigation sidebar (190px, amber active states)
│   │   ├── header.py          # Breadcrumb header + risk badge + SOS button
│   │   ├── chat_widget.py     # Full chat panel: bubbles, chips, typing indicator
│   │   ├── stat_card.py       # KPI metric card (icon + value + accent stripe)
│   │   └── risk_badge.py      # Coloured risk level pill badge
│   └── pages/
│       ├── dashboard.py       # Hero + stat cards + embedded chat
│       ├── awareness.py       # 13-topic card grid + detail panel
│       ├── assessment.py      # 6-step wizard + live gauge + result report
│       ├── scam_analyzer.py   # Paste-and-analyze + history log
│       ├── emergency.py       # Helplines + escape plan
│       └── resources.py       # Accordion legal/NGO/safety reference
│
├── utils/
│   ├── logger.py              # Logging configuration
│   └── threading_utils.py     # Background task helpers
│
├── tests/
│   └── test_suite.py          # 50 automated test cases (7 test classes)
│
├── data/
│   └── knowledge_base.py      # Raw KB data (105 entries across 13 categories)
│
└── docs/
    └── project_report.md      # Academic project report
```

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.10+ |
| GUI Framework | CustomTkinter | ≥ 5.2.2 |
| Theme Detection | darkdetect | ≥ 0.8.0 |
| Database | SQLite 3 | stdlib |
| AI Engine | Rule-Based Expert System | Custom |
| Concurrency | `threading` + `root.after()` | stdlib |
| Testing | `unittest` | stdlib |

> **No external AI APIs.** AegisAI runs entirely offline using a hand-crafted rule base and knowledge base — making it safe and private for vulnerable users.

---

## 🚀 Installation

### Prerequisites
- Python **3.10 or higher**
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/tiyamisu/AegisAI.git
cd AegisAI

# 2. (Recommended) Create a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the application
python main.py
```

### Optional Flags

```bash
# Run the full automated test suite
python main.py --test

# Enable debug-level logging
python main.py --debug
```

---

## 📖 Usage

### Launching the App
```
python main.py
```
The GUI opens at **1280×780px** (minimum 960×640px, fully resizable).

### Navigation
Use the **left sidebar** to switch between the 6 sections:

| Section | Description |
|---|---|
| 🏠 Dashboard | Chat with the AI assistant |
| 📚 Awareness | Browse 13 educational topic cards |
| 🛡️ Risk Assessment | Take the guided 15-question evaluation |
| 🔍 Scam Analyzer | Paste a job offer to detect red flags |
| 🆘 Emergency Help | Helplines and escape guidance |
| 📁 Resources | Legal rights, NGOs, reporting |

### SOS Button
The **🆘 SOS** button in the top-right header instantly navigates to the Emergency page and flashes the navigation item red.

### Chat Commands
Type or click quick chips:
- `"what is human trafficking"` — educational overview
- `"start risk assessment"` — launch the wizard
- `"check job offer"` — open scam analyzer
- `"emergency help"` — navigate to emergency page

---

## 🧠 Expert System Design

### Knowledge Base
- **105 entries** across **13 categories** loaded from `data/knowledge_base.py`
- Each entry: `{ category, query_patterns, response, keywords, confidence }`
- Categories: trafficking_basics, warning_signs, recruitment_scams, child_trafficking, forced_labour, online_grooming, victim_support, emergency_assistance, reporting_procedures, legal_rights, safety_measures, ngo_support, faqs

### Rule Engine
- **52 IF-THEN rules** using forward chaining inference
- Working Memory stores asserted facts (e.g., `has_document_confiscation = True`)
- Conflict resolution: priority-based rule ordering
- Rule example:
  ```
  IF  has_document_confiscation AND has_movement_restriction
  THEN classify = CRITICAL, type = FORCED_LABOUR
  ```

### Risk Classification
| Score Range | Level | Meaning |
|---|---|---|
| 0–19 | 🟢 Low | No significant trafficking indicators |
| 20–44 | 🟡 Medium | Some warning signs — exercise caution |
| 45–69 | 🔴 High | Strong indicators — seek advice immediately |
| 70+ | 🚨 Critical | Immediate danger — call emergency services |

### Scam Detector
- **110 red-flag indicators** covering:
  - Unrealistic salary promises
  - Vague job descriptions
  - Requests for personal documents upfront
  - Overseas jobs without proper registration
  - Romantic involvement in job offers
  - Debt bondage language
- Suspicion score: weighted sum → mapped to percentage

---

## 💾 Database Schema

AegisAI uses **SQLite** for local persistence at `data/aegis_ai.db`.

```sql
-- Session state
CREATE TABLE sessions (
    session_id    TEXT PRIMARY KEY,
    risk_level    TEXT DEFAULT 'UNKNOWN',
    risk_score    INTEGER DEFAULT 0,
    is_emergency  INTEGER DEFAULT 0,
    created_at    TEXT,
    updated_at    TEXT
);

-- Chat message history
CREATE TABLE chat_messages (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    TEXT,
    role          TEXT,      -- 'user' | 'bot'
    text          TEXT,
    is_emergency  INTEGER DEFAULT 0,
    timestamp     TEXT
);

-- Risk assessment results
CREATE TABLE assessment_results (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    TEXT,
    risk_level    TEXT,
    risk_score    INTEGER,
    risk_pct      REAL,
    summary       TEXT,
    timestamp     TEXT
);

-- Scam scan logs
CREATE TABLE scam_logs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    TEXT,
    job_text      TEXT,
    risk_level    TEXT,
    suspicion_pct REAL,
    red_flags     TEXT,      -- JSON array
    timestamp     TEXT
);
```

---

## 🧪 Test Suite

Run all 50 tests:
```bash
python main.py --test
```

| Test Class | Tests | Coverage |
|---|---|---|
| `TestKnowledgeBaseManager` | 8 | KB loading, query, category filter |
| `TestExpertSystemEngine` | 10 | Rule firing, fact assertion, classification |
| `TestRiskAssessmentModule` | 8 | Wizard flow, scoring, result generation |
| `TestScamDetector` | 8 | Flag detection, scoring, level mapping |
| `TestChatBot` | 8 | Intent routing, response generation |
| `TestIntegration` | 5 | End-to-end service wiring |
| `TestUserAcceptance` | 3 | Simulated user journeys |
| **Total** | **50** | **All passing ✅** |

---

## 🎨 Design System

The UI is built on a warm **Navy + Amber** design language (`ui/theme.py`).

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| `BG_DARK` | `#1A1A2E` | App root background |
| `BG_SIDEBAR` | `#16213E` | Left navigation sidebar |
| `BG_CARD` | `#1F2B47` | Cards, panels, chat area |
| `BG_INPUT` | `#253354` | Input fields, text areas |
| `ACCENT` | `#F59E0B` | Primary amber — buttons, active states |
| `ACCENT_HOVER` | `#FBBF24` | Hover on amber elements |
| `SUCCESS` | `#10B981` | Low risk, positive feedback |
| `WARNING` | `#F59E0B` | Medium risk, caution |
| `DANGER` | `#EF4444` | High risk, errors |
| `CRITICAL` | `#FF2D55` | Critical emergency states |
| `TEXT_PRIMARY` | `#F1F5F9` | Main body text |
| `TEXT_SECONDARY` | `#94A3B8` | Labels, secondary info |

### Typography

| Token | Font | Size | Weight | Usage |
|---|---|---|---|---|
| `FONT_HERO` | Segoe UI | 24pt | Bold | Page hero titles |
| `FONT_TITLE` | Segoe UI | 17pt | Bold | Section headings |
| `FONT_SUBTITLE` | Segoe UI | 13pt | Bold | Card headings |
| `FONT_BODY` | Segoe UI | 12pt | Regular | Body content |
| `FONT_SMALL` | Segoe UI | 11pt | Regular | Labels, nav |
| `FONT_TINY` | Segoe UI | 10pt | Regular | Badges, timestamps |

### Layout

- **Sidebar width:** 190px
- **Header height:** 52px
- **Corner radius:** 8px (default) / 12px (cards) / 5px (chips)
- **Standard padding:** 14px
- **Card padding:** 16px

---

## 🤝 Contributing

This is an academic project but contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and run tests: `python main.py --test`
4. Commit with a descriptive message
5. Push and open a Pull Request

### Code Style
- Follow PEP 8
- Use type hints on all public functions
- Add docstrings to all classes and public methods
- All UI colors must come from `ui/theme.py` — no hardcoded hex values

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

```
MIT License

Copyright (c) 2026 Tiyasha Sarkar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgements

- **Childline India** (1098) and **NHRC** (14433) for their life-saving hotlines
- **International Justice Mission**, **Prerana**, **Shakti Vahini** for NGO content
- The open-source community behind **CustomTkinter**
- All researchers and advocates working to end human trafficking

---

<div align="center">

**Made with ❤️ to protect the vulnerable**

*If you or someone you know is in danger, call **112** (India National Emergency) immediately.*

</div>
