import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lab_notebook import LabNotebook

print("\n" + "="*70)
print("EXAMPLE: Logging an Experiment")
print("="*70 + "\n")

# Initialize notebook
notebook = LabNotebook()

# Create a new experiment
exp_id = notebook.create_experiment(
    title="Enzyme Kinetics Study - Catalase",
    objective="Determine Km and Vmax values for catalase enzyme",
    hypothesis="Catalase will show Michaelis-Menten kinetics with H2O2 substrate",
    materials=[
        "Catalase enzyme (purified)",
        "H2O2 substrate (various concentrations)",
        "Phosphate buffer pH 7.0",
        "Spectrophotometer",
        "Cuvettes"
    ],
    tags=["Enzyme Kinetics", "Biochemistry", "Catalase"]
)

print("\n" + "="*70)
print("Adding Observations:")
print("="*70 + "\n")

# Add observations throughout the experiment
notebook.add_observation(
    exp_id,
    "Prepared substrate solutions: 0.1, 0.5, 1.0, 2.0, 5.0, 10.0 mM H2O2"
)

notebook.add_observation(
    exp_id,
    "Added enzyme (final concentration 10 nM) to each substrate concentration"
)

notebook.add_observation(
    exp_id,
    "Measured initial reaction rates by monitoring absorbance at 240 nm"
)

notebook.add_observation(
    exp_id,
    "All reactions performed at 25°C in triplicate"
)

# Add results
print("\n" + "="*70)
print("Adding Results:")
print("="*70 + "\n")

results = {
    "substrate_0.1mM": "5.2 µmol/min",
    "substrate_0.5mM": "18.3 µmol/min",
    "substrate_1.0mM": "28.5 µmol/min",
    "substrate_2.0mM": "38.2 µmol/min",
    "substrate_5.0mM": "45.8 µmol/min",
    "substrate_10.0mM": "47.1 µmol/min",
    "Km_calculated": "1.2 mM",
    "Vmax_calculated": "50.0 µmol/min"
}

notebook.add_results(exp_id, results)

# Complete the experiment
print("\n" + "="*70)
print("Completing Experiment:")
print("="*70 + "\n")

notebook.complete_experiment(
    exp_id,
    conclusions=(
        "Catalase follows Michaelis-Menten kinetics with H2O2 substrate. "
        "Determined Km = 1.2 mM and Vmax = 50.0 µmol/min. "
        "The high catalytic efficiency (kcat/Km) confirms catalase's role "
        "as an efficient antioxidant enzyme. Results are consistent with "
        "literature values for bovine liver catalase."
    )
)

# Display complete experiment
notebook.display_experiment(exp_id)

# List all experiments
print("\n" + "="*70)
print("Current Experiments in Notebook:")
print("="*70 + "\n")

all_experiments = notebook.list_experiments()
for exp in all_experiments:
    print(f"{exp['id']}: {exp['title']} [{exp['status']}]")

print("\n✅ Experiment logging example completed!")