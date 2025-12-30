"""
Test script for Protocol Manager & Lab Notebook
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from protocol_manager import ProtocolManager
from lab_notebook import LabNotebook
from sample_tracker import SampleTracker
from report_generator import ReportGenerator

print("🧪 Testing Protocol Manager & Lab Notebook...\n")

# Test 1: Protocol Manager
print("Test 1: Protocol Manager...")
try:
    manager = ProtocolManager()
    print("✅ Protocol Manager initialized\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    exit()

# Test 2: Lab Notebook
print("Test 2: Lab Notebook...")
try:
    notebook = LabNotebook()
    print("✅ Lab Notebook initialized\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    exit()

# Test 3: Sample Tracker
print("Test 3: Sample Tracker...")
try:
    tracker = SampleTracker()
    print("✅ Sample Tracker initialized\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    exit()

# Test 4: Report Generator
print("Test 4: Report Generator...")
try:
    reporter = ReportGenerator()
    print("✅ Report Generator initialized\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    exit()

print("🎉 All modules loaded successfully!")
print("\n💡 Next steps:")
print("   python examples/create_protocol.py")
print("   python examples/log_experiment.py")
print("   python examples/track_samples.py")
print("   python examples/generate_report.py")