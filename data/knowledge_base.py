"""
AegisAI Knowledge Base
======================
Rule-Based Expert System — Knowledge Repository
Contains 100+ entries across 13 categories.

Categories:
  1.  Human Trafficking Basics
  2.  Warning Signs
  3.  Recruitment Scams
  4.  Child Trafficking
  5.  Forced Labour
  6.  Online Grooming
  7.  Victim Support
  8.  Emergency Assistance
  9.  Reporting Procedures
  10. Legal Rights
  11. Safety Measures
  12. NGO Support
  13. FAQs
"""

# ---------------------------------------------------------------------------
# KNOWLEDGE BASE — Master Dictionary
# Each entry has: intent, keywords, user_queries, response, category, priority
# ---------------------------------------------------------------------------

KNOWLEDGE_BASE = {

    # =========================================================================
    # CATEGORY 1: HUMAN TRAFFICKING BASICS
    # =========================================================================

    "KB001": {
        "category": "human_trafficking_basics",
        "intent": "define_trafficking",
        "priority": 1,
        "keywords": ["what is", "define", "meaning", "human trafficking", "explain", "definition"],
        "user_queries": [
            "what is human trafficking",
            "define human trafficking",
            "explain human trafficking",
            "what does human trafficking mean",
            "tell me about human trafficking"
        ],
        "response": (
            "Human trafficking is a serious crime and a grave violation of human rights. "
            "It involves the recruitment, transportation, transfer, harbouring, or receipt of "
            "people through force, fraud, or coercion for the purpose of exploitation.\n\n"
            "Exploitation includes:\n"
            "  • Sexual exploitation (forced prostitution, pornography)\n"
            "  • Forced labour (factories, farms, construction)\n"
            "  • Domestic servitude (unpaid household work)\n"
            "  • Forced begging or petty crime\n"
            "  • Organ trafficking\n"
            "  • Child soldiers\n\n"
            "Key fact: Traffickers use deception, manipulation, and violence. "
            "Victims do NOT need to cross borders — trafficking happens within a country too."
        )
    },

    "KB002": {
        "category": "human_trafficking_basics",
        "intent": "trafficking_statistics",
        "priority": 2,
        "keywords": ["statistics", "numbers", "how many", "victims", "global", "india", "data", "facts"],
        "user_queries": [
            "how many people are trafficked",
            "trafficking statistics",
            "how many victims of trafficking",
            "human trafficking numbers in india",
            "global trafficking data"
        ],
        "response": (
            "Human Trafficking — Key Statistics:\n\n"
            "Global:\n"
            "  • 40.3 million people live in modern slavery worldwide (ILO, 2022)\n"
            "  • $150 billion generated annually — 2nd largest criminal enterprise\n"
            "  • 71% of victims are women and girls\n"
            "  • 25% of victims are children\n"
            "  • 1 in 4 victims is a child\n\n"
            "India:\n"
            "  • 6,533 trafficking cases registered in 2022 (NCRB)\n"
            "  • Most affected states: West Bengal, Rajasthan, Assam, Andhra Pradesh\n"
            "  • 50,000–100,000 children trafficked every year (estimated)\n"
            "  • India is both a source, transit, and destination country\n\n"
            "Note: Reported cases represent only a fraction of actual incidents."
        )
    },

    "KB003": {
        "category": "human_trafficking_basics",
        "intent": "types_of_trafficking",
        "priority": 1,
        "keywords": ["types", "kinds", "forms", "categories", "different", "labour trafficking",
                     "sex trafficking", "organ trafficking", "domestic"],
        "user_queries": [
            "what are the types of human trafficking",
            "types of trafficking",
            "different forms of trafficking",
            "kinds of human trafficking",
            "sex trafficking vs labour trafficking"
        ],
        "response": (
            "Types of Human Trafficking:\n\n"
            "1. SEX TRAFFICKING\n"
            "   Victims are forced or coerced into commercial sexual acts. "
            "Includes forced prostitution, pornography, and sexual servitude.\n\n"
            "2. LABOUR TRAFFICKING\n"
            "   Victims are forced to work in agriculture, factories, construction, "
            "fishing, or domestic service without pay or under threat.\n\n"
            "3. DOMESTIC SERVITUDE\n"
            "   Victims are kept in homes as unpaid servants, often isolated from "
            "the outside world and controlled through fear.\n\n"
            "4. CHILD TRAFFICKING\n"
            "   Children recruited for sexual exploitation, forced labour, begging, "
            "or child marriage.\n\n"
            "5. ORGAN TRAFFICKING\n"
            "   Victims are coerced or deceived into giving up organs (usually kidneys).\n\n"
            "6. FORCED BEGGING\n"
            "   Victims, especially children, are forced to beg on streets for traffickers.\n\n"
            "7. FORCED CRIMINALITY\n"
            "   Victims forced to commit crimes: petty theft, drug trafficking, etc."
        )
    },

    "KB004": {
        "category": "human_trafficking_basics",
        "intent": "how_trafficking_works",
        "priority": 1,
        "keywords": ["how", "work", "operate", "process", "recruit", "trap", "methods", "tactics"],
        "user_queries": [
            "how does human trafficking work",
            "how do traffickers operate",
            "how are people trafficked",
            "how do traffickers recruit victims",
            "trafficking methods and tactics"
        ],
        "response": (
            "How Traffickers Operate — The 3-Stage Process:\n\n"
            "STAGE 1: RECRUITMENT\n"
            "  • Fake job offers (domestic work, modeling, factory jobs)\n"
            "  • False promises of education, love, or better life\n"
            "  • Online luring via social media and dating apps\n"
            "  • Exploitation of poverty and desperation\n"
            "  • Recruitment through trusted community members\n\n"
            "STAGE 2: CONTROL\n"
            "  • Confiscating identity documents (passport, Aadhaar)\n"
            "  • Debt bondage — creating fake debts victims must 'work off'\n"
            "  • Physical violence and threats\n"
            "  • Isolation from family and friends\n"
            "  • Moving victims frequently to prevent escape\n\n"
            "STAGE 3: EXPLOITATION\n"
            "  • Forcing victims to work without pay\n"
            "  • Using victims for sexual exploitation\n"
            "  • Keeping victims in poor conditions\n"
            "  • Threatening victims' families\n\n"
            "Traffickers prey on VULNERABILITY: poverty, unemployment, family problems, "
            "and social exclusion."
        )
    },

    "KB005": {
        "category": "human_trafficking_basics",
        "intent": "trafficking_vs_smuggling",
        "priority": 3,
        "keywords": ["difference", "smuggling", "migration", "illegal", "border", "versus", "vs"],
        "user_queries": [
            "difference between trafficking and smuggling",
            "is trafficking same as smuggling",
            "trafficking vs illegal migration"
        ],
        "response": (
            "Trafficking vs. Smuggling — Key Differences:\n\n"
            "HUMAN TRAFFICKING:\n"
            "  • Victim is exploited (the crime continues after movement)\n"
            "  • Consent is irrelevant — even if initially given, exploitation removes it\n"
            "  • Can happen without crossing any border (domestic trafficking)\n"
            "  • The trafficker profits from ongoing exploitation\n"
            "  • Victim is a CRIME VICTIM, not a criminal\n\n"
            "HUMAN SMUGGLING:\n"
            "  • A person pays to be smuggled across borders (transaction ends on arrival)\n"
            "  • Requires border crossing\n"
            "  • Person is usually a willing participant\n"
            "  • The smuggler profits from the transport fee\n\n"
            "IMPORTANT: Smuggling can BECOME trafficking if the person is then exploited."
        )
    },

    "KB006": {
        "category": "human_trafficking_basics",
        "intent": "vulnerability_factors",
        "priority": 2,
        "keywords": ["vulnerable", "risk factors", "who", "target", "why", "affected", "susceptible"],
        "user_queries": [
            "who is vulnerable to trafficking",
            "why are some people targeted",
            "risk factors for trafficking",
            "who do traffickers target"
        ],
        "response": (
            "Vulnerability Factors — Who Traffickers Target:\n\n"
            "SOCIAL FACTORS:\n"
            "  • Poverty and lack of economic opportunity\n"
            "  • Unemployment or underemployment\n"
            "  • Discrimination based on gender, caste, or ethnicity\n"
            "  • Social exclusion and marginalization\n\n"
            "PERSONAL FACTORS:\n"
            "  • Runaway or homeless youth\n"
            "  • History of abuse or neglect\n"
            "  • Substance dependency\n"
            "  • Mental health challenges\n"
            "  • Lack of education\n\n"
            "SITUATIONAL FACTORS:\n"
            "  • Migrants and refugees\n"
            "  • Children without parental supervision\n"
            "  • Natural disaster or conflict survivors\n"
            "  • People desperate for work or money\n\n"
            "Remember: ANYONE can be a target. Traffickers are skilled manipulators."
        )
    },

    # =========================================================================
    # CATEGORY 2: WARNING SIGNS
    # =========================================================================

    "KB007": {
        "category": "warning_signs",
        "intent": "general_warning_signs",
        "priority": 1,
        "keywords": ["warning signs", "red flags", "signs", "indicators", "how to tell",
                     "identify", "recognize", "spot"],
        "user_queries": [
            "what are warning signs of trafficking",
            "how to identify a trafficking victim",
            "red flags of human trafficking",
            "how to recognize trafficking",
            "warning signs to look for"
        ],
        "response": (
            "General Warning Signs of Human Trafficking:\n\n"
            "BEHAVIORAL SIGNS:\n"
            "  • Appears fearful, anxious, or submissive\n"
            "  • Avoids eye contact and speaking freely\n"
            "  • Seems coached or scripted in responses\n"
            "  • Does not speak on their own behalf\n"
            "  • Appears disoriented or confused about location\n\n"
            "PHYSICAL SIGNS:\n"
            "  • Signs of physical abuse, malnourishment\n"
            "  • Branded or tattooed (trafficker's mark of ownership)\n"
            "  • Inappropriate dress for weather or situation\n"
            "  • Multiple people living in cramped conditions\n\n"
            "CIRCUMSTANTIAL SIGNS:\n"
            "  • Lacks ID documents (someone else holds them)\n"
            "  • Does not know their home address\n"
            "  • Has a 'manager' or controller who speaks for them\n"
            "  • Works excessive hours with no pay\n"
            "  • Not allowed to speak alone or have privacy\n\n"
            "If you notice these signs, DO NOT confront the suspected trafficker.\n"
            "Call 1098 (Childline) or 100 (Police) to report."
        )
    },

    "KB008": {
        "category": "warning_signs",
        "intent": "signs_in_children",
        "priority": 1,
        "keywords": ["child", "children", "minor", "kid", "young", "boy", "girl", "signs in child"],
        "user_queries": [
            "warning signs of child trafficking",
            "how to tell if a child is being trafficked",
            "signs a child is in danger",
            "red flags in children",
            "my child is behaving differently"
        ],
        "response": (
            "Warning Signs of Child Trafficking:\n\n"
            "AT SCHOOL:\n"
            "  • Sudden unexplained absences\n"
            "  • Decline in academic performance\n"
            "  • Withdrawal from friends and activities\n"
            "  • Unexplained gifts, money, or new phone\n\n"
            "AT HOME:\n"
            "  • Secretive about online activity\n"
            "  • Older 'boyfriend' or 'girlfriend'\n"
            "  • Coming home very late or going missing overnight\n"
            "  • Running away from home repeatedly\n"
            "  • Speaking in coded language\n\n"
            "PHYSICAL SIGNS:\n"
            "  • Signs of physical or sexual abuse\n"
            "  • Tattoos or brands (may indicate ownership by trafficker)\n"
            "  • Malnourished or appears unhealthy\n"
            "  • Sexually transmitted infections (in minors)\n\n"
            "BEHAVIORAL CHANGES:\n"
            "  • Sudden change in friend group to older adults\n"
            "  • Excessive use of hotel key cards\n"
            "  • Talks about exciting trips or expensive things\n\n"
            "IMMEDIATE HELP: Call Childline 1098 (Free, 24/7)"
        )
    },

    "KB009": {
        "category": "warning_signs",
        "intent": "signs_in_workplace",
        "priority": 2,
        "keywords": ["workplace", "work", "factory", "labour", "worker", "employee", "job site"],
        "user_queries": [
            "signs of trafficking at workplace",
            "labour trafficking warning signs",
            "how to spot forced labour",
            "signs someone is being exploited at work"
        ],
        "response": (
            "Warning Signs of Labour Trafficking at the Workplace:\n\n"
            "  • Workers live at the worksite or in overcrowded housing provided by employer\n"
            "  • Workers cannot leave freely or are guarded\n"
            "  • Workers are not paid or wages are withheld\n"
            "  • Deductions made for food, housing, tools (debt bondage)\n"
            "  • Workers are afraid to speak about their conditions\n"
            "  • Employer holds workers' ID documents\n"
            "  • Workers show signs of physical abuse\n"
            "  • Workers do not know their employer's full name or address\n"
            "  • Workers are threatened with deportation (for migrants)\n"
            "  • Excessive working hours with no rest days\n\n"
            "If you see these signs: Report to the local Labour Commissioner or\n"
            "call the National Human Rights Commission at 14433."
        )
    },

    "KB010": {
        "category": "warning_signs",
        "intent": "online_warning_signs",
        "priority": 2,
        "keywords": ["online", "social media", "internet", "chat", "message", "dating app",
                     "stranger", "facebook", "instagram", "whatsapp"],
        "user_queries": [
            "warning signs online",
            "online trafficking signs",
            "suspicious online behavior",
            "signs someone is grooming me online",
            "online red flags"
        ],
        "response": (
            "Online Warning Signs — Digital Red Flags:\n\n"
            "FROM A STRANGER ONLINE:\n"
            "  • Extremely fast emotional connection ('love bombing')\n"
            "  • Asks for personal photos or videos quickly\n"
            "  • Offers money, gifts, or modeling opportunities\n"
            "  • Wants to move conversation to private platform\n"
            "  • Asks you to keep the relationship secret\n"
            "  • Profile seems too good to be true\n"
            "  • Claims to be from abroad and needs help\n\n"
            "JOB OFFERS ONLINE:\n"
            "  • Jobs posted without company name or contact details\n"
            "  • High pay for unclear or vague work\n"
            "  • Asks for advance payment or fees\n"
            "  • No formal interview process\n"
            "  • Asks for passport, Aadhaar before hiring\n\n"
            "PROTECT YOURSELF:\n"
            "  • Never share personal photos with strangers\n"
            "  • Verify any job offer independently\n"
            "  • Tell a trusted adult about suspicious online contact\n"
            "  • Report suspicious profiles to the platform"
        )
    },

    "KB011": {
        "category": "warning_signs",
        "intent": "signs_in_community",
        "priority": 3,
        "keywords": ["neighbor", "community", "street", "house", "nearby", "suspicious activity",
                     "area", "locality"],
        "user_queries": [
            "signs of trafficking in my community",
            "suspicious activity near me",
            "how to spot trafficking in neighborhood",
            "what to watch for in my area"
        ],
        "response": (
            "Community-Level Warning Signs:\n\n"
            "  • A house or apartment with many unknown people coming and going at odd hours\n"
            "  • Windows covered or boarded up at residential premises\n"
            "  • Many people living in a small space with few belongings\n"
            "  • People who appear frightened or unable to speak freely\n"
            "  • Children who appear to be unaccompanied or unsupervised\n"
            "  • People who seem malnourished or have visible injuries\n"
            "  • Vehicles parked outside with unknown occupants watching a property\n\n"
            "WHAT TO DO:\n"
            "  • Do NOT confront anyone or investigate yourself\n"
            "  • Note details: vehicle numbers, descriptions, times\n"
            "  • Report to police (100) or Childline (1098)\n"
            "  • Your report is anonymous if requested"
        )
    },

    # =========================================================================
    # CATEGORY 3: RECRUITMENT SCAMS
    # =========================================================================

    "KB012": {
        "category": "recruitment_scams",
        "intent": "fake_job_offers",
        "priority": 1,
        "keywords": ["fake job", "job scam", "false job", "fraudulent", "job offer", "suspicious job",
                     "overseas job", "abroad work", "easy money"],
        "user_queries": [
            "how to identify fake job offers",
            "what are common job scams",
            "how do I know if a job is fake",
            "suspicious job offer what to do",
            "is this job offer real"
        ],
        "response": (
            "Fake Job Offer Red Flags:\n\n"
            "SALARY RED FLAGS:\n"
            "  • Salary that is 3x–10x the market rate for no reason\n"
            "  • 'Earn ₹50,000–₹1,00,000 per month easily'\n"
            "  • No skill or experience required for high pay\n\n"
            "JOB DESCRIPTION RED FLAGS:\n"
            "  • Vague description: 'female staff needed', 'hostess wanted'\n"
            "  • 'Entertainment industry' without specifics\n"
            "  • Requires travel to unknown or foreign location\n"
            "  • No company name, address, or registration details\n\n"
            "PROCESS RED FLAGS:\n"
            "  • No formal interview or just a WhatsApp chat\n"
            "  • Hired immediately without verification\n"
            "  • Asks for upfront payment for 'visa', 'training', 'kit'\n"
            "  • Asks for your passport, Aadhaar before you start\n"
            "  • Wants you to travel before signing any contract\n\n"
            "RULE: A legitimate employer will NEVER:\n"
            "  ✗ Ask for money from you\n"
            "  ✗ Take your documents before employment\n"
            "  ✗ Hire you without a proper contract\n"
            "  ✗ Offer unrealistic pay for simple work"
        )
    },

    "KB013": {
        "category": "recruitment_scams",
        "intent": "modeling_scams",
        "priority": 2,
        "keywords": ["modeling", "model", "actress", "entertainment", "photoshoot", "audition",
                     "film", "glamour", "fashion"],
        "user_queries": [
            "is this modeling job real",
            "modeling job scam",
            "fake modeling agency",
            "entertainment job warning signs",
            "someone offered me a modeling job"
        ],
        "response": (
            "Modeling and Entertainment Job Scams:\n\n"
            "HOW THE SCAM WORKS:\n"
            "  1. Recruiter approaches victim (in person or online)\n"
            "  2. Flatters victim about their looks or talent\n"
            "  3. Promises fame, high pay, career opportunities\n"
            "  4. Requests photos, personal information\n"
            "  5. Moves victim to private location for 'audition'\n"
            "  6. Victim is trapped and exploited\n\n"
            "RED FLAGS:\n"
            "  • Approached by a stranger on the street or social media\n"
            "  • 'Audition' is in a private home or hotel room\n"
            "  • Asks for explicit photos\n"
            "  • No formal agency registration or portfolio\n"
            "  • Pressure to decide immediately\n"
            "  • 'Registration fees' required\n\n"
            "VERIFY A LEGITIMATE AGENCY:\n"
            "  ✓ Look up agency registration\n"
            "  ✓ Never pay fees to an agency\n"
            "  ✓ Read all contracts carefully\n"
            "  ✓ Take a trusted adult to any meeting\n"
            "  ✓ Reject any request for compromising photos"
        )
    },

    "KB014": {
        "category": "recruitment_scams",
        "intent": "domestic_worker_scams",
        "priority": 2,
        "keywords": ["domestic", "maid", "housework", "cook", "servant", "caretaker",
                     "babysitter", "household", "nanny"],
        "user_queries": [
            "domestic worker job scams",
            "maid job trafficking",
            "housework job red flags",
            "is domestic work job safe"
        ],
        "response": (
            "Domestic Worker Recruitment Scams:\n\n"
            "COMMON TACTICS:\n"
            "  • Promises of high salary for cooking/cleaning in a big city\n"
            "  • Recruiter from own village or community (trusted face)\n"
            "  • Employer is 'unknown' and lives far away\n"
            "  • Contract is verbal, not written\n"
            "  • Victim is taken far from family without address details\n\n"
            "SIGNS OF DOMESTIC SERVITUDE TRAFFICKING:\n"
            "  • Employer controls all movement\n"
            "  • Worker cannot contact family\n"
            "  • Wages are withheld or not paid\n"
            "  • Worker sleeps in kitchen or storage space\n"
            "  • Worker has no rest days\n"
            "  • Passport / ID held by employer\n\n"
            "PROTECT YOURSELF:\n"
            "  ✓ Always get a written contract\n"
            "  ✓ Know the full name and address of employer\n"
            "  ✓ Share employer's contact with family\n"
            "  ✓ Ensure you can contact family at all times\n"
            "  ✓ Do not let anyone hold your ID documents"
        )
    },

    "KB015": {
        "category": "recruitment_scams",
        "intent": "marriage_scams",
        "priority": 2,
        "keywords": ["marriage", "bride", "groom", "wedding", "proposal", "love marriage",
                     "forced marriage", "arranged", "matchmaking"],
        "user_queries": [
            "marriage trafficking",
            "fake marriage offer",
            "trafficking through marriage",
            "forced marriage warning signs"
        ],
        "response": (
            "Marriage-Based Trafficking (Bride Trafficking):\n\n"
            "HOW IT WORKS:\n"
            "  • Families in poor or rural areas approached with lavish marriage proposals\n"
            "  • Man or family appears wealthy and respectable\n"
            "  • Bride is taken to another city/state/country\n"
            "  • Bride is isolated, abused, or sold to others\n\n"
            "RED FLAGS:\n"
            "  • Family you don't know offers marriage quickly\n"
            "  • They discourage the family from visiting after marriage\n"
            "  • Husband controls all money and movement\n"
            "  • Bride cannot contact her own family\n"
            "  • Bride is forced to work without pay\n"
            "  • Bride is moved to unknown locations repeatedly\n\n"
            "IN INDIA:\n"
            "  • States with high bride trafficking: Haryana, Punjab (from West Bengal, Jharkhand)\n"
            "  • Childline 1098 handles cases of child marriage and forced marriage\n"
            "  • National Commission for Women: 011-26942369"
        )
    },

    "KB016": {
        "category": "recruitment_scams",
        "intent": "overseas_job_scams",
        "priority": 1,
        "keywords": ["abroad", "foreign", "overseas", "gulf", "dubai", "international",
                     "visa", "foreign job", "work abroad", "middle east"],
        "user_queries": [
            "overseas job offer suspicious",
            "foreign job scam",
            "gulf job trafficking",
            "Dubai job warning signs",
            "international job red flags"
        ],
        "response": (
            "Overseas / Foreign Job Scams:\n\n"
            "COMMON DECEPTIONS:\n"
            "  • Hotel/restaurant jobs in Gulf countries with great salary\n"
            "  • 'Sponsorship' will be arranged for you\n"
            "  • Recruiter takes passport for 'visa processing'\n"
            "  • Contract shown is different from what is signed abroad\n"
            "  • On arrival, job conditions are completely different\n\n"
            "HIGH-RISK DESTINATIONS FROM INDIA:\n"
            "  • UAE, Saudi Arabia, Qatar, Kuwait (domestic workers)\n"
            "  • Southeast Asia: Cambodia, Myanmar, Thailand (tech scam centres)\n"
            "  • CAUTION: 'Online job from home' offers in Cambodia/Myanmar are\n"
            "    often forced cyber-scam operations\n\n"
            "BEFORE GOING ABROAD:\n"
            "  ✓ Verify recruiter with Ministry of External Affairs eMigrate portal\n"
            "  ✓ Keep a copy of ALL documents with family\n"
            "  ✓ Know the Indian Embassy number at your destination\n"
            "  ✓ Never surrender your passport to anyone\n"
            "  ✓ Register with NORKA / eMigrate if going to ECR countries\n\n"
            "Indian Embassy Emergency: Check mea.gov.in for destination number"
        )
    },

    # =========================================================================
    # CATEGORY 4: CHILD TRAFFICKING
    # =========================================================================

    "KB017": {
        "category": "child_trafficking",
        "intent": "child_trafficking_overview",
        "priority": 1,
        "keywords": ["child trafficking", "children", "minor", "child labour", "child exploitation",
                     "underage"],
        "user_queries": [
            "what is child trafficking",
            "how are children trafficked",
            "child trafficking in india",
            "child exploitation"
        ],
        "response": (
            "Child Trafficking — Overview:\n\n"
            "DEFINITION:\n"
            "Any recruitment, transportation, transfer, or receipt of a CHILD for the "
            "purpose of exploitation is trafficking — even without force or deception.\n"
            "Children CANNOT consent to being trafficked.\n\n"
            "FORMS OF CHILD TRAFFICKING:\n"
            "  • Sexual exploitation (child prostitution, pornography)\n"
            "  • Child labour (factories, brick kilns, farms, begging rings)\n"
            "  • Child domestic servitude\n"
            "  • Child soldiers\n"
            "  • Child marriage\n"
            "  • Illegal adoption\n\n"
            "INDIA SPECIFIC:\n"
            "  • Child Marriage Restraint Act prohibits marriage under 18 (girls) / 21 (boys)\n"
            "  • Child Labour (Prohibition & Regulation) Act, 1986\n"
            "  • POCSO Act, 2012 — Protection of Children from Sexual Offences\n\n"
            "EMERGENCY: Call Childline 1098 — Free, 24/7, confidential"
        )
    },

    "KB018": {
        "category": "child_trafficking",
        "intent": "child_begging_rings",
        "priority": 2,
        "keywords": ["begging", "beggar", "street child", "ring", "organized begging"],
        "user_queries": [
            "child begging trafficking",
            "organized begging rings",
            "children forced to beg",
            "begging ring trafficking"
        ],
        "response": (
            "Child Begging Rings — Trafficking through Forced Begging:\n\n"
            "HOW IT WORKS:\n"
            "  • Children are recruited (or kidnapped) from poor families\n"
            "  • They are deliberately maimed or drugged to generate more sympathy\n"
            "  • 'Gang leaders' collect all the money earned\n"
            "  • Children receive no wages — they live in deplorable conditions\n"
            "  • Children are rotated across cities to avoid detection\n\n"
            "WARNING SIGNS:\n"
            "  • Child appears drugged or sedated\n"
            "  • Adult nearby watching but not visibly related\n"
            "  • Child has visible injuries that appear deliberate\n"
            "  • Child cannot speak about where they live\n\n"
            "WHAT TO DO:\n"
            "  • Call Childline 1098 with location details\n"
            "  • Give money directly to shelter organizations, not beggars\n"
            "  • Do NOT attempt to rescue the child yourself — this can be dangerous"
        )
    },

    "KB019": {
        "category": "child_trafficking",
        "intent": "online_child_exploitation",
        "priority": 1,
        "keywords": ["CSAM", "online exploitation", "child pornography", "POCSO", "online abuse",
                     "child images", "video"],
        "user_queries": [
            "online child sexual exploitation",
            "child exploitation online",
            "someone sent me child images",
            "reporting online child abuse"
        ],
        "response": (
            "Online Child Sexual Exploitation (OCSEA):\n\n"
            "WHAT IS IT:\n"
            "  • Creation, distribution, or possession of child sexual abuse material (CSAM)\n"
            "  • Online grooming to produce sexual images/videos\n"
            "  • Sextortion — threatening to publish images unless demands are met\n\n"
            "LEGAL STATUS IN INDIA:\n"
            "  • POCSO Act, Section 13 & 14: Production and use of child for pornographic purposes\n"
            "    → Punishment: 5–7 years imprisonment + fine\n"
            "  • IT Act Section 67B: Publishing/transmitting child sexual abuse material\n"
            "    → Punishment: Up to 7 years + fine\n\n"
            "HOW TO REPORT:\n"
            "  • NCMEC CyberTipline: cybertipline.org\n"
            "  • National Cyber Crime Reporting Portal: cybercrime.gov.in\n"
            "  • Childline: 1098\n"
            "  • REPORT DON'T SHARE — Never forward CSAM material"
        )
    },

    "KB020": {
        "category": "child_trafficking",
        "intent": "child_marriage_trafficking",
        "priority": 2,
        "keywords": ["child marriage", "underage marriage", "forced marriage minor", "early marriage"],
        "user_queries": [
            "child marriage and trafficking",
            "child marriage warning signs",
            "is child marriage trafficking",
            "how to stop child marriage"
        ],
        "response": (
            "Child Marriage and Trafficking:\n\n"
            "LEGAL STATUS:\n"
            "  • Child Marriage Restraint Act, 2006: Marriage below 18 (girls) or 21 (boys) is ILLEGAL\n"
            "  • Prohibition of Child Marriage Act, 2006\n"
            "  • Child marriage can be declared void (not valid)\n\n"
            "LINK TO TRAFFICKING:\n"
            "  • Young brides are often sold to older men\n"
            "  • Brides trafficked across state borders under guise of marriage\n"
            "  • Girls forced into sexual servitude after 'marriage'\n"
            "  • Traffickers pose as legitimate families seeking marriage\n\n"
            "STOP A CHILD MARRIAGE:\n"
            "  • Report to Child Marriage Prohibition Officer (appointed in every district)\n"
            "  • Call Childline: 1098\n"
            "  • File complaint with local police\n"
            "  • Report to District Magistrate\n\n"
            "The marriage can be stopped even on the day of the wedding."
        )
    },

    # =========================================================================
    # CATEGORY 5: FORCED LABOUR
    # =========================================================================

    "KB021": {
        "category": "forced_labour",
        "intent": "forced_labour_definition",
        "priority": 1,
        "keywords": ["forced labour", "bonded labour", "debt bondage", "forced work",
                     "slavery", "modern slavery"],
        "user_queries": [
            "what is forced labour",
            "bonded labour meaning",
            "debt bondage explained",
            "signs of forced labour",
            "forced labour in india"
        ],
        "response": (
            "Forced Labour — Definition and Types:\n\n"
            "FORCED LABOUR:\n"
            "Work extracted from a person under threat of penalty, involving no free choice "
            "to refuse or stop.\n\n"
            "BONDED LABOUR (Most common in India):\n"
            "  • Person takes a loan (often very small)\n"
            "  • They must work to repay the debt\n"
            "  • Interest is inflated; the debt never reduces\n"
            "  • Children inherit the parent's debt\n"
            "  • Debt is passed down generations\n\n"
            "SECTORS MOST AFFECTED:\n"
            "  • Brick kilns\n"
            "  • Agriculture (especially sugarcane, rice)\n"
            "  • Stone quarries\n"
            "  • Domestic work\n"
            "  • Textile mills\n"
            "  • Construction\n\n"
            "LEGAL PROTECTION:\n"
            "  • Bonded Labour System (Abolition) Act, 1976\n"
            "  • Bonded labour is ILLEGAL in India\n"
            "  • Any bonded debt is automatically cancelled by law"
        )
    },

    "KB022": {
        "category": "forced_labour",
        "intent": "forced_labour_indicators",
        "priority": 1,
        "keywords": ["indicators", "signs", "identify", "recognize forced labour", "symptoms"],
        "user_queries": [
            "indicators of forced labour",
            "how to recognize forced labour",
            "what are signs of labour trafficking"
        ],
        "response": (
            "Forced Labour — 15 Key Indicators (ILO):\n\n"
            "1.  Abuse of vulnerability — exploiting poverty or migration status\n"
            "2.  Deception — false promises about job or conditions\n"
            "3.  Restriction of movement — locked in, guarded\n"
            "4.  Isolation — cut off from family and outside world\n"
            "5.  Physical and sexual violence — threat or actual\n"
            "6.  Intimidation and threats — against self or family\n"
            "7.  Retention of identity documents — passport/ID held\n"
            "8.  Withholding of wages — not paid or wages deducted\n"
            "9.  Debt bondage — impossible debt for recruitment/living\n"
            "10. Abusive working conditions — dangerous, no rest\n"
            "11. Excessive overtime — forced to work beyond legal hours\n"
            "12. Employer accommodation dependency — live-in with no choice\n"
            "13. No freedom to change employer\n"
            "14. Subject to surveillance — constantly watched\n"
            "15. Fear of authorities — told they will be arrested if they speak up"
        )
    },

    "KB023": {
        "category": "forced_labour",
        "intent": "brick_kiln_trafficking",
        "priority": 3,
        "keywords": ["brick kiln", "bhatta", "kiln", "brick", "migrant worker"],
        "user_queries": [
            "brick kiln forced labour",
            "trafficking in brick kilns",
            "bonded labour brick kiln"
        ],
        "response": (
            "Brick Kiln Bonded Labour — A Major Problem in India:\n\n"
            "HOW IT WORKS:\n"
            "  • Migrant families recruited from Jharkhand, Chhattisgarh, UP, Bihar\n"
            "  • Advanced payment (advance/peshgi) is given at recruitment\n"
            "  • Entire family must work to repay the advance\n"
            "  • Deductions for food, tools, transport keep the debt growing\n"
            "  • Families live on the kiln premises — no freedom to leave\n\n"
            "LEGAL REMEDIES:\n"
            "  • Bonded Labour System (Abolition) Act, 1976 — ALL debts cancelled\n"
            "  • File complaint with District Magistrate\n"
            "  • Contact the local Labour Commissioner\n"
            "  • NGO: Jan Sahas (jansahas.in) works specifically on bonded labour rescue\n\n"
            "HELPLINE: National Human Rights Commission — 14433"
        )
    },

    # =========================================================================
    # CATEGORY 6: ONLINE GROOMING
    # =========================================================================

    "KB024": {
        "category": "online_grooming",
        "intent": "grooming_definition",
        "priority": 1,
        "keywords": ["grooming", "online grooming", "what is grooming", "groomed", "predator"],
        "user_queries": [
            "what is online grooming",
            "what does grooming mean",
            "how does online grooming happen",
            "signs of being groomed online"
        ],
        "response": (
            "Online Grooming — What It Is:\n\n"
            "DEFINITION:\n"
            "Grooming is the process by which an offender gains a child or young person's "
            "trust and breaks down their inhibitions in order to exploit them — often for "
            "sexual purposes or to recruit them into trafficking.\n\n"
            "THE GROOMING PROCESS:\n"
            "  Stage 1: Target Selection — finds vulnerable, lonely, or isolated person\n"
            "  Stage 2: Gaining Trust — becomes the 'perfect friend' or 'loving partner'\n"
            "  Stage 3: Filling Needs — provides gifts, money, affection\n"
            "  Stage 4: Isolation — cuts victim off from family and friends\n"
            "  Stage 5: Desensitization — gradually introduces sexual topics\n"
            "  Stage 6: Maintaining Control — uses blackmail, shame, threats\n\n"
            "IMPORTANT:\n"
            "  • Grooming can happen to boys and girls\n"
            "  • Groomer can be any age or gender\n"
            "  • It can take days, weeks, or months\n"
            "  • It is NOT the victim's fault"
        )
    },

    "KB025": {
        "category": "online_grooming",
        "intent": "grooming_red_flags",
        "priority": 1,
        "keywords": ["grooming signs", "grooming red flags", "suspicious online contact",
                     "someone online", "adult messaging teen"],
        "user_queries": [
            "signs someone is grooming me online",
            "grooming red flags to watch for",
            "suspicious behavior online",
            "is this person grooming me"
        ],
        "response": (
            "Online Grooming — Red Flags to Recognize:\n\n"
            "  🚩 They want to be your ONLY source of support\n"
            "  🚩 They tell you to keep your relationship secret\n"
            "  🚩 They give you gifts, money, or mobile recharge\n"
            "  🚩 They seem to understand you better than anyone else\n"
            "  🚩 They talk about sex or send sexual content\n"
            "  🚩 They ask you to send photos (then request more revealing ones)\n"
            "  🚩 They want to meet in person quickly\n"
            "  🚩 They get angry or threatening when you say no\n"
            "  🚩 They say 'if you loved me, you would do this'\n"
            "  🚩 They claim to be your 'boyfriend/girlfriend' very quickly\n"
            "  🚩 They make you feel guilty for not complying\n\n"
            "IF THIS IS HAPPENING TO YOU:\n"
            "  • You are NOT alone and it is NOT your fault\n"
            "  • Stop communication and block the person\n"
            "  • Tell a trusted adult immediately\n"
            "  • Report to Childline: 1098\n"
            "  • Report to Cyber Crime Portal: cybercrime.gov.in"
        )
    },

    "KB026": {
        "category": "online_grooming",
        "intent": "sextortion",
        "priority": 1,
        "keywords": ["sextortion", "blackmail", "nude photos", "leaked", "threat", "share photo",
                     "video call scam", "intimate images"],
        "user_queries": [
            "someone has my photos and is threatening me",
            "sextortion what to do",
            "someone threatening to share my photos",
            "nude photo blackmail",
            "video call scam"
        ],
        "response": (
            "Sextortion — What to Do:\n\n"
            "WHAT IS SEXTORTION:\n"
            "  A crime where someone threatens to share intimate images/videos unless "
            "you pay money, send more images, or perform sexual acts.\n\n"
            "DO:\n"
            "  ✓ STOP all contact with the person immediately\n"
            "  ✓ DO NOT pay — payment only leads to more demands\n"
            "  ✓ Save evidence: screenshots of messages/threats\n"
            "  ✓ Note the platform, username, phone number\n"
            "  ✓ Report to the platform (Instagram, WhatsApp, etc.)\n"
            "  ✓ Report to Cyber Crime: cybercrime.gov.in or call 1930\n"
            "  ✓ Tell a trusted adult or counselor\n\n"
            "DO NOT:\n"
            "  ✗ Pay the blackmailer\n"
            "  ✗ Send more images\n"
            "  ✗ Meet the person\n"
            "  ✗ Delete the evidence (needed for police)\n\n"
            "REMEMBER: This is a CRIME against YOU. The criminal is the one who\n"
            "should be ashamed, not you. Help is available."
        )
    },

    "KB027": {
        "category": "online_grooming",
        "intent": "social_media_safety",
        "priority": 2,
        "keywords": ["social media safety", "instagram safe", "facebook safe", "privacy settings",
                     "online safety tips"],
        "user_queries": [
            "how to stay safe on social media",
            "online safety tips",
            "protecting myself online",
            "social media privacy"
        ],
        "response": (
            "Online Safety — Practical Steps:\n\n"
            "PROFILE SETTINGS:\n"
            "  ✓ Set all social media profiles to PRIVATE\n"
            "  ✓ Do not accept friend/follow requests from strangers\n"
            "  ✓ Do not display phone number, school, or location publicly\n"
            "  ✓ Use a non-identifying profile picture\n\n"
            "COMMUNICATION:\n"
            "  ✓ Never share personal photos with strangers online\n"
            "  ✓ Never share your home address, school, or daily routine\n"
            "  ✓ If someone makes you uncomfortable, block and report immediately\n"
            "  ✓ Meet online contacts only in public places with a trusted adult present\n\n"
            "CONTENT:\n"
            "  ✓ Think before you post — once online, always online\n"
            "  ✓ Don't share photos that reveal your location\n"
            "  ✓ Turn off location tagging on photos\n\n"
            "REPORTING:\n"
            "  ✓ Use platform reporting features for suspicious content\n"
            "  ✓ Report to Cyber Crime: cybercrime.gov.in"
        )
    },

    # =========================================================================
    # CATEGORY 7: VICTIM SUPPORT
    # =========================================================================

    "KB028": {
        "category": "victim_support",
        "intent": "victim_rights",
        "priority": 1,
        "keywords": ["rights", "victim rights", "legal rights victim", "entitlement",
                     "deserve", "support"],
        "user_queries": [
            "what rights do trafficking victims have",
            "victim rights india",
            "am I entitled to help",
            "what support can I get as a victim"
        ],
        "response": (
            "Rights of Trafficking Victims in India:\n\n"
            "YOU HAVE THE RIGHT TO:\n"
            "  1. BE TREATED AS A VICTIM, NOT A CRIMINAL\n"
            "     • Trafficking victims are not prosecuted for crimes committed under coercion\n\n"
            "  2. FREE LEGAL AID\n"
            "     • District Legal Services Authority (DLSA) provides free lawyers\n\n"
            "  3. COMPENSATION\n"
            "     • Crime Victims Compensation Scheme under NALSA\n"
            "     • Victim Compensation Fund under Nirbhaya Fund\n\n"
            "  4. SHELTER & REHABILITATION\n"
            "     • Government-run Ujjawala shelters\n"
            "     • Protection under Juvenile Justice Act (for children)\n\n"
            "  5. CONFIDENTIALITY\n"
            "     • Your name and details cannot be published in media\n\n"
            "  6. IN-CAMERA TRIAL\n"
            "     • Court proceedings conducted privately to protect dignity\n\n"
            "  7. REPATRIATION\n"
            "     • If from another state, right to be returned to home state\n"
            "     • If foreign national, embassy must be informed"
        )
    },

    "KB029": {
        "category": "victim_support",
        "intent": "trauma_support",
        "priority": 1,
        "keywords": ["trauma", "mental health", "counseling", "therapy", "emotional",
                     "PTSD", "healing", "recover", "help me"],
        "user_queries": [
            "I need emotional support",
            "I feel traumatized",
            "help for trafficking survivors",
            "mental health support for victims",
            "counseling for trafficking"
        ],
        "response": (
            "Emotional and Psychological Support:\n\n"
            "WHAT YOU MAY BE FEELING (All normal responses to trauma):\n"
            "  • Fear, anxiety, nightmares\n"
            "  • Shame or guilt (remember: it is NOT your fault)\n"
            "  • Anger, sadness, confusion\n"
            "  • Difficulty trusting people\n"
            "  • Flashbacks\n\n"
            "YOU ARE NOT ALONE. YOU ARE STRONG. IT WAS NOT YOUR FAULT.\n\n"
            "SUPPORT AVAILABLE:\n"
            "  • Vandrevala Foundation: 1860-2662-345 (24/7 mental health helpline)\n"
            "  • iCall: 9152987821 (TISS-run counseling)\n"
            "  • Snehi: 044-24640050\n"
            "  • Prerana (for trafficking survivors): +91-22-23720856\n\n"
            "HEALING TAKES TIME:\n"
            "  • Seek professional counseling when ready\n"
            "  • Connect with survivor support groups\n"
            "  • Your recovery journey is your own pace"
        )
    },

    "KB030": {
        "category": "victim_support",
        "intent": "rehabilitation_programs",
        "priority": 2,
        "keywords": ["rehabilitation", "shelter", "safe house", "reintegration", "recovery",
                     "program", "support scheme"],
        "user_queries": [
            "rehabilitation programs for trafficking victims",
            "shelter for trafficking survivors",
            "government schemes for victims",
            "how to rebuild life after trafficking"
        ],
        "response": (
            "Rehabilitation Programs and Support:\n\n"
            "GOVERNMENT SCHEMES (India):\n\n"
            "  UJJAWALA SCHEME:\n"
            "    • Rescue and rehabilitation of women and child victims\n"
            "    • Shelter homes, counseling, legal aid, vocational training\n"
            "    • Contact: Ministry of Women and Child Development\n\n"
            "  SWADHAR GREH:\n"
            "    • Temporary relief for women in distress\n"
            "    • Food, clothing, shelter, legal aid\n\n"
            "  SAKHI (OSC — One Stop Centres):\n"
            "    • Medical assistance, police facilitation, legal aid, counseling\n"
            "    • Located in government hospitals\n"
            "    • Helpline: 181\n\n"
            "  JUVENILE JUSTICE ACT (for children):\n"
            "    • Child Care Institutions (CCIs)\n"
            "    • Specialized Adoption Agency for orphan trafficking victims\n\n"
            "NGO REHABILITATION:\n"
            "  • Prerana (Mumbai): Full rehabilitation program\n"
            "  • Apne Aap Women Worldwide: Economic empowerment\n"
            "  • Restore India: vocational training for survivors"
        )
    },

    # =========================================================================
    # CATEGORY 8: EMERGENCY ASSISTANCE
    # =========================================================================

    "KB031": {
        "category": "emergency_assistance",
        "intent": "immediate_danger",
        "priority": 1,
        "keywords": ["help me", "emergency", "danger", "trapped", "i am in danger", "help now",
                     "immediate help", "urgent", "scared", "held"],
        "user_queries": [
            "I am in danger right now",
            "help me I am trapped",
            "I need immediate help",
            "I am being held against my will",
            "emergency help trafficking"
        ],
        "response": (
            "⚠️  EMERGENCY — CALL THESE NUMBERS RIGHT NOW ⚠️\n\n"
            "  🆘 Police Emergency:    100  (24/7, FREE)\n"
            "  🆘 Childline:          1098  (24/7, FREE, for children)\n"
            "  🆘 Women's Helpline:   1091  (24/7, FREE)\n"
            "  🆘 NHRC Helpline:     14433\n\n"
            "IF YOU CANNOT CALL:\n"
            "  • Send a WhatsApp message to a trusted person with your location\n"
            "  • Text 'HELP' to anyone who can call police on your behalf\n"
            "  • Signal to someone nearby — wave, write a note, use eye contact\n"
            "  • If near a public place, try to approach a shopkeeper or security guard\n\n"
            "STAY SAFE:\n"
            "  • Do NOT confront your captor directly\n"
            "  • Do NOT run if it puts you in greater danger\n"
            "  • Comply until you have a safe opportunity to escape\n"
            "  • Remember: Your life is more important than any documents"
        )
    },

    "KB032": {
        "category": "emergency_assistance",
        "intent": "escape_planning",
        "priority": 1,
        "keywords": ["escape", "run away", "how to escape", "get out", "leave", "flee",
                     "safe exit", "plan to leave"],
        "user_queries": [
            "how do I escape trafficking",
            "how to safely leave",
            "escape plan from trafficker",
            "how to get away from captor",
            "plan to escape"
        ],
        "response": (
            "Safe Escape Planning — Step by Step:\n\n"
            "BEFORE YOU LEAVE:\n"
            "  1. Wait for the right opportunity (captor absent or distracted)\n"
            "  2. Memorize or note down important phone numbers\n"
            "  3. Know the address or area you are in (look at street signs, landmarks)\n"
            "  4. Identify exits from the building\n"
            "  5. Do not take unnecessary risks — wait for a safe window\n\n"
            "WHEN YOU LEAVE:\n"
            "  1. Go to a public, crowded place immediately\n"
            "  2. Approach a shopkeeper, security guard, or person in uniform\n"
            "  3. Ask them to call police (100) or Childline (1098)\n"
            "  4. Tell them 'I need help — I have been trafficked'\n"
            "  5. Do not return to the location\n\n"
            "AFTER ESCAPE:\n"
            "  1. Seek medical attention if needed\n"
            "  2. Do not shower before medical exam if assaulted (evidence)\n"
            "  3. Cooperate with police\n"
            "  4. Ask for a lawyer and victim advocate\n"
            "  5. Contact family when it is safe to do so"
        )
    },

    "KB033": {
        "category": "emergency_assistance",
        "intent": "safety_signals",
        "priority": 2,
        "keywords": ["signal", "code word", "silent help", "call for help", "signal police",
                     "sign for help"],
        "user_queries": [
            "how to signal for help silently",
            "secret signal for trafficking",
            "how to call for help without being heard",
            "signal to police without talking"
        ],
        "response": (
            "Silent Help Signals and Codes:\n\n"
            "SIGNAL FOR HELP HAND SIGN:\n"
            "  1. Hold your hand up with palm facing out\n"
            "  2. Tuck your thumb across your palm\n"
            "  3. Fold your fingers down over the thumb\n"
            "  This 'Signal for Help' is recognized internationally\n\n"
            "IF CALLING EMERGENCY SERVICES:\n"
            "  • If you cannot speak: Call 112 and tap or breathe into phone\n"
            "  • Operator will attempt to locate you\n"
            "  • Stay on the line even if you cannot speak\n\n"
            "NOTES OR MESSAGES:\n"
            "  • Write 'CALL POLICE' on a piece of paper\n"
            "  • Slip it to someone when your captor isn't watching\n"
            "  • Leave notes in bathrooms in public places\n\n"
            "IN A SHOP OR RESTAURANT:\n"
            "  • Ask to 'order a pizza' (known internationally as a distress signal)\n"
            "  • Ask for 'Angela' (bar code for women needing help in many places)"
        )
    },

    "KB034": {
        "category": "emergency_assistance",
        "intent": "just_escaped",
        "priority": 1,
        "keywords": ["just escaped", "recently escaped", "got out", "free now", "just got away",
                     "what now", "after escape"],
        "user_queries": [
            "I just escaped what should I do",
            "I got away from traffickers",
            "I am free now what do I do",
            "just escaped trafficking",
            "escaped what are next steps"
        ],
        "response": (
            "You Are Safe Now — Immediate Next Steps:\n\n"
            "FIRST PRIORITY — YOUR PHYSICAL SAFETY:\n"
            "  1. Get to a safe, public location\n"
            "  2. Contact police (100) or Childline (1098) immediately\n"
            "  3. Tell them you have escaped a trafficking situation\n\n"
            "MEDICAL:\n"
            "  4. Seek medical attention at the nearest government hospital (free)\n"
            "  5. If sexually assaulted: Do not bathe before medical examination\n"
            "     (evidence is important for your case)\n\n"
            "LEGAL:\n"
            "  6. You are a VICTIM — you will not be arrested\n"
            "  7. Request a free lawyer from District Legal Services Authority\n"
            "  8. Request a female officer if you are more comfortable\n\n"
            "SHELTER:\n"
            "  9. Ask for a shelter home (Ujjawala/Swadhar) if you cannot go home\n"
            "  10. NGOs like Prerana and Shakti Vahini can assist immediately\n\n"
            "FAMILY:\n"
            "  11. Contact family when you feel it is safe to do so\n"
            "  12. A social worker can help facilitate contact"
        )
    },

    "KB035": {
        "category": "emergency_assistance",
        "intent": "someone_else_in_danger",
        "priority": 1,
        "keywords": ["someone else", "my friend", "my sister", "relative", "I think",
                     "neighbor", "i know someone", "report for someone"],
        "user_queries": [
            "I think someone I know is being trafficked",
            "my friend might be a trafficking victim",
            "how to help someone in trafficking",
            "my sister is missing and I think she was trafficked"
        ],
        "response": (
            "Helping Someone You Believe Is Being Trafficked:\n\n"
            "DO NOT:\n"
            "  ✗ Confront the suspected trafficker\n"
            "  ✗ Attempt a solo rescue — this is dangerous\n"
            "  ✗ Pressure the victim to leave before they are ready\n\n"
            "DO:\n"
            "  ✓ Stay calm and maintain contact with the potential victim (if safe)\n"
            "  ✓ Note and document what you have observed\n"
            "  ✓ Report to authorities with as much detail as possible:\n"
            "    - Person's description\n"
            "    - Last known location\n"
            "    - Suspected trafficker's description\n"
            "    - Any vehicle details\n\n"
            "REPORT TO:\n"
            "  • Police: 100\n"
            "  • Childline (if a child): 1098\n"
            "  • Anti-Human Trafficking Unit: Contact via local police\n"
            "  • Shakti Vahini: +91-11-43062100\n\n"
            "MISSING PERSON:\n"
            "  • File a Missing Person FIR immediately — police MUST accept it\n"
            "  • TrackChild Portal: trackthemissingchild.gov.in"
        )
    },

    # =========================================================================
    # CATEGORY 9: REPORTING PROCEDURES
    # =========================================================================

    "KB036": {
        "category": "reporting_procedures",
        "intent": "how_to_report_police",
        "priority": 1,
        "keywords": ["report", "police", "FIR", "complaint", "file", "how to report", "go to police"],
        "user_queries": [
            "how to report human trafficking to police",
            "how to file an FIR for trafficking",
            "reporting trafficking to authorities",
            "what to say to police",
            "go to police for trafficking"
        ],
        "response": (
            "How to Report to Police — Step by Step:\n\n"
            "STEP 1: Go to the nearest Police Station\n"
            "  • You can go to ANY police station — they must accept your complaint\n"
            "  • They cannot refuse to file an FIR for trafficking\n\n"
            "STEP 2: Ask for an FIR (First Information Report)\n"
            "  • Say: 'I want to file an FIR under Section 370 IPC for human trafficking'\n"
            "  • An FIR must be filed free of charge\n\n"
            "STEP 3: Provide Details\n"
            "  • Trafficker's name/description (if known)\n"
            "  • Location where victim is/was held\n"
            "  • Timeline of events\n"
            "  • Names of other victims (if known)\n\n"
            "STEP 4: Get a Copy\n"
            "  • Demand a copy of the FIR — it is your legal right\n"
            "  • Keep the FIR number safe\n\n"
            "IF POLICE REFUSE:\n"
            "  • Contact the Superintendent of Police (SP) or SSP\n"
            "  • File an online complaint: complaints.policeonline.in\n"
            "  • Contact the State Human Rights Commission\n"
            "  • Report to NHRC: 14433"
        )
    },

    "KB037": {
        "category": "reporting_procedures",
        "intent": "report_childline",
        "priority": 1,
        "keywords": ["childline", "1098", "child report", "child help", "childline report"],
        "user_queries": [
            "how to contact childline",
            "how to use 1098",
            "childline reporting",
            "report child trafficking to childline"
        ],
        "response": (
            "Childline India — 1098:\n\n"
            "WHAT IS CHILDLINE:\n"
            "  • India's first 24-hour, free, emergency phone helpline for children in crisis\n"
            "  • Operates in 500+ cities across India\n"
            "  • Managed by Childline India Foundation (CIF)\n\n"
            "WHEN TO CALL 1098:\n"
            "  • Child is being abused or is in danger\n"
            "  • Child has been trafficked or is missing\n"
            "  • Child marriage is about to happen or has happened\n"
            "  • Child is in need of shelter, food, or medical help\n"
            "  • Child is being exploited for labour or begging\n\n"
            "HOW TO CALL:\n"
            "  • Dial 1098 from any phone (landline or mobile)\n"
            "  • The call is FREE from any network\n"
            "  • Available 24 hours, 7 days a week, 365 days\n"
            "  • You can report anonymously\n\n"
            "WHAT HAPPENS AFTER:\n"
            "  • Childline team arrives at the location\n"
            "  • Child is taken to safety\n"
            "  • Medical care and counseling provided\n"
            "  • Police involvement coordinated"
        )
    },

    "KB038": {
        "category": "reporting_procedures",
        "intent": "report_online_crime",
        "priority": 2,
        "keywords": ["online crime", "cyber crime", "online trafficking", "report online",
                     "cybercrime portal", "digital crime"],
        "user_queries": [
            "report online trafficking",
            "how to report cyber crime related to trafficking",
            "online reporting for trafficking",
            "cybercrime report"
        ],
        "response": (
            "Reporting Online Crimes Related to Trafficking:\n\n"
            "NATIONAL CYBER CRIME REPORTING PORTAL:\n"
            "  Website: cybercrime.gov.in\n"
            "  Helpline: 1930\n"
            "  For: Online trafficking, grooming, CSAM, sextortion\n\n"
            "HOW TO REPORT ONLINE:\n"
            "  1. Go to cybercrime.gov.in\n"
            "  2. Click 'Report Other Cyber Crimes'\n"
            "  3. Register/login (or report anonymously for some categories)\n"
            "  4. Select 'Child Sexual Abuse Material' or 'Human Trafficking'\n"
            "  5. Upload screenshots/evidence\n"
            "  6. Submit and note your complaint number\n\n"
            "FOR CHILD SEXUAL ABUSE MATERIAL (CSAM):\n"
            "  • Report at: cybercrime.gov.in (click 'Report & Track')\n"
            "  • NCMEC: cybertipline.org (international platform)\n\n"
            "SOCIAL MEDIA PLATFORMS:\n"
            "  • Instagram: Report profile → 'Human exploitation'\n"
            "  • Facebook: Report → 'Violence and Criminal Behaviour'\n"
            "  • WhatsApp: Block + Report contact"
        )
    },

    "KB039": {
        "category": "reporting_procedures",
        "intent": "report_nhrc",
        "priority": 3,
        "keywords": ["NHRC", "human rights commission", "national", "rights violation", "14433"],
        "user_queries": [
            "how to complain to NHRC",
            "NHRC trafficking complaint",
            "national human rights commission complaint"
        ],
        "response": (
            "National Human Rights Commission (NHRC) — India:\n\n"
            "WHAT NHRC DOES:\n"
            "  • Investigates human rights violations\n"
            "  • Can issue summons to state governments\n"
            "  • Can recommend compensation for victims\n"
            "  • Monitors places of detention and shelter homes\n\n"
            "HOW TO COMPLAIN:\n"
            "  Helpline: 14433\n"
            "  Online: nhrc.nic.in → 'Complaint Registration'\n"
            "  Post: Manav Adhikar Bhawan, Block-C, GPO Complex,\n"
            "        INA, New Delhi – 110023\n\n"
            "INFORMATION TO INCLUDE:\n"
            "  • Name, address, and contact of the complainant\n"
            "  • Nature of human rights violation\n"
            "  • Name of the public official/authority involved\n"
            "  • Date and location of the incident\n"
            "  • Steps already taken (FIR, court case, etc.)\n\n"
            "NOTE: NHRC does not take up cases older than 1 year\n"
            "unless exceptional reasons are provided."
        )
    },

    "KB040": {
        "category": "reporting_procedures",
        "intent": "anonymous_reporting",
        "priority": 2,
        "keywords": ["anonymous", "without name", "safely report", "confidential report",
                     "report without revealing identity"],
        "user_queries": [
            "can I report anonymously",
            "report trafficking without giving my name",
            "how to report safely and confidentially",
            "anonymous reporting options"
        ],
        "response": (
            "Anonymous Reporting Options:\n\n"
            "YES — you can report anonymously through several channels:\n\n"
            "  1. CHILDLINE 1098\n"
            "     You do not need to give your name\n\n"
            "  2. POLICE (100)\n"
            "     You can provide information without filing a formal FIR\n"
            "     (though FIR requires identification for formal proceedings)\n\n"
            "  3. CYBERCRIME PORTAL (cybercrime.gov.in)\n"
            "     Some categories allow anonymous reporting\n\n"
            "  4. NGO TIPLINES:\n"
            "     • Shakti Vahini: +91-11-43062100 (anonymous tips accepted)\n"
            "     • Prerana: tips accepted without identification\n\n"
            "  5. IWATCH (Ministry of Home Affairs):\n"
            "     • mha.gov.in/division_of_mha/counter-terrorism-and-counter-radicalization-division/iwatch\n"
            "     • Can report suspicious activity anonymously\n\n"
            "YOUR SAFETY MATTERS:\n"
            "  • If you fear retaliation, request witness protection\n"
            "  • Police can arrange safe reporting locations"
        )
    },

    # =========================================================================
    # CATEGORY 10: LEGAL RIGHTS
    # =========================================================================

    "KB041": {
        "category": "legal_rights",
        "intent": "india_trafficking_laws",
        "priority": 1,
        "keywords": ["law", "IPC", "legal", "section 370", "ITPA", "act", "punishment",
                     "penalty", "criminal law", "legislation"],
        "user_queries": [
            "what laws cover human trafficking in india",
            "trafficking laws india",
            "section 370 IPC",
            "punishment for trafficking in india",
            "legal framework trafficking"
        ],
        "response": (
            "Key Indian Laws on Human Trafficking:\n\n"
            "1. SECTION 370, IPC (as amended 2013)\n"
            "   Scope: Comprehensive law covering all forms of trafficking\n"
            "   Punishment:\n"
            "     • Basic trafficking: 7–10 years rigorous imprisonment + fine\n"
            "     • Trafficking of child: 10 years to life + fine\n"
            "     • Trafficking by public servant: 10 years to life\n"
            "     • Habitual offender: Life imprisonment\n\n"
            "2. IMMORAL TRAFFIC PREVENTION ACT (ITPA), 1956\n"
            "   Scope: Specifically targets sex trafficking and prostitution\n"
            "   Punishment: Up to 7 years imprisonment\n\n"
            "3. POCSO ACT, 2012\n"
            "   Scope: Protection of children from sexual offences\n"
            "   Punishment: Minimum 7 years, up to life\n\n"
            "4. CHILD LABOUR (P&R) ACT, 1986\n"
            "   Scope: Prohibits employment of children under 14 in hazardous work\n\n"
            "5. BONDED LABOUR SYSTEM (ABOLITION) ACT, 1976\n"
            "   Scope: Abolishes bonded labour; all bonded debts are void\n\n"
            "6. JUVENILE JUSTICE ACT, 2015\n"
            "   Scope: Care and protection of children in conflict with law"
        )
    },

    "KB042": {
        "category": "legal_rights",
        "intent": "international_law",
        "priority": 3,
        "keywords": ["international law", "UN protocol", "Palermo", "UNCRC", "international",
                     "global law", "convention"],
        "user_queries": [
            "international laws on trafficking",
            "UN palermo protocol",
            "global trafficking laws",
            "international conventions on trafficking"
        ],
        "response": (
            "International Legal Framework:\n\n"
            "1. UN PALERMO PROTOCOL (2000)\n"
            "   Full name: Protocol to Prevent, Suppress and Punish Trafficking in Persons\n"
            "   • First legally binding international instrument on trafficking\n"
            "   • Defines trafficking internationally\n"
            "   • Signed by 170+ countries including India\n\n"
            "2. UN CONVENTION ON THE RIGHTS OF THE CHILD (UNCRC), 1989\n"
            "   • Article 34: Protection from sexual exploitation\n"
            "   • Article 35: Protection from sale, trafficking, abduction of children\n\n"
            "3. ILO CONVENTION 182 (1999)\n"
            "   • Worst forms of child labour, including trafficking, must be eliminated\n\n"
            "4. SUSTAINABLE DEVELOPMENT GOALS (SDGs)\n"
            "   • Goal 8.7: End forced labour, trafficking, and child labour by 2025\n"
            "   • Goal 5.2: Eliminate violence against women and girls\n\n"
            "5. SAARC CONVENTION ON PREVENTING TRAFFICKING (2002)\n"
            "   • Regional framework for South Asia\n"
            "   • India is a signatory"
        )
    },

    "KB043": {
        "category": "legal_rights",
        "intent": "victim_not_criminal",
        "priority": 1,
        "keywords": ["arrested", "criminal", "prosecution", "charged", "illegal",
                     "am i in trouble", "illegal immigrant"],
        "user_queries": [
            "will I be arrested if I report",
            "am I a criminal",
            "I was forced to do illegal things",
            "can I be prosecuted as a victim",
            "I am afraid of arrest"
        ],
        "response": (
            "Trafficking Victims Are NOT Criminals:\n\n"
            "IF YOU WERE FORCED TO DO SOMETHING ILLEGAL:\n"
            "  • Under Indian law, actions taken under coercion are NOT criminal\n"
            "  • Courts recognize 'coercion' as a complete defence\n"
            "  • You cannot be prosecuted for crimes committed because you were trafficked\n\n"
            "FOR FOREIGN NATIONALS:\n"
            "  • You will NOT be deported immediately if you are a trafficking victim\n"
            "  • You have the right to remain in India for the duration of legal proceedings\n"
            "  • Your embassy must be notified (they can help you)\n\n"
            "FOR UNDOCUMENTED WORKERS:\n"
            "  • If you are a trafficking victim, immigration enforcement can be paused\n"
            "  • This is known as 'humanitarian grounds' protection\n\n"
            "WHAT TO SAY TO POLICE:\n"
            "  'I am a victim of human trafficking. I was forced to [action].\n"
            "   I want to cooperate and report the people who did this to me.'\n\n"
            "Request a free lawyer immediately from DLSA."
        )
    },

    "KB044": {
        "category": "legal_rights",
        "intent": "compensation_rights",
        "priority": 2,
        "keywords": ["compensation", "money", "payment", "damages", "claim", "relief fund"],
        "user_queries": [
            "can trafficking victims get compensation",
            "financial help for victims",
            "compensation scheme trafficking india",
            "how to claim victim compensation"
        ],
        "response": (
            "Compensation Rights for Trafficking Victims:\n\n"
            "NALSA VICTIM COMPENSATION SCHEME:\n"
            "  • National Legal Services Authority runs a Victim Compensation Scheme\n"
            "  • Trafficking victims are entitled to compensation\n"
            "  • Apply to the State Legal Services Authority (SLSA) in your state\n\n"
            "COMPENSATION AMOUNTS (vary by state):\n"
            "  • Sexual assault/rape: ₹3–10 lakhs\n"
            "  • Child trafficking: ₹5–7 lakhs\n"
            "  • Labour trafficking: ₹1–3 lakhs\n\n"
            "HOW TO CLAIM:\n"
            "  1. File an FIR with police\n"
            "  2. Apply through your free lawyer (DLSA) to the SLSA\n"
            "  3. Or directly apply to the District Legal Services Authority\n\n"
            "NIRBHAYA FUND:\n"
            "  • Government fund for women and children victims of violence\n"
            "  • Funds Ujjawala, OSCs, and other rehabilitation programs\n\n"
            "NGO SUPPORT:\n"
            "  • Some NGOs provide emergency cash assistance — ask at shelter"
        )
    },

    "KB045": {
        "category": "legal_rights",
        "intent": "witness_protection",
        "priority": 2,
        "keywords": ["witness protection", "safe testimony", "fear of testifying",
                     "protect witness", "afraid to testify"],
        "user_queries": [
            "can I be protected as a witness",
            "witness protection for trafficking victims",
            "I am afraid to testify",
            "how to testify safely"
        ],
        "response": (
            "Witness Protection for Trafficking Victims:\n\n"
            "WITNESS PROTECTION SCHEME, 2018:\n"
            "  • India's first formal witness protection scheme\n"
            "  • Available for witnesses in cases involving serious crimes including trafficking\n"
            "  • Apply to the State Witness Protection Scheme Committee\n\n"
            "PROTECTION MEASURES AVAILABLE:\n"
            "  • Changing identity documents\n"
            "  • Relocation of witness and family\n"
            "  • Safe house accommodation\n"
            "  • Police protection during trial\n"
            "  • In-camera testimony (testify without public present)\n"
            "  • Screen/curtain to hide identity in court\n"
            "  • Video conferencing testimony\n\n"
            "HOW TO REQUEST:\n"
            "  1. Inform the investigating police officer or public prosecutor\n"
            "  2. Apply through your lawyer to the District Court\n"
            "  3. The court evaluates the threat level\n\n"
            "ADDITIONAL PROTECTION:\n"
            "  • Your name CANNOT be published in media\n"
            "  • Your address is not disclosed in court records"
        )
    },

    # =========================================================================
    # CATEGORY 11: SAFETY MEASURES
    # =========================================================================

    "KB046": {
        "category": "safety_measures",
        "intent": "personal_safety_tips",
        "priority": 1,
        "keywords": ["safety tips", "protect myself", "stay safe", "personal safety",
                     "prevention tips", "how to be safe"],
        "user_queries": [
            "how to protect myself from trafficking",
            "personal safety tips",
            "how to stay safe",
            "trafficking prevention tips for myself"
        ],
        "response": (
            "Personal Safety Tips — Protect Yourself:\n\n"
            "TRAVEL SAFETY:\n"
            "  ✓ Always share your travel plans with a trusted family member\n"
            "  ✓ Keep a copy of all documents with a trusted person\n"
            "  ✓ Memorize at least one emergency phone number\n"
            "  ✓ Stay in contact regularly when away from home\n"
            "  ✓ Use registered, reputable transport\n\n"
            "DIGITAL SAFETY:\n"
            "  ✓ Never share personal photos or location online\n"
            "  ✓ Verify identities of people met online\n"
            "  ✓ Be suspicious of too-good-to-be-true offers\n"
            "  ✓ Keep privacy settings strict on all platforms\n\n"
            "DOCUMENT SAFETY:\n"
            "  ✓ NEVER give your passport or Aadhaar to an employer\n"
            "  ✓ Keep originals; provide certified copies only\n"
            "  ✓ Register documents at the local police station if travelling abroad\n\n"
            "JOB SAFETY:\n"
            "  ✓ Research any employer thoroughly before accepting\n"
            "  ✓ Always sign a written contract\n"
            "  ✓ Never pay fees to get a job\n"
            "  ✓ Ensure someone knows your workplace address"
        )
    },

    "KB047": {
        "category": "safety_measures",
        "intent": "community_prevention",
        "priority": 3,
        "keywords": ["community", "prevention", "awareness", "educate", "campaign",
                     "neighbourhood", "village"],
        "user_queries": [
            "how to prevent trafficking in community",
            "community awareness about trafficking",
            "spread awareness about trafficking",
            "how can I help prevent trafficking"
        ],
        "response": (
            "Community-Level Trafficking Prevention:\n\n"
            "AWARENESS ACTIONS:\n"
            "  ✓ Share factual information about trafficking in your social circle\n"
            "  ✓ Organize awareness sessions in schools and colleges\n"
            "  ✓ Display helpline numbers (1098, 100) in public spaces\n"
            "  ✓ Counter myths about trafficking\n\n"
            "COMMUNITY NETWORKS:\n"
            "  ✓ Form or join a neighbourhood watch\n"
            "  ✓ Identify and support vulnerable families\n"
            "  ✓ Help connect vulnerable youth with educational opportunities\n"
            "  ✓ Report suspicious recruitment activity\n\n"
            "PANCHAYAT / LOCAL GOVERNMENT:\n"
            "  ✓ Engage local leaders in anti-trafficking discussions\n"
            "  ✓ Request Child Protection Committees at village level\n"
            "  ✓ Participate in Gram Sabha discussions on child welfare\n\n"
            "PARTNER WITH NGOS:\n"
            "  • Apne Aap, CRY, Bachpan Bachao Andolan (BBA)\n"
            "  • These organizations support community-level prevention"
        )
    },

    "KB048": {
        "category": "safety_measures",
        "intent": "safety_for_migrants",
        "priority": 2,
        "keywords": ["migrant", "migration", "moving", "move city", "new city",
                     "rural to urban", "interstate", "work migration"],
        "user_queries": [
            "safety for migrant workers",
            "safety when moving for work",
            "how to be safe as a migrant",
            "protection for workers migrating"
        ],
        "response": (
            "Safety Measures for Migrant Workers:\n\n"
            "BEFORE YOU MIGRATE:\n"
            "  ✓ Verify the employer through official channels\n"
            "  ✓ Get a written contract in your language\n"
            "  ✓ Share employer name, address, and contact with family\n"
            "  ✓ Know the address and phone of local police at destination\n"
            "  ✓ Register with the Labour Department (for inter-state migrants)\n"
            "  ✓ Keep certified copies of all documents with a trusted person\n\n"
            "INTER-STATE MIGRANT WORKMEN ACT, 1979:\n"
            "  • Employers must register inter-state workers\n"
            "  • Workers entitled to same wages as local workers\n"
            "  • Accommodation and transport must be provided\n\n"
            "AFTER ARRIVING:\n"
            "  ✓ Contact family within 24 hours of arrival\n"
            "  ✓ Note down your exact work address\n"
            "  ✓ Build connections with other workers\n"
            "  ✓ Know: You can ALWAYS leave a job — no 'locked contract' is legal\n\n"
            "HELPLINES:\n"
            "  • Labour Department: 1800-425-1013 (toll free)\n"
            "  • NHRC: 14433"
        )
    },

    # =========================================================================
    # CATEGORY 12: NGO SUPPORT
    # =========================================================================

    "KB049": {
        "category": "ngo_support",
        "intent": "national_ngos",
        "priority": 2,
        "keywords": ["NGO", "organization", "help organization", "support organization",
                     "who can help", "anti trafficking organization"],
        "user_queries": [
            "which NGOs work on trafficking in India",
            "organizations that help trafficking victims",
            "anti trafficking NGOs India",
            "where to get help from NGO"
        ],
        "response": (
            "Major Anti-Trafficking NGOs in India:\n\n"
            "SHAKTI VAHINI\n"
            "  Focus: Rescue, rehabilitation, legal aid\n"
            "  Phone: +91-11-43062100\n"
            "  Web: shaktivahini.org\n\n"
            "PRERANA (Mumbai)\n"
            "  Focus: Child trafficking survivors, sex trafficking\n"
            "  Phone: +91-22-23720856\n"
            "  Web: preranaantitrafficking.org\n\n"
            "APNE AAP WOMEN WORLDWIDE\n"
            "  Focus: Women in prostitution, trafficking prevention\n"
            "  Phone: +91-11-26584836\n"
            "  Web: apneaap.org\n\n"
            "BACHPAN BACHAO ANDOLAN (BBA) — Kailash Satyarthi\n"
            "  Focus: Child labour, child trafficking rescue\n"
            "  Phone: +91-11-29217313\n"
            "  Web: bba.org.in\n\n"
            "JAN SAHAS\n"
            "  Focus: Bonded labour, forced labour rescue\n"
            "  Web: jansahas.in\n\n"
            "STOP TRAFFICKING AND OPPRESSION OF CHILDREN & WOMEN (STOP)\n"
            "  Focus: Northeast India trafficking\n\n"
            "RESTORE INDIA\n"
            "  Focus: Survivor rehabilitation and training"
        )
    },

    "KB050": {
        "category": "ngo_support",
        "intent": "government_helplines",
        "priority": 1,
        "keywords": ["helpline", "toll free", "call", "number", "contact", "hotline",
                     "government help"],
        "user_queries": [
            "government helplines for trafficking",
            "toll free numbers trafficking",
            "helpline numbers for victims",
            "emergency contact numbers india"
        ],
        "response": (
            "Government Helplines and Emergency Numbers:\n\n"
            "══════════════════════════════════════════\n"
            "  🆘 Police Emergency          :  100\n"
            "  🆘 Childline India           :  1098\n"
            "  🆘 Women's Helpline          :  1091\n"
            "  🆘 NHRC Helpline             :  14433\n"
            "  🆘 National Emergency        :  112\n"
            "  🆘 Cyber Crime               :  1930\n"
            "  🆘 Labour Helpline           :  1800-425-1013\n"
            "  🆘 Anti-Poisoning/Emergency  :  1066\n"
            "  🆘 Women's One Stop Centre   :  181\n"
            "══════════════════════════════════════════\n\n"
            "MENTAL HEALTH:\n"
            "  • Vandrevala Foundation: 1860-2662-345\n"
            "  • iCall (TISS): 9152987821\n"
            "  • Snehi: 044-24640050\n\n"
            "LEGAL AID:\n"
            "  • NALSA: 15100\n"
            "  • District Legal Services Authority: Contact district court"
        )
    },

    "KB051": {
        "category": "ngo_support",
        "intent": "shelter_homes",
        "priority": 2,
        "keywords": ["shelter", "safe house", "where to go", "safe place", "temporary home",
                     "refuge", "accommodation"],
        "user_queries": [
            "where can trafficking victims stay",
            "shelter homes for trafficking survivors",
            "safe houses for victims",
            "where to go after escaping trafficking"
        ],
        "response": (
            "Shelter and Safe Accommodation:\n\n"
            "GOVERNMENT SHELTERS:\n\n"
            "  UJJAWALA SHELTER HOMES\n"
            "    • Specifically for trafficking victims\n"
            "    • Services: Shelter, food, counseling, legal aid, vocational training\n"
            "    • Contact: Ministry of Women & Child Development, 011-23388601\n\n"
            "  SWADHAR GREH\n"
            "    • For women in difficult circumstances\n"
            "    • Short-term shelter and support\n"
            "    • Contact: WCD district offices\n\n"
            "  SHORT STAY HOMES\n"
            "    • Run by state governments\n"
            "    • Temporary refuge for women and children\n\n"
            "NGO SHELTER HOMES:\n"
            "  • Prerana (Mumbai): +91-22-23720856\n"
            "  • Shakti Vahini (Delhi): +91-11-43062100\n"
            "  • CINI India (Kolkata): 1800-103-1616\n\n"
            "HOW TO ACCESS:\n"
            "  1. Call Childline 1098 — they will arrange shelter\n"
            "  2. Contact nearest NGO\n"
            "  3. Ask police to refer you to an Ujjawala shelter\n"
            "  4. District Magistrate can order shelter admission"
        )
    },

    # =========================================================================
    # CATEGORY 13: FAQs
    # =========================================================================

    "KB052": {
        "category": "faqs",
        "intent": "faq_can_men_be_trafficked",
        "priority": 3,
        "keywords": ["men", "male", "boy", "man", "male victim", "trafficking men"],
        "user_queries": [
            "can men be trafficked",
            "are men victims of trafficking",
            "male trafficking victims",
            "boy trafficking"
        ],
        "response": (
            "FAQ: Can Men and Boys Be Trafficked?\n\n"
            "YES — Absolutely. Men and boys are also victims of trafficking.\n\n"
            "Men and boys are commonly trafficked for:\n"
            "  • Forced labour (construction, agriculture, fishing, factories)\n"
            "  • Sexual exploitation (less reported due to stigma)\n"
            "  • Forced begging\n"
            "  • Forced criminality\n"
            "  • Organ trafficking\n\n"
            "The ILO estimates that 29% of trafficking victims globally are men and boys.\n\n"
            "BARRIERS TO REPORTING FOR MEN:\n"
            "  • Social stigma and shame\n"
            "  • Fear of not being believed\n"
            "  • Limited support services for male victims\n\n"
            "SUPPORT AVAILABLE:\n"
            "  All helplines accept male callers:\n"
            "  • Police: 100\n"
            "  • NHRC: 14433\n"
            "  • Childline (for boys under 18): 1098\n"
            "  You deserve help. Your experience is valid."
        )
    },

    "KB053": {
        "category": "faqs",
        "intent": "faq_consent_and_trafficking",
        "priority": 2,
        "keywords": ["consent", "agreed", "willing", "I said yes", "went voluntarily",
                     "I agreed", "chose to go"],
        "user_queries": [
            "I agreed to go so is it still trafficking",
            "can consent make trafficking not a crime",
            "I went willingly is it still trafficking",
            "does consent mean it is not trafficking"
        ],
        "response": (
            "FAQ: Does Consent Affect Trafficking?\n\n"
            "NO — Initial consent does NOT mean it is not trafficking.\n\n"
            "WHY CONSENT DOESN'T MATTER:\n"
            "  • If you were deceived (false job offer, fake relationship),\n"
            "    your 'consent' was obtained fraudulently — it is void.\n"
            "  • If you consented but are then exploited, the exploitation\n"
            "    itself is the crime.\n"
            "  • Traffickers count on you thinking 'I agreed, so I can't complain.'\n"
            "    This is false.\n\n"
            "UN PALERMO PROTOCOL SAYS:\n"
            "  'Consent of the victim to the intended exploitation shall be\n"
            "   irrelevant where any of the means of trafficking have been used.'\n\n"
            "FOR CHILDREN:\n"
            "  A child's consent to trafficking is NEVER valid, regardless of\n"
            "  circumstances. The law protects children absolutely.\n\n"
            "YOU ARE A VICTIM. SEEK HELP WITHOUT SHAME."
        )
    },

    "KB054": {
        "category": "faqs",
        "intent": "faq_what_if_no_documents",
        "priority": 2,
        "keywords": ["no documents", "no ID", "no passport", "documents taken",
                     "no Aadhaar", "without papers"],
        "user_queries": [
            "my documents were taken what do I do",
            "I have no ID can I still get help",
            "trafficker took my passport",
            "can I report without documents"
        ],
        "response": (
            "FAQ: What If My Documents Were Taken?\n\n"
            "YOU CAN STILL GET HELP — documents are NOT required:\n\n"
            "  1. REPORT TO POLICE (100)\n"
            "     You do not need an ID to report. Police will accept your complaint\n"
            "     and record your testimony.\n\n"
            "  2. CHILDLINE (1098)\n"
            "     No documentation needed — just call.\n\n"
            "  3. RECOVERING YOUR DOCUMENTS:\n"
            "     • Your employer/recruiter holding your documents is ILLEGAL under\n"
            "       Section 344 IPC (wrongful confinement) and relevant trafficking laws\n"
            "     • Police can recover your documents as part of investigation\n"
            "     • Aadhaar: Re-enroll at any Aadhaar centre (free)\n"
            "     • Passport: Report to nearest Passport Seva Kendra / Indian Embassy\n\n"
            "  4. LEGAL AID:\n"
            "     A free lawyer from DLSA can help you recover documents\n\n"
            "REMEMBER: The person who took your documents committed a CRIME."
        )
    },

    "KB055": {
        "category": "faqs",
        "intent": "faq_difference_trafficking_exploitation",
        "priority": 3,
        "keywords": ["exploitation", "abuse", "difference", "what counts", "is this trafficking"],
        "user_queries": [
            "is what I am going through trafficking",
            "difference between exploitation and trafficking",
            "is this considered trafficking",
            "am I being trafficked"
        ],
        "response": (
            "FAQ: Is What I'm Experiencing Trafficking?\n\n"
            "Ask yourself these questions:\n\n"
            "  1. Were you recruited with FALSE PROMISES?\n"
            "     (Different job, relationship, education than promised)\n\n"
            "  2. Are you being CONTROLLED or unable to leave freely?\n\n"
            "  3. Are you being FORCED to work or perform acts you don't want to?\n\n"
            "  4. Are you being THREATENED (yourself or your family)?\n\n"
            "  5. Has your FREEDOM been taken away in any way?\n\n"
            "  6. Are you being EXPLOITED (someone profits from your situation)?\n\n"
            "If you answered YES to ANY of these:\n"
            "  → Your situation may be trafficking or exploitation.\n"
            "  → You deserve help and protection.\n"
            "  → Contact AegisAI's risk assessment for a detailed evaluation.\n"
            "  → Call 1098 or 100 to speak with a professional.\n\n"
            "When in doubt — REACH OUT. A professional can help you understand\n"
            "your situation and options."
        )
    },

    "KB056": {
        "category": "faqs",
        "intent": "faq_family_member_trafficked",
        "priority": 2,
        "keywords": ["family", "mother", "father", "sibling", "relative", "trafficked family",
                     "my family member"],
        "user_queries": [
            "my family member was trafficked",
            "how to help a trafficked family member",
            "my relative might be trafficked",
            "I think my mother is being exploited"
        ],
        "response": (
            "FAQ: Helping a Trafficked Family Member:\n\n"
            "IMMEDIATE STEPS:\n\n"
            "  1. REPORT MISSING PERSON (if location unknown):\n"
            "     • Go to nearest police station\n"
            "     • File a Missing Person FIR — police MUST accept it\n"
            "     • TrackChild: trackthemissingchild.gov.in\n\n"
            "  2. SHARE INFORMATION WITH AUTHORITIES:\n"
            "     • Last known location\n"
            "     • Who they were last with\n"
            "     • Any job offers or travel they mentioned\n"
            "     • Photographs\n\n"
            "  3. CONTACT ANTI-TRAFFICKING UNITS:\n"
            "     • National Anti Human Trafficking Unit (NAHTU): via police\n"
            "     • Shakti Vahini: +91-11-43062100\n\n"
            "  4. CARE FOR YOURSELF TOO:\n"
            "     • This is an incredibly stressful situation\n"
            "     • Seek counseling support for yourself\n"
            "     • iCall: 9152987821\n\n"
            "  DO NOT:\n"
            "     ✗ Pay ransom to traffickers\n"
            "     ✗ Attempt to retrieve your family member alone\n"
            "     ✗ Negotiate with traffickers directly"
        )
    },

    "KB057": {
        "category": "faqs",
        "intent": "faq_how_long_does_help_take",
        "priority": 3,
        "keywords": ["how long", "time", "quick", "when", "process time", "wait"],
        "user_queries": [
            "how long does rescue take",
            "when will I get help",
            "how long does the process take",
            "how quickly can I get shelter"
        ],
        "response": (
            "FAQ: How Quickly Can You Get Help?\n\n"
            "EMERGENCY SITUATIONS:\n"
            "  • Call 100 (Police) or 1098 (Childline) — Response in 30–60 minutes\n"
            "  • If in immediate danger, these are your fastest options\n\n"
            "SHELTER ACCESS:\n"
            "  • Government shelters (Ujjawala): Can be accessed within 24 hours\n"
            "    via Childline or police referral\n"
            "  • NGO shelters: Often faster — same day in many cities\n\n"
            "MEDICAL HELP:\n"
            "  • Government hospitals must provide free emergency care\n"
            "  • Access immediately — no paperwork needed for emergency treatment\n\n"
            "LEGAL PROCESS:\n"
            "  • FIR filing: Same day\n"
            "  • Free lawyer: Within 24–48 hours via DLSA\n"
            "  • Court proceedings: These take longer (months to years)\n"
            "  • Compensation: Can take 3–6 months after application\n\n"
            "BE PERSISTENT — if one channel is slow, use another simultaneously."
        )
    },

    # =========================================================================
    # ADDITIONAL ENTRIES — Mix of categories to reach 100+
    # =========================================================================

    "KB058": {
        "category": "human_trafficking_basics",
        "intent": "trafficking_myths",
        "priority": 2,
        "keywords": ["myth", "misconception", "false", "stereotype", "not true", "believe"],
        "user_queries": [
            "myths about human trafficking",
            "common misconceptions about trafficking",
            "what people get wrong about trafficking"
        ],
        "response": (
            "Common Myths vs. Facts About Human Trafficking:\n\n"
            "MYTH: Trafficking only happens to women.\n"
            "FACT: Men, boys, and non-binary individuals are also trafficked.\n\n"
            "MYTH: Trafficking always involves crossing international borders.\n"
            "FACT: Most trafficking is domestic — it happens within one country.\n\n"
            "MYTH: Victims are always visibly chained or imprisoned.\n"
            "FACT: Control is often psychological — fear, debt, threats.\n\n"
            "MYTH: Victims always try to escape or ask for help.\n"
            "FACT: Trauma bonding, fear, and shame prevent many from seeking help.\n\n"
            "MYTH: Only poor or uneducated people are trafficked.\n"
            "FACT: Educated, middle-class people are also targeted.\n\n"
            "MYTH: You can always tell a trafficking victim by their appearance.\n"
            "FACT: Victims may be well-dressed and appear 'normal'.\n\n"
            "MYTH: If the victim agreed to go, it is not trafficking.\n"
            "FACT: Consent obtained through deception is not legally valid."
        )
    },

    "KB059": {
        "category": "recruitment_scams",
        "intent": "tech_scam_centres",
        "priority": 1,
        "keywords": ["tech scam", "crypto scam", "Myanmar", "Cambodia", "online job",
                     "work from home abroad", "fraud centre", "scam centre"],
        "user_queries": [
            "tech scam centre trafficking",
            "Cambodia Myanmar job scam",
            "online job scam abroad",
            "crypto trading job abroad scam",
            "work from home in foreign country"
        ],
        "response": (
            "⚠️ URGENT WARNING: Tech Scam Centre Trafficking ⚠️\n\n"
            "WHAT IS THIS:\n"
            "  A major new form of trafficking where victims are lured with\n"
            "  high-paying online jobs (crypto trading, customer service, tech support)\n"
            "  in Southeast Asia — then forced to commit cyber fraud.\n\n"
            "LOCATION: Primarily Myanmar, Cambodia, Laos, Thailand border regions\n\n"
            "HOW IT WORKS:\n"
            "  1. Job offer on LinkedIn, Facebook, or WhatsApp\n"
            "  2. High salary (₹1–2 lakhs/month) for 'online work'\n"
            "  3. Visa and flight arranged by 'company'\n"
            "  4. On arrival, passport confiscated\n"
            "  5. Forced to run crypto, romance, or investment scams\n"
            "  6. Physical violence if quota not met\n\n"
            "RED FLAGS:\n"
            "  🚩 Job is in Myanmar, Cambodia, Thailand, Laos, or border areas\n"
            "  🚩 Company arranges visa, accommodation, and transport\n"
            "  🚩 No formal company registration or address\n"
            "  🚩 Extremely high pay for 'typing' or 'online' work\n\n"
            "IF TRAPPED:\n"
            "  • Contact Indian Embassy immediately\n"
            "  • MEA Helpline: +91-11-23012113 or mea.gov.in"
        )
    },

    "KB060": {
        "category": "warning_signs",
        "intent": "domestic_worker_signs",
        "priority": 2,
        "keywords": ["domestic worker", "maid", "house", "nanny", "housekeeper", "caretaker signs"],
        "user_queries": [
            "signs a domestic worker is being exploited",
            "warning signs for domestic servants",
            "how to know if a maid is being trafficked"
        ],
        "response": (
            "Warning Signs of Domestic Servitude Trafficking:\n\n"
            "  • Worker appears fearful of employer\n"
            "  • Worker is not allowed to speak privately\n"
            "  • Worker does not eat with the family and gets leftovers\n"
            "  • Worker sleeps in the kitchen, storage room, or on the floor\n"
            "  • Worker is not allowed to go out alone\n"
            "  • Worker has no day off despite working 7 days a week\n"
            "  • Worker's wages are sent directly to a third party\n"
            "  • Worker does not have their own phone or access to communication\n"
            "  • Worker appears malnourished, unkempt, or has unexplained injuries\n"
            "  • Worker does not know the exact address of the house\n"
            "  • Children in the house describe worker as 'always there'\n\n"
            "If you are a domestic worker being exploited:\n"
            "  • Call 181 (Women's Helpline)\n"
            "  • Contact domestic workers' unions in your city\n"
            "  • Contact Prerana or Shakti Vahini for support"
        )
    },

    "KB061": {
        "category": "child_trafficking",
        "intent": "missing_child",
        "priority": 1,
        "keywords": ["missing child", "lost child", "child not home", "child disappeared",
                     "can't find child", "child gone"],
        "user_queries": [
            "my child is missing",
            "child has not come home",
            "child disappeared",
            "report missing child",
            "child gone missing what to do"
        ],
        "response": (
            "Missing Child — Immediate Actions:\n\n"
            "WITHIN THE FIRST HOUR:\n"
            "  1. Call Childline: 1098 immediately\n"
            "  2. Call Police: 100\n"
            "  3. Alert neighbours and community\n\n"
            "AT THE POLICE STATION:\n"
            "  • Go IMMEDIATELY — do not wait 24 hours\n"
            "  • Police MUST file a Missing Person report right away for children\n"
            "  • Bring: Recent photo, description of clothing, last known location\n"
            "  • Note down the FIR number\n\n"
            "ONLINE RESOURCES:\n"
            "  • TrackChild Portal: trackthemissingchild.gov.in\n"
            "  • Upload child's photo and information\n"
            "  • Police use this to match found children\n\n"
            "  • Khoya Paya Portal: khoyapaya.gov.in\n"
            "  • National database for missing/found children\n\n"
            "NGOs THAT HELP:\n"
            "  • Bachpan Bachao Andolan: +91-11-29217313\n"
            "  • Childline: 1098\n"
            "  • Shakti Vahini: +91-11-43062100\n\n"
            "SHARE ON SOCIAL MEDIA with recent photo and last known location."
        )
    },

    "KB062": {
        "category": "forced_labour",
        "intent": "construction_trafficking",
        "priority": 3,
        "keywords": ["construction", "builder", "site", "laborer", "construction worker",
                     "building site"],
        "user_queries": [
            "trafficking in construction",
            "forced labour construction site",
            "construction worker exploitation"
        ],
        "response": (
            "Forced Labour in Construction — What to Know:\n\n"
            "COMMON PATTERNS:\n"
            "  • Workers recruited from villages with advance payment\n"
            "  • Transported to distant cities far from home\n"
            "  • Live at the worksite in poor temporary shelters\n"
            "  • Wages are delayed or deducted endlessly\n"
            "  • Workers owe 'advance' and cannot leave\n"
            "  • No safety equipment or healthcare\n\n"
            "LEGAL RIGHTS OF CONSTRUCTION WORKERS:\n"
            "  • Buildings and Other Construction Workers Act, 1996\n"
            "  • Entitled to: Minimum wages, safety equipment, weekly rest, ESI benefits\n"
            "  • Register with State Building & Construction Workers Welfare Board\n\n"
            "IF YOU ARE TRAPPED:\n"
            "  • Call Labour Department Helpline: 1800-425-1013\n"
            "  • Contact NHRC: 14433\n"
            "  • Contact Jan Sahas: jansahas.in (specializes in bonded labour rescue)\n\n"
            "YOUR DEBT IS VOID BY LAW — Bonded Labour (Abolition) Act, 1976"
        )
    },

    "KB063": {
        "category": "online_grooming",
        "intent": "gaming_grooming",
        "priority": 2,
        "keywords": ["gaming", "game", "online game", "multiplayer", "discord", "gamer"],
        "user_queries": [
            "grooming through online games",
            "gaming community trafficking",
            "predators in online games",
            "suspicious person in game chat"
        ],
        "response": (
            "Grooming Through Online Gaming — Awareness:\n\n"
            "HOW IT HAPPENS:\n"
            "  • Predators join popular games (Free Fire, PUBG, Roblox, Minecraft)\n"
            "  • Build friendship over weeks of gaming together\n"
            "  • Move conversation to private chat (Discord, WhatsApp)\n"
            "  • Begin asking personal questions\n"
            "  • Request photos or videos\n"
            "  • Eventually meet in person or recruit for trafficking\n\n"
            "RED FLAGS IN GAMING:\n"
            "  🚩 Player asks for personal details (age, city, school)\n"
            "  🚩 Offers expensive in-game items or gift cards\n"
            "  🚩 Wants to move to private chat outside the game\n"
            "  🚩 Sends sexual content in game chat\n"
            "  🚩 Wants to meet 'in person' quickly\n\n"
            "SAFE GAMING RULES:\n"
            "  ✓ Never share real name, location, or school\n"
            "  ✓ Use a game username, not your real name\n"
            "  ✓ Block and report players who make you uncomfortable\n"
            "  ✓ Tell a parent if something feels wrong\n"
            "  ✓ Keep privacy settings on game platforms strict"
        )
    },

    "KB064": {
        "category": "victim_support",
        "intent": "legal_aid_access",
        "priority": 2,
        "keywords": ["lawyer", "legal aid", "free lawyer", "DLSA", "NALSA", "advocate",
                     "legal help", "free legal"],
        "user_queries": [
            "how to get free legal help",
            "free lawyer for trafficking victims",
            "legal aid for victims",
            "how to access DLSA"
        ],
        "response": (
            "Free Legal Aid for Trafficking Victims:\n\n"
            "YOU ARE ENTITLED TO FREE LEGAL AID UNDER:\n"
            "  • Legal Services Authorities Act, 1987\n"
            "  • Article 39A, Constitution of India\n\n"
            "HOW TO ACCESS:\n\n"
            "  NALSA (National Legal Services Authority)\n"
            "    Helpline: 15100\n"
            "    Website: nalsa.gov.in\n\n"
            "  DLSA (District Legal Services Authority)\n"
            "    • Located at the District Court in your area\n"
            "    • Provides free lawyers, legal advice, and mediation\n"
            "    • Visit in person or call the district court helpline\n\n"
            "  STATE LEGAL SERVICES AUTHORITY (SLSA)\n"
            "    • At the High Court level\n"
            "    • Handles compensation claims and appeals\n\n"
            "ELIGIBLE PERSONS (free legal aid):\n"
            "  ✓ Women (in any case)\n"
            "  ✓ Children\n"
            "  ✓ Victims of trafficking (automatic entitlement)\n"
            "  ✓ Persons with disabilities\n"
            "  ✓ Anyone earning below the income threshold\n\n"
            "You can also request legal aid through a police officer or any NGO."
        )
    },

    "KB065": {
        "category": "reporting_procedures",
        "intent": "court_process",
        "priority": 3,
        "keywords": ["court", "trial", "hearing", "testify", "magistrate", "judge",
                     "what happens in court"],
        "user_queries": [
            "what happens in court for trafficking case",
            "how does trial work",
            "do I have to appear in court",
            "court process for trafficking case"
        ],
        "response": (
            "The Court Process for Trafficking Cases:\n\n"
            "AFTER FIR IS FILED:\n"
            "  1. Police investigation begins (30–90 days)\n"
            "  2. Police file a Chargesheet with the court\n"
            "  3. Court examines chargesheet and frames charges\n\n"
            "DURING TRIAL:\n"
            "  • You will be asked to give testimony\n"
            "  • You have the right to:\n"
            "    - In-camera proceedings (private, no public)\n"
            "    - Female judge (can be requested)\n"
            "    - Testify behind a screen or via video link\n"
            "    - Have a support person with you\n"
            "    - Have your name protected from media\n\n"
            "SPECIAL COURTS:\n"
            "  • Many states now have Special Courts for trafficking cases\n"
            "  • These fast-track courts aim for quicker resolution\n\n"
            "TIMELINE:\n"
            "  • Fast-track courts: 6–18 months\n"
            "  • Regular courts: 1–5 years\n\n"
            "YOUR SUPPORT PERSON:\n"
            "  • A trained victim advocate or NGO worker can accompany you throughout"
        )
    },

    "KB066": {
        "category": "safety_measures",
        "intent": "digital_evidence_preservation",
        "priority": 2,
        "keywords": ["evidence", "screenshot", "save messages", "proof", "document",
                     "record", "preserve"],
        "user_queries": [
            "how to preserve evidence of trafficking",
            "what evidence to keep",
            "how to document trafficking",
            "save evidence for police"
        ],
        "response": (
            "Preserving Evidence — What to Save:\n\n"
            "DIGITAL EVIDENCE:\n"
            "  ✓ Screenshots of messages, emails, job offers\n"
            "  ✓ Screenshots of social media profiles of traffickers\n"
            "  ✓ Phone call logs (screenshots from call history)\n"
            "  ✓ Photos of the location (if safe to take)\n"
            "  ✓ Photos of any written notices, contracts, or threats\n\n"
            "PHYSICAL EVIDENCE:\n"
            "  ✓ Any contracts or written documents (keep originals)\n"
            "  ✓ Note down: dates, times, names, vehicle numbers, addresses\n"
            "  ✓ Clothing worn during the incident (do not wash if assaulted)\n"
            "  ✓ Any receipts, tickets, or invoices\n\n"
            "HOW TO PRESERVE:\n"
            "  ✓ Email yourself screenshots to a secure email account\n"
            "  ✓ Save to a cloud account the trafficker doesn't know about\n"
            "  ✓ Give copies to a trusted person outside the situation\n"
            "  ✓ Note: Deleting evidence can harm your case\n\n"
            "IMPORTANT: Do not post evidence on social media — this can\n"
            "            alert the trafficker and compromise the case."
        )
    },

    "KB067": {
        "category": "human_trafficking_basics",
        "intent": "trafficking_in_india_regions",
        "priority": 3,
        "keywords": ["region", "state", "where", "india region", "which state", "area",
                     "most affected"],
        "user_queries": [
            "which states in india are most affected by trafficking",
            "trafficking hotspots in india",
            "where does trafficking happen most in india"
        ],
        "response": (
            "Human Trafficking in India — Regional Overview:\n\n"
            "MAJOR SOURCE STATES (where victims come from):\n"
            "  • West Bengal — highest number of trafficking cases\n"
            "  • Jharkhand — bonded labour, domestic workers, child trafficking\n"
            "  • Assam — sex trafficking, domestic workers\n"
            "  • Bihar — bonded labour, child labour\n"
            "  • Odisha — domestic work trafficking\n"
            "  • Chhattisgarh — brick kiln bonded labour\n\n"
            "MAJOR DESTINATION STATES:\n"
            "  • Delhi (NCR) — domestic work, sex trafficking\n"
            "  • Maharashtra (Mumbai) — sex trafficking, labour\n"
            "  • Haryana, Punjab — bride trafficking from WB, Assam\n"
            "  • Andhra Pradesh — domestic workers\n"
            "  • Karnataka (Bengaluru) — tech/service industry exploitation\n\n"
            "INTERNATIONAL ROUTES:\n"
            "  • India → Gulf countries (domestic work)\n"
            "  • India → Southeast Asia (cyber scam centres)\n"
            "  • Nepal/Bangladesh → India → Gulf\n"
            "  • India is a transit country for some international routes"
        )
    },

    "KB068": {
        "category": "ngo_support",
        "intent": "international_orgs",
        "priority": 3,
        "keywords": ["ILO", "UNICEF", "UNODC", "UN women", "international organization",
                     "global NGO"],
        "user_queries": [
            "international organizations fighting trafficking",
            "UN organizations for trafficking",
            "global NGOs anti trafficking"
        ],
        "response": (
            "International Organizations — Anti-Trafficking:\n\n"
            "UN AGENCIES:\n"
            "  • UNODC (UN Office on Drugs and Crime)\n"
            "    blueheart.unodc.org\n"
            "  • ILO (International Labour Organization)\n"
            "    ilo.org/global/topics/forced-labour\n"
            "  • UNICEF — Child trafficking and protection\n"
            "    unicef.org\n"
            "  • UN Women — Gender-based trafficking\n"
            "    unwomen.org\n\n"
            "INTERNATIONAL NGOS:\n"
            "  • ECPAT International (Child sex trafficking)\n"
            "    ecpat.org\n"
            "  • Polaris Project (USA, global advocacy)\n"
            "    polarisproject.org\n"
            "  • La Strada International (Europe)\n"
            "    lastradainternational.org\n"
            "  • IJM (International Justice Mission — India offices)\n"
            "    ijm.org\n\n"
            "REPORTING INTERNATIONAL CSAM:\n"
            "  • NCMEC (National Center for Missing & Exploited Children)\n"
            "    cybertipline.org"
        )
    },

    "KB069": {
        "category": "forced_labour",
        "intent": "agricultural_trafficking",
        "priority": 3,
        "keywords": ["farm", "agriculture", "crop", "farmer", "sugarcane", "rice field",
                     "plantation"],
        "user_queries": [
            "trafficking in agriculture",
            "forced labour on farms",
            "agricultural workers exploitation"
        ],
        "response": (
            "Forced Labour in Agriculture:\n\n"
            "COMMON IN:\n"
            "  • Sugarcane harvesting (Maharashtra, UP)\n"
            "  • Rice cultivation (Andhra Pradesh, Telangana)\n"
            "  • Tea plantations (Assam)\n"
            "  • Cotton fields (Gujarat, AP)\n"
            "  • Fisheries (coastal states)\n\n"
            "HOW IT WORKS:\n"
            "  • Families recruited from tribal or poor areas during lean seasons\n"
            "  • 'Mukadam' (labour contractor) provides advance\n"
            "  • Entire family transported to farm regions\n"
            "  • Long working hours, poor food and housing\n"
            "  • Cannot leave until 'debt' is repaid (it never is)\n\n"
            "YOUR RIGHTS:\n"
            "  • Minimum Wages Act — you must be paid minimum wage\n"
            "  • Bonded Labour (Abolition) Act — advance is not a bond\n"
            "  • Inter-State Migrant Workmen Act — protections for migrant farm workers\n\n"
            "REPORT TO:\n"
            "  • District Labour Commissioner\n"
            "  • NHRC: 14433\n"
            "  • Jan Sahas (bonded labour): jansahas.in"
        )
    },

    "KB070": {
        "category": "victim_support",
        "intent": "reintegration_livelihood",
        "priority": 3,
        "keywords": ["livelihood", "job", "work after trafficking", "earn", "start over",
                     "skills", "training", "employment"],
        "user_queries": [
            "how to find work after trafficking",
            "livelihood support for survivors",
            "vocational training for trafficking victims",
            "employment help for survivors"
        ],
        "response": (
            "Livelihood and Reintegration Support:\n\n"
            "VOCATIONAL TRAINING PROGRAMS:\n"
            "  • Ujjawala Scheme: Vocational training as part of rehabilitation\n"
            "  • PMKVY (Pradhan Mantri Kaushal Vikas Yojana): Free skill development\n"
            "  • Jan Shikshan Sansthan: Vocational training in communities\n"
            "  • Apne Aap: Economic empowerment for marginalized women\n\n"
            "GOVERNMENT SCHEMES:\n"
            "  • PM Jan Dhan Yojana: Bank account access\n"
            "  • Stand-Up India: Loans for women entrepreneurs\n"
            "  • MUDRA Loan: Small business loan for survivors\n"
            "  • MGNREGS: Rural employment guarantee scheme\n\n"
            "NGO PROGRAMS:\n"
            "  • Restore India: Tailoring, handicrafts, digital literacy\n"
            "  • Prerana: Education and vocational training\n"
            "  • Shakti Vahini: Economic reintegration support\n\n"
            "EDUCATION:\n"
            "  • Free education under Right to Education Act (under 14)\n"
            "  • Open School (NIOS) for those who missed schooling\n"
            "  • Bridge courses available at shelter homes\n\n"
            "You have survived something extraordinarily difficult.\n"
            "Your strength will carry you forward."
        )
    },

    # --- 30 more compact entries to exceed 100 ---

    "KB071": {
        "category": "emergency_assistance",
        "intent": "safe_house_contacts",
        "priority": 1,
        "keywords": ["safe house", "emergency shelter", "immediate shelter", "tonight"],
        "user_queries": ["I need a safe place tonight", "emergency shelter now", "where to go right now"],
        "response": (
            "EMERGENCY SHELTER — RIGHT NOW:\n\n"
            "Call Childline 1098 or Women's Helpline 181.\n"
            "They will arrange immediate safe accommodation.\n\n"
            "NGO Emergency Lines:\n"
            "  • Shakti Vahini: +91-11-43062100\n"
            "  • Prerana: +91-22-23720856\n"
            "  • iCall (counseling): 9152987821\n\n"
            "Government Emergency: Call 181 (OSC) for women's crisis shelter."
        )
    },

    "KB072": {
        "category": "warning_signs",
        "intent": "debt_bondage_signs",
        "priority": 2,
        "keywords": ["debt", "owe money", "advance", "loan work", "peshgi", "debt bondage signs"],
        "user_queries": ["signs of debt bondage", "how to know if I am in debt bondage", "debt bondage what is"],
        "response": (
            "Debt Bondage — Warning Signs:\n\n"
            "  • You owe money to your employer for recruitment, transport, or housing\n"
            "  • Your wages are entirely consumed by 'deductions'\n"
            "  • The debt amount never seems to decrease\n"
            "  • You are told you cannot leave until the debt is paid\n"
            "  • Interest is added to the debt regularly\n"
            "  • Family members are also held responsible for your debt\n\n"
            "THIS IS ILLEGAL. Under the Bonded Labour (Abolition) Act, 1976,\n"
            "ALL such debts are automatically cancelled. You owe NOTHING.\n\n"
            "Call NHRC: 14433 or Labour Helpline: 1800-425-1013"
        )
    },

    "KB073": {
        "category": "recruitment_scams",
        "intent": "social_media_job_scams",
        "priority": 2,
        "keywords": ["facebook job", "instagram job", "whatsapp job", "telegram job",
                     "social media recruitment"],
        "user_queries": [
            "job scam on social media",
            "fake job on facebook",
            "whatsapp job offer scam",
            "instagram job offer suspicious"
        ],
        "response": (
            "Social Media Job Scam Red Flags:\n\n"
            "  🚩 Job posted in a Facebook group without company details\n"
            "  🚩 Recruiter contacts you via Instagram DM out of the blue\n"
            "  🚩 Job offer sent via WhatsApp from an unknown number\n"
            "  🚩 Telegram group promising 'easy online work'\n"
            "  🚩 Links to job forms asking for Aadhaar, bank details\n"
            "  🚩 Requests advance payment for 'registration'\n\n"
            "VERIFY BEFORE APPLYING:\n"
            "  ✓ Search the company name independently\n"
            "  ✓ Visit the company's official website\n"
            "  ✓ Call the company's official number to verify\n"
            "  ✓ Never pay to get a job\n"
            "  ✓ Do not share personal documents via social media"
        )
    },

    "KB074": {
        "category": "child_trafficking",
        "intent": "child_labour_vs_trafficking",
        "priority": 2,
        "keywords": ["child labour", "child work", "child employment", "working child"],
        "user_queries": [
            "difference between child labour and child trafficking",
            "is child labour trafficking",
            "child labour vs trafficking"
        ],
        "response": (
            "Child Labour vs. Child Trafficking:\n\n"
            "CHILD LABOUR:\n"
            "  Work that deprives children of their childhood, potential, and dignity.\n"
            "  Harmful to physical/mental development.\n"
            "  Prohibited under Child Labour (P&R) Act, 1986\n\n"
            "CHILD TRAFFICKING:\n"
            "  Recruitment, transportation, or receipt of a child for exploitation.\n"
            "  Prohibited under Section 370 IPC and POCSO Act.\n\n"
            "RELATIONSHIP:\n"
            "  Child labour can BE a form of trafficking when:\n"
            "  • Child was recruited through deception\n"
            "  • Child is under control/coercion\n"
            "  • Child's wages are taken by an adult\n"
            "  • Child cannot leave freely\n\n"
            "BOTH are crimes. Report either to Childline 1098."
        )
    },

    "KB075": {
        "category": "faqs",
        "intent": "faq_reporting_fear",
        "priority": 1,
        "keywords": ["afraid to report", "scared to report", "fear reporting", "what if I report",
                     "safe to report"],
        "user_queries": [
            "I am afraid to report trafficking",
            "what happens if I report and nothing is done",
            "is it safe to report",
            "I am scared to call police"
        ],
        "response": (
            "Fear of Reporting — Addressing Your Concerns:\n\n"
            "YOUR FEARS MAY INCLUDE:\n"
            "  • 'The trafficker will hurt me or my family'\n"
            "  • 'Police won't believe me'\n"
            "  • 'I will be arrested'\n"
            "  • 'Nothing will change'\n\n"
            "THE REALITY:\n"
            "  ✓ You are protected by witness protection laws\n"
            "  ✓ You are a VICTIM — you will not be arrested\n"
            "  ✓ You can report anonymously through Childline or NGOs\n"
            "  ✓ Reports have led to rescues, prosecutions, and convictions\n\n"
            "IF YOU CANNOT CALL RIGHT NOW:\n"
            "  • Use the cybercrime portal online (cybercrime.gov.in)\n"
            "  • Send information to an NGO via their website\n"
            "  • Tell a trusted community member who can report for you\n\n"
            "YOUR REPORT CAN SAVE YOU AND OTHERS."
        )
    },

    "KB076": {
        "category": "online_grooming",
        "intent": "romance_scam",
        "priority": 2,
        "keywords": ["romance scam", "fake boyfriend", "fake girlfriend", "love scam",
                     "online romance"],
        "user_queries": [
            "romance scam trafficking",
            "online boyfriend trafficking me",
            "fake love relationship trafficking",
            "romance scam what to do"
        ],
        "response": (
            "Romance Scams and Trafficking:\n\n"
            "HOW IT WORKS:\n"
            "  1. Trafficker creates a fake romantic relationship online\n"
            "  2. 'Boyfriend/girlfriend' builds deep emotional bond over weeks/months\n"
            "  3. Victim is asked to meet in person\n"
            "  4. Victim is trafficked for sexual or labour exploitation\n"
            "  5. OR: Victim is used as an unwitting accomplice ('relay')\n\n"
            "RED FLAGS:\n"
            "  🚩 Partner refuses video calls or photos are inconsistent\n"
            "  🚩 Rapidly intense relationship ('you're the only one for me')\n"
            "  🚩 Stories keep changing about who they are\n"
            "  🚩 Asks for money or favours\n"
            "  🚩 Wants to meet in a private or unfamiliar location\n"
            "  🚩 Discourages you from telling family about the relationship\n\n"
            "WHAT TO DO:\n"
            "  • Reverse search profile photos (Google Images)\n"
            "  • Tell a trusted adult\n"
            "  • Report to Cyber Crime: 1930 or cybercrime.gov.in\n"
            "  • Never meet someone you know only online in a private place"
        )
    },

    "KB077": {
        "category": "legal_rights",
        "intent": "right_to_interpreter",
        "priority": 3,
        "keywords": ["language", "interpreter", "translator", "understand", "different language"],
        "user_queries": [
            "I don't speak the local language can I still get help",
            "right to interpreter for trafficking victim",
            "language barrier and trafficking"
        ],
        "response": (
            "Language Rights for Trafficking Victims:\n\n"
            "YOU HAVE THE RIGHT TO:\n"
            "  • An interpreter when making a police complaint\n"
            "  • Understand all legal proceedings in your language\n"
            "  • Have court documents translated\n\n"
            "WHAT TO DO:\n"
            "  • Ask police: 'I need a translator / interpreter'\n"
            "  • The government must provide one free of charge\n"
            "  • NGOs often have multilingual staff — contact them\n\n"
            "CHILDLINE (1098) has multilingual support in many states.\n\n"
            "If you are a foreign national:\n"
            "  • Your embassy will provide an interpreter\n"
            "  • Contact your country's embassy immediately"
        )
    },

    "KB078": {
        "category": "safety_measures",
        "intent": "phone_safety",
        "priority": 2,
        "keywords": ["phone", "mobile", "device", "safe phone", "phone tracked",
                     "location tracked", "phone monitored"],
        "user_queries": [
            "is my phone being monitored",
            "safe phone usage for victims",
            "how to use phone safely when in danger",
            "phone safety tips"
        ],
        "response": (
            "Phone Safety for People in Danger:\n\n"
            "IF YOUR PHONE MAY BE MONITORED:\n"
            "  • Use a different phone (friend's, library, shop)\n"
            "  • Use incognito/private browsing mode\n"
            "  • Delete browser history after use\n"
            "  • Use a payphone if available\n"
            "  • Turn off location services on your phone\n\n"
            "SAFE COMMUNICATION:\n"
            "  • Signal App: Encrypted, self-destructing messages\n"
            "  • Use email only if trafficker doesn't know the account\n"
            "  • Communicate from a device the trafficker has never touched\n\n"
            "EMERGENCY CALL WITHOUT UNLOCKING:\n"
            "  • Most Android: Hold power button → Emergency Call\n"
            "  • iPhone: Press side + volume button → Emergency SOS\n"
            "  • This calls 112 without needing PIN\n\n"
            "IF TRAFFICKER CHECKS YOUR PHONE:\n"
            "  • Memorize key numbers instead of saving them\n"
            "  • Use coded language with trusted contacts\n"
            "  • A pre-agreed code word can signal 'send help'"
        )
    },

    "KB079": {
        "category": "recruitment_scams",
        "intent": "education_scholarship_scam",
        "priority": 2,
        "keywords": ["scholarship", "education scam", "study abroad scam", "fake school",
                     "university scam", "admission scam"],
        "user_queries": [
            "education scam trafficking",
            "fake scholarship offer",
            "study abroad trafficking",
            "education used to recruit victims"
        ],
        "response": (
            "Education and Scholarship Scams — Trafficking Red Flags:\n\n"
            "HOW IT WORKS:\n"
            "  • Offer of scholarship or education abroad\n"
            "  • 'Sponsor' pays for visa, travel, accommodation\n"
            "  • On arrival, the school does not exist\n"
            "  • Victim is exploited (domestic work, sex work)\n\n"
            "RED FLAGS:\n"
            "  🚩 School cannot be verified online\n"
            "  🚩 Sponsor asks for passport or Aadhaar upfront\n"
            "  🚩 No formal admission letter from a registered institution\n"
            "  🚩 Scholarship requires you to work for the sponsor first\n"
            "  🚩 Unusually generous scholarship for no clear reason\n\n"
            "VERIFY EDUCATION INSTITUTIONS:\n"
            "  ✓ UGC (for Indian universities): ugc.gov.in\n"
            "  ✓ AICTE: aicte-india.org\n"
            "  ✓ For foreign universities: Check official embassy lists\n"
            "  ✓ Never pay fees to a 'scholarship agent'"
        )
    },

    "KB080": {
        "category": "human_trafficking_basics",
        "intent": "trafficking_economic_impact",
        "priority": 3,
        "keywords": ["economic", "economy", "cost", "billion", "profitable", "money",
                     "criminal enterprise"],
        "user_queries": [
            "economic impact of trafficking",
            "how much money does trafficking make",
            "trafficking as criminal enterprise"
        ],
        "response": (
            "The Economics of Human Trafficking:\n\n"
            "GLOBAL SCALE:\n"
            "  • $150 billion generated annually (ILO, 2022)\n"
            "  • 2nd largest criminal enterprise globally\n"
            "  • Forced sexual exploitation: $99 billion/year\n"
            "  • Forced labour: $34 billion/year\n"
            "  • Domestic servitude: $9 billion/year\n\n"
            "WHY IT IS PROFITABLE FOR TRAFFICKERS:\n"
            "  • Unlike drugs, a human can be sold/exploited repeatedly\n"
            "  • Low detection and prosecution rates\n"
            "  • High demand in destination markets\n"
            "  • Vulnerability of source populations is easy to exploit\n\n"
            "IMPACT ON VICTIMS:\n"
            "  • Average victim earns $0 (all profits go to trafficker)\n"
            "  • Victims may remain in exploitation for years\n"
            "  • Long-term economic marginalization after escape\n\n"
            "Trafficking is DRIVEN BY DEMAND. Reducing demand is key to ending it."
        )
    },

    "KB081": {
        "category": "emergency_assistance",
        "intent": "medical_emergency",
        "priority": 1,
        "keywords": ["medical", "hospital", "injured", "sick", "hurt", "medical help",
                     "healthcare", "doctor"],
        "user_queries": [
            "I need medical help",
            "I was hurt by trafficker",
            "medical assistance for trafficking victim",
            "I need to see a doctor"
        ],
        "response": (
            "Medical Help for Trafficking Victims:\n\n"
            "IMMEDIATE MEDICAL EMERGENCY:\n"
            "  • Call 108 (Ambulance — free, 24/7)\n"
            "  • Go to nearest Government Hospital Emergency\n"
            "  • All government hospitals MUST provide emergency care free\n\n"
            "WHAT TO TELL THE DOCTOR:\n"
            "  • You are safe to tell the doctor you were trafficked\n"
            "  • Medical staff are bound by confidentiality\n"
            "  • They can alert police with your consent\n\n"
            "IF SEXUALLY ASSAULTED:\n"
            "  • Go to hospital BEFORE bathing (preserves evidence)\n"
            "  • Ask for a Medico-Legal Case (MLC) examination\n"
            "  • Demand female doctor if preferred\n"
            "  • One Stop Centre (OSC) at hospitals also provides medical care: 181\n\n"
            "MENTAL HEALTH CRISIS:\n"
            "  • iCall: 9152987821\n"
            "  • Vandrevala Foundation: 1860-2662-345 (24/7)"
        )
    },

    "KB082": {
        "category": "faqs",
        "intent": "faq_what_is_aegisai",
        "priority": 1,
        "keywords": ["what is aegisai", "about aegisai", "how does this work", "this chatbot",
                     "about this system"],
        "user_queries": [
            "what is AegisAI",
            "what can you help me with",
            "how does this chatbot work",
            "about this system"
        ],
        "response": (
            "About AegisAI:\n\n"
            "AegisAI is an AI-powered chatbot designed to help with:\n\n"
            "  📚 EDUCATION: Learn about human trafficking, warning signs, and laws\n"
            "  ⚠️  RISK ASSESSMENT: Evaluate your situation with a guided questionnaire\n"
            "  🔍 JOB ANALYSIS: Check if a job offer has trafficking red flags\n"
            "  🆘 EMERGENCY HELP: Get step-by-step guidance in dangerous situations\n"
            "  📞 RESOURCES: Find helplines, NGOs, and shelter information\n"
            "  ⚖️  LEGAL RIGHTS: Understand your rights and reporting procedures\n\n"
            "IMPORTANT LIMITATIONS:\n"
            "  • AegisAI is NOT a substitute for emergency services\n"
            "  • In immediate danger: Call 100 (Police) or 1098 (Childline)\n"
            "  • AegisAI does NOT store any personal information\n"
            "  • AegisAI does NOT provide legal or medical advice\n\n"
            "How can I help you today?"
        )
    },

    "KB083": {
        "category": "victim_support",
        "intent": "survivor_stories",
        "priority": 3,
        "keywords": ["survivor", "story", "overcome", "others like me", "not alone",
                     "hope", "recovery story"],
        "user_queries": [
            "are there others who survived trafficking",
            "can I recover from trafficking",
            "survivor stories",
            "I feel hopeless is there any hope"
        ],
        "response": (
            "You Are Not Alone — Survivors Speak:\n\n"
            "Millions of survivors have rebuilt their lives after trafficking.\n\n"
            "WHAT SURVIVORS SAY:\n"
            "  'I thought I had no future. With support from the shelter\n"
            "   and training, I now run a small business.' — Survivor, Mumbai\n\n"
            "  'The shame nearly killed me. But I learned: the crime was\n"
            "   done TO me. I am not my trafficking.' — Survivor, Delhi\n\n"
            "  'My children are my reason to heal. Recovery is slow\n"
            "   but every day gets a little better.' — Survivor, Kolkata\n\n"
            "RECOVERY IS POSSIBLE:\n"
            "  ✓ With counseling and peer support\n"
            "  ✓ With vocational training and livelihood support\n"
            "  ✓ With legal justice\n"
            "  ✓ With time, patience, and community\n\n"
            "SURVIVOR ORGANIZATIONS:\n"
            "  • Apne Aap Survivor Network\n"
            "  • SANLAAP Survivor Group (West Bengal)\n"
            "  • Restore India Survivor Community\n\n"
            "You are stronger than you know."
        )
    },

    "KB084": {
        "category": "legal_rights",
        "intent": "state_specific_laws",
        "priority": 3,
        "keywords": ["state law", "maharashtra", "west bengal", "UP", "state specific",
                     "state rules"],
        "user_queries": [
            "state specific trafficking laws",
            "Maharashtra anti trafficking",
            "West Bengal trafficking laws"
        ],
        "response": (
            "State-Level Anti-Trafficking Initiatives:\n\n"
            "ANTI-HUMAN TRAFFICKING UNITS (AHTUs):\n"
            "  • Established by Ministry of Home Affairs across India\n"
            "  • Present in 330+ districts\n"
            "  • Specialized police units for trafficking cases\n\n"
            "STATE INITIATIVES:\n\n"
            "WEST BENGAL:\n"
            "  • Ujjala Project (state scheme for survivor rehabilitation)\n"
            "  • SANLAAP NGO works extensively in the state\n\n"
            "MAHARASHTRA:\n"
            "  • Disha Project — rescued bonded labourers\n"
            "  • Strong AHTU presence in Mumbai\n\n"
            "ANDHRA PRADESH & TELANGANA:\n"
            "  • HELP NGO — extensive anti-trafficking network\n\n"
            "ASSAM:\n"
            "  • STOP NGO — Northeast India focus\n"
            "  • Strict border monitoring on Bangladesh-Assam border\n\n"
            "CONTACT YOUR STATE AHTU through local police station."
        )
    },

    "KB085": {
        "category": "recruitment_scams",
        "intent": "loan_for_job_scam",
        "priority": 2,
        "keywords": ["loan for job", "pay for job", "advance fee", "registration fee",
                     "kit fee", "upfront payment"],
        "user_queries": [
            "job that asks me to take a loan",
            "job requiring advance payment",
            "asked to pay for job registration",
            "job fee before starting"
        ],
        "response": (
            "Jobs Requiring Advance Payments — Always a Scam:\n\n"
            "THE RULE:\n"
            "  A LEGITIMATE JOB NEVER ASKS YOU TO PAY MONEY.\n\n"
            "COMMON FEE SCAMS:\n"
            "  🚩 'Registration fee' — ₹500 to ₹5,000\n"
            "  🚩 'Training kit' purchase required\n"
            "  🚩 'Security deposit' refundable later (never is)\n"
            "  🚩 'Visa processing fee' for foreign jobs\n"
            "  🚩 'Background check fee'\n"
            "  🚩 'Uniform purchase' requirement\n\n"
            "HOW THE SCAM ESCALATES TO TRAFFICKING:\n"
            "  1. Person pays fee and is now financially invested\n"
            "  2. Told to travel to location to 'start work'\n"
            "  3. Job does not exist — victim is exploited\n"
            "  4. Now owes 'transport debt' in addition\n\n"
            "WHAT TO DO:\n"
            "  ✗ Never pay any fee for any job\n"
            "  ✓ Report fraudulent job offers to police or\n"
            "    National Consumer Helpline: 1800-11-4000"
        )
    },

    "KB086": {
        "category": "online_grooming",
        "intent": "parents_guide_grooming",
        "priority": 2,
        "keywords": ["parent", "parents", "child online", "teenager online", "protect child",
                     "parental control"],
        "user_queries": [
            "how to protect my child from online grooming",
            "parent guide to online safety",
            "my teenager is being groomed what do I do",
            "how to talk to child about grooming"
        ],
        "response": (
            "Parent's Guide to Protecting Children from Online Grooming:\n\n"
            "OPEN CONVERSATION:\n"
            "  ✓ Talk regularly about online safety without being preachy\n"
            "  ✓ Ask: 'Who do you talk to online? Has anyone made you uncomfortable?'\n"
            "  ✓ Make it clear they won't be punished for telling you\n"
            "  ✓ Teach them: 'You can always tell me anything'\n\n"
            "TECHNICAL MEASURES:\n"
            "  ✓ Enable parental controls on devices and apps\n"
            "  ✓ Use Google Family Link or Apple Screen Time\n"
            "  ✓ Keep devices in common areas, not bedrooms at night\n"
            "  ✓ Know your child's usernames and platforms (age-appropriate)\n\n"
            "BEHAVIORAL SIGNS TO WATCH:\n"
            "  🚩 Child hides phone or laptop when you enter\n"
            "  🚩 Receives gifts from unknown sources\n"
            "  🚩 Becomes secretive, withdrawn, or aggressive\n"
            "  🚩 New older 'friend' you don't know\n\n"
            "IF GROOMING IS SUSPECTED:\n"
            "  1. Do NOT confront the groomer directly\n"
            "  2. Preserve evidence (screenshots)\n"
            "  3. Call Childline: 1098 for guidance\n"
            "  4. Report to Cyber Crime: cybercrime.gov.in"
        )
    },

    "KB087": {
        "category": "safety_measures",
        "intent": "document_safety",
        "priority": 2,
        "keywords": ["document", "passport", "Aadhaar", "ID card", "original documents",
                     "keep safe"],
        "user_queries": [
            "how to keep documents safe",
            "employer wants my passport",
            "should I give my ID to recruiter",
            "document safety for workers"
        ],
        "response": (
            "Document Safety — Protecting Your Identity:\n\n"
            "GOLDEN RULE: Never surrender ORIGINAL documents to anyone.\n\n"
            "WHAT IS LEGAL:\n"
            "  ✓ Employer may VIEW your documents for verification\n"
            "  ✓ Police may take documents as evidence (with receipt)\n"
            "  ✗ NO employer can 'keep' or 'hold' your passport or Aadhaar\n\n"
            "WHAT TO DO BEFORE TRAVEL/WORK:\n"
            "  ✓ Make certified photocopies of all documents\n"
            "  ✓ Store originals separately or with family\n"
            "  ✓ Upload digital copies to a secure cloud account\n"
            "  ✓ Register your travel with the nearest police station\n\n"
            "IF YOUR DOCUMENTS ARE TAKEN:\n"
            "  • This is a CRIME under Section 344 IPC\n"
            "  • Report to police immediately\n"
            "  • Demand return of documents — if refused, file FIR\n\n"
            "RECOVERING LOST DOCUMENTS:\n"
            "  • Aadhaar: Nearest Aadhaar enrolment centre (free)\n"
            "  • Passport: Report to Passport Seva Kendra / Embassy\n"
            "  • PAN Card: NSDL portal: tin.tin.nsdl.com"
        )
    },

    "KB088": {
        "category": "child_trafficking",
        "intent": "school_dropout_risk",
        "priority": 2,
        "keywords": ["dropout", "school leaving", "out of school", "not studying",
                     "stopped school", "education stop"],
        "user_queries": [
            "school dropout and trafficking",
            "children who stop school risk",
            "dropout trafficking connection"
        ],
        "response": (
            "School Dropout and Trafficking Risk:\n\n"
            "THE LINK:\n"
            "  Children who drop out of school are at significantly higher risk of:\n"
            "  • Child labour and bonded labour\n"
            "  • Early or forced marriage\n"
            "  • Being recruited by traffickers for 'work'\n"
            "  • Online grooming (more idle time online)\n\n"
            "COMMON REASONS FOR DROPOUT:\n"
            "  • Family poverty — child needed to work\n"
            "  • Distance from school\n"
            "  • Child marriage (especially girls)\n"
            "  • Discrimination\n"
            "  • Migration of family\n\n"
            "WHAT CAN HELP:\n"
            "  • Right to Education (RTE) Act — free education until 14 is a RIGHT\n"
            "  • Mid-Day Meal Scheme — keep children in school\n"
            "  • Kasturba Gandhi Balika Vidyalaya — residential schools for girls\n"
            "  • NIOS (Open School) — alternative for older dropouts\n\n"
            "REPORT CHILD OUT OF SCHOOL:\n"
            "  • Childline: 1098\n"
            "  • District Education Officer"
        )
    },

    "KB089": {
        "category": "ngo_support",
        "intent": "ngo_northeast_india",
        "priority": 3,
        "keywords": ["northeast", "assam", "manipur", "meghalaya", "nagaland",
                     "northeast india trafficking"],
        "user_queries": [
            "trafficking in northeast india",
            "NGOs for northeast india trafficking",
            "help for northeast india victims"
        ],
        "response": (
            "Anti-Trafficking Support in Northeast India:\n\n"
            "KEY NGOS:\n"
            "  • STOP (Assam): Rescue and rehabilitation\n"
            "  • MSEMVS (Manipur): Women and children\n"
            "  • HELP (Assam): Community-level prevention\n"
            "  • Impulse NGO Network (Meghalaya): Trafficking prevention\n"
            "  • APATCO (Assam): Anti-trafficking coordination\n\n"
            "REGIONAL CHALLENGES:\n"
            "  • Porous international borders (Bangladesh, Myanmar, Bhutan)\n"
            "  • High migration rates creating vulnerability\n"
            "  • Limited resources in remote areas\n\n"
            "EMERGENCY NUMBERS:\n"
            "  • Childline: 1098 (available across all NE states)\n"
            "  • Police: 100\n"
            "  • Impulse NGO: 0364-2521014\n\n"
            "ROUTE OF TRAFFICKING:\n"
            "  Common: Assam/Manipur → Delhi/Mumbai for domestic work\n"
            "  International: Bangladesh border → India → Gulf"
        )
    },

    "KB090": {
        "category": "legal_rights",
        "intent": "compensation_claim_process",
        "priority": 2,
        "keywords": ["claim compensation", "how to apply", "compensation process",
                     "victim fund", "apply for money"],
        "user_queries": [
            "how to claim compensation as trafficking victim",
            "compensation application process",
            "apply for victim fund",
            "steps to get compensation"
        ],
        "response": (
            "How to Claim Victim Compensation:\n\n"
            "STEP 1: File an FIR\n"
            "  • Compensation applications are linked to FIR numbers\n\n"
            "STEP 2: Get a Free Lawyer\n"
            "  • Contact DLSA at the district court\n"
            "  • Your lawyer will guide the compensation application\n\n"
            "STEP 3: Apply to SLSA\n"
            "  • State Legal Services Authority administers NALSA Victim Compensation\n"
            "  • Application form available at DLSA office or nalsa.gov.in\n\n"
            "STEP 4: Court Application\n"
            "  • The trial court or High Court can also order compensation\n"
            "  • This is in ADDITION to any government scheme compensation\n\n"
            "DOCUMENTS NEEDED:\n"
            "  • FIR copy\n"
            "  • Medical reports (if applicable)\n"
            "  • Identity proof\n"
            "  • Statement of losses/impact\n\n"
            "TIMELINE:\n"
            "  • Interim compensation can be ordered quickly\n"
            "  • Final amount determined at trial\n"
            "  • Range: ₹1 lakh – ₹10 lakhs depending on offence"
        )
    },

    "KB091": {
        "category": "warning_signs",
        "intent": "hotel_motel_signs",
        "priority": 3,
        "keywords": ["hotel", "motel", "lodge", "guesthouse", "suspicious hotel activity"],
        "user_queries": [
            "signs of trafficking in hotels",
            "suspicious hotel activity",
            "how to spot trafficking in a hotel"
        ],
        "response": (
            "Warning Signs of Trafficking in Hotels and Lodges:\n\n"
            "SIGNS HOTEL STAFF SHOULD WATCH FOR:\n"
            "  • Guest appears frightened and does not speak freely\n"
            "  • Many male visitors to a room throughout the day\n"
            "  • Multiple people checking into one room\n"
            "  • Guest requests no housekeeping for extended periods\n"
            "  • Evidence of large amounts of cash or multiple phones\n"
            "  • Guest appears to be under instruction from a 'manager'\n"
            "  • Do Not Disturb sign left for unusually long periods\n\n"
            "FOR GUESTS WHO SUSPECT TRAFFICKING:\n"
            "  • Ask hotel staff for help discreetly\n"
            "  • Call police (100) from the hotel phone\n"
            "  • Use the Signal for Help hand gesture to staff\n\n"
            "HOTEL TRAINING:\n"
            "  • Many hotels now have mandatory trafficking awareness training\n"
            "  • Global program: TraffickStop by the Tourism Child-Protection Code"
        )
    },

    "KB092": {
        "category": "forced_labour",
        "intent": "fishing_industry_trafficking",
        "priority": 3,
        "keywords": ["fishing", "boat", "sea", "fisherman", "trawler", "maritime"],
        "user_queries": [
            "trafficking in fishing industry",
            "forced labour on fishing boats",
            "maritime trafficking"
        ],
        "response": (
            "Forced Labour in the Fishing Industry:\n\n"
            "HOW IT HAPPENS:\n"
            "  • Men are recruited with promises of good wages on fishing boats\n"
            "  • Once at sea, they cannot escape\n"
            "  • Work 18–20 hours a day in dangerous conditions\n"
            "  • Wages withheld or non-existent\n"
            "  • Physical abuse by boat captains\n"
            "  • Moved between vessels to avoid detection\n\n"
            "COMMON IN:\n"
            "  • Indian coastal states: Tamil Nadu, Kerala, Andhra Pradesh\n"
            "  • Thailand, Indonesia fishing industry\n\n"
            "INDICATORS:\n"
            "  • Missing/disoriented fishermen with no ID\n"
            "  • Fishermen afraid to speak in presence of boat owner\n"
            "  • No pay despite months of work\n\n"
            "REPORT TO:\n"
            "  • Indian Coast Guard: 1554\n"
            "  • NHRC: 14433\n"
            "  • Local Fisheries Department"
        )
    },

    "KB093": {
        "category": "faqs",
        "intent": "faq_NGO_vs_government",
        "priority": 3,
        "keywords": ["NGO or government", "who is better to contact", "which is safer to contact",
                     "NGO vs police"],
        "user_queries": [
            "should I contact NGO or police",
            "is NGO better than police for trafficking",
            "difference between NGO help and government help"
        ],
        "response": (
            "FAQ: NGO vs. Government — Who Should You Contact?\n\n"
            "THE ANSWER: BOTH — they work best together.\n\n"
            "GO TO AN NGO FIRST IF:\n"
            "  ✓ You are afraid of police or don't trust them\n"
            "  ✓ You need immediate emotional support\n"
            "  ✓ You need shelter tonight\n"
            "  ✓ You want to understand your options before going to police\n"
            "  ✓ You are undocumented or have no ID\n\n"
            "GO TO POLICE FIRST IF:\n"
            "  ✓ You are in immediate danger\n"
            "  ✓ You know where a victim is being held\n"
            "  ✓ You want to start a formal legal case\n"
            "  ✓ You are reporting a missing person\n\n"
            "NGOs CAN:\n"
            "  • Accompany you to the police station\n"
            "  • Advocate for proper treatment\n"
            "  • Provide documentation support\n\n"
            "COMBINED APPROACH:\n"
            "  Contact Childline 1098 — they coordinate BOTH NGO and police response."
        )
    },

    "KB094": {
        "category": "human_trafficking_basics",
        "intent": "trafficker_profiles",
        "priority": 2,
        "keywords": ["who are traffickers", "trafficker profile", "who traffics",
                     "what do traffickers look like", "recognise trafficker"],
        "user_queries": [
            "who are traffickers",
            "what do traffickers look like",
            "can someone I know be a trafficker",
            "trafficker profile"
        ],
        "response": (
            "Who Are Traffickers? — Profiles and Facts:\n\n"
            "TRAFFICKERS CAN BE:\n"
            "  • Known community members or family members (most common in India)\n"
            "  • Intimate partners or 'love interests'\n"
            "  • Recruiters from own village or caste\n"
            "  • Employers (direct exploitation)\n"
            "  • Organized crime groups\n"
            "  • Corrupt officials (rare but exists)\n\n"
            "FACTS ABOUT TRAFFICKERS:\n"
            "  • 55% of trafficking is perpetrated by someone the victim knows\n"
            "  • Women can also be traffickers — often former victims themselves\n"
            "  • Traffickers often appear kind, generous, and helpful at first\n"
            "  • They do not 'look' dangerous — they are skilled manipulators\n\n"
            "COMMON COVER IDENTITIES:\n"
            "  • 'Helpful uncle' with a job offer\n"
            "  • 'Loving boyfriend'\n"
            "  • 'Labour contractor' from home village\n"
            "  • 'Modeling agent' or 'talent scout'\n\n"
            "TRUST YOUR INSTINCTS — if something feels wrong, it probably is."
        )
    },

    "KB095": {
        "category": "emergency_assistance",
        "intent": "witnessed_trafficking",
        "priority": 1,
        "keywords": ["I witnessed", "saw trafficking", "witnessed exploitation",
                     "saw something suspicious", "bystander"],
        "user_queries": [
            "I witnessed trafficking what should I do",
            "I saw something that might be trafficking",
            "what to do if you witness trafficking",
            "bystander response to trafficking"
        ],
        "response": (
            "If You Witness Suspected Trafficking:\n\n"
            "DO:\n"
            "  ✓ Stay calm and observe safely\n"
            "  ✓ Note: Location, time, descriptions, vehicle numbers\n"
            "  ✓ If safe, try to alert the potential victim discreetly\n"
            "  ✓ Call police (100) or Childline (1098) immediately\n"
            "  ✓ Remain available to give your statement to police\n\n"
            "DO NOT:\n"
            "  ✗ Intervene directly or confront the suspected trafficker\n"
            "  ✗ Attempt a solo rescue\n"
            "  ✗ Take photos that put you or the victim at risk\n"
            "  ✗ Leave without reporting\n\n"
            "WHAT TO TELL POLICE:\n"
            "  • 'I want to report suspected human trafficking'\n"
            "  • Location/address\n"
            "  • Description of people involved\n"
            "  • What you saw and when\n"
            "  • Vehicle details if applicable\n\n"
            "You could save a life. REPORT — it takes 2 minutes."
        )
    },

    "KB096": {
        "category": "safety_measures",
        "intent": "internet_safety_children",
        "priority": 2,
        "keywords": ["internet safety children", "child internet", "safe internet use",
                     "kids online", "children online safety"],
        "user_queries": [
            "internet safety for children",
            "how to keep kids safe online",
            "online safety for young people",
            "child internet safety tips"
        ],
        "response": (
            "Internet Safety for Children and Young People:\n\n"
            "THE BASICS:\n"
            "  ✓ Never share: Full name, school, address, phone number online\n"
            "  ✓ Always tell a trusted adult if something online upsets you\n"
            "  ✓ Use privacy settings on all platforms\n"
            "  ✓ Only accept friend requests from people you know in real life\n"
            "  ✓ Remember: Not everyone online is who they say they are\n\n"
            "THE 3 Rs OF ONLINE SAFETY:\n"
            "  RECOGNIZE: Unsafe situations (someone asking for photos, secrets)\n"
            "  RESPOND: Leave the conversation, block the person\n"
            "  REPORT: Tell a trusted adult and report to the platform\n\n"
            "HELPFUL RESOURCES:\n"
            "  • Cyber Safety Pledge: cybercrime.gov.in\n"
            "  • Safe surfing guide: csk.gov.in\n"
            "  • NCERT cyber safety module: ncert.nic.in\n\n"
            "PARENTS: Keep the dialogue open. No punishment for telling the truth."
        )
    },

    "KB097": {
        "category": "legal_rights",
        "intent": "repatriation_rights",
        "priority": 2,
        "keywords": ["repatriation", "return home", "go back", "home state", "another state",
                     "foreign victim"],
        "user_queries": [
            "how to get back to my home state after trafficking",
            "repatriation for trafficking victims",
            "foreign victim wants to go home"
        ],
        "response": (
            "Repatriation Rights for Trafficking Victims:\n\n"
            "DOMESTIC VICTIMS (Inter-state):\n"
            "  • You have the right to be repatriated to your home state\n"
            "  • Police must facilitate safe return\n"
            "  • A Childline worker or NGO can accompany you\n"
            "  • Social welfare officer in your home state will receive you\n"
            "  • Process: Police → Ujjawala shelter → Home state authorities\n\n"
            "FOREIGN NATIONALS:\n"
            "  • Your embassy MUST be notified immediately\n"
            "  • You have the right to stay in India during legal proceedings\n"
            "  • UNHCR can assist if you are a refugee\n"
            "  • After proceedings: Safe repatriation to home country\n"
            "  • UNODC and IOM assist with international repatriation\n\n"
            "FOR NEPAL/BANGLADESH NATIONALS:\n"
            "  • Bilateral agreements exist for repatriation\n"
            "  • Border protection organizations assist\n"
            "  • IOM (International Organization for Migration): iom.int\n\n"
            "Contact NHRC: 14433 if repatriation is being delayed."
        )
    },

    "KB098": {
        "category": "recruitment_scams",
        "intent": "identify_fake_agent",
        "priority": 1,
        "keywords": ["agent", "broker", "recruitment agent", "placement agency", "fake agent",
                     "dubious recruiter"],
        "user_queries": [
            "how to identify fake recruitment agent",
            "verify placement agency",
            "is this recruiter legitimate",
            "fake broker warning signs"
        ],
        "response": (
            "Verifying Recruitment Agents and Placement Agencies:\n\n"
            "LEGITIMATE AGENTS WILL:\n"
            "  ✓ Have a registered office with verifiable address\n"
            "  ✓ Provide a written contract before any payment\n"
            "  ✓ Be registered with the Ministry of Labour (for domestic placements)\n"
            "  ✓ For foreign jobs: Be registered with MEA's eMigrate system\n"
            "  ✓ Give you a copy of all documents\n"
            "  ✓ Never ask for an upfront fee from the job seeker\n\n"
            "HOW TO VERIFY:\n"
            "  • eMigrate Portal: emigrate.gov.in (for overseas agents)\n"
            "  • Check Ministry of Labour's registered agency list\n"
            "  • Google the agency + 'reviews' and 'scam'\n"
            "  • Visit the office in person before agreeing to anything\n"
            "  • Ask for company registration number and verify it\n\n"
            "RED FLAGS:\n"
            "  🚩 Agent works only from a phone/WhatsApp — no office\n"
            "  🚩 Cannot provide company registration details\n"
            "  🚩 Pressures you to decide today\n"
            "  🚩 Asks for fees upfront\n"
            "  🚩 Not listed on any official government portal"
        )
    },

    "KB099": {
        "category": "faqs",
        "intent": "faq_student_awareness",
        "priority": 3,
        "keywords": ["student", "college", "university", "young person", "campus",
                     "awareness student"],
        "user_queries": [
            "how can students help fight trafficking",
            "student anti trafficking initiatives",
            "what can I do as a student",
            "campus anti trafficking"
        ],
        "response": (
            "Students — How You Can Make a Difference:\n\n"
            "LEARN:\n"
            "  ✓ Understand the signs of trafficking and grooming\n"
            "  ✓ Know the helpline numbers (1098, 100, 1091)\n"
            "  ✓ Take AegisAI's education module to learn more\n\n"
            "SPREAD AWARENESS:\n"
            "  ✓ Share factual posts on social media\n"
            "  ✓ Organize awareness events on campus\n"
            "  ✓ Display helpline posters in hostels and canteens\n"
            "  ✓ Write for your college newspaper/magazine\n\n"
            "VOLUNTEER:\n"
            "  ✓ Volunteer with anti-trafficking NGOs\n"
            "  ✓ Teach internet safety in local schools\n"
            "  ✓ Participate in Bachpan Bachao Andolan campaigns\n\n"
            "REPORT:\n"
            "  ✓ If you suspect trafficking on campus or in your community\n"
            "  ✓ Report to: 1098, 100, or cybercrime.gov.in\n\n"
            "IMPORTANT:\n"
            "  Your campus has an Internal Complaints Committee (ICC).\n"
            "  This can also handle exploitation-related complaints."
        )
    },

    "KB100": {
        "category": "faqs",
        "intent": "faq_immediate_crisis",
        "priority": 1,
        "keywords": ["crisis", "right now", "immediate", "now", "urgent help", "help immediately"],
        "user_queries": [
            "I need help right now",
            "immediate crisis help",
            "what to do in a trafficking crisis",
            "urgent I need help now"
        ],
        "response": (
            "🆘 IMMEDIATE CRISIS — HELP IS HERE 🆘\n\n"
            "CALL THESE NUMBERS RIGHT NOW:\n\n"
            "  🔴  Police: 100\n"
            "  🔴  Childline: 1098\n"
            "  🔴  Women's Helpline: 1091\n"
            "  🔴  National Emergency: 112\n"
            "  🔴  Cyber Crime: 1930\n\n"
            "IF YOU CANNOT CALL:\n"
            "  • Send your location to a trusted contact via WhatsApp\n"
            "  • Text 'HELP [your location]' to any trusted person\n"
            "  • Use the hand signal: palm up, tuck thumb, fold fingers over\n"
            "  • Approach any person in uniform or go to a public shop\n\n"
            "YOU ARE NOT ALONE.\n"
            "HELP IS COMING.\n"
            "STAY AS SAFE AS YOU CAN UNTIL HELP ARRIVES."
        )
    },

    "KB101": {
        "category": "warning_signs",
        "intent": "transportation_signs",
        "priority": 2,
        "keywords": ["transport", "bus", "train", "airport", "station", "vehicle",
                     "railway"],
        "user_queries": [
            "signs of trafficking at railway station",
            "trafficking at airports",
            "transportation red flags trafficking"
        ],
        "response": (
            "Warning Signs at Transportation Hubs:\n\n"
            "AT RAILWAY STATIONS / BUS STANDS:\n"
            "  • Person appears confused, disoriented, or frightened\n"
            "  • Young person travelling with an older adult, appears uncomfortable\n"
            "  • Child travelling alone or with strangers\n"
            "  • Person without luggage or belongings for a long journey\n"
            "  • Person who seems coached when questioned about destination\n\n"
            "AT AIRPORTS:\n"
            "  • Traveller whose passport is held by a third party\n"
            "  • Person who cannot explain their travel purpose\n"
            "  • Large group of similar-looking workers under one handler\n"
            "  • Person showing signs of physical abuse or malnourishment\n\n"
            "WHAT TO DO:\n"
            "  • Alert Railway Protection Force (RPF) or airport security\n"
            "  • RPF Helpline at railway stations: 182\n"
            "  • Childline at stations: 1098 (active at major stations)\n"
            "  • Do NOT approach suspected trafficker directly"
        )
    },

    "KB102": {
        "category": "victim_support",
        "intent": "identity_rebuilding",
        "priority": 3,
        "keywords": ["identity", "who am I", "lost self", "rebuild identity", "self worth",
                     "self esteem"],
        "user_queries": [
            "I lost my sense of identity after trafficking",
            "how to rebuild self after exploitation",
            "I don't know who I am anymore",
            "help rebuilding identity after trauma"
        ],
        "response": (
            "Rebuilding Identity After Trafficking:\n\n"
            "WHAT TRAFFICKING DOES TO IDENTITY:\n"
            "  • Traffickers systematically strip away your sense of self\n"
            "  • They may give you a different name or identity\n"
            "  • They use shame, blame, and control to make you feel worthless\n"
            "  • This is intentional — it makes control easier\n\n"
            "THE TRUTH:\n"
            "  ✦ Your worth is not defined by what was done to you\n"
            "  ✦ What happened to you was a CRIME — not your identity\n"
            "  ✦ Healing is a journey, not a destination\n"
            "  ✦ Your values, dreams, and personality still exist\n\n"
            "STEPS TO REBUILD:\n"
            "  1. Connect with a trauma-informed counselor\n"
            "  2. Join survivor peer support groups\n"
            "  3. Rediscover activities that brought you joy\n"
            "  4. Allow yourself to grieve what was taken\n"
            "  5. Set small, achievable goals\n\n"
            "PROFESSIONAL SUPPORT:\n"
            "  • iCall (TISS): 9152987821\n"
            "  • Vandrevala Foundation: 1860-2662-345"
        )
    },

    "KB103": {
        "category": "child_trafficking",
        "intent": "child_adoption_scam",
        "priority": 2,
        "keywords": ["adoption", "fake adoption", "child adoption scam", "child sold",
                     "illegal adoption"],
        "user_queries": [
            "child trafficking through adoption",
            "illegal adoption trafficking",
            "fake adoption agency",
            "selling children under adoption"
        ],
        "response": (
            "Child Trafficking Through Illegal Adoption:\n\n"
            "HOW IT WORKS:\n"
            "  • Children sold by poor families, hospitals, or orphanages\n"
            "  • False birth certificates created\n"
            "  • Children adopted abroad for exploitation\n"
            "  • 'Brokers' charge huge fees from adoptive parents\n\n"
            "LEGAL ADOPTION IN INDIA:\n"
            "  • Only through CARA (Central Adoption Resource Authority)\n"
            "  • Website: cara.nic.in\n"
            "  • Regulated under Juvenile Justice Act, 2015\n"
            "  • International adoption: Even more strictly regulated\n\n"
            "RED FLAGS:\n"
            "  🚩 Adoption arranged privately without CARA\n"
            "  🚩 Broker requests large cash payments\n"
            "  🚩 Very quick process without home study\n"
            "  🚩 Child's documents don't match physical characteristics\n\n"
            "REPORT ILLEGAL ADOPTION:\n"
            "  • CARA: cara@nic.in or 011-24076182\n"
            "  • Childline: 1098\n"
            "  • Local Child Welfare Committee (CWC)"
        )
    },

    "KB104": {
        "category": "reporting_procedures",
        "intent": "report_missing_adult",
        "priority": 2,
        "keywords": ["missing adult", "adult missing", "spouse missing", "friend missing",
                     "report adult missing"],
        "user_queries": [
            "how to report a missing adult",
            "my spouse is missing",
            "adult went missing might be trafficked"
        ],
        "response": (
            "Reporting a Missing Adult Who May Be Trafficked:\n\n"
            "STEP 1: File Missing Person FIR Immediately\n"
            "  • Go to police station — do NOT wait 24 hours (myth)\n"
            "  • Police MUST file FIR for missing persons immediately\n"
            "  • Bring: Photo, physical description, last known location\n\n"
            "STEP 2: Provide Context\n"
            "  • Any suspicious job offers they received\n"
            "  • Who they were with last\n"
            "  • Any travel plans mentioned\n"
            "  • Online contacts you know of\n\n"
            "STEP 3: Parallel Actions\n"
            "  • Share on social media (with family permission)\n"
            "  • Contact NGOs who have national networks:\n"
            "    - Shakti Vahini: +91-11-43062100\n"
            "    - Missing Link Trust: +91-22-25630571\n\n"
            "STEP 4: Online Portals\n"
            "  • TrackChild: trackthemissingchild.gov.in\n"
            "  • Khoya Paya: khoyapaya.gov.in\n\n"
            "Do not pay ransom. Inform police of any contact from the abductors."
        )
    },

    "KB105": {
        "category": "safety_measures",
        "intent": "safety_exit_plan",
        "priority": 1,
        "keywords": ["exit plan", "leave safely", "plan to leave", "safe exit plan",
                     "how to leave"],
        "user_queries": [
            "how to make an exit plan",
            "safety plan for leaving a dangerous situation",
            "plan to leave trafficker",
            "preparing to leave safely"
        ],
        "response": (
            "Creating a Safe Exit Plan:\n\n"
            "STEP 1: ASSESS YOUR SITUATION\n"
            "  • When is the trafficker/controller least present?\n"
            "  • Are there other people who might help you?\n"
            "  • What exits are available from your location?\n\n"
            "STEP 2: BUILD YOUR RESOURCES\n"
            "  • Memorize emergency numbers (1098, 100, 1091)\n"
            "  • Save any money you can safely access\n"
            "  • Try to access your documents (or make a note of their location)\n"
            "  • Identify a person you trust who can help\n\n"
            "STEP 3: PLAN THE EXIT\n"
            "  • Choose a time when you are least monitored\n"
            "  • Identify a destination (police station, NGO, hospital, public area)\n"
            "  • If possible, pre-arrange contact with a trusted person\n"
            "  • Have a cover story prepared if you are questioned\n\n"
            "STEP 4: EXECUTE AND SEEK HELP\n"
            "  • Go directly to your planned destination\n"
            "  • Call 100 or 1098 as soon as you are safe\n"
            "  • Do not return to collect belongings — safety first\n\n"
            "REMEMBER: No plan is perfect. Your instincts and safety matter most."
        )
    },
}

# ---------------------------------------------------------------------------
# CATEGORY INDEX — for fast lookup
# ---------------------------------------------------------------------------

CATEGORY_INDEX = {
    "human_trafficking_basics": [],
    "warning_signs": [],
    "recruitment_scams": [],
    "child_trafficking": [],
    "forced_labour": [],
    "online_grooming": [],
    "victim_support": [],
    "emergency_assistance": [],
    "reporting_procedures": [],
    "legal_rights": [],
    "safety_measures": [],
    "ngo_support": [],
    "faqs": [],
}

# Populate index automatically
for entry_id, entry in KNOWLEDGE_BASE.items():
    cat = entry.get("category", "")
    if cat in CATEGORY_INDEX:
        CATEGORY_INDEX[cat].append(entry_id)

# ---------------------------------------------------------------------------
# KEYWORD INDEX — for fast keyword-based retrieval
# ---------------------------------------------------------------------------

KEYWORD_INDEX = {}

for entry_id, entry in KNOWLEDGE_BASE.items():
    for kw in entry.get("keywords", []):
        kw_lower = kw.lower()
        if kw_lower not in KEYWORD_INDEX:
            KEYWORD_INDEX[kw_lower] = []
        KEYWORD_INDEX[kw_lower].append(entry_id)

# ---------------------------------------------------------------------------
# PRIORITY EMERGENCY ENTRIES — highest priority for risk critical response
# ---------------------------------------------------------------------------

EMERGENCY_ENTRY_IDS = [
    kb_id for kb_id, entry in KNOWLEDGE_BASE.items()
    if entry.get("priority", 3) == 1 and
    entry.get("category") == "emergency_assistance"
]

# ---------------------------------------------------------------------------
# STATS
# ---------------------------------------------------------------------------

def get_kb_stats():
    """Return summary statistics of the knowledge base."""
    stats = {
        "total_entries": len(KNOWLEDGE_BASE),
        "categories": {},
    }
    for cat, ids in CATEGORY_INDEX.items():
        stats["categories"][cat] = len(ids)
    return stats


if __name__ == "__main__":
    s = get_kb_stats()
    print(f"Total Knowledge Base Entries: {s['total_entries']}")
    print("\nEntries per Category:")
    for cat, count in s["categories"].items():
        print(f"  {cat:<35}: {count} entries")
    print(f"\nTotal Keywords Indexed: {len(KEYWORD_INDEX)}")
    print(f"Emergency Entry IDs: {EMERGENCY_ENTRY_IDS}")
