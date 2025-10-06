#!/usr/bin/env python3
"""
Score a single test result against ground truth.
Handles the new detailed ground truth format with reasoning fields.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime

def load_json(filepath: Path) -> Dict:
    """Load and validate JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

def extract_sections(misalignments: List[Dict]) -> Set[str]:
    """Extract section numbers from misalignment list."""
    return {m.get('section', '') for m in misalignments if 'section' in m}

def extract_files(misalignments: List[Dict]) -> Set[str]:
    """Extract file paths from Type 3 misalignments."""
    return {m.get('file', '') for m in misalignments if 'file' in m}

def score_type1(llm_output: List, ground_truth: List[Dict]) -> Dict:
    """Score Type 1 (Missing Implementation) detection."""
    # Extract sections from ground truth
    gt_sections = extract_sections(ground_truth)
    
    # Handle different LLM output formats
    if isinstance(llm_output, list):
        if all(isinstance(item, dict) for item in llm_output):
            llm_sections = extract_sections(llm_output)
        else:
            # Simple list of section numbers
            llm_sections = set(str(s) for s in llm_output)
    else:
        llm_sections = set()
    
    # Calculate metrics
    true_positives = llm_sections & gt_sections
    false_positives = llm_sections - gt_sections
    false_negatives = gt_sections - llm_sections
    
    precision = len(true_positives) / len(llm_sections) if llm_sections else 0
    recall = len(true_positives) / len(gt_sections) if gt_sections else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # Calculate point score
    points = len(true_positives) * 1.0 - len(false_positives) * 0.25
    
    return {
        "true_positives": list(true_positives),
        "false_positives": list(false_positives),
        "false_negatives": list(false_negatives),
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "points": points,
        "total_ground_truth": len(gt_sections),
        "total_detected": len(llm_sections)
    }

def score_type2(llm_output: List, ground_truth: List[Dict]) -> Dict:
    """Score Type 2 (Incorrect Implementation) detection."""
    # Build ground truth mapping
    gt_map = {}
    for item in ground_truth:
        section = item.get('section', '')
        if section:
            gt_map[section] = set(item.get('files', []))
    
    # Process LLM output
    llm_map = {}
    if isinstance(llm_output, list):
        for item in llm_output:
            if isinstance(item, dict):
                section = item.get('section', '')
                if section:
                    llm_map[section] = set(item.get('files', []))
    
    # Score based on section + at least one file overlap
    true_positives = []
    false_positives = []
    
    for section, llm_files in llm_map.items():
        if section in gt_map:
            # Check if at least one file overlaps
            if llm_files & gt_map[section]:
                true_positives.append(section)
            else:
                # Section correct but wrong files
                false_positives.append(section)
        else:
            false_positives.append(section)
    
    false_negatives = [s for s in gt_map.keys() if s not in true_positives]
    
    precision = len(true_positives) / len(llm_map) if llm_map else 0
    recall = len(true_positives) / len(gt_map) if gt_map else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # Calculate point score
    points = len(true_positives) * 1.0 - len(false_positives) * 0.25
    
    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "points": points,
        "total_ground_truth": len(gt_map),
        "total_detected": len(llm_map)
    }

def score_type3(llm_output: List, ground_truth: List[Dict]) -> Dict:
    """Score Type 3 (Extraneous Code) detection."""
    # Extract files from ground truth (new format has individual files)
    gt_files = extract_files(ground_truth)
    
    # Process LLM output - expecting files in the new format
    llm_files = set()
    if isinstance(llm_output, list):
        for item in llm_output:
            if isinstance(item, dict):
                # New format: {file: "path", reasoning: "..."}
                file_path = item.get('file', '')
                if file_path:
                    llm_files.add(file_path)
                # Also handle old format for backwards compatibility
                feature = item.get('feature', '')
                if feature and not file_path:
                    # Old feature format - extract files if present
                    for f in item.get('files', []):
                        llm_files.add(f)
            else:
                # Simple string (file path)
                llm_files.add(str(item))
    
    # Score based on file matching
    true_positives = llm_files & gt_files
    false_positives = llm_files - gt_files
    false_negatives = gt_files - llm_files
    
    precision = len(true_positives) / len(llm_files) if llm_files else 0
    recall = len(true_positives) / len(gt_files) if gt_files else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # Calculate point score
    points = len(true_positives) * 1.0 - len(false_positives) * 0.25
    
    return {
        "true_positives": list(true_positives),
        "false_positives": list(false_positives),
        "false_negatives": list(false_negatives),
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "points": points,
        "total_ground_truth": len(gt_files),
        "total_detected": len(llm_files)
    }

def score_combined(llm_output: Dict, ground_truth: Dict) -> Dict:
    """Score combined detection of all three types."""
    results = {}
    
    # Score each type if present
    if 'type1_missing' in ground_truth:
        llm_type1 = llm_output.get('type1_missing', [])
        gt_type1 = ground_truth['type1_missing']
        results['type1'] = score_type1(llm_type1, gt_type1)
    
    if 'type2_incorrect' in ground_truth:
        llm_type2 = llm_output.get('type2_incorrect', [])
        gt_type2 = ground_truth['type2_incorrect']
        results['type2'] = score_type2(llm_type2, gt_type2)
    
    if 'type3_extraneous' in ground_truth:
        llm_type3 = llm_output.get('type3_extraneous', [])
        gt_type3 = ground_truth['type3_extraneous']
        results['type3'] = score_type3(llm_type3, gt_type3)
    
    # Calculate combined metrics
    total_precision = []
    total_recall = []
    total_f1 = []
    total_points = 0
    
    for type_results in results.values():
        total_precision.append(type_results['precision'])
        total_recall.append(type_results['recall'])
        total_f1.append(type_results['f1_score'])
        total_points += type_results['points']
    
    results['combined'] = {
        "avg_precision": sum(total_precision) / len(total_precision) if total_precision else 0,
        "avg_recall": sum(total_recall) / len(total_recall) if total_recall else 0,
        "avg_f1": sum(total_f1) / len(total_f1) if total_f1 else 0,
        "total_points": total_points
    }
    
    return results

def main():
    if len(sys.argv) != 3:
        print("Usage: python score_result.py <llm_output.json> <ground_truth.json>")
        print("\nExample:")
        print("  python score_result.py results/raw/cursor/baseline_balanced/type1_run1.json \\")
        print("                         benchmark/branches/baseline_balanced/ground-truth-type1.json")
        sys.exit(1)
    
    llm_output_path = Path(sys.argv[1])
    ground_truth_path = Path(sys.argv[2])
    
    # Load files
    llm_output = load_json(llm_output_path)
    ground_truth_data = load_json(ground_truth_path)
    
    # Determine test type from ground truth
    test_type = ground_truth_data.get('test_type', 'unknown')
    
    # Score based on test type
    if test_type == 'type1_missing':
        gt_misalignments = ground_truth_data['ground_truth']['misalignments']
        llm_detections = llm_output.get('type1_missing', [])
        results = score_type1(llm_detections, gt_misalignments)
        
    elif test_type == 'type2_incorrect':
        gt_misalignments = ground_truth_data['ground_truth']['misalignments']
        llm_detections = llm_output.get('type2_incorrect', [])
        results = score_type2(llm_detections, gt_misalignments)
        
    elif test_type == 'type3_extraneous':
        gt_misalignments = ground_truth_data['ground_truth']['misalignments']
        llm_detections = llm_output.get('type3_extraneous', [])
        results = score_type3(llm_detections, gt_misalignments)
        
    elif test_type == 'combined_all_types':
        gt = ground_truth_data['ground_truth']
        results = score_combined(llm_output, gt)
    else:
        print(f"Error: Unknown test type '{test_type}'")
        sys.exit(1)
    
    # Add metadata
    output = {
        "metadata": {
            "llm_output_file": str(llm_output_path),
            "ground_truth_file": str(ground_truth_path),
            "test_branch": ground_truth_data.get('test_branch', 'unknown'),
            "test_type": test_type,
            "scored_at": datetime.now().isoformat()
        },
        "scores": results
    }
    
    # Print results
    print(json.dumps(output, indent=2))
    
    # Also print summary
    print("\n" + "="*60)
    print("SCORING SUMMARY")
    print("="*60)
    
    if test_type == 'combined_all_types':
        for type_name, type_scores in results.items():
            if type_name != 'combined':
                print(f"\n{type_name.upper()}:")
                print(f"  Precision: {type_scores['precision']:.1%}")
                print(f"  Recall: {type_scores['recall']:.1%}")
                print(f"  F1 Score: {type_scores['f1_score']:.3f}")
                print(f"  Points: {type_scores['points']:.2f}")
        
        print(f"\nCOMBINED:")
        print(f"  Avg Precision: {results['combined']['avg_precision']:.1%}")
        print(f"  Avg Recall: {results['combined']['avg_recall']:.1%}")
        print(f"  Avg F1: {results['combined']['avg_f1']:.3f}")
        print(f"  Total Points: {results['combined']['total_points']:.2f}")
    else:
        print(f"\nTest Type: {test_type}")
        print(f"Precision: {results['precision']:.1%}")
        print(f"Recall: {results['recall']:.1%}")
        print(f"F1 Score: {results['f1_score']:.3f}")
        print(f"Points: {results['points']:.2f}")
        print(f"\nDetection Details:")
        print(f"  True Positives: {len(results['true_positives'])}")
        print(f"  False Positives: {len(results['false_positives'])}")
        print(f"  False Negatives: {len(results['false_negatives'])}")

if __name__ == "__main__":
    main()
