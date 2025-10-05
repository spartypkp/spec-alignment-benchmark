#!/usr/bin/env python3
"""
Validate test result files for completeness and correctness.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

def validate_result_file(file_path: Path) -> Dict[str, Any]:
    """Validate a single test result file."""
    
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return {
            'valid': False,
            'errors': [f'Invalid JSON: {e}'],
            'warnings': []
        }
    except Exception as e:
        return {
            'valid': False,
            'errors': [f'Could not read file: {e}'],
            'warnings': []
        }
    
    # Check required fields
    required_fields = [
        'test_id', 'framework', 'model', 'test_repository',
        'prompt_used', 'start_time', 'end_time', 'framework_output'
    ]
    
    for field in required_fields:
        if field not in data:
            errors.append(f'Missing required field: {field}')
    
    # Validate framework output structure
    if 'framework_output' in data:
        output = data['framework_output']
        
        if not isinstance(output, dict):
            errors.append('framework_output must be a dictionary')
        elif 'gaps_found' not in output and 'findings' not in output:
            warnings.append('framework_output missing gaps_found or findings')
    
    # Validate timestamps
    if 'start_time' in data and 'end_time' in data:
        try:
            start = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
            duration = (end - start).total_seconds()
            
            if duration < 0:
                errors.append('end_time is before start_time')
            elif duration > 3600:  # More than 1 hour
                warnings.append(f'Test took {duration/60:.1f} minutes (unusually long)')
            
            if 'duration_seconds' in data:
                reported_duration = data['duration_seconds']
                if abs(reported_duration - duration) > 1:
                    warnings.append('duration_seconds does not match calculated duration')
        except Exception as e:
            errors.append(f'Invalid timestamp format: {e}')
    
    # Check model consistency
    if 'model' in data:
        if data['model'] != 'claude-3.5-sonnet':
            errors.append(f"Wrong model used: {data['model']} (expected claude-3.5-sonnet)")
    
    # Check framework validity
    if 'framework' in data:
        if data['framework'] not in ['cursor', 'claude-code']:
            errors.append(f"Unknown framework: {data['framework']}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'file': str(file_path)
    }


def validate_all_results(results_dir: Path) -> None:
    """Validate all result files in directory."""
    
    print("Validating test results...")
    print("=" * 60)
    
    all_valid = True
    frameworks = {}
    
    # Validate each framework's results
    for framework_dir in results_dir.iterdir():
        if not framework_dir.is_dir():
            continue
            
        framework_name = framework_dir.name
        frameworks[framework_name] = {
            'valid': [],
            'invalid': [],
            'total': 0
        }
        
        # Validate each test file
        for result_file in framework_dir.glob('*.json'):
            if result_file.name.startswith('run-'):
                result = validate_result_file(result_file)
                frameworks[framework_name]['total'] += 1
                
                if result['valid']:
                    frameworks[framework_name]['valid'].append(result_file.name)
                else:
                    frameworks[framework_name]['invalid'].append(result_file.name)
                    all_valid = False
                    
                    print(f"\n❌ {result_file}")
                    for error in result['errors']:
                        print(f"   ERROR: {error}")
                
                if result['warnings']:
                    print(f"\n⚠️  {result_file}")
                    for warning in result['warnings']:
                        print(f"   WARNING: {warning}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for framework, stats in frameworks.items():
        valid_count = len(stats['valid'])
        invalid_count = len(stats['invalid'])
        total = stats['total']
        
        if total == 0:
            print(f"\n{framework}: No test files found")
        else:
            status = "✅" if invalid_count == 0 else "❌"
            print(f"\n{framework}: {status}")
            print(f"  Valid:   {valid_count}/{total}")
            print(f"  Invalid: {invalid_count}/{total}")
            
            if invalid_count > 0:
                print(f"  Invalid files: {', '.join(stats['invalid'])}")
    
    if all_valid:
        print("\n✅ All test results are valid!")
        sys.exit(0)
    else:
        print("\n❌ Some test results have validation errors. Please fix before analysis.")
        sys.exit(1)


def main():
    """Main entry point."""
    
    results_dir = Path(__file__).parent.parent / 'results' / 'raw'
    
    if not results_dir.exists():
        print(f"Results directory not found: {results_dir}")
        sys.exit(1)
    
    validate_all_results(results_dir)


if __name__ == '__main__':
    main()
