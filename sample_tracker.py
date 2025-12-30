"""
Sample Tracker
==============

Track samples, inventory, and storage locations.

Author: Oluwaseun O. Ajayi
Email: oluwaseun.ajayi@uga.edu
GitHub: @Oluwaseun-O-Ajayi
Institution: University of Georgia
"""

import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


class SampleTracker:
    """
    Track research samples and inventory.
    """
    
    def __init__(self, sample_dir='samples'):
        """
        Initialize Sample Tracker.
        
        Args:
            sample_dir: Directory to store sample records
        """
        self.sample_dir = Path(sample_dir)
        self.sample_dir.mkdir(exist_ok=True)
        
        # Initialize inventory database
        self.inventory_file = self.sample_dir / 'inventory.json'
        if not self.inventory_file.exists():
            with open(self.inventory_file, 'w') as f:
                json.dump({'samples': []}, f)
        
        print(f"✅ Sample Tracker Initialized")
        print(f"   Samples: {self.sample_dir.absolute()}")
    
    def add_sample(self, sample_id, sample_type, description,
                   location, quantity, unit, concentration=None,
                   batch=None, source=None, notes=None):
        """
        Add a new sample to inventory.
        
        Args:
            sample_id: Unique sample identifier
            sample_type: Type of sample (DNA, Protein, Chemical, etc.)
            description: Sample description
            location: Storage location
            quantity: Amount of sample
            unit: Unit of measurement
            concentration: Optional concentration
            batch: Batch number
            source: Sample source/origin
            notes: Additional notes
        
        Returns:
            Sample ID
        """
        # Load current inventory
        with open(self.inventory_file, 'r') as f:
            inventory = json.load(f)
        
        # Check if sample ID already exists
        existing_ids = [s['sample_id'] for s in inventory['samples']]
        if sample_id in existing_ids:
            print(f"❌ Sample ID already exists: {sample_id}")
            return None
        
        # Create sample record
        sample = {
            'sample_id': sample_id,
            'type': sample_type,
            'description': description,
            'location': location,
            'quantity': quantity,
            'unit': unit,
            'concentration': concentration,
            'batch': batch,
            'source': source or '',
            'notes': notes or '',
            'added': datetime.now().isoformat(),
            'status': 'Available',
            'usage_history': []
        }
        
        # Add to inventory
        inventory['samples'].append(sample)
        
        # Save inventory
        with open(self.inventory_file, 'w') as f:
            json.dump(inventory, f, indent=2)
        
        print(f"✅ Sample added: {sample_id}")
        print(f"   Type: {sample_type}")
        print(f"   Quantity: {quantity} {unit}")
        print(f"   Location: {location}")
        
        return sample_id
    
    def get_sample(self, sample_id):
        """
        Retrieve sample information.
        
        Args:
            sample_id: Sample ID
        
        Returns:
            Sample dictionary
        """
        with open(self.inventory_file, 'r') as f:
            inventory = json.load(f)
        
        for sample in inventory['samples']:
            if sample['sample_id'] == sample_id:
                return sample
        
        print(f"❌ Sample not found: {sample_id}")
        return None
    
    def update_sample(self, sample_id, **updates):
        """
        Update sample information.
        
        Args:
            sample_id: Sample ID
            **updates: Fields to update
        """
        with open(self.inventory_file, 'r') as f:
            inventory = json.load(f)
        
        for sample in inventory['samples']:
            if sample['sample_id'] == sample_id:
                sample.update(updates)
                sample['last_modified'] = datetime.now().isoformat()
                
                # Save updated inventory
                with open(self.inventory_file, 'w') as f:
                    json.dump(inventory, f, indent=2)
                
                print(f"✅ Sample updated: {sample_id}")
                return
        
        print(f"❌ Sample not found: {sample_id}")
    
    def use_sample(self, sample_id, amount_used, unit, used_by, 
                   experiment_id=None, notes=None):
        """
        Record sample usage.
        
        Args:
            sample_id: Sample ID
            amount_used: Amount used
            unit: Unit of measurement
            used_by: Person using sample
            experiment_id: Associated experiment ID
            notes: Usage notes
        """
        sample = self.get_sample(sample_id)
        if not sample:
            return
        
        # Record usage
        usage = {
            'date': datetime.now().isoformat(),
            'amount': amount_used,
            'unit': unit,
            'used_by': used_by,
            'experiment_id': experiment_id,
            'notes': notes or ''
        }
        
        # Update quantity
        if sample['unit'] == unit:
            new_quantity = sample['quantity'] - amount_used
            
            # Update sample
            with open(self.inventory_file, 'r') as f:
                inventory = json.load(f)
            
            for s in inventory['samples']:
                if s['sample_id'] == sample_id:
                    s['quantity'] = new_quantity
                    s['usage_history'].append(usage)
                    
                    # Update status if depleted
                    if new_quantity <= 0:
                        s['status'] = 'Depleted'
                    
                    break
            
            # Save inventory
            with open(self.inventory_file, 'w') as f:
                json.dump(inventory, f, indent=2)
            
            print(f"✅ Usage recorded for {sample_id}")
            print(f"   Remaining: {new_quantity} {unit}")
        else:
            print(f"❌ Unit mismatch: {unit} vs {sample['unit']}")
    
    def list_samples(self, sample_type=None, location=None, status=None):
        """
        List samples with optional filters.
        
        Args:
            sample_type: Filter by sample type
            location: Filter by location
            status: Filter by status
        
        Returns:
            List of samples
        """
        with open(self.inventory_file, 'r') as f:
            inventory = json.load(f)
        
        samples = inventory['samples']
        
        # Apply filters
        if sample_type:
            samples = [s for s in samples if s['type'] == sample_type]
        if location:
            samples = [s for s in samples if s['location'] == location]
        if status:
            samples = [s for s in samples if s['status'] == status]
        
        return samples
    
    def display_sample(self, sample_id):
        """
        Display sample details.
        
        Args:
            sample_id: Sample ID
        """
        sample = self.get_sample(sample_id)
        if not sample:
            return
        
        print(f"\n{'='*70}")
        print(f"SAMPLE: {sample['sample_id']}")
        print(f"{'='*70}")
        print(f"Type: {sample['type']}")
        print(f"Description: {sample['description']}")
        print(f"Status: {sample['status']}")
        print(f"Quantity: {sample['quantity']} {sample['unit']}")
        if sample.get('concentration'):
            print(f"Concentration: {sample['concentration']}")
        print(f"Location: {sample['location']}")
        if sample.get('batch'):
            print(f"Batch: {sample['batch']}")
        if sample.get('source'):
            print(f"Source: {sample['source']}")
        print(f"Added: {sample['added']}")
        
        if sample.get('notes'):
            print(f"\nNotes: {sample['notes']}")
        
        # Usage history
        if sample.get('usage_history'):
            print(f"\nUsage History:")
            for usage in sample['usage_history']:
                print(f"  [{usage['date']}]")
                print(f"  Amount: {usage['amount']} {usage['unit']}")
                print(f"  Used by: {usage['used_by']}")
                if usage.get('experiment_id'):
                    print(f"  Experiment: {usage['experiment_id']}")
                print()
        
        print(f"{'='*70}\n")
    
    def export_inventory(self, output_file='inventory_export.csv'):
        """
        Export inventory to CSV.
        
        Args:
            output_file: Output filename
        """
        samples = self.list_samples()
        
        if not samples:
            print("❌ No samples to export")
            return
        
        # Create DataFrame
        df = pd.DataFrame(samples)
        
        # Drop usage history for CSV (too complex)
        if 'usage_history' in df.columns:
            df = df.drop('usage_history', axis=1)
        
        df.to_csv(output_file, index=False)
        
        print(f"✅ Exported {len(samples)} samples to {output_file}")
    
    def plot_inventory_by_type(self, save_path=None):
        """
        Visualize inventory distribution by type.
        
        Args:
            save_path: Optional path to save figure
        """
        samples = self.list_samples()
        
        if not samples:
            print("❌ No samples to plot")
            return
        
        # Count by type
        df = pd.DataFrame(samples)
        type_counts = df['type'].value_counts()
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        type_counts.plot(kind='bar', ax=ax, color='steelblue',
                        edgecolor='black', linewidth=1)
        
        ax.set_xlabel('Sample Type', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Samples', fontsize=12, fontweight='bold')
        ax.set_title('Inventory Distribution by Sample Type', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Plot saved to: {save_path}")
        
        plt.show()
    
    def plot_inventory_by_location(self, save_path=None):
        """
        Visualize inventory distribution by location.
        
        Args:
            save_path: Optional path to save figure
        """
        samples = self.list_samples()
        
        if not samples:
            print("❌ No samples to plot")
            return
        
        # Count by location
        df = pd.DataFrame(samples)
        location_counts = df['location'].value_counts()
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        location_counts.plot(kind='barh', ax=ax, color='coral',
                            edgecolor='black', linewidth=1)
        
        ax.set_xlabel('Number of Samples', fontsize=12, fontweight='bold')
        ax.set_ylabel('Location', fontsize=12, fontweight='bold')
        ax.set_title('Inventory Distribution by Location', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Plot saved to: {save_path}")
        
        plt.show()
    
    def get_low_stock_alerts(self, threshold=10):
        """
        Get samples with low stock.
        
        Args:
            threshold: Quantity threshold for alert
        
        Returns:
            List of low stock samples
        """
        samples = self.list_samples(status='Available')
        
        low_stock = [s for s in samples if s['quantity'] <= threshold]
        
        if low_stock:
            print(f"⚠️  {len(low_stock)} samples below threshold ({threshold})")
            for sample in low_stock:
                print(f"   {sample['sample_id']}: {sample['quantity']} {sample['unit']}")
        else:
            print(f"✅ All samples above threshold")
        
        return low_stock


# Example usage
if __name__ == "__main__":
    print("\n" + "="*70)
    print("SAMPLE TRACKER - Example Usage")
    print("="*70 + "\n")
    
    # Initialize tracker
    tracker = SampleTracker()
    
    # Add samples
    tracker.add_sample(
        sample_id="DNA-001",
        sample_type="DNA",
        description="Plasmid pUC19",
        location="Freezer A, Box 3",
        quantity=100,
        unit="µg",
        concentration="500 ng/µL",
        batch="B2024-01",
        source="Lab prep",
        notes="High quality prep, verified by sequencing"
    )
    
    tracker.add_sample(
        sample_id="PROT-045",
        sample_type="Protein",
        description="His-tagged GFP",
        location="Freezer B, Rack 2",
        quantity=5,
        unit="mg",
        concentration="2 mg/mL",
        batch="P2024-03"
    )
    
    # Display sample
    tracker.display_sample("DNA-001")
    
    # Use sample
    tracker.use_sample(
        sample_id="DNA-001",
        amount_used=10,
        unit="µg",
        used_by="Dr. Smith",
        experiment_id="EXP_20241230_120000",
        notes="Used for transformation"
    )
    
    # Check updated sample
    tracker.display_sample("DNA-001")
    
    # List all samples
    all_samples = tracker.list_samples()
    print(f"\nTotal samples in inventory: {len(all_samples)}")
    
    print("\n✅ Sample Tracker example completed!")