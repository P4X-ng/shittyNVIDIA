#!/usr/bin/env python3
"""
Comprehensive test suite for shittyNVIDIA .pf files
Tests syntax, structure, and content validity
"""

import sys
import subprocess
from pathlib import Path

def test_file_exists():
    """Test that all required files exist"""
    print("Testing file existence...")
    required_files = [
        'Pfyfile.pf',
        'Pfyfile.nvidia-fail.pf',
        'Pfyfile.driver-chaos.pf',
        'Pfyfile.gpu-disaster.pf',
        'PFYFILE_README.md',
        'README.md',
        'validate_pf_files.py'
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"  ✅ {filename}")
        else:
            print(f"  ❌ {filename} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_validator_runs():
    """Test that the validator runs successfully"""
    print("\nTesting validator execution...")
    try:
        result = subprocess.run(
            ['python3', 'validate_pf_files.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("  ✅ Validator executed successfully")
            print(f"  Output: {result.stdout.splitlines()[-2]}")  # Last meaningful line
            return True
        else:
            print(f"  ❌ Validator failed with code {result.returncode}")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Error running validator: {e}")
        return False

def test_task_structure():
    """Test that .pf files have proper task structure"""
    print("\nTesting .pf file structure...")
    pf_files = list(Path('.').glob('Pfyfile*.pf'))
    
    all_valid = True
    total_tasks = 0
    
    for pf_file in sorted(pf_files):
        with open(pf_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        task_count = content.count('task ')
        end_count = content.count('\nend\n') + content.count('\nend$')
        shell_count = content.count('shell ')
        describe_count = content.count('describe ')
        
        total_tasks += task_count
        
        # Basic validation
        valid = True
        issues = []
        
        if task_count == 0:
            issues.append("no tasks defined")
            valid = False
        
        if describe_count < task_count:
            issues.append(f"missing descriptions ({describe_count}/{task_count})")
        
        if shell_count < task_count:
            issues.append(f"missing shell commands ({shell_count}/{task_count})")
        
        if valid:
            print(f"  ✅ {pf_file.name}: {task_count} tasks, {shell_count} shell commands")
        else:
            print(f"  ❌ {pf_file.name}: {', '.join(issues)}")
            all_valid = False
    
    print(f"\n  Total tasks across all files: {total_tasks}")
    return all_valid and total_tasks == 30

def test_documentation():
    """Test that documentation is comprehensive"""
    print("\nTesting documentation...")
    
    # Check PFYFILE_README
    with open('PFYFILE_README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    required_sections = [
        'What are .pf files',
        'Requirements',
        'Installation',
        'Available Task Files',
        'Usage Examples',
        'Troubleshooting'
    ]
    
    all_present = True
    for section in required_sections:
        if section in readme_content:
            print(f"  ✅ Section: {section}")
        else:
            print(f"  ❌ Section missing: {section}")
            all_present = False
    
    return all_present

def test_satirical_content():
    """Test that content maintains satirical theme"""
    print("\nTesting satirical content consistency...")
    
    keywords = [
        'fail', 'error', 'crash', 'broken', 'worst',
        'zero', 'never', 'impossible', 'disaster'
    ]
    
    all_files = list(Path('.').glob('Pfyfile*.pf'))
    all_files.append(Path('README.md'))
    
    all_satirical = True
    for filepath in all_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        found_keywords = [kw for kw in keywords if kw in content]
        if len(found_keywords) >= 3:
            print(f"  ✅ {filepath.name}: {len(found_keywords)} satirical keywords")
        else:
            print(f"  ⚠️  {filepath.name}: only {len(found_keywords)} satirical keywords")
            all_satirical = False
    
    return all_satirical

def main():
    """Run all tests"""
    print("=" * 60)
    print("shittyNVIDIA .pf Files - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ('File Existence', test_file_exists),
        ('Validator Execution', test_validator_runs),
        ('Task Structure', test_task_structure),
        ('Documentation', test_documentation),
        ('Satirical Content', test_satirical_content)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n  ❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! shittyNVIDIA .pf files are ready!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
