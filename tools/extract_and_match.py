"""
Psychonauts 2 Data Extraction and Matching Tool
This script processes UE4SS extracted data and matches it with existing AP world data
"""

import csv
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class PN2DataMatcher:
    def __init__(self, extracted_data_path: str, world_data_path: str):
        self.extracted_path = Path(extracted_data_path)
        self.world_path = Path(world_data_path)
        self.existing_items = {}
        self.existing_locations = {}
        self.extracted_items = []
        self.extracted_locations = []
        
    def load_existing_items(self):
        """Load existing items from CSV"""
        items_csv = self.world_path / "Psychonauts_2_Item_List.csv"
        if items_csv.exists():
            with open(items_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.existing_items[row['Item']] = row
        print(f"Loaded {len(self.existing_items)} existing items")
    
    def load_existing_locations(self):
        """Load existing locations/checks from CSV"""
        checks_csv = self.world_path / "Psychonauts_2_Check_List.csv"
        if checks_csv.exists():
            with open(checks_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.existing_locations[row['Check']] = row
        print(f"Loaded {len(self.existing_locations)} existing checks")
    
    def parse_extracted_collectibles(self):
        """Parse extracted collectible data from UE4SS dumps"""
        # Check for global_extraction.txt first (from CTRL+F3)
        global_extraction = self.extracted_path / "global_extraction.txt"
        if global_extraction.exists():
            print(f"\nProcessing global_extraction.txt...")
            self.parse_global_extraction(global_extraction)
            return
        
        # Fall back to individual collectible files
        collectible_files = list(self.extracted_path.glob("collectible_*.txt"))
        
        for file_path in collectible_files:
            print(f"\nProcessing {file_path.name}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract class name from file
                class_match = re.search(r'Class: (\w+)', content)
                if not class_match:
                    continue
                
                class_name = class_match.group(1)
                
                # Find all instances
                instances = re.findall(r'\[(\d+)\] (.+?)\n', content)
                
                for index, full_name in instances:
                    # Parse the full name to extract useful info
                    # Format is typically: Class /Path/To/Object.Object:PersistentLevel.ActorName
                    parts = full_name.split('.')
                    if len(parts) >= 2:
                        actor_name = parts[-1].split('_')[0] if '_' in parts[-1] else parts[-1]
                        
                        # Try to extract location from path
                        location_match = re.search(r'/Game/(?:Levels?|Maps?)/([^/]+)', full_name)
                        location = location_match.group(1) if location_match else "Unknown"
                        
                        self.extracted_items.append({
                            'class': class_name,
                            'full_name': full_name,
                            'actor_name': actor_name,
                            'location': location,
                            'index': index
                        })
        
        print(f"\nExtracted {len(self.extracted_items)} items from game data")
    
    def parse_global_extraction(self, file_path):
        """Parse the global_extraction.txt file from CTRL+F3"""
        print("Parsing global extraction data...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse detailed listings section
        sections = re.split(r'=== (.+?) ===', content)
        
        for i in range(1, len(sections), 2):
            if i + 1 >= len(sections):
                break
            
            level_name = sections[i].strip()
            level_content = sections[i + 1]
            
            # Extract items from this level
            lines = level_content.split('\n')
            current_category = None
            
            for line in lines:
                if line.strip() in ['PSI CARDS:', 'FIGMENTS:', 'NUGGETS:', 'BAGGAGE:', 'MEMORIES:', 'HALF-A-MINDS:']:
                    current_category = line.strip().rstrip(':')
                elif line.strip().startswith('['):
                    # Parse item line: [1] BlueprintGeneratedClass /Game/Levels/...
                    match = re.match(r'\[(\d+)\]\s+(.+)', line.strip())
                    if match and current_category:
                        index = match.group(1)
                        full_name = match.group(2)
                        
                        parts = full_name.split('.')
                        actor_name = parts[-1].split('_')[0] if len(parts) >= 2 and '_' in parts[-1] else parts[-1] if parts else "Unknown"
                        
                        self.extracted_items.append({
                            'class': current_category,
                            'full_name': full_name,
                            'actor_name': actor_name,
                            'location': level_name,
                            'index': index
                        })
        
        print(f"Extracted {len(self.extracted_items)} items from global extraction")
    
    def parse_all_classes(self):
        """Parse the all_classes.txt file to understand game structure"""
        classes_file = self.extracted_path / "all_classes_detailed.txt"
        if not classes_file.exists():
            classes_file = self.extracted_path / "all_classes.txt"
        
        if not classes_file.exists():
            print("all_classes.txt not found")
            return
        
        relevant_classes = []
        with open(classes_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Look for collectible-related classes
                if any(keyword in line.lower() for keyword in 
                      ['pickup', 'collectible', 'card', 'figment', 'nugget', 
                       'baggage', 'memory', 'vault']):
                    relevant_classes.append(line.strip())
        
        print(f"\nFound {len(relevant_classes)} potentially relevant classes:")
        for cls in relevant_classes[:20]:  # Show first 20
            print(f"  {cls}")
    
    def match_items(self) -> Dict[str, List]:
        """Match extracted items with existing CSV entries"""
        matches = {
            'exact': [],
            'partial': [],
            'missing_in_csv': [],
            'missing_in_game': []
        }
        
        # Find items in game but not in CSV
        for extracted in self.extracted_items:
            found = False
            actor_name = extracted['actor_name'].lower()
            
            for csv_item_id, csv_item in self.existing_items.items():
                csv_name = csv_item_id.lower()
                
                if actor_name in csv_name or csv_name in actor_name:
                    matches['partial'].append({
                        'csv': csv_item_id,
                        'game': extracted['full_name'],
                        'location': extracted['location']
                    })
                    found = True
                    break
            
            if not found:
                matches['missing_in_csv'].append(extracted)
        
        # Find items in CSV but not found in game data
        extracted_names = {item['actor_name'].lower() for item in self.extracted_items}
        for csv_item_id in self.existing_items.keys():
            csv_name = csv_item_id.lower()
            if not any(name in csv_name or csv_name in name for name in extracted_names):
                matches['missing_in_game'].append(csv_item_id)
        
        return matches
    
    def generate_report(self, output_file: str = "match_report.txt"):
        """Generate a comprehensive matching report"""
        matches = self.match_items()
        
        report_path = self.world_path.parent / output_file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("Psychonauts 2 Data Matching Report\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Existing CSV Items: {len(self.existing_items)}\n")
            f.write(f"Existing CSV Checks: {len(self.existing_locations)}\n")
            f.write(f"Extracted Game Items: {len(self.extracted_items)}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("PARTIAL MATCHES (need verification)\n")
            f.write("-" * 80 + "\n")
            for match in matches['partial'][:50]:  # Show first 50
                f.write(f"CSV: {match['csv']}\n")
                f.write(f"Game: {match['game']}\n")
                f.write(f"Location: {match['location']}\n\n")
            
            f.write("\n" + "-" * 80 + "\n")
            f.write("ITEMS IN GAME BUT NOT IN CSV (may need to be added)\n")
            f.write("-" * 80 + "\n")
            for item in matches['missing_in_csv'][:50]:
                f.write(f"Class: {item['class']}\n")
                f.write(f"Name: {item['actor_name']}\n")
                f.write(f"Full: {item['full_name']}\n")
                f.write(f"Location: {item['location']}\n\n")
            
            f.write("\n" + "-" * 80 + "\n")
            f.write("ITEMS IN CSV BUT NOT FOUND IN GAME DATA (may need different search)\n")
            f.write("-" * 80 + "\n")
            for item in matches['missing_in_game'][:50]:
                f.write(f"{item}\n")
        
        print(f"\nReport saved to: {report_path}")
        return matches
    
    def export_game_data_to_csv(self):
        """Export extracted game data to CSV format for easy comparison"""
        output_file = self.world_path.parent / "extracted_game_items.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Index', 'Class', 'ActorName', 'Location', 'FullName']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, item in enumerate(self.extracted_items):
                writer.writerow({
                    'Index': i,
                    'Class': item['class'],
                    'ActorName': item['actor_name'],
                    'Location': item['location'],
                    'FullName': item['full_name']
                })
        
        print(f"Exported game data to: {output_file}")

def main():
    """Main execution function"""
    extracted_data = r"C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\extracted_data"
    world_data = r"C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\worlds\psychonauts2\data"
    
    matcher = PN2DataMatcher(extracted_data, world_data)
    
    print("Loading existing CSV data...")
    matcher.load_existing_items()
    matcher.load_existing_locations()
    
    print("\nParsing extracted game data...")
    matcher.parse_extracted_collectibles()
    matcher.parse_all_classes()
    
    print("\nGenerating matching report...")
    matches = matcher.generate_report()
    
    print("\nExporting game data to CSV...")
    matcher.export_game_data_to_csv()
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Partial matches found: {len(matches['partial'])}")
    print(f"Items in game but not in CSV: {len(matches['missing_in_csv'])}")
    print(f"Items in CSV but not found in game: {len(matches['missing_in_game'])}")
    print("\nNext steps:")
    print("1. Launch Psychonauts 2 and load a save")
    print("2. Press CTRL+F3 in-game for global extraction (includes Grulovia!)")
    print("3. Run this script again to generate matching report")
    print("4. Review match_report.txt to verify matches")

if __name__ == "__main__":
    main()
