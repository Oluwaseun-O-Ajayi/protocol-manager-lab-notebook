import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sample_tracker import SampleTracker

print("\n" + "="*70)
print("EXAMPLE: Sample Inventory Management")
print("="*70 + "\n")

# Initialize tracker
tracker = SampleTracker()

# Add various sample types
print("Adding samples to inventory...\n")

# DNA samples
tracker.add_sample(
    sample_id="DNA-P001",
    sample_type="DNA",
    description="Plasmid pET28a(+)",
    location="Freezer A, Box 1, Position A1",
    quantity=200,
    unit="µg",
    concentration="1000 ng/µL",
    batch="B2024-12-001",
    source="Commercial (Novagen)",
    notes="High copy number expression vector with His-tag"
)

tracker.add_sample(
    sample_id="DNA-G045",
    sample_type="DNA",
    description="Genomic DNA - E. coli K12",
    location="Freezer A, Box 2, Position B3",
    quantity=150,
    unit="µg",
    concentration="500 ng/µL",
    batch="B2024-12-002",
    source="Lab prep - 2024-12-15"
)

# Protein samples
tracker.add_sample(
    sample_id="PROT-GFP-01",
    sample_type="Protein",
    description="His-tagged GFP (Green Fluorescent Protein)",
    location="Freezer B, Rack 3, Box 5",
    quantity=10,
    unit="mg",
    concentration="5 mg/mL",
    batch="P2024-11-089",
    source="Purified in-house",
    notes="Store in 10% glycerol, avoid freeze-thaw"
)

tracker.add_sample(
    sample_id="PROT-CAT-12",
    sample_type="Protein",
    description="Catalase from bovine liver",
    location="Freezer B, Rack 2, Box 3",
    quantity=25,
    unit="mg",
    concentration="10 mg/mL",
    batch="P2024-12-034",
    source="Commercial (Sigma)"
)

# Chemical samples
tracker.add_sample(
    sample_id="CHEM-IPTG",
    sample_type="Chemical",
    description="IPTG (Isopropyl β-D-1-thiogalactopyranoside)",
    location="Refrigerator, Shelf 2",
    quantity=5,
    unit="g",
    batch="C2024-08-123",
    source="Commercial (Gold Biotechnology)",
    notes="Make 1M stock solution in water"
)

# Display sample inventory
print("\n" + "="*70)
print("Current Inventory:")
print("="*70 + "\n")

all_samples = tracker.list_samples()
print(f"Total samples: {len(all_samples)}\n")

for sample in all_samples:
    print(f"{sample['sample_id']} - {sample['description']}")
    print(f"  Type: {sample['type']}")
    print(f"  Quantity: {sample['quantity']} {sample['unit']}")
    print(f"  Location: {sample['location']}")
    print()

# Use a sample
print("\n" + "="*70)
print("Recording Sample Usage:")
print("="*70 + "\n")

tracker.use_sample(
    sample_id="DNA-P001",
    amount_used=20,
    unit="µg",
    used_by="Dr. Ajayi",
    experiment_id="EXP_20241230_120000",
    notes="Used for transformation into BL21 cells"
)

# Display updated sample
tracker.display_sample("DNA-P001")

# Check inventory by location
print("\n" + "="*70)
print("Samples in Freezer A:")
print("="*70 + "\n")

freezer_a_samples = [s for s in tracker.list_samples() if 'Freezer A' in s['location']]
for sample in freezer_a_samples:
    print(f"{sample['sample_id']}: {sample['description']}")

# Check low stock
print("\n" + "="*70)
print("Low Stock Check:")
print("="*70 + "\n")

tracker.get_low_stock_alerts(threshold=15)

# Export inventory
print("\n" + "="*70)
print("Exporting Inventory:")
print("="*70 + "\n")

tracker.export_inventory('reports/inventory_export.csv')

# Visualize inventory
print("\n" + "="*70)
print("Generating Inventory Visualizations:")
print("="*70 + "\n")

tracker.plot_inventory_by_type(save_path='reports/inventory_by_type.png')
tracker.plot_inventory_by_location(save_path='reports/inventory_by_location.png')

print("\n✅ Sample tracking example completed!")