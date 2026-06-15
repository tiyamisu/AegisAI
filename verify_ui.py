"""Quick UI import verification."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

errors = []

def chk(label, fn):
    try:
        fn()
        print(f"  OK  {label}")
    except Exception as e:
        print(f"  FAIL  {label}: {e}")
        errors.append(label)

chk("ui.theme",             lambda: __import__("ui.theme", fromlist=["Theme"]))
chk("ui.components.sidebar", lambda: __import__("ui.components.sidebar", fromlist=["Sidebar"]))
chk("ui.components.header",  lambda: __import__("ui.components.header", fromlist=["Header"]))
chk("ui.components.chat_widget", lambda: __import__("ui.components.chat_widget", fromlist=["ChatWidget"]))
chk("ui.components.stat_card",   lambda: __import__("ui.components.stat_card", fromlist=["StatCard"]))
chk("ui.components.risk_badge",  lambda: __import__("ui.components.risk_badge", fromlist=["RiskBadge"]))
chk("ui.pages.dashboard",    lambda: __import__("ui.pages.dashboard", fromlist=["DashboardPage"]))
chk("ui.pages.awareness",    lambda: __import__("ui.pages.awareness", fromlist=["AwarenessPage"]))
chk("ui.pages.assessment",   lambda: __import__("ui.pages.assessment", fromlist=["AssessmentPage"]))
chk("ui.pages.scam_analyzer",lambda: __import__("ui.pages.scam_analyzer", fromlist=["ScamAnalyzerPage"]))
chk("ui.pages.emergency",    lambda: __import__("ui.pages.emergency", fromlist=["EmergencyPage"]))
chk("ui.pages.resources",    lambda: __import__("ui.pages.resources", fromlist=["ResourcesPage"]))
chk("ui.app_window",         lambda: __import__("ui.app_window", fromlist=["AegisAIApp"]))

print()
if errors:
    print("FAILED:", errors)
else:
    print("ALL UI IMPORTS: OK")
