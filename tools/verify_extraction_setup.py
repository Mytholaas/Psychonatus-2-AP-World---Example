"""
Verify Pak Extraction Setup
Checks that all required tools and files are ready
"""

import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} (need 3.7+)")
        return False

def check_quickbms():
    """Check if QuickBMS is installed"""
    print("\nChecking QuickBMS...")
    quickbms = Path("tools/quickbms/quickbms.exe")
    if quickbms.exists():
        size_mb = quickbms.stat().st_size / (1024**2)
        print(f"  ✅ QuickBMS found ({size_mb:.1f} MB)")
        return True
    else:
        print(f"  ❌ QuickBMS not found at: {quickbms}")
        return False

def check_extraction_script():
    """Check if UE4 extraction script exists"""
    print("\nChecking UE4 extraction script...")
    script = Path("tools/quickbms/unreal_tournament_4.bms")
    if script.exists():
        print(f"  ✅ UE4 script found")
        return True
    else:
        print(f"  ❌ Script not found at: {script}")
        return False

def check_pak_file():
    """Check if Psychonauts 2 pak file exists"""
    print("\nChecking Psychonauts 2 pak file...")
    pak = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Psychonauts 2\Psychonauts2\Content\Paks\Psychonauts2-WindowsNoEditor.pak")
    if pak.exists():
        size_gb = pak.stat().st_size / (1024**3)
        print(f"  ✅ Pak file found ({size_gb:.2f} GB)")
        return True
    else:
        print(f"  ❌ Pak file not found")
        print(f"     Expected: {pak}")
        return False

def check_disk_space():
    """Check available disk space"""
    print("\nChecking disk space...")
    import shutil
    repo_path = Path.cwd()
    stat = shutil.disk_usage(repo_path)
    free_gb = stat.free / (1024**3)
    
    if free_gb >= 10:
        print(f"  ✅ {free_gb:.1f} GB free (sufficient)")
        return True
    else:
        print(f"  ⚠️  {free_gb:.1f} GB free (recommend at least 10 GB)")
        return False

def check_python_tools():
    """Check if Python tools exist"""
    print("\nChecking Python tools...")
    tools = [
        "tools/pak_extractor.py",
        "tools/parse_uasset.py",
        "tools/extract_and_match.py"
    ]
    
    all_found = True
    for tool in tools:
        tool_path = Path(tool)
        if tool_path.exists():
            print(f"  ✅ {tool}")
        else:
            print(f"  ❌ {tool} (missing)")
            all_found = False
    
    return all_found

def check_csv_files():
    """Check if existing CSV files are present"""
    print("\nChecking existing CSV files...")
    csvs = [
        "worlds/psychonauts2/data/Psychonauts_2_Item_List.csv",
        "worlds/psychonauts2/data/Psychonauts_2_Check_List.csv"
    ]
    
    all_found = True
    for csv in csvs:
        csv_path = Path(csv)
        if csv_path.exists():
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines()) - 1  # Subtract header
            print(f"  ✅ {csv_path.name} ({lines} entries)")
        else:
            print(f"  ❌ {csv} (missing)")
            all_found = False
    
    return all_found

def main():
    """Run all checks"""
    print("=" * 70)
    print("PSYCHONAUTS 2 PAK EXTRACTION - SETUP VERIFICATION")
    print("=" * 70)
    
    checks = [
        ("Python Version", check_python_version),
        ("QuickBMS", check_quickbms),
        ("Extraction Script", check_extraction_script),
        ("Game Pak File", check_pak_file),
        ("Disk Space", check_disk_space),
        ("Python Tools", check_python_tools),
        ("CSV Files", check_csv_files)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print(f"\n  ❌ Error checking {name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"\n✅ ALL CHECKS PASSED ({passed}/{total})")
        print("\nYou're ready to extract!")
        print("\nNext step: Run extract_pak_data.bat")
    else:
        print(f"\n⚠️  {passed}/{total} checks passed")
        print("\nPlease fix the issues marked with ❌ above")
        print("Refer to EXTRACTION_SETUP_COMPLETE.md for help")
    
    print()

if __name__ == "__main__":
    main()
