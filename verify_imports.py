"""Quick import verification for the redesigned AegisAI."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

errors = []

def check(label, fn):
    try:
        fn()
        print(f"  OK  {label}")
    except Exception as e:
        print(f"  FAIL  {label}: {e}")
        errors.append(label)

check("models.message",    lambda: __import__("models.message", fromlist=["ChatMessage"]))
check("models.assessment", lambda: __import__("models.assessment", fromlist=["RiskLevel"]))
check("models.scam",       lambda: __import__("models.scam", fromlist=["SuspicionLevel"]))
check("models.session",    lambda: __import__("models.session", fromlist=["AppSession"]))
check("knowledge.kb_manager", lambda: __import__("knowledge.kb_manager", fromlist=["KBManager"]))
check("knowledge.rule_engine", lambda: __import__("knowledge.rule_engine", fromlist=["RuleEngine"]))
check("services.session_service",    lambda: __import__("services.session_service", fromlist=["SessionService"]))
check("services.intent_service",     lambda: __import__("services.intent_service", fromlist=["Intent"]))
check("services.chat_service",       lambda: __import__("services.chat_service", fromlist=["ChatService"]))
check("services.assessment_service", lambda: __import__("services.assessment_service", fromlist=["AssessmentService"]))
check("services.scam_service",       lambda: __import__("services.scam_service", fromlist=["ScamService"]))
check("utils.logger",       lambda: __import__("utils.logger", fromlist=["setup_logging"]))
check("utils.threading_utils", lambda: __import__("utils.threading_utils", fromlist=["run_in_thread"]))
check("ui.theme",           lambda: __import__("ui.theme", fromlist=["Theme"]))
check("customtkinter",      lambda: __import__("customtkinter"))

# Functional checks
from knowledge.kb_manager import KBManager
from knowledge.rule_engine import RuleEngine
from services.intent_service import IntentService, Intent
from services.assessment_service import AssessmentService
from services.session_service import SessionService

kb = KBManager()
stats = kb.stats()
print("KB stats:", stats)

engine = RuleEngine()
intent_svc = IntentService(kb)
intent = intent_svc.classify("what is human trafficking")
print("Intent for 'what is human trafficking':", intent.name)

assess = AssessmentService(engine)
q = assess.start()
print("First Q:", q.text[:80])

sess = SessionService.instance()
from models.assessment import RiskLevel
sess.set_risk_level(RiskLevel.HIGH)
print("Session risk:", sess.state.risk_level.label)

print()
if errors:
    print("FAILED:", errors)
else:
    print("ALL CHECKS PASSED")
