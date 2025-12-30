# Protocol Manager & Digital Lab Notebook 📓🔬

A comprehensive Python toolkit for managing research protocols, logging experiments, tracking samples, and generating professional lab reports. Designed for researchers who want to organize their lab work efficiently.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

This toolkit provides a complete digital lab management system, replacing paper notebooks and spreadsheets with an organized, version-controlled, and searchable system.

## 🌟 Key Features

### 📋 Protocol Manager
- **Version Control** - Track protocol changes with automatic versioning
- **Template Library** - Pre-built templates for common procedures (PCR, Western blot, etc.)
- **Lab Checklists** - Generate printable checklists for bench work
- **Search & Filter** - Find protocols by keywords and tags

### 📓 Digital Lab Notebook
- **Experiment Logging** - Document experiments with timestamps
- **Observation Tracking** - Record real-time observations
- **Results Management** - Store and organize experimental results
- **Status Tracking** - Monitor in-progress and completed experiments

### 🧪 Sample Tracker
- **Inventory Management** - Track all lab samples in one place
- **Usage History** - Record when and how samples are used
- **Low Stock Alerts** - Get notified when supplies run low
- **Location Mapping** - Know exactly where each sample is stored

### 📊 Report Generator
- **Experiment Reports** - Professional formatted experiment summaries
- **Protocol Summaries** - Detailed protocol documentation
- **Inventory Reports** - Complete inventory status reports
- **Weekly Summaries** - Track research activity over time

## ⚡ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Oluwaseun-O-Ajayi/protocol-manager-lab-notebook.git
cd protocol-manager-lab-notebook

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from protocol_manager import ProtocolManager
from lab_notebook import LabNotebook
from sample_tracker import SampleTracker
from report_generator import ReportGenerator

# Initialize components
protocol_mgr = ProtocolManager()
notebook = LabNotebook()
tracker = SampleTracker()
reporter = ReportGenerator()

# Create a protocol
protocol_id = protocol_mgr.create_protocol(
    name="DNA Extraction",
    description="Extract genomic DNA from tissue samples",
    steps=["Add lysis buffer", "Incubate at 55°C", "Centrifuge", "..."],
    materials=["Lysis buffer", "Proteinase K", "..."],
    tags=["DNA", "Extraction"]
)

# Log an experiment
exp_id = notebook.create_experiment(
    title="Gene Expression Analysis",
    objective="Measure gene X expression levels",
    materials=["RNA samples", "RT-PCR kit"]
)

# Track a sample
tracker.add_sample(
    sample_id="DNA-001",
    sample_type="DNA",
    description="Plasmid pUC19",
    location="Freezer A, Box 3",
    quantity=100,
    unit="µg"
)

# Generate report
reporter.generate_experiment_report(experiment)
```

## 📦 Requirements

```
pandas>=1.5.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

## 💻 Modules

### 1. Protocol Manager

Manage and version control your lab protocols.

**Create Protocol:**
```python
from protocol_manager import ProtocolManager

manager = ProtocolManager()

protocol_id = manager.create_protocol(
    name="PCR Amplification",
    description="Standard PCR protocol",
    steps=[
        {"action": "Initial denaturation", "temperature": "95°C", "duration": "3 min"},
        {"action": "Denaturation", "temperature": "95°C", "duration": "30 sec"},
        {"action": "Annealing", "temperature": "55°C", "duration": "30 sec"},
        {"action": "Extension", "temperature": "72°C", "duration": "1 min"}
    ],
    materials=["Taq polymerase", "dNTPs", "Primers", "Template DNA"],
    tags=["PCR", "Molecular Biology"]
)
```

**Use Template:**
```python
# Create protocol from pre-built template
protocol_id = manager.create_from_template(
    'pcr_protocol',
    name="PCR for Gene X"
)
```

**Update Protocol:**
```python
# Updates create new version automatically
new_id = manager.update_protocol(
    protocol_id,
    notes="Added optimization for GC-rich templates"
)
```

**Generate Checklist:**
```python
checklist = manager.create_checklist(
    protocol_id,
    output_file='pcr_checklist.txt'
)
```

### 2. Digital Lab Notebook

Log experiments with full traceability.

**Create Experiment:**
```python
from lab_notebook import LabNotebook

notebook = LabNotebook()

exp_id = notebook.create_experiment(
    title="Protein Expression Optimization",
    objective="Optimize IPTG concentration",
    hypothesis="0.5mM IPTG will give highest yield",
    materials=["E. coli cells", "IPTG", "LB media"],
    tags=["Protein Expression", "Optimization"]
)
```

**Add Observations:**
```python
notebook.add_observation(
    exp_id,
    "Induced cultures with 0.1, 0.5, 1.0 mM IPTG at OD600=0.6"
)

notebook.add_observation(
    exp_id,
    "Incubated 4 hours at 37°C"
)
```

**Add Results:**
```python
results = {
    '0.1mM': '15 mg/L',
    '0.5mM': '45 mg/L',
    '1.0mM': '38 mg/L'
}

notebook.add_results(exp_id, results)
```

**Complete Experiment:**
```python
notebook.complete_experiment(
    exp_id,
    conclusions="Optimal expression at 0.5mM IPTG"
)
```

**Search Experiments:**
```python
# Find experiments by keyword
matches = notebook.search_experiments("protein")

# Filter by status
in_progress = notebook.list_experiments(status="In Progress")
completed = notebook.list_experiments(status="Completed")
```

### 3. Sample Tracker

Manage your lab inventory efficiently.

**Add Sample:**
```python
from sample_tracker import SampleTracker

tracker = SampleTracker()

tracker.add_sample(
    sample_id="PROT-GFP-01",
    sample_type="Protein",
    description="His-tagged GFP",
    location="Freezer B, Rack 3",
    quantity=10,
    unit="mg",
    concentration="5 mg/mL",
    batch="P2024-089"
)
```

**Record Usage:**
```python
tracker.use_sample(
    sample_id="PROT-GFP-01",
    amount_used=2,
    unit="mg",
    used_by="Dr. Ajayi",
    experiment_id="EXP_20241230_120000",
    notes="Used for fluorescence assay"
)
```

**Check Inventory:**
```python
# List all samples
all_samples = tracker.list_samples()

# Filter by type
dna_samples = tracker.list_samples(sample_type="DNA")

# Filter by location
freezer_a = tracker.list_samples(location="Freezer A")
```

**Low Stock Alerts:**
```python
low_stock = tracker.get_low_stock_alerts(threshold=10)
```

**Visualizations:**
```python
# Inventory by sample type
tracker.plot_inventory_by_type(save_path='inventory_types.png')

# Inventory by location
tracker.plot_inventory_by_location(save_path='inventory_locations.png')
```

### 4. Report Generator

Generate professional lab reports.

**Experiment Report:**
```python
from report_generator import ReportGenerator

reporter = ReportGenerator()

# Load experiment
experiment = notebook.load_experiment('EXP_20241230_120000')

# Generate report
reporter.generate_experiment_report(
    experiment,
    output_file='experiment_report.txt'
)
```

**Protocol Summary:**
```python
protocol = manager.load_protocol('pcr_protocol_20241230')

reporter.generate_protocol_summary(
    protocol,
    output_file='protocol_summary.txt'
)
```

**Inventory Report:**
```python
samples = tracker.list_samples()

reporter.generate_inventory_report(
    samples,
    output_file='inventory_report.txt'
)
```

**Weekly Summary:**
```python
from datetime import datetime, timedelta

end_date = datetime.now().isoformat()
start_date = (datetime.now() - timedelta(days=7)).isoformat()

experiments = notebook.list_experiments()
all_exp_data = [notebook.load_experiment(e['id']) for e in experiments]

reporter.generate_weekly_summary(
    all_exp_data,
    start_date=start_date,
    end_date=end_date,
    output_file='weekly_summary.txt'
)
```

## 📁 Project Structure

```
protocol-manager-lab-notebook/
├── protocol_manager.py         # Protocol management with version control
├── lab_notebook.py             # Digital experiment logging
├── sample_tracker.py           # Sample inventory management
├── report_generator.py         # Report generation
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
├── templates/                  # Protocol templates
│   ├── pcr_protocol.json
│   └── protein_purification.json
├── examples/                   # Example scripts
│   ├── create_protocol.py
│   ├── log_experiment.py
│   ├── track_samples.py
│   └── generate_report.py
├── protocols/                  # Stored protocols
│   └── README.md
├── experiments/                # Experiment logs
│   └── README.md
├── samples/                    # Sample inventory
│   └── README.md
├── reports/                    # Generated reports
│   └── README.md
└── data/                       # Experimental data
    └── README.md
```

## 🔬 Example Workflows

### Workflow 1: Complete Experiment Documentation

```python
from protocol_manager import ProtocolManager
from lab_notebook import LabNotebook
from report_generator import ReportGenerator

# 1. Load protocol
manager = ProtocolManager()
protocol = manager.load_protocol('pcr_protocol_20241230')

# 2. Create experiment
notebook = LabNotebook()
exp_id = notebook.create_experiment(
    title="Gene X Amplification",
    protocol_id=protocol['id'],
    objective="Amplify and clone Gene X"
)

# 3. Log observations as you work
notebook.add_observation(exp_id, "PCR setup complete")
notebook.add_observation(exp_id, "Running thermocycler program")
notebook.add_observation(exp_id, "Gel electrophoresis shows single band at expected size")

# 4. Add results
notebook.add_results(exp_id, {
    'product_size': '1.2 kb',
    'yield': '45 ng/µL',
    'purity': 'Clean single band'
})

# 5. Complete and generate report
notebook.complete_experiment(exp_id, "Successfully amplified Gene X")

reporter = ReportGenerator()
experiment = notebook.load_experiment(exp_id)
reporter.generate_experiment_report(experiment)
```

### Workflow 2: Sample Management

```python
from sample_tracker import SampleTracker

tracker = SampleTracker()

# Add new samples from prep
tracker.add_sample(
    sample_id="DNA-G100",
    sample_type="DNA",
    description="Genomic DNA from strain A",
    location="Freezer A, Box 5",
    quantity=250,
    unit="µg",
    batch="B2024-12-30"
)

# Use samples in experiments
tracker.use_sample(
    sample_id="DNA-G100",
    amount_used=50,
    unit="µg",
    used_by="Dr. Ajayi",
    experiment_id="EXP_20241230_150000"
)

# Check what's running low
low_stock = tracker.get_low_stock_alerts(threshold=20)

# Generate inventory report
tracker.export_inventory('current_inventory.csv')
```

### Workflow 3: Protocol Development

```python
from protocol_manager import ProtocolManager

manager = ProtocolManager()

# Start with template
protocol_id = manager.create_from_template('pcr_protocol')

# Test and optimize
# ... run experiments ...

# Update protocol with optimizations
optimized_id = manager.update_protocol(
    protocol_id,
    notes="Optimized annealing temperature to 58°C for better specificity"
)

# Generate summary and checklist
manager.display_protocol(optimized_id)
manager.create_checklist(optimized_id, output_file='optimized_pcr_checklist.txt')
```

## 🎯 Real-World Applications

### Academic Research
- **Thesis Work** - Complete experiment documentation for publications
- **Lab Group** - Standardized protocols across research group
- **Reproducibility** - Detailed records for methods sections
- **Progress Tracking** - Monitor research milestones

### Pharmaceutical/Biotech
- **GLP Compliance** - Maintain detailed lab records
- **Quality Control** - Track sample batches and testing
- **SOP Management** - Version-controlled standard operating procedures
- **Audit Trail** - Complete experiment traceability

### Teaching Labs
- **Student Training** - Standardized protocol access
- **Lab Safety** - Proper procedure documentation
- **Assessment** - Track student experiment completion
- **Resource Management** - Monitor reagent usage

## 🛠️ Customization

### Adding Custom Protocol Templates

Create new JSON files in the `templates/` folder:

```json
{
  "name": "Your Protocol Name",
  "description": "Brief description",
  "steps": [
    {"action": "Step 1", "duration": "10 min"},
    {"action": "Step 2", "temperature": "37°C"}
  ],
  "materials": ["Item 1", "Item 2"],
  "tags": ["Tag1", "Tag2"]
}
```

### Extending Functionality

```python
from protocol_manager import ProtocolManager

class CustomProtocolManager(ProtocolManager):
    def export_to_pdf(self, protocol_id):
        """Add PDF export functionality."""
        # Your custom code here
        pass
```

## 📊 Data Management

### Backup Your Data

```bash
# Backup all lab data
tar -czf lab_backup_$(date +%Y%m%d).tar.gz \
    protocols/ experiments/ samples/ reports/ data/
```

### Export Data

```python
# Export experiments to CSV
notebook = LabNotebook()
notebook.export_to_csv('all_experiments.csv')

# Export inventory
tracker = SampleTracker()
tracker.export_inventory('inventory_backup.csv')
```

## 🔒 Data Security

- All data stored locally - you control your research data
- JSON format for easy backup and version control
- No cloud dependencies - works offline
- Git-friendly for team collaboration

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- PDF report generation
- Database backend option (SQLite, PostgreSQL)
- Web interface (Flask/Django)
- Mobile app integration
- Barcode/QR code sample tracking
- Integration with lab instruments
- Multi-user collaboration features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by electronic lab notebook (ELN) systems
- Designed for practical lab use
- Built for researchers, by researchers

## 📧 Contact

**Oluwaseun O. Ajayi**  
PhD Researcher in Chemistry  
University of Georgia

- **GitHub**: [@Oluwaseun-O-Ajayi](https://github.com/Oluwaseun-O-Ajayi)
- **Academic Email**: oluwaseun.ajayi@uga.edu
- **Personal Email**: seunolanikeajayi@gmail.com

## 📖 Citation

If you use this toolkit in your research:

```bibtex
@software{protocol_manager_lab_notebook,
  author = {Oluwaseun O. Ajayi},
  title = {Protocol Manager & Digital Lab Notebook},
  year = {2024},
  url = {https://github.com/Oluwaseun-O-Ajayi/protocol-manager-lab-notebook}
}
```

## 🚀 Getting Started

1. **Install the toolkit**
   ```bash
   git clone https://github.com/Oluwaseun-O-Ajayi/protocol-manager-lab-notebook.git
   cd protocol-manager-lab-notebook
   pip install -r requirements.txt
   ```

2. **Try the examples**
   ```bash
   python examples/create_protocol.py
   python examples/log_experiment.py
   python examples/track_samples.py
   python examples/generate_report.py
   ```

3. **Start using in your lab!**

---

⭐ **Star this repository** if you find it useful for your research!

**Made with ❤️ for the research community**