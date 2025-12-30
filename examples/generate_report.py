import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lab_notebook import LabNotebook
from protocol_manager import ProtocolManager
from sample_tracker import SampleTracker
from report_generator import ReportGenerator

print("\n" + "="*70)
print("EXAMPLE: Generating Lab Reports")
print("="*70 + "\n")

# Initialize components
notebook = LabNotebook()
protocol_manager = ProtocolManager()
sample_tracker = SampleTracker()
report_gen = ReportGenerator()

# Load an experiment
print("Loading experiment data...\n")
experiments = notebook.list_experiments()

if experiments:
    # Get the most recent experiment
    exp_id = experiments[0]['id']
    experiment = notebook.load_experiment(exp_id)
    
    # Generate experiment report
    print("="*70)
    print("Generating Experiment Report:")
    print("="*70 + "\n")
    
    report_gen.generate_experiment_report(
        experiment,
        output_file=f"{exp_id}_report.txt"
    )

# Load a protocol
print("\n" + "="*70)
print("Generating Protocol Summary:")
print("="*70 + "\n")

protocols = protocol_manager.list_protocols()
if protocols:
    protocol_id = protocols[0]['id']
    protocol = protocol_manager.load_protocol(protocol_id)
    
    report_gen.generate_protocol_summary(
        protocol,
        output_file=f"{protocol_id}_summary.txt"
    )

# Generate inventory report
print("\n" + "="*70)
print("Generating Inventory Report:")
print("="*70 + "\n")

samples = sample_tracker.list_samples()
if samples:
    report_gen.generate_inventory_report(
        samples,
        output_file='inventory_status_report.txt'
    )

# Generate weekly summary
print("\n" + "="*70)
print("Generating Weekly Summary:")
print("="*70 + "\n")

from datetime import datetime, timedelta

end_date = datetime.now().isoformat()
start_date = (datetime.now() - timedelta(days=7)).isoformat()

all_experiments = [notebook.load_experiment(e['id']) for e in experiments]

report_gen.generate_weekly_summary(
    all_experiments,
    start_date=start_date,
    end_date=end_date,
    output_file='weekly_summary.txt'
)

print("\n" + "="*70)
print("All Reports Generated Successfully!")
print("="*70)
print("\nCheck the 'reports/' folder for generated files:")
print("  - Experiment reports")
print("  - Protocol summaries")
print("  - Inventory reports")
print("  - Weekly summaries")

print("\n✅ Report generation example completed!")