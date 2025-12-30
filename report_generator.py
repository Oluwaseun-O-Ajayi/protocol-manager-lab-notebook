"""
Report Generator
================

Generate professional lab reports from experiments and protocols.

Author: Oluwaseun O. Ajayi
Email: oluwaseun.ajayi@uga.edu
GitHub: @Oluwaseun-O-Ajayi
Institution: University of Georgia
"""

from datetime import datetime
from pathlib import Path
import json


class ReportGenerator:
    """
    Generate professional reports from lab data.
    """
    
    def __init__(self, report_dir='reports'):
        """
        Initialize Report Generator.
        
        Args:
            report_dir: Directory to store reports
        """
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)
        
        print(f"✅ Report Generator Initialized")
        print(f"   Reports: {self.report_dir.absolute()}")
    
    def generate_experiment_report(self, experiment, output_file=None):
        """
        Generate detailed experiment report.
        
        Args:
            experiment: Experiment dictionary
            output_file: Optional output filename
        
        Returns:
            Report text
        """
        report = []
        report.append("=" * 80)
        report.append("EXPERIMENT REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Header
        report.append(f"Title: {experiment['title']}")
        report.append(f"Experiment ID: {experiment['id']}")
        report.append(f"Date: {experiment['created']}")
        report.append(f"Status: {experiment['status']}")
        if experiment.get('protocol_id'):
            report.append(f"Protocol: {experiment['protocol_id']}")
        report.append("")
        
        # Objective
        if experiment.get('objective'):
            report.append("OBJECTIVE")
            report.append("-" * 80)
            report.append(experiment['objective'])
            report.append("")
        
        # Hypothesis
        if experiment.get('hypothesis'):
            report.append("HYPOTHESIS")
            report.append("-" * 80)
            report.append(experiment['hypothesis'])
            report.append("")
        
        # Materials
        if experiment.get('materials'):
            report.append("MATERIALS")
            report.append("-" * 80)
            for material in experiment['materials']:
                report.append(f"  • {material}")
            report.append("")
        
        # Methods
        if experiment.get('protocol_id'):
            report.append("METHODS")
            report.append("-" * 80)
            report.append(f"Protocol: {experiment['protocol_id']}")
            report.append("See protocol document for detailed procedures.")
            report.append("")
        
        # Observations
        if experiment.get('observations'):
            report.append("OBSERVATIONS")
            report.append("-" * 80)
            for i, obs in enumerate(experiment['observations'], 1):
                report.append(f"{i}. [{obs['timestamp']}]")
                report.append(f"   {obs['observation']}")
                report.append("")
        
        # Results
        if experiment.get('results'):
            report.append("RESULTS")
            report.append("-" * 80)
            for key, value in experiment['results'].items():
                report.append(f"  {key}: {value}")
            report.append("")
        
        # Conclusions
        if experiment.get('conclusions'):
            report.append("CONCLUSIONS")
            report.append("-" * 80)
            report.append(experiment['conclusions'])
            report.append("")
        
        # Attachments
        if experiment.get('attachments'):
            report.append("ATTACHMENTS")
            report.append("-" * 80)
            for att in experiment['attachments']:
                report.append(f"  • {att['type']}: {att['file']}")
            report.append("")
        
        # Footer
        report.append("=" * 80)
        report.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        # Save to file
        if not output_file:
            output_file = f"{experiment['id']}_report.txt"
        
        output_path = self.report_dir / output_file
        with open(output_path, 'w') as f:
            f.write(report_text)
        
        print(f"✅ Experiment report generated: {output_file}")
        return report_text
    
    def generate_protocol_summary(self, protocol, output_file=None):
        """
        Generate protocol summary report.
        
        Args:
            protocol: Protocol dictionary
            output_file: Optional output filename
        
        Returns:
            Report text
        """
        report = []
        report.append("=" * 80)
        report.append("PROTOCOL SUMMARY")
        report.append("=" * 80)
        report.append("")
        
        # Header
        report.append(f"Protocol: {protocol['name']}")
        report.append(f"ID: {protocol['id']}")
        report.append(f"Version: {protocol.get('version', 1)}")
        report.append(f"Created: {protocol['created']}")
        if protocol.get('tags'):
            report.append(f"Tags: {', '.join(protocol['tags'])}")
        report.append("")
        
        # Description
        report.append("DESCRIPTION")
        report.append("-" * 80)
        report.append(protocol['description'])
        report.append("")
        
        # Materials
        if protocol.get('materials'):
            report.append("REQUIRED MATERIALS")
            report.append("-" * 80)
            for i, material in enumerate(protocol['materials'], 1):
                report.append(f"{i}. {material}")
            report.append("")
        
        # Procedure
        report.append("PROCEDURE")
        report.append("-" * 80)
        for i, step in enumerate(protocol['steps'], 1):
            report.append(f"Step {i}:")
            if isinstance(step, dict):
                report.append(f"  Action: {step.get('action', '')}")
                if step.get('duration'):
                    report.append(f"  Duration: {step['duration']}")
                if step.get('temperature'):
                    report.append(f"  Temperature: {step['temperature']}")
                if step.get('notes'):
                    report.append(f"  Notes: {step['notes']}")
            else:
                report.append(f"  {step}")
            report.append("")
        
        # Notes
        if protocol.get('notes'):
            report.append("ADDITIONAL NOTES")
            report.append("-" * 80)
            report.append(protocol['notes'])
            report.append("")
        
        # Footer
        report.append("=" * 80)
        report.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        # Save to file
        if not output_file:
            output_file = f"{protocol['id']}_summary.txt"
        
        output_path = self.report_dir / output_file
        with open(output_path, 'w') as f:
            f.write(report_text)
        
        print(f"✅ Protocol summary generated: {output_file}")
        return report_text
    
    def generate_inventory_report(self, samples, output_file='inventory_report.txt'):
        """
        Generate inventory status report.
        
        Args:
            samples: List of sample dictionaries
            output_file: Output filename
        
        Returns:
            Report text
        """
        report = []
        report.append("=" * 80)
        report.append("INVENTORY REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Samples: {len(samples)}")
        report.append("")
        
        # Group by type
        by_type = {}
        for sample in samples:
            sample_type = sample['type']
            if sample_type not in by_type:
                by_type[sample_type] = []
            by_type[sample_type].append(sample)
        
        # Summary by type
        report.append("SUMMARY BY TYPE")
        report.append("-" * 80)
        for sample_type, type_samples in by_type.items():
            available = len([s for s in type_samples if s['status'] == 'Available'])
            depleted = len([s for s in type_samples if s['status'] == 'Depleted'])
            report.append(f"{sample_type}:")
            report.append(f"  Total: {len(type_samples)}")
            report.append(f"  Available: {available}")
            report.append(f"  Depleted: {depleted}")
        report.append("")
        
        # Detailed listing
        report.append("DETAILED INVENTORY")
        report.append("-" * 80)
        report.append("")
        
        for sample_type, type_samples in sorted(by_type.items()):
            report.append(f"{sample_type.upper()}")
            report.append("-" * 40)
            
            for sample in type_samples:
                report.append(f"ID: {sample['sample_id']}")
                report.append(f"  Description: {sample['description']}")
                report.append(f"  Status: {sample['status']}")
                report.append(f"  Quantity: {sample['quantity']} {sample['unit']}")
                report.append(f"  Location: {sample['location']}")
                if sample.get('concentration'):
                    report.append(f"  Concentration: {sample['concentration']}")
                report.append("")
        
        # Low stock alerts
        low_stock = [s for s in samples if s['quantity'] <= 10 and s['status'] == 'Available']
        if low_stock:
            report.append("LOW STOCK ALERTS")
            report.append("-" * 80)
            for sample in low_stock:
                report.append(f"⚠️  {sample['sample_id']}: {sample['quantity']} {sample['unit']}")
            report.append("")
        
        # Footer
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        # Save to file
        output_path = self.report_dir / output_file
        with open(output_path, 'w') as f:
            f.write(report_text)
        
        print(f"✅ Inventory report generated: {output_file}")
        return report_text
    
    def generate_weekly_summary(self, experiments, start_date, end_date, 
                               output_file='weekly_summary.txt'):
        """
        Generate weekly activity summary.
        
        Args:
            experiments: List of experiment dictionaries
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            output_file: Output filename
        
        Returns:
            Report text
        """
        report = []
        report.append("=" * 80)
        report.append("WEEKLY ACTIVITY SUMMARY")
        report.append("=" * 80)
        report.append("")
        report.append(f"Period: {start_date} to {end_date}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Filter experiments by date range
        week_experiments = [
            exp for exp in experiments
            if start_date <= exp['created'] <= end_date
        ]
        
        # Statistics
        total = len(week_experiments)
        completed = len([e for e in week_experiments if e['status'] == 'Completed'])
        in_progress = len([e for e in week_experiments if e['status'] == 'In Progress'])
        
        report.append("STATISTICS")
        report.append("-" * 80)
        report.append(f"Total Experiments: {total}")
        report.append(f"Completed: {completed}")
        report.append(f"In Progress: {in_progress}")
        report.append("")
        
        # List experiments
        if week_experiments:
            report.append("EXPERIMENTS")
            report.append("-" * 80)
            
            for exp in week_experiments:
                report.append(f"\n{exp['title']}")
                report.append(f"  ID: {exp['id']}")
                report.append(f"  Status: {exp['status']}")
                report.append(f"  Date: {exp['created']}")
                if exp.get('tags'):
                    report.append(f"  Tags: {', '.join(exp['tags'])}")
        else:
            report.append("No experiments in this period.")
        
        report.append("")
        report.append("=" * 80)
        report.append("END OF SUMMARY")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        # Save to file
        output_path = self.report_dir / output_file
        with open(output_path, 'w') as f:
            f.write(report_text)
        
        print(f"✅ Weekly summary generated: {output_file}")
        return report_text


# Example usage
if __name__ == "__main__":
    print("\n" + "="*70)
    print("REPORT GENERATOR - Example Usage")
    print("="*70 + "\n")
    
    # Initialize generator
    generator = ReportGenerator()
    
    # Example experiment
    experiment = {
        'id': 'EXP_20241230_120000',
        'title': 'Protein Expression Optimization',
        'created': '2024-12-30T12:00:00',
        'status': 'Completed',
        'protocol_id': 'protein_expression_20241230_120000',
        'objective': 'Optimize IPTG concentration for protein expression',
        'hypothesis': 'Higher IPTG concentration will increase protein yield',
        'materials': ['E. coli BL21', 'IPTG', 'LB media'],
        'observations': [
            {
                'timestamp': '2024-12-30T12:00:00',
                'observation': 'Induced cultures with different IPTG concentrations'
            }
        ],
        'results': {
            '0.5mM_IPTG': '45 mg/L',
            'optimal_concentration': '0.5mM'
        },
        'conclusions': 'Optimal expression at 0.5mM IPTG',
        'attachments': []
    }
    
    # Generate experiment report
    report = generator.generate_experiment_report(experiment)
    print("\n" + report)
    
    print("\n✅ Report Generator example completed!")