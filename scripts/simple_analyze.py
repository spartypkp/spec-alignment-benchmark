#!/usr/bin/env python3
"""
Simple Analyzer - One script to rule them all.
Replaces the entire 7-script pipeline with something that actually works.

Usage:
    python simple_analyze.py                    # Analyze everything
    python simple_analyze.py --branch baseline  # Analyze specific branch
    python simple_analyze.py --test run1        # Analyze specific test
    python simple_analyze.py --debug            # Show detailed output
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict
import statistics
import argparse


# Color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def load_json(filepath: Path) -> Dict:
    """Load JSON file safely."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"{Colors.RED}Error loading {filepath}: {e}{Colors.ENDC}")
        return {}


def normalize_output(raw_output: Dict, test_type: str) -> Dict:
    """
    Normalize Cursor's various output formats to standard structure.
    Handles the format mismatch that breaks the current pipeline.
    """
    normalized = {
        'type1_missing': [],
        'type2_incorrect': [],
        'type3_extraneous': []
    }
    
    # Combined test - already in correct format
    if 'type1_missing' in raw_output:
        return raw_output
    
    # Individual tests - all use 'misalignments' key
    if 'misalignments' in raw_output:
        misalignments = raw_output['misalignments']
        
        if test_type == 'type1':
            # Type1: Extract sections only
            normalized['type1_missing'] = [
                item.get('section', '') for item in misalignments
                if 'section' in item
            ]
        
        elif test_type == 'type2':
            # Type2: Keep section + files structure
            normalized['type2_incorrect'] = misalignments
        
        elif test_type == 'type3':
            # Type3: Extract files (note: raw has 'file', ground truth has 'expected_files')
            normalized['type3_extraneous'] = [
                item.get('file', '') for item in misalignments
                if 'file' in item
            ]
    
    return normalized


def calculate_metrics(detected: List, expected: List) -> Dict:
    """Calculate precision, recall, F1 score."""
    if not detected and not expected:
        return {'precision': 1.0, 'recall': 1.0, 'f1': 1.0, 'tp': 0, 'fp': 0, 'fn': 0}
    
    # Convert to sets for comparison
    if detected and isinstance(detected[0], str):
        detected_set = set(detected)
    elif detected:
        detected_set = {item.get('section', item.get('file', '')) for item in detected}
    else:
        detected_set = set()
    
    expected_set = set(expected)
    
    tp = len(detected_set & expected_set)  # True positives
    fp = len(detected_set - expected_set)  # False positives
    fn = len(expected_set - detected_set)  # False negatives
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'fn': fn
    }


def analyze_single_test(raw_file: Path, ground_truth_file: Path, test_type: str, debug: bool = False) -> Dict:
    """Analyze a single test file against ground truth."""
    raw_data = load_json(raw_file)
    ground_truth = load_json(ground_truth_file)
    
    if not raw_data or not ground_truth:
        return {}
    
    # Normalize the output format
    normalized = normalize_output(raw_data, test_type)
    
    # Get expected values based on test type
    if test_type == 'type1':
        detected = normalized['type1_missing']
        expected = ground_truth.get('expected_sections', [])
    elif test_type == 'type2':
        detected = [item.get('section', '') for item in normalized['type2_incorrect']]
        expected = ground_truth.get('expected_sections', [])
    elif test_type == 'type3':
        detected = normalized['type3_extraneous']
        expected = ground_truth.get('expected_files', [])
    elif test_type == 'combined':
        # Analyze all three types
        results = {}
        for t, key, exp_key in [
            ('type1', 'type1_missing', 'type1_missing'),
            ('type2', 'type2_incorrect', 'type2_incorrect'),
            ('type3', 'type3_extraneous', 'type3_extraneous')
        ]:
            if exp_key == 'type1_missing':
                detected = normalized[key]
                expected = [item['section'] for item in ground_truth.get('ground_truth', {}).get(exp_key, [])]
            elif exp_key == 'type2_incorrect':
                detected = [item.get('section', '') for item in normalized[key]]
                expected = [item['section'] for item in ground_truth.get('ground_truth', {}).get(exp_key, [])]
            else:  # type3
                detected = normalized[key]
                expected = [item['file'] for item in ground_truth.get('ground_truth', {}).get(exp_key, [])]
            
            results[t] = calculate_metrics(detected, expected)
            if debug:
                print(f"  {t}: Detected {detected}, Expected {expected}")
        return results
    else:
        return {}
    
    metrics = calculate_metrics(detected, expected)
    
    if debug:
        print(f"  Detected: {detected}")
        print(f"  Expected: {expected}")
        print(f"  Metrics: P={metrics['precision']:.2f}, R={metrics['recall']:.2f}, F1={metrics['f1']:.2f}")
    
    return metrics


def analyze_branch(branch_name: str, debug: bool = False) -> Dict:
    """Analyze all tests for a branch."""
    results = defaultdict(lambda: defaultdict(list))
    base_path = Path(f"results/raw/cursor/{branch_name}")
    ground_truth_base = Path(f"benchmark/branches/{branch_name}")
    
    if not base_path.exists():
        print(f"{Colors.RED}Branch {branch_name} not found{Colors.ENDC}")
        return {}
    
    # Process each test type
    for test_type in ['type1', 'type2', 'type3', 'combined']:
        test_dir = base_path / test_type
        if not test_dir.exists():
            continue
        
        # Determine ground truth file
        if test_type == 'combined':
            gt_file = ground_truth_base / f"ground-truth-combined.json"
        else:
            gt_file = ground_truth_base / f"ground-truth-{test_type}.json"
        
        if not gt_file.exists():
            print(f"{Colors.YELLOW}Ground truth missing for {branch_name}/{test_type}{Colors.ENDC}")
            continue
        
        # Process each run
        for run_file in sorted(test_dir.glob("run*.json")):
            if debug:
                print(f"Analyzing {run_file.name}...")
            
            metrics = analyze_single_test(run_file, gt_file, test_type, debug)
            
            if test_type == 'combined':
                for subtype, submetrics in metrics.items():
                    results[test_type][subtype].append(submetrics)
            else:
                if metrics:
                    results[test_type]['metrics'].append(metrics)
    
    return results


def print_branch_summary(branch_name: str, results: Dict):
    """Print a nice summary for a branch."""
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}Branch: {branch_name}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    
    for test_type in ['type1', 'type2', 'type3', 'combined']:
        if test_type not in results:
            continue
        
        print(f"\n{Colors.CYAN}▶ {test_type.upper()} Tests{Colors.ENDC}")
        
        if test_type == 'combined':
            for subtype in ['type1', 'type2', 'type3']:
                if subtype in results[test_type]:
                    metrics_list = results[test_type][subtype]
                    if metrics_list:
                        avg_f1 = statistics.mean([m['f1'] for m in metrics_list])
                        avg_precision = statistics.mean([m['precision'] for m in metrics_list])
                        avg_recall = statistics.mean([m['recall'] for m in metrics_list])
                        
                        color = Colors.GREEN if avg_f1 > 0.7 else Colors.YELLOW if avg_f1 > 0.4 else Colors.RED
                        print(f"  {subtype}: {color}F1={avg_f1:.2%}, P={avg_precision:.2%}, R={avg_recall:.2%}{Colors.ENDC}")
        else:
            metrics_list = results[test_type].get('metrics', [])
            if metrics_list:
                avg_f1 = statistics.mean([m['f1'] for m in metrics_list])
                avg_precision = statistics.mean([m['precision'] for m in metrics_list])
                avg_recall = statistics.mean([m['recall'] for m in metrics_list])
                
                # Count detections
                total_tp = sum([m['tp'] for m in metrics_list])
                total_fp = sum([m['fp'] for m in metrics_list])
                total_fn = sum([m['fn'] for m in metrics_list])
                
                color = Colors.GREEN if avg_f1 > 0.7 else Colors.YELLOW if avg_f1 > 0.4 else Colors.RED
                print(f"  {color}F1={avg_f1:.2%}, Precision={avg_precision:.2%}, Recall={avg_recall:.2%}{Colors.ENDC}")
                print(f"  Detections: {total_tp} correct, {total_fp} false positives, {total_fn} missed")


def generate_full_report():
    """Generate a complete analysis report."""
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║           SIMPLE ANALYZER - FULL REPORT                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    branches = ['control_perfect', 'baseline_balanced', 'type1_heavy', 'type2_heavy', 'subtle_only', 'distributed']
    all_results = {}
    
    for branch in branches:
        results = analyze_branch(branch)
        if results:
            all_results[branch] = results
            print_branch_summary(branch, results)
    
    # Overall summary
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}OVERALL SUMMARY{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    
    total_tests = 0
    working_tests = 0
    
    for branch, results in all_results.items():
        for test_type, data in results.items():
            if test_type == 'combined':
                for subtype, metrics_list in data.items():
                    total_tests += len(metrics_list)
                    working_tests += sum(1 for m in metrics_list if m['f1'] > 0)
            else:
                metrics_list = data.get('metrics', [])
                total_tests += len(metrics_list)
                working_tests += sum(1 for m in metrics_list if m['f1'] > 0)
    
    print(f"\nTotal tests analyzed: {total_tests}")
    print(f"Tests with detections: {working_tests} ({working_tests/total_tests:.1%})")
    print(f"\n{Colors.GREEN}✓ Analysis complete!{Colors.ENDC}")
    
    # Save results to JSON
    output_file = Path("results/simple_analysis_results.json")
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nDetailed results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Simple analyzer for benchmark results')
    parser.add_argument('--branch', help='Analyze specific branch only')
    parser.add_argument('--test', help='Analyze specific test file')
    parser.add_argument('--debug', action='store_true', help='Show detailed debug output')
    args = parser.parse_args()
    
    if args.branch:
        results = analyze_branch(args.branch, args.debug)
        if results:
            print_branch_summary(args.branch, results)
    elif args.test:
        print("Single test analysis not implemented yet")
    else:
        generate_full_report()


if __name__ == "__main__":
    main()
