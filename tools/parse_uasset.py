"""
Psychonauts 2 .uasset File Parser
Extracts class names and object paths from Unreal Engine asset files
"""

import struct
import json
from pathlib import Path
from typing import List, Dict, Optional

class UAssetParser:
    """Simple parser for UE4 .uasset files to extract basic metadata"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = None
        
    def parse(self) -> Optional[Dict]:
        """Parse .uasset file and extract metadata
        
        Returns:
            Dictionary with class name, object path, and other metadata
        """
        try:
            with open(self.file_path, 'rb') as f:
                self.data = f.read()
            
            # Look for common UE4 patterns
            info = {
                'file_name': self.file_path.name,
                'file_path': str(self.file_path),
                'class_name': self.extract_class_name(),
                'object_path': self.extract_object_path(),
                'level': self.extract_level_name(),
                'type': self.guess_collectible_type()
            }
            
            return info if info['class_name'] or info['object_path'] else None
            
        except Exception as e:
            print(f"Error parsing {self.file_path.name}: {e}")
            return None
    
    def extract_class_name(self) -> Optional[str]:
        """Try to extract the class name from the asset"""
        # Common class name patterns in UE4 assets
        patterns = [
            b'BlueprintGeneratedClass',
            b'Class /Script/',
            b'/Script/Engine.BlueprintGeneratedClass'
        ]
        
        for pattern in patterns:
            idx = self.data.find(pattern)
            if idx != -1:
                # Try to read string after pattern
                try:
                    # Look ahead for a string
                    search_area = self.data[idx:idx+200]
                    # Find null-terminated strings
                    strings = search_area.split(b'\x00')
                    for s in strings:
                        decoded = s.decode('utf-8', errors='ignore').strip()
                        if decoded and 'BP_' in decoded:
                            return decoded
                except:
                    continue
        
        # Fallback: search for BP_ prefixed names
        if b'BP_' in self.data:
            idx = self.data.find(b'BP_')
            if idx != -1:
                try:
                    # Extract string around BP_
                    search_area = self.data[max(0, idx-10):idx+100]
                    strings = search_area.split(b'\x00')
                    for s in strings:
                        decoded = s.decode('utf-8', errors='ignore').strip()
                        if 'BP_' in decoded and len(decoded) < 100:
                            # Clean up the string
                            decoded = decoded.split('\x00')[0]
                            return decoded
                except:
                    pass
        
        return None
    
    def extract_object_path(self) -> Optional[str]:
        """Extract the full object path (e.g., /Game/Levels/...)"""
        # Look for /Game/ paths
        if b'/Game/' in self.data:
            try:
                idx = self.data.find(b'/Game/')
                search_area = self.data[idx:idx+500]
                # Find null-terminated string
                null_idx = search_area.find(b'\x00')
                if null_idx > 0:
                    path = search_area[:null_idx].decode('utf-8', errors='ignore')
                    if path.startswith('/Game/') and len(path) < 500:
                        return path
            except:
                pass
        
        return None
    
    def extract_level_name(self) -> Optional[str]:
        """Extract level name from path"""
        obj_path = self.extract_object_path()
        if obj_path:
            # Pattern: /Game/Levels/LEVELNAME/...
            parts = obj_path.split('/')
            if 'Levels' in parts:
                level_idx = parts.index('Levels')
                if level_idx + 1 < len(parts):
                    return parts[level_idx + 1]
        
        # Fallback: check file path
        path_parts = self.file_path.parts
        if 'Levels' in path_parts:
            level_idx = path_parts.index('Levels')
            if level_idx + 1 < len(path_parts):
                return path_parts[level_idx + 1]
        
        return None
    
    def guess_collectible_type(self) -> Optional[str]:
        """Guess the collectible type from filename and content"""
        name_lower = self.file_path.name.lower()
        
        type_patterns = {
            'PSI_CARD': ['psicard', 'psycard'],
            'FIGMENT': ['figment'],
            'NUGGET': ['nugget', 'wisdom'],
            'BAGGAGE': ['baggage', 'emotional'],
            'MEMORY': ['memory', 'vault'],
            'HALF_A_MIND': ['halfamind', 'half-a-mind', 'halfmind']
        }
        
        for coll_type, patterns in type_patterns.items():
            if any(p in name_lower for p in patterns):
                return coll_type
        
        return None


class PakDataAnalyzer:
    """Analyzes extracted pak data to find collectibles"""
    
    def __init__(self, extracted_pak_path: Path):
        self.pak_path = extracted_pak_path
        self.collectibles = []
    
    def scan_for_collectibles(self):
        """Scan extracted pak data for collectible assets"""
        print("=" * 80)
        print("SCANNING EXTRACTED PAK DATA")
        print("=" * 80)
        print(f"\nScanning: {self.pak_path}")
        
        if not self.pak_path.exists():
            print(f"[ERROR] Path does not exist: {self.pak_path}")
            return []
        
        # Find all .uasset files
        uasset_files = list(self.pak_path.rglob("*.uasset"))
        print(f"Found {len(uasset_files)} .uasset files")
        
        # Filter to collectible-related files
        collectible_keywords = [
            'psicard', 'figment', 'nugget', 'baggage',
            'memory', 'halfamind', 'collectible'
        ]
        
        relevant_files = [
            f for f in uasset_files
            if any(kw in f.name.lower() for kw in collectible_keywords)
        ]
        
        print(f"Found {len(relevant_files)} collectible-related .uasset files")
        print("\nParsing files...")
        
        for i, file_path in enumerate(relevant_files):
            if i % 10 == 0:
                print(f"  Processed {i}/{len(relevant_files)}...", end='\r')
            
            parser = UAssetParser(file_path)
            result = parser.parse()
            
            if result:
                self.collectibles.append(result)
        
        print(f"\n\n[OK] Parsed {len(self.collectibles)} collectibles")
        
        # Group by type
        by_type = {}
        for item in self.collectibles:
            item_type = item.get('type', 'UNKNOWN')
            by_type.setdefault(item_type, []).append(item)
        
        print("\nBreakdown by type:")
        for item_type, items in sorted(by_type.items()):
            print(f"  {item_type}: {len(items)}")
        
        return self.collectibles
    
    def export_to_json(self, output_path: Path):
        """Export collectibles data to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.collectibles, f, indent=2)
        print(f"\n[OK] Exported to: {output_path}")
    
    def export_to_csv(self, output_path: Path):
        """Export collectibles data to CSV"""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'file_name', 'type', 'class_name', 'object_path', 'level'
            ])
            writer.writeheader()
            writer.writerows(self.collectibles)
        
        print(f"[OK] Exported CSV to: {output_path}")


def main():
    """Main execution"""
    pak_path = Path(r"C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example\extracted_pak_data")
    
    if not pak_path.exists():
        print("[ERROR] Extracted pak data not found!")
        print(f"Expected location: {pak_path}")
        print("\nRun extract_pak_data.bat first to extract the pak files.")
        return
    
    analyzer = PakDataAnalyzer(pak_path)
    collectibles = analyzer.scan_for_collectibles()
    
    if collectibles:
        # Export results
        output_json = pak_path / "parsed_collectibles.json"
        output_csv = pak_path / "parsed_collectibles.csv"
        
        analyzer.export_to_json(output_json)
        analyzer.export_to_csv(output_csv)
        
        print("\n" + "=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print("\n1. Review parsed_collectibles.csv")
        print("2. Compare with your existing CSVs:")
        print("   - worlds/psychonauts2/data/Psychonauts_2_Item_List.csv")
        print("   - worlds/psychonauts2/data/Psychonauts_2_Check_List.csv")
        print("3. Update CSVs with correct class names and object paths")

if __name__ == "__main__":
    main()
