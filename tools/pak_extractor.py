"""
Psychonauts 2 Pak File Extractor
Extracts game data from Psychonauts 2 pak files using QuickBMS
"""

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict

class PN2PakExtractor:
    def __init__(self):
        self.repo_root = Path(r"C:\Users\adkin\source\repos\Psychonauts-2-AP-World---Example")
        self.quickbms_path = self.repo_root / "tools" / "quickbms" / "quickbms.exe"
        self.script_path = self.repo_root / "tools" / "quickbms" / "unreal_tournament_4.bms"
        self.pak_file = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Psychonauts 2\Psychonauts2\Content\Paks\Psychonauts2-WindowsNoEditor.pak")
        self.output_path = self.repo_root / "extracted_pak_data"
        
    def extract_pak(self, filter_pattern: str = None):
        """Extract pak file using QuickBMS
        
        Args:
            filter_pattern: Optional pattern to filter files (e.g., '*Collectible*')
        """
        print("=" * 80)
        print("PSYCHONAUTS 2 PAK FILE EXTRACTION")
        print("=" * 80)
        print(f"\nPak file: {self.pak_file}")
        print(f"Size: {self.pak_file.stat().st_size / (1024**3):.2f} GB")
        print(f"Output: {self.output_path}")
        
        # Create output directory
        self.output_path.mkdir(exist_ok=True)
        
        # Build QuickBMS command
        cmd = [
            str(self.quickbms_path),
            "-o",  # Overwrite existing files
            str(self.script_path),
            str(self.pak_file),
            str(self.output_path)
        ]
        
        if filter_pattern:
            cmd.append("-f")
            cmd.append(filter_pattern)
        
        print(f"\nRunning extraction...")
        print(f"Command: {' '.join(cmd)}")
        print("\nThis may take several minutes for a 30GB pak file...")
        print("(QuickBMS will show progress)")
        print("\n" + "-" * 80)
        
        try:
            result = subprocess.run(cmd, capture_output=False, text=True)
            
            if result.returncode == 0:
                print("\n" + "-" * 80)
                print("[SUCCESS] Extraction complete!")
                self.analyze_extracted_files()
            else:
                print("\n" + "-" * 80)
                print(f"[ERROR] Extraction failed with code {result.returncode}")
                
        except Exception as e:
            print(f"\n[ERROR] Extraction failed: {e}")
    
    def analyze_extracted_files(self):
        """Analyze extracted files and find collectibles"""
        print("\n" + "=" * 80)
        print("ANALYZING EXTRACTED FILES")
        print("=" * 80)
        
        collectible_keywords = [
            'psicard', 'figment', 'nugget', 'baggage', 
            'memory', 'halfamind', 'collectible', 'pickup'
        ]
        
        relevant_files = []
        
        for root, dirs, files in os.walk(self.output_path):
            for file in files:
                file_lower = file.lower()
                if any(keyword in file_lower for keyword in collectible_keywords):
                    full_path = Path(root) / file
                    relevant_files.append({
                        'name': file,
                        'path': str(full_path.relative_to(self.output_path)),
                        'size': full_path.stat().st_size
                    })
        
        print(f"\nFound {len(relevant_files)} collectible-related files:")
        
        # Group by type
        by_type = {}
        for f in relevant_files:
            for keyword in collectible_keywords:
                if keyword in f['name'].lower():
                    by_type.setdefault(keyword, []).append(f)
                    break
        
        for keyword, files in sorted(by_type.items()):
            print(f"\n{keyword.upper()}: {len(files)} files")
            for f in files[:5]:  # Show first 5
                print(f"  - {f['name']}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
        
        # Save catalog
        catalog_path = self.output_path / "collectibles_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(relevant_files, f, indent=2)
        
        print(f"\n[OK] Catalog saved to: {catalog_path}")
        
        return relevant_files
    
    def quick_extract_collectibles_only(self):
        """Extract only collectible-related files (faster)"""
        print("Starting targeted extraction (collectibles only)...")
        print("This will be much faster than extracting the entire 30GB pak!\n")
        
        # Extract with filter
        self.extract_pak(filter_pattern="*Collectible*,*PsiCard*,*Figment*,*Nugget*,*Baggage*,*Memory*,*HalfAMind*")

def main():
    """Main extraction workflow"""
    extractor = PN2PakExtractor()
    
    print("=" * 80)
    print("PSYCHONAUTS 2 DATA EXTRACTION TOOL")
    print("=" * 80)
    print("\nOptions:")
    print("1. Quick extract (collectibles only) - RECOMMENDED")
    print("2. Full extraction (entire 30GB pak) - SLOW")
    print("3. Analyze already extracted files")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        extractor.quick_extract_collectibles_only()
    elif choice == "2":
        extractor.extract_pak()
    elif choice == "3":
        if extractor.output_path.exists():
            extractor.analyze_extracted_files()
        else:
            print(f"[ERROR] No extracted files found at {extractor.output_path}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
