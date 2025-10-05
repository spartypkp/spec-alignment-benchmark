#!/usr/bin/env python3
"""
Aggregate scored results across multiple runs for statistical analysis.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import statistics
import argparse
from datetime import datetime

def load_scored_results(directory: Path) -> List[Dict]:
    """Load all scored results from a directory."""
    results = []
    for file in directory.glob("*_scored.json"):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                results.append(data)
        except Exception as e:
            print(f"Warning: Could not load {file}: {e}")
    return results

def group_by_test_type(results: List[Dict]) -> Dict[str, List[Dict]]:
    """Group results by test type."""
    grouped = {}
    for result in results:
        test_type = result['metadata']['test_type']
        if test_type not in grouped:
            grouped[test_type] = []
        grouped[test_type].append(result)
    return grouped

def calculate_statistics(scores: List[float]) -> Dict[str, float]:
    """Calculate descriptive statistics for a set of scores."""
    if not scores:
        return {
            "mean": 0,
            "std": 0,
            "min": 0,
            "max": 0,
            "median": 0,
            "count": 0
        }
    
    return {
        "mean": statistics.mean(scores),
        "std": statistics.stdev(scores) if len(scores) > 1 else 0,
        "min": min(scores),
        "max": max(scores),
        "median": statistics.median(scores),
        "count": len(scores)
    }

def aggregate_type_results(results: List[Dict]) -> Dict[str, Any]:
    """Aggregate results for a single test type."""
    # Extract metrics across runs
    precisions = []
    recalls = []
    f1_scores = []
    points = []
    true_positives = []
    false_positives = []
    false_negatives = []
    
    for result in results:
        scores = result['scores']
        
        # Handle combined vs single type scoring
        if 'combined' in scores:
            # For combined tests, use averaged metrics
            precisions.append(scores['combined']['avg_precision'])
            recalls.append(scores['combined']['avg_recall'])
            f1_scores.append(scores['combined']['avg_f1'])
            points.append(scores['combined']['total_points'])
            
            # Sum up detection counts across types
            tp_count = 0
            fp_count = 0
            fn_count = 0
            for type_key in ['type1', 'type2', 'type3']:
                if type_key in scores:
                    tp_count += len(scores[type_key]['true_positives'])
                    fp_count += len(scores[type_key]['false_positives'])
                    fn_count += len(scores[type_key]['false_negatives'])
            
            true_positives.append(tp_count)
            false_positives.append(fp_count)
            false_negatives.append(fn_count)
        else:
            # Single type test
            precisions.append(scores['precision'])
            recalls.append(scores['recall'])
            f1_scores.append(scores['f1_score'])
            points.append(scores['points'])
            true_positives.append(len(scores['true_positives']))
            false_positives.append(len(scores['false_positives']))
            false_negatives.append(len(scores['false_negatives']))
    
    return {
        "run_count": len(results),
        "metrics": {
            "precision": calculate_statistics(precisions),
            "recall": calculate_statistics(recalls),
            "f1_score": calculate_statistics(f1_scores),
            "points": calculate_statistics(points)
        },
        "detection_counts": {
            "true_positives": calculate_statistics(true_positives),
            "false_positives": calculate_statistics(false_positives),
            "false_negatives": calculate_statistics(false_negatives)
        }
    }

def aggregate_branch_results(framework: str, branch: str, results_dir: Path) -> Dict[str, Any]:
    """Aggregate all results for a specific framework and branch."""
    branch_dir = results_dir / "processed" / framework / branch
    
    if not branch_dir.exists():
        return {
            "error": f"No results found for {framework}/{branch}"
        }
    
    # Load all scored results
    results = load_scored_results(branch_dir)
    
    if not results:
        return {
            "error": f"No scored results found in {branch_dir}"
        }
    
    # Group by test type
    grouped = group_by_test_type(results)
    
    # Aggregate each test type
    aggregated = {
        "framework": framework,
        "branch": branch,
        "total_runs": len(results),
        "test_types": {}
    }
    
    for test_type, type_results in grouped.items():
        aggregated["test_types"][test_type] = aggregate_type_results(type_results)
    
    # Calculate overall metrics across all test types
    all_f1_scores = []
    all_points = []
    
    for test_type, type_data in aggregated["test_types"].items():
        all_f1_scores.extend([
            type_data["metrics"]["f1_score"]["mean"]
            for _ in range(type_data["run_count"])
        ])
        all_points.extend([
            type_data["metrics"]["points"]["mean"]
            for _ in range(type_data["run_count"])
        ])
    
    aggregated["overall"] = {
        "avg_f1_score": statistics.mean(all_f1_scores) if all_f1_scores else 0,
        "avg_points": statistics.mean(all_points) if all_points else 0,
        "total_test_runs": len(results)
    }
    
    return aggregated

def save_aggregated_results(data: Dict, output_path: Path):
    """Save aggregated results to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add metadata
    data["metadata"] = {
        "aggregated_at": datetime.now().isoformat(),
        "version": "1.0.0"
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved aggregated results to {output_path}")

def print_summary(data: Dict):
    """Print a human-readable summary of aggregated results."""
    print("\n" + "="*70)
    print(f"AGGREGATION SUMMARY: {data['framework'].upper()} - {data['branch']}")
    print("="*70)
    
    print(f"\nTotal test runs: {data['total_runs']}")
    
    for test_type, type_data in data['test_types'].items():
        print(f"\n{test_type.upper()} ({type_data['run_count']} runs)")
        print("-" * 40)
        
        metrics = type_data['metrics']
        print(f"  F1 Score: {metrics['f1_score']['mean']:.3f} ± {metrics['f1_score']['std']:.3f}")
        print(f"  Precision: {metrics['precision']['mean']:.1%} ± {metrics['precision']['std']:.1%}")
        print(f"  Recall: {metrics['recall']['mean']:.1%} ± {metrics['recall']['std']:.1%}")
        print(f"  Points: {metrics['points']['mean']:.2f} ± {metrics['points']['std']:.2f}")
        
        counts = type_data['detection_counts']
        print(f"  Avg Detections:")
        print(f"    True Positives: {counts['true_positives']['mean']:.1f}")
        print(f"    False Positives: {counts['false_positives']['mean']:.1f}")
        print(f"    False Negatives: {counts['false_negatives']['mean']:.1f}")
    
    if 'overall' in data:
        print(f"\nOVERALL PERFORMANCE")
        print("-" * 40)
        print(f"  Average F1 Score: {data['overall']['avg_f1_score']:.3f}")
        print(f"  Average Points: {data['overall']['avg_points']:.2f}")

def main():
    parser = argparse.ArgumentParser(
        description="Aggregate scored results for statistical analysis"
    )
    parser.add_argument(
        "--framework",
        required=True,
        choices=["cursor", "claude-code"],
        help="Framework to analyze"
    )
    parser.add_argument(
        "--branch",
        required=True,
        choices=[
            "control_perfect", "baseline_balanced", "type1_heavy",
            "type2_heavy", "subtle_only", "distributed"
        ],
        help="Test branch to analyze"
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results"),
        help="Base results directory (default: results)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: auto-generated)"
    )
    
    args = parser.parse_args()
    
    # Aggregate results
    aggregated = aggregate_branch_results(
        args.framework,
        args.branch,
        args.results_dir
    )
    
    # Check for errors
    if "error" in aggregated:
        print(f"Error: {aggregated['error']}")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = (
            args.results_dir / "analysis" / args.framework / 
            args.branch / f"{args.branch}_summary.json"
        )
    
    # Save results
    save_aggregated_results(aggregated, output_path)
    
    # Print summary
    print_summary(aggregated)

if __name__ == "__main__":
    main()
