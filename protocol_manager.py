"""
Protocol Manager
================

Manage research protocols with version control, templates, and checklists.

Author: Oluwaseun O. Ajayi
Email: oluwaseun.ajayi@uga.edu
GitHub: @Oluwaseun-O-Ajayi
Institution: University of Georgia
"""

import json
import os
from datetime import datetime
from pathlib import Path
import hashlib


class ProtocolManager:
    """
    Manage research protocols with templates and version control.
    """
    
    def __init__(self, protocol_dir='protocols', template_dir='templates'):
        """
        Initialize Protocol Manager.
        
        Args:
            protocol_dir: Directory to store protocols
            template_dir: Directory containing protocol templates
        """
        self.protocol_dir = Path(protocol_dir)
        self.template_dir = Path(template_dir)
        
        # Create directories if they don't exist
        self.protocol_dir.mkdir(exist_ok=True)
        self.template_dir.mkdir(exist_ok=True)
        
        print(f"✅ Protocol Manager Initialized")
        print(f"   Protocols: {self.protocol_dir.absolute()}")
        print(f"   Templates: {self.template_dir.absolute()}")
    
    def create_protocol(self, name, description, steps, 
                       materials=None, notes=None, tags=None):
        """
        Create a new protocol.
        
        Args:
            name: Protocol name
            description: Brief description
            steps: List of protocol steps
            materials: List of required materials
            notes: Additional notes
            tags: List of tags for categorization
        
        Returns:
            Protocol ID (filename)
        """
        # Generate protocol ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        protocol_id = f"{name.lower().replace(' ', '_')}_{timestamp}"
        
        # Create protocol data
        protocol = {
            'id': protocol_id,
            'name': name,
            'description': description,
            'created': datetime.now().isoformat(),
            'version': 1,
            'steps': steps,
            'materials': materials or [],
            'notes': notes or '',
            'tags': tags or [],
            'checksum': ''
        }
        
        # Calculate checksum for version control
        protocol['checksum'] = self._calculate_checksum(protocol)
        
        # Save protocol
        filepath = self.protocol_dir / f"{protocol_id}.json"
        with open(filepath, 'w') as f:
            json.dump(protocol, f, indent=2)
        
        print(f"✅ Protocol created: {name}")
        print(f"   ID: {protocol_id}")
        print(f"   Steps: {len(steps)}")
        
        return protocol_id
    
    def load_protocol(self, protocol_id):
        """
        Load a protocol by ID.
        
        Args:
            protocol_id: Protocol ID or filename
        
        Returns:
            Protocol dictionary
        """
        # Handle both with and without .json extension
        if not protocol_id.endswith('.json'):
            protocol_id = f"{protocol_id}.json"
        
        filepath = self.protocol_dir / protocol_id
        
        if not filepath.exists():
            print(f"❌ Protocol not found: {protocol_id}")
            return None
        
        with open(filepath, 'r') as f:
            protocol = json.load(f)
        
        print(f"✅ Protocol loaded: {protocol['name']}")
        return protocol
    
    def update_protocol(self, protocol_id, **updates):
        """
        Update an existing protocol (creates new version).
        
        Args:
            protocol_id: Protocol ID
            **updates: Fields to update (steps, materials, notes, etc.)
        
        Returns:
            New protocol ID
        """
        # Load existing protocol
        protocol = self.load_protocol(protocol_id)
        if not protocol:
            return None
        
        # Update fields
        for key, value in updates.items():
            if key in protocol:
                protocol[key] = value
        
        # Increment version
        protocol['version'] += 1
        protocol['modified'] = datetime.now().isoformat()
        
        # Update checksum
        protocol['checksum'] = self._calculate_checksum(protocol)
        
        # Create new protocol ID with version
        base_name = protocol['name'].lower().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_id = f"{base_name}_v{protocol['version']}_{timestamp}"
        protocol['id'] = new_id
        
        # Save as new version
        filepath = self.protocol_dir / f"{new_id}.json"
        with open(filepath, 'w') as f:
            json.dump(protocol, f, indent=2)
        
        print(f"✅ Protocol updated: {protocol['name']}")
        print(f"   New version: {protocol['version']}")
        print(f"   New ID: {new_id}")
        
        return new_id
    
    def list_protocols(self, tag=None):
        """
        List all available protocols.
        
        Args:
            tag: Optional tag to filter by
        
        Returns:
            List of protocol summaries
        """
        protocols = []
        
        for filepath in self.protocol_dir.glob('*.json'):
            with open(filepath, 'r') as f:
                protocol = json.load(f)
            
            # Filter by tag if specified
            if tag and tag not in protocol.get('tags', []):
                continue
            
            summary = {
                'id': protocol['id'],
                'name': protocol['name'],
                'version': protocol.get('version', 1),
                'steps': len(protocol.get('steps', [])),
                'created': protocol.get('created', 'Unknown'),
                'tags': protocol.get('tags', [])
            }
            protocols.append(summary)
        
        # Sort by creation date (newest first)
        protocols.sort(key=lambda x: x['created'], reverse=True)
        
        return protocols
    
    def display_protocol(self, protocol_id):
        """
        Display protocol in readable format.
        
        Args:
            protocol_id: Protocol ID
        """
        protocol = self.load_protocol(protocol_id)
        if not protocol:
            return
        
        print(f"\n{'='*70}")
        print(f"PROTOCOL: {protocol['name']}")
        print(f"{'='*70}")
        print(f"Version: {protocol.get('version', 1)}")
        print(f"Created: {protocol.get('created', 'Unknown')}")
        print(f"Tags: {', '.join(protocol.get('tags', []))}")
        print(f"\nDescription:")
        print(f"  {protocol['description']}")
        
        # Materials
        if protocol.get('materials'):
            print(f"\nMaterials Required:")
            for i, material in enumerate(protocol['materials'], 1):
                print(f"  {i}. {material}")
        
        # Steps
        print(f"\nProtocol Steps:")
        for i, step in enumerate(protocol['steps'], 1):
            print(f"\n  Step {i}:")
            if isinstance(step, dict):
                print(f"    Action: {step.get('action', '')}")
                if step.get('duration'):
                    print(f"    Duration: {step['duration']}")
                if step.get('temperature'):
                    print(f"    Temperature: {step['temperature']}")
                if step.get('notes'):
                    print(f"    Notes: {step['notes']}")
            else:
                print(f"    {step}")
        
        # Notes
        if protocol.get('notes'):
            print(f"\nAdditional Notes:")
            print(f"  {protocol['notes']}")
        
        print(f"\n{'='*70}\n")
    
    def create_checklist(self, protocol_id, output_file=None):
        """
        Create a checklist from protocol for lab use.
        
        Args:
            protocol_id: Protocol ID
            output_file: Optional output file path
        
        Returns:
            Checklist string
        """
        protocol = self.load_protocol(protocol_id)
        if not protocol:
            return None
        
        checklist = []
        checklist.append(f"PROTOCOL CHECKLIST: {protocol['name']}")
        checklist.append(f"Date: _____________  Performed by: _____________")
        checklist.append(f"Version: {protocol.get('version', 1)}")
        checklist.append("=" * 70)
        
        # Materials checklist
        if protocol.get('materials'):
            checklist.append("\nMATERIALS CHECKLIST:")
            for material in protocol['materials']:
                checklist.append(f"[ ] {material}")
        
        # Steps checklist
        checklist.append("\nPROCEDURE CHECKLIST:")
        for i, step in enumerate(protocol['steps'], 1):
            if isinstance(step, dict):
                action = step.get('action', str(step))
            else:
                action = step
            checklist.append(f"[ ] Step {i}: {action}")
        
        checklist.append("\n" + "=" * 70)
        checklist.append("Notes:")
        checklist.append("_" * 70)
        checklist.append("_" * 70)
        
        checklist_str = "\n".join(checklist)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(checklist_str)
            print(f"✅ Checklist saved to: {output_file}")
        
        return checklist_str
    
    def load_template(self, template_name):
        """
        Load a protocol template.
        
        Args:
            template_name: Template filename
        
        Returns:
            Template dictionary
        """
        if not template_name.endswith('.json'):
            template_name = f"{template_name}.json"
        
        filepath = self.template_dir / template_name
        
        if not filepath.exists():
            print(f"❌ Template not found: {template_name}")
            return None
        
        with open(filepath, 'r') as f:
            template = json.load(f)
        
        print(f"✅ Template loaded: {template.get('name', template_name)}")
        return template
    
    def create_from_template(self, template_name, **customizations):
        """
        Create protocol from template with customizations.
        
        Args:
            template_name: Template filename
            **customizations: Fields to customize
        
        Returns:
            Protocol ID
        """
        template = self.load_template(template_name)
        if not template:
            return None
        
        # Apply customizations
        for key, value in customizations.items():
            if key in template:
                template[key] = value
        
        # Create protocol from template
        protocol_id = self.create_protocol(
            name=template.get('name'),
            description=template.get('description'),
            steps=template.get('steps'),
            materials=template.get('materials'),
            notes=template.get('notes'),
            tags=template.get('tags')
        )
        
        return protocol_id
    
    def _calculate_checksum(self, protocol):
        """Calculate MD5 checksum for version control."""
        # Create string from critical fields
        data = json.dumps({
            'name': protocol['name'],
            'steps': protocol['steps'],
            'materials': protocol.get('materials', [])
        }, sort_keys=True)
        
        return hashlib.md5(data.encode()).hexdigest()
    
    def search_protocols(self, keyword):
        """
        Search protocols by keyword.
        
        Args:
            keyword: Search term
        
        Returns:
            List of matching protocols
        """
        keyword = keyword.lower()
        matches = []
        
        for filepath in self.protocol_dir.glob('*.json'):
            with open(filepath, 'r') as f:
                protocol = json.load(f)
            
            # Search in name, description, and tags
            searchable = (
                protocol['name'].lower() + ' ' +
                protocol['description'].lower() + ' ' +
                ' '.join(protocol.get('tags', []))
            )
            
            if keyword in searchable:
                matches.append({
                    'id': protocol['id'],
                    'name': protocol['name'],
                    'description': protocol['description']
                })
        
        print(f"✅ Found {len(matches)} matching protocols")
        return matches


# Example usage
if __name__ == "__main__":
    print("\n" + "="*70)
    print("PROTOCOL MANAGER - Example Usage")
    print("="*70 + "\n")
    
    # Initialize manager
    manager = ProtocolManager()
    
    # Create a sample protocol
    protocol_id = manager.create_protocol(
        name="DNA Extraction",
        description="Standard protocol for genomic DNA extraction from tissue samples",
        steps=[
            {"action": "Add lysis buffer to sample", "duration": "5 min"},
            {"action": "Incubate", "temperature": "55°C", "duration": "30 min"},
            {"action": "Add proteinase K", "duration": "10 min"},
            {"action": "Centrifuge", "duration": "10 min", "notes": "13,000 rpm"},
            {"action": "Transfer supernatant to new tube"},
            {"action": "Add isopropanol for precipitation"},
            {"action": "Centrifuge and wash pellet"},
            {"action": "Resuspend in TE buffer"}
        ],
        materials=[
            "Lysis buffer",
            "Proteinase K",
            "Isopropanol",
            "70% Ethanol",
            "TE Buffer",
            "1.5 mL tubes"
        ],
        tags=["DNA", "Extraction", "Molecular Biology"],
        notes="Store DNA at -20°C after extraction"
    )
    
    # Display protocol
    manager.display_protocol(protocol_id)
    
    # Create checklist
    checklist = manager.create_checklist(protocol_id)
    print(checklist)
    
    print("\n✅ Protocol Manager example completed!")