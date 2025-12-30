"""
Digital Lab Notebook
====================

Log and track experiments with timestamps, results, and analysis.

Author: Oluwaseun O. Ajayi
Email: oluwaseun.ajayi@uga.edu
GitHub: @Oluwaseun-O-Ajayi
Institution: University of Georgia
"""

import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


class LabNotebook:
    """
    Digital lab notebook for experiment logging and tracking.
    """
    
    def __init__(self, notebook_dir='experiments', data_dir='data'):
        """
        Initialize Lab Notebook.
        
        Args:
            notebook_dir: Directory to store experiment logs
            data_dir: Directory to store associated data files
        """
        self.notebook_dir = Path(notebook_dir)
        self.data_dir = Path(data_dir)
        
        # Create directories
        self.notebook_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        print(f"✅ Lab Notebook Initialized")
        print(f"   Experiments: {self.notebook_dir.absolute()}")
        print(f"   Data: {self.data_dir.absolute()}")
    
    def create_experiment(self, title, protocol_id=None, objective=None,
                         hypothesis=None, materials=None, tags=None):
        """
        Create a new experiment entry.
        
        Args:
            title: Experiment title
            protocol_id: Associated protocol ID
            objective: Experiment objective
            hypothesis: Hypothesis being tested
            materials: Materials used
            tags: Tags for categorization
        
        Returns:
            Experiment ID
        """
        # Generate experiment ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exp_id = f"EXP_{timestamp}"
        
        # Create experiment record
        experiment = {
            'id': exp_id,
            'title': title,
            'protocol_id': protocol_id,
            'objective': objective or '',
            'hypothesis': hypothesis or '',
            'materials': materials or [],
            'tags': tags or [],
            'created': datetime.now().isoformat(),
            'status': 'In Progress',
            'observations': [],
            'results': {},
            'conclusions': '',
            'attachments': []
        }
        
        # Save experiment
        filepath = self.notebook_dir / f"{exp_id}.json"
        with open(filepath, 'w') as f:
            json.dump(experiment, f, indent=2)
        
        print(f"✅ Experiment created: {title}")
        print(f"   ID: {exp_id}")
        print(f"   Status: {experiment['status']}")
        
        return exp_id
    
    def load_experiment(self, exp_id):
        """
        Load an experiment by ID.
        
        Args:
            exp_id: Experiment ID
        
        Returns:
            Experiment dictionary
        """
        if not exp_id.endswith('.json'):
            exp_id = f"{exp_id}.json"
        
        filepath = self.notebook_dir / exp_id
        
        if not filepath.exists():
            print(f"❌ Experiment not found: {exp_id}")
            return None
        
        with open(filepath, 'r') as f:
            experiment = json.load(f)
        
        print(f"✅ Experiment loaded: {experiment['title']}")
        return experiment
    
    def add_observation(self, exp_id, observation, timestamp=None):
        """
        Add timestamped observation to experiment.
        
        Args:
            exp_id: Experiment ID
            observation: Observation text
            timestamp: Optional custom timestamp
        """
        experiment = self.load_experiment(exp_id)
        if not experiment:
            return
        
        # Create observation entry
        obs_entry = {
            'timestamp': timestamp or datetime.now().isoformat(),
            'observation': observation
        }
        
        experiment['observations'].append(obs_entry)
        
        # Save updated experiment
        filepath = self.notebook_dir / f"{experiment['id']}.json"
        with open(filepath, 'w') as f:
            json.dump(experiment, f, indent=2)
        
        print(f"✅ Observation added to {experiment['title']}")
    
    def add_results(self, exp_id, results_data, data_file=None):
        """
        Add results to experiment.
        
        Args:
            exp_id: Experiment ID
            results_data: Dictionary of results
            data_file: Optional path to associated data file
        """
        experiment = self.load_experiment(exp_id)
        if not experiment:
            return
        
        # Update results
        experiment['results'].update(results_data)
        
        # Add data file reference if provided
        if data_file:
            experiment['attachments'].append({
                'type': 'data',
                'file': str(data_file),
                'added': datetime.now().isoformat()
            })
        
        # Save updated experiment
        filepath = self.notebook_dir / f"{experiment['id']}.json"
        with open(filepath, 'w') as f:
            json.dump(experiment, f, indent=2)
        
        print(f"✅ Results added to {experiment['title']}")
    
    def complete_experiment(self, exp_id, conclusions):
        """
        Mark experiment as complete with conclusions.
        
        Args:
            exp_id: Experiment ID
            conclusions: Experiment conclusions
        """
        experiment = self.load_experiment(exp_id)
        if not experiment:
            return
        
        experiment['status'] = 'Completed'
        experiment['conclusions'] = conclusions
        experiment['completed'] = datetime.now().isoformat()
        
        # Save updated experiment
        filepath = self.notebook_dir / f"{experiment['id']}.json"
        with open(filepath, 'w') as f:
            json.dump(experiment, f, indent=2)
        
        print(f"✅ Experiment completed: {experiment['title']}")
    
    def display_experiment(self, exp_id):
        """
        Display experiment in readable format.
        
        Args:
            exp_id: Experiment ID
        """
        experiment = self.load_experiment(exp_id)
        if not experiment:
            return
        
        print(f"\n{'='*70}")
        print(f"EXPERIMENT: {experiment['title']}")
        print(f"{'='*70}")
        print(f"ID: {experiment['id']}")
        print(f"Status: {experiment['status']}")
        print(f"Created: {experiment['created']}")
        if experiment.get('completed'):
            print(f"Completed: {experiment['completed']}")
        print(f"Tags: {', '.join(experiment.get('tags', []))}")
        
        if experiment.get('protocol_id'):
            print(f"\nProtocol: {experiment['protocol_id']}")
        
        if experiment.get('objective'):
            print(f"\nObjective:")
            print(f"  {experiment['objective']}")
        
        if experiment.get('hypothesis'):
            print(f"\nHypothesis:")
            print(f"  {experiment['hypothesis']}")
        
        # Materials
        if experiment.get('materials'):
            print(f"\nMaterials:")
            for material in experiment['materials']:
                print(f"  - {material}")
        
        # Observations
        if experiment.get('observations'):
            print(f"\nObservations:")
            for i, obs in enumerate(experiment['observations'], 1):
                print(f"  [{obs['timestamp']}]")
                print(f"  {obs['observation']}\n")
        
        # Results
        if experiment.get('results'):
            print(f"\nResults:")
            for key, value in experiment['results'].items():
                print(f"  {key}: {value}")
        
        # Conclusions
        if experiment.get('conclusions'):
            print(f"\nConclusions:")
            print(f"  {experiment['conclusions']}")
        
        # Attachments
        if experiment.get('attachments'):
            print(f"\nAttachments:")
            for att in experiment['attachments']:
                print(f"  - {att['type']}: {att['file']}")
        
        print(f"\n{'='*70}\n")
    
    def list_experiments(self, status=None, tag=None):
        """
        List all experiments.
        
        Args:
            status: Filter by status ('In Progress', 'Completed')
            tag: Filter by tag
        
        Returns:
            List of experiment summaries
        """
        experiments = []
        
        for filepath in self.notebook_dir.glob('EXP_*.json'):
            with open(filepath, 'r') as f:
                exp = json.load(f)
            
            # Apply filters
            if status and exp.get('status') != status:
                continue
            if tag and tag not in exp.get('tags', []):
                continue
            
            summary = {
                'id': exp['id'],
                'title': exp['title'],
                'status': exp['status'],
                'created': exp['created'],
                'tags': exp.get('tags', [])
            }
            experiments.append(summary)
        
        # Sort by creation date
        experiments.sort(key=lambda x: x['created'], reverse=True)
        
        return experiments
    
    def export_to_csv(self, output_file='experiments_summary.csv'):
        """
        Export all experiments to CSV.
        
        Args:
            output_file: Output CSV filename
        """
        experiments = self.list_experiments()
        
        if not experiments:
            print("❌ No experiments to export")
            return
        
        df = pd.DataFrame(experiments)
        df.to_csv(output_file, index=False)
        
        print(f"✅ Exported {len(experiments)} experiments to {output_file}")
    
    def plot_experiment_timeline(self, save_path=None):
        """
        Visualize experiment timeline.
        
        Args:
            save_path: Optional path to save figure
        """
        experiments = self.list_experiments()
        
        if not experiments:
            print("❌ No experiments to plot")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(experiments)
        df['created'] = pd.to_datetime(df['created'])
        df['month'] = df['created'].dt.to_period('M')
        
        # Count experiments per month
        monthly_counts = df.groupby('month').size()
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        monthly_counts.plot(kind='bar', ax=ax, color='steelblue', 
                           edgecolor='black', linewidth=1)
        
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Experiments', fontsize=12, fontweight='bold')
        ax.set_title('Experiment Activity Timeline', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Timeline saved to: {save_path}")
        
        plt.show()
    
    def search_experiments(self, keyword):
        """
        Search experiments by keyword.
        
        Args:
            keyword: Search term
        
        Returns:
            List of matching experiments
        """
        keyword = keyword.lower()
        matches = []
        
        for filepath in self.notebook_dir.glob('EXP_*.json'):
            with open(filepath, 'r') as f:
                exp = json.load(f)
            
            # Search in title, objective, and tags
            searchable = (
                exp['title'].lower() + ' ' +
                exp.get('objective', '').lower() + ' ' +
                ' '.join(exp.get('tags', []))
            )
            
            if keyword in searchable:
                matches.append({
                    'id': exp['id'],
                    'title': exp['title'],
                    'status': exp['status']
                })
        
        print(f"✅ Found {len(matches)} matching experiments")
        return matches


# Example usage
if __name__ == "__main__":
    print("\n" + "="*70)
    print("LAB NOTEBOOK - Example Usage")
    print("="*70 + "\n")
    
    # Initialize notebook
    notebook = LabNotebook()
    
    # Create experiment
    exp_id = notebook.create_experiment(
        title="Protein Expression Optimization",
        objective="Optimize IPTG concentration for protein expression",
        hypothesis="Higher IPTG concentration will increase protein yield",
        materials=[
            "E. coli BL21 cells",
            "IPTG",
            "LB media",
            "Antibiotics"
        ],
        tags=["Protein Expression", "Optimization"]
    )
    
    # Add observations
    notebook.add_observation(exp_id, 
        "Induced cultures with 0.1mM, 0.5mM, and 1.0mM IPTG")
    notebook.add_observation(exp_id, 
        "Incubated at 37°C for 4 hours")
    notebook.add_observation(exp_id, 
        "Harvested cells and prepared lysates")
    
    # Add results
    results = {
        '0.1mM_IPTG': '15 mg/L',
        '0.5mM_IPTG': '45 mg/L',
        '1.0mM_IPTG': '38 mg/L',
        'optimal_concentration': '0.5mM'
    }
    notebook.add_results(exp_id, results)
    
    # Complete experiment
    notebook.complete_experiment(exp_id,
        "Optimal protein expression achieved at 0.5mM IPTG. "
        "Higher concentrations did not improve yield and may stress cells.")
    
    # Display experiment
    notebook.display_experiment(exp_id)
    
    print("\n✅ Lab Notebook example completed!")