"""
FModel JSON Parser for Psychonauts 2
Parses JSON exports from FModel and extracts collectible data
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Optional

class FModelJSONParser:
    """Parser for FModel JSON exports"""
    
    def __init__(self, fmodel_export_path: Path):
        self.export_path = fmodel_export_path
        self.collectibles = []
        
    def parse_all_json_files(self):
        """Scan and parse all JSON files exported by FModel"""
        print("=" * 80)
        print("PARSING FMODEL JSON EXPORTS")
        print("=" * 80)
        print(f"\nScanning: {self.export_path}")
        
        if not self.export_path.exists():
            print(f"[ERROR] Export path does not exist: {self.export_path}")
            print("\nPlease export files from FModel first:")
            print("1. Open FModel")
            print("2. Load Psychonauts2-WindowsNoEditor.pak")
            print("3. Navigate to collectibles")
            print("4. Right-click → Save Properties (.json)")
            print(f"5. Export to: {self.export_path}")
            return []
        
        # Find all JSON files
        json_files = list(self.export_path.rglob("*.json"))
        print(f"Found {len(json_files)} JSON files")
        
        if len(json_files) == 0:
            print("\n[WARNING] No JSON files found!")
            print("Make sure you exported files from FModel to this location.")
            return []
        
        # Parse each file
        for json_file in json_files:
            try:
                collectible = self.parse_json_file(json_file)
                if collectible:
                    self.collectibles.append(collectible)
            except Exception as e:
                print(f"[ERROR] Failed to parse {json_file.name}: {e}")
        
        print(f"\n[OK] Parsed {len(self.collectibles)} collectibles")
        
        # Group by type
        by_type = {}
        for item in self.collectibles:
            item_type = item.get('type', 'UNKNOWN')
            by_type.setdefault(item_type, []).append(item)
        
        print("\nBreakdown by type:")
        for item_type, items in sorted(by_type.items()):
            print(f"  {item_type}: {len(items)}")
        
        return self.collectibles
    
    def parse_json_file(self, json_path: Path) -> Optional[Dict]:
        """Parse a single FModel JSON export"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract basic info
        result = {
            'file_name': json_path.name.replace('.json', ''),
            'file_path': str(json_path.relative_to(self.export_path)),
            'class_name': None,
            'object_path': None,
            'display_name': None,
            'level': None,
            'type': self.guess_collectible_type(json_path.name),
            'properties': {}
        }
        
        # Try to extract data from FModel's JSON structure
        # FModel exports have different structures, try multiple patterns
        
        # Pattern 1: Direct properties
        if isinstance(data, list) and len(data) > 0:
            properties = data[0].get('Properties', {})
            result['properties'] = properties
            
            # Try to get class name
            if 'Class' in data[0]:
                result['class_name'] = data[0]['Class']
            
            # Try to get display name
            if 'DisplayName' in properties:
                result['display_name'] = properties['DisplayName']
        
        # Pattern 2: Root properties
        elif isinstance(data, dict):
            if 'Properties' in data:
                result['properties'] = data['Properties']
            
            if 'Type' in data:
                result['class_name'] = data['Type']
            
            if 'Name' in data:
                result['display_name'] = data['Name']
        
        # Extract object path from file path
        # FModel preserves the game's folder structure
        path_parts = json_path.parts
        if 'Psychonauts2' in path_parts or 'Game' in path_parts:
            # Reconstruct the /Game/ path
            try:
                start_idx = path_parts.index('Content') if 'Content' in path_parts else -1
                if start_idx > 0:
                    rel_parts = path_parts[start_idx+1:]
                    # Remove .json and reconstruct
                    object_parts = [p for p in rel_parts if p != json_path.name]
                    object_parts.append(json_path.stem)  # stem = filename without extension
                    result['object_path'] = '/Game/' + '/'.join(object_parts)
            except:
                pass
        
        # Extract level from path
        if 'Levels' in path_parts:
            level_idx = path_parts.index('Levels')
            if level_idx + 1 < len(path_parts):
                result['level'] = path_parts[level_idx + 1]
        
        # If no class name found, use filename
        if not result['class_name']:
            result['class_name'] = json_path.stem
        
        return result
    
    def guess_collectible_type(self, filename: str) -> str:
        """Guess collectible type from filename"""
        name_lower = filename.lower()
        
        if 'psicard' in name_lower or 'psycard' in name_lower:
            return 'PSI_CARD'
        elif 'figment' in name_lower:
            return 'FIGMENT'
        elif 'nugget' in name_lower:
            return 'NUGGET'
        elif 'baggage' in name_lower:
            return 'BAGGAGE'
        elif 'memory' in name_lower or 'vault' in name_lower:
            return 'MEMORY'
        elif 'half' in name_lower and 'mind' in name_lower:
            return 'HALF_A_MIND'
        else:
            return 'UNKNOWN'
    
    def export_to_csv(self, output_path: Path):
        """Export parsed collectibles to CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'file_name', 'type', 'class_name', 'object_path', 
                'display_name', 'level'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in self.collectibles:
                writer.writerow({
                    'file_name': item['file_name'],
                    'type': item['type'],
                    'class_name': item['class_name'],
                    'object_path': item['object_path'] or '',
                    'display_name': item['display_name'] or '',
                    'level': item['level'] or ''
                })
        
        print(f"\n[OK] Exported to CSV: {output_path}")
    
    def export_to_json(self, output_path: Path):
        """Export parsed collectibles to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.collectibles, f, indent=2)
        
        print(f"[OK] Exported to JSON: {output_path}")


def main():
    """Main execution"""
    # Path where FModel exports are saved
    fmodel_export_path = Path(r"C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\extracted_fmodel_data")
    
    if not fmodel_export_path.exists():
        print("=" * 80)
        print("FMODEL EXPORT FOLDER NOT FOUND")
        print("=" * 80)
        print(f"\nExpected location: {fmodel_export_path}")
        print("\nTo set up:")
        print("1. Run launch_fmodel.bat")
        print("2. Load Psychonauts2-WindowsNoEditor.pak")
        print("3. Export collectible files as JSON")
        print(f"4. Save to: {fmodel_export_path}")
        print("\nSee FMODEL_GUIDE.md for detailed instructions")
        return
    
    # Parse all JSON files
    parser = FModelJSONParser(fmodel_export_path)
    collectibles = parser.parse_all_json_files()
    
    if collectibles:
        # Export results
        output_csv = Path(r"C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\worlds\psychonauts2\fmodel_extracted_collectibles.csv")
        output_json = Path(r"C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\worlds\psychonauts2\fmodel_extracted_collectibles.json")
        
        parser.export_to_csv(output_csv)
        parser.export_to_json(output_json)
        
        print("\n" + "=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print("\n1. Review fmodel_extracted_collectibles.csv")
        print("2. Run extract_and_match.py to compare with existing CSVs")
        print("3. Update Item_List.csv and Check_List.csv with correct data")
    else:
        print("\n[INFO] No collectibles found. Export files from FModel first.")

if __name__ == "__main__":
    main()
