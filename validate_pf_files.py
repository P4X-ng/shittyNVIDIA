#!/usr/bin/env python3
"""
Simple validator for .pf task files
Tests that the files have valid syntax and structure
"""

import re
import sys
from pathlib import Path

def validate_pf_file(filepath):
    """Validate a .pf file for proper syntax"""
    errors = []
    warnings = []
    
    with open(filepath, 'r') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Check for balanced task/end blocks
    task_stack = []
    task_count = 0
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Check for task definitions
        if line.startswith('task '):
            task_name = line.split()[1] if len(line.split()) > 1 else None
            if task_name:
                task_stack.append((task_name, i))
                task_count += 1
            else:
                errors.append(f"Line {i}: Task without name")
        
        # Check for end statements
        elif line == 'end':
            if task_stack:
                task_stack.pop()
            else:
                errors.append(f"Line {i}: 'end' without matching 'task'")
        
        # Check for describe statements
        elif line.startswith('describe '):
            if not task_stack:
                warnings.append(f"Line {i}: 'describe' outside of task block")
        
        # Check for shell statements
        elif line.startswith('shell ') or line.startswith('shell_lang '):
            if not task_stack:
                warnings.append(f"Line {i}: 'shell' outside of task block")
    
    # Check for unclosed tasks
    if task_stack:
        for task_name, line_num in task_stack:
            errors.append(f"Line {line_num}: Task '{task_name}' not closed with 'end'")
    
    return {
        'filepath': filepath,
        'task_count': task_count,
        'errors': errors,
        'warnings': warnings,
        'valid': len(errors) == 0
    }

def main():
    """Validate all .pf files in current directory"""
    pf_files = list(Path('.').glob('*.pf'))
    
    if not pf_files:
        print("No .pf files found in current directory")
        return 1
    
    print("shittyNVIDIA Task File Validator")
    print("=" * 50)
    print()
    
    all_valid = True
    total_tasks = 0
    
    for pf_file in sorted(pf_files):
        result = validate_pf_file(pf_file)
        total_tasks += result['task_count']
        
        print(f"File: {result['filepath']}")
        print(f"  Tasks: {result['task_count']}")
        
        if result['errors']:
            all_valid = False
            print(f"  ❌ Errors: {len(result['errors'])}")
            for error in result['errors']:
                print(f"     - {error}")
        else:
            print(f"  ✅ No errors")
        
        if result['warnings']:
            print(f"  ⚠️  Warnings: {len(result['warnings'])}")
            for warning in result['warnings']:
                print(f"     - {warning}")
        
        print()
    
    print("=" * 50)
    print(f"Total tasks defined: {total_tasks}")
    print(f"All files valid: {'✅ Yes' if all_valid else '❌ No'}")
    
    return 0 if all_valid else 1

if __name__ == '__main__':
    sys.exit(main())
