#!/usr/bin/env python3
"""
Scoring script for comparing LLM outputs against ground truth.
Uses simple set operations for objective, reproducible scoring.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

def load_json(file_path: Path) -> Dict:
    """Load a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def score_type1(llm_output: List[str], ground_truth: List[str]) -> Dict:
    """
    Score Type 1 (Missing Implementation) detection.
    Simple set comparison of section headers.
    """
    found = set(llm_output)
    expected = set(ground_truth)
    
    true_positives = found & expected
    false_positives = found - expected
    false_negatives = expected - found
    
    precision = len(true_positives) / len(found) if found else 0
    recall = len(true_positives) / len(expected) if expected else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "true_positives": list(true_positives),
        "false_positives": list(false_positives),
        "false_negatives": list(false_negatives),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "score": len(true_positives) - (0.25 * len(false_positives))
    }

def score_type2(llm_output: List[Dict], ground_truth: List[Dict]) -> Dict:
    """
    Score Type 2 (Incorrect Implementation) detection.
    Match section AND at least one file overlap.
    """
    true_positives = []
    false_negatives = list(ground_truth)  # Start with all, remove matches
    false_positives = []
    
    # Check each LLM finding
    for llm_item in llm_output:
        matched = False
        for gt_item in ground_truth:
            if llm_item["section"] == gt_item["section"]:
                # Check if any files match
                llm_files = set(llm_item.get("files", []))
                gt_files = set(gt_item.get("files", []))
                if llm_files & gt_files:  # Intersection
                    matched = True
                    true_positives.append({
                        "section": llm_item["section"],
                        "matched_files": list(llm_files & gt_files)
                    })
                    # Remove from false negatives
                    if gt_item in false_negatives:
                        false_negatives.remove(gt_item)
                    break
        
        if not matched:
            false_positives.append(llm_item)
    
    precision = len(true_positives) / len(llm_output) if llm_output else 0
    recall = len(true_positives) / len(ground_truth) if ground_truth else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "score": len(true_positives) - (0.25 * len(false_positives))
    }

def score_type3(llm_output: List[str], ground_truth: List[str]) -> Dict:
    """
    Score Type 3 (Extraneous Code) detection.
    Simple set comparison of file paths.
    """
    found = set(llm_output)
    expected = set(ground_truth)
    
    true_positives = found & expected
    false_positives = found - expected
    false_negatives = expected - found
    
    precision = len(true_positives) / len(found) if found else 0
    recall = len(true_positives) / len(expected) if expected else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "true_positives": list(true_positives),
        "false_positives": list(false_positives),
        "false_negatives": list(false_negatives),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "score": len(true_positives) - (0.25 * len(false_positives))
    }

def score_results(llm_output_path: Path, ground_truth_path: Path) -> Dict:
    """Score LLM output against ground truth."""
    
    llm_output = load_json(llm_output_path)
    ground_truth = load_json(ground_truth_path)
    
    # Determine test type from analysis_type field
    analysis_type = llm_output.get("analysis_type", "unknown")
    
    results = {
        "test_file": str(llm_output_path),
        "analysis_type": analysis_type
    }
    
    if analysis_type == "type1_missing":
        results["type1"] = score_type1(
            llm_output.get("type1_missing", []),
            ground_truth.get("type1_missing", [])
        )
    
    elif analysis_type == "type2_incorrect":
        results["type2"] = score_type2(
            llm_output.get("type2_incorrect", []),
            ground_truth.get("type2_incorrect", [])
        )
    
    elif analysis_type == "type3_extraneous":
        results["type3"] = score_type3(
            llm_output.get("type3_extraneous", []),
            ground_truth.get("type3_extraneous", [])
        )
    
    elif analysis_type == "combined_all_types":
        results["type1"] = score_type1(
            llm_output.get("type1_missing", []),
            ground_truth.get("type1_missing", [])
        )
        results["type2"] = score_type2(
            llm_output.get("type2_incorrect", []),
            ground_truth.get("type2_incorrect", [])
        )
        results["type3"] = score_type3(
            llm_output.get("type3_extraneous", []),
            ground_truth.get("type3_extraneous", [])
        )
        
        # Calculate combined score
        total_score = (results["type1"]["score"] + 
                      results["type2"]["score"] + 
                      results["type3"]["score"])
        results["combined_score"] = round(total_score, 2)
    
    return results

def print_results(results: Dict):
    """Print scoring results in a readable format."""
    
    print("\n" + "="*60)
    print(f"SCORING RESULTS: {results['analysis_type']}")
    print("="*60)
    
    for type_name in ["type1", "type2", "type3"]:
        if type_name in results:
            print(f"\n{type_name.upper()} Results:")
            type_results = results[type_name]
            
            print(f"  Precision: {type_results['precision']:.1%}")
            print(f"  Recall:    {type_results['recall']:.1%}")
            print(f"  F1 Score:  {type_results['f1']:.3f}")
            print(f"  Score:     {type_results['score']:.2f}")
            
            if type_results['true_positives']:
                print(f"  ✓ Found correctly: {len(type_results['true_positives'])}")
            if type_results['false_positives']:
                print(f"  ✗ False positives: {len(type_results['false_positives'])}")
            if type_results['false_negatives']:
                print(f"  ✗ Missed: {len(type_results['false_negatives'])}")
    
    if "combined_score" in results:
        print(f"\n{'='*60}")
        print(f"COMBINED SCORE: {results['combined_score']:.2f}")
        print("="*60)

def main():
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage: python score.py <llm_output.json> <ground_truth.json>")
        sys.exit(1)
    
    llm_output_path = Path(sys.argv[1])
    ground_truth_path = Path(sys.argv[2])
    
    if not llm_output_path.exists():
        print(f"Error: LLM output file not found: {llm_output_path}")
        sys.exit(1)
    
    if not ground_truth_path.exists():
        print(f"Error: Ground truth file not found: {ground_truth_path}")
        sys.exit(1)
    
    try:
        results = score_results(llm_output_path, ground_truth_path)
        print_results(results)
        
        # Save results to file
        output_file = llm_output_path.parent / f"scored_{llm_output_path.stem}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error scoring results: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
