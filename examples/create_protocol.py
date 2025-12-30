import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from protocol_manager import ProtocolManager

print("\n" + "="*70)
print("EXAMPLE: Creating a Custom Protocol")
print("="*70 + "\n")

# Initialize manager
manager = ProtocolManager()

# Create custom protocol
protocol_id = manager.create_protocol(
    name="Western Blot Analysis",
    description="Protocol for protein detection via Western blotting",
    steps=[
        {
            "action": "Run SDS-PAGE gel",
            "duration": "60 min",
            "notes": "Use 10% or 12% gel depending on protein size"
        },
        {
            "action": "Transfer proteins to PVDF membrane",
            "duration": "90 min",
            "temperature": "4°C",
            "notes": "Use transfer buffer with 20% methanol"
        },
        {
            "action": "Block membrane",
            "duration": "1 hour",
            "notes": "Use 5% milk in TBST"
        },
        {
            "action": "Incubate with primary antibody",
            "duration": "overnight",
            "temperature": "4°C",
            "notes": "Dilute antibody as per datasheet"
        },
        {
            "action": "Wash membrane",
            "duration": "15 min",
            "notes": "3 x 5 min washes with TBST"
        },
        {
            "action": "Incubate with secondary antibody",
            "duration": "1 hour",
            "notes": "HRP-conjugated, 1:5000 dilution"
        },
        {
            "action": "Wash membrane",
            "duration": "15 min",
            "notes": "3 x 5 min washes with TBST"
        },
        {
            "action": "Develop with ECL substrate",
            "duration": "5 min"
        },
        {
            "action": "Image using chemiluminescence detector"
        }
    ],
    materials=[
        "SDS-PAGE gel",
        "Transfer buffer",
        "PVDF membrane",
        "Blocking buffer (5% milk in TBST)",
        "Primary antibody",
        "Secondary antibody (HRP-conjugated)",
        "TBST (Tris-buffered saline with Tween)",
        "ECL substrate",
        "Imaging system"
    ],
    tags=["Western Blot", "Protein Analysis", "Immunoblotting"],
    notes="Always include positive control and molecular weight markers"
)

# Display the protocol
print("\n" + "="*70)
print("Created Protocol:")
print("="*70)
manager.display_protocol(protocol_id)

# Create a checklist for lab use
print("\n" + "="*70)
print("Generating Lab Checklist:")
print("="*70 + "\n")

checklist = manager.create_checklist(
    protocol_id,
    output_file=f"reports/{protocol_id}_checklist.txt"
)
print(checklist)

# Create protocol from template
print("\n" + "="*70)
print("Creating Protocol from Template:")
print("="*70 + "\n")

pcr_protocol_id = manager.create_from_template(
    'pcr_protocol',
    name="PCR for Gene X Amplification",
    notes="Specific protocol for amplifying Gene X from genomic DNA"
)

manager.display_protocol(pcr_protocol_id)

print("\n✅ Protocol creation examples completed!")