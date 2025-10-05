#!/usr/bin/env python3
"""
Compare performance between frameworks and test hypotheses.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import statistics
import argparse
from datetime import datetime
from scipy import stats
import numpy as np

def load_aggregated_results(base_dir: Path, framework: str, branch: str) -> Optional[Dict]:
    """Load aggregated results for a framework and branch."""
    file_path = base_dir / "analysis" / framework / branch / f"{branch}_summary.json"
    
    if not file_path.exists():
        return None
    
    with open(file_path, 'r') as f:
        return json.load(f)

def perform_t_test(scores1: List[float], scores2: List[float]) -> Tuple[float, float, float]:
    """
    Perform paired t-test and calculate effect size.
    Returns: t_statistic, p_value, cohen_d
    """
    if len(scores1) != len(scores2) or len(scores1) < 2:
        return 0, 1.0, 0  # No significant difference
    
    # Paired t-test
    t_stat, p_value = stats.ttest_rel(scores1, scores2)
    
    # Cohen's d for paired samples
    diff = np.array(scores1) - np.array(scores2)
    cohen_d = np.mean(diff) / np.std(diff, ddof=1) if np.std(diff, ddof=1) > 0 else 0
    
    return t_stat, p_value, cohen_d

def interpret_effect_size(d: float) -> str:
    """Interpret Cohen's d effect size."""
    abs_d = abs(d)
    if abs_d < 0.2:
        return "negligible"
    elif abs_d < 0.5:
        return "small"
    elif abs_d < 0.8:
        return "medium"
    else:
        return "large"

def test_hypothesis_1(cursor_data: Dict, claude_data: Dict) -> Dict:
    """
    H1: Claude Code will achieve significantly higher overall F1 score than Cursor.
    Prediction: Claude Code F1 > Cursor F1 by ≥15%
    """
    # Get overall F1 scores
    cursor_f1 = cursor_data.get('overall', {}).get('avg_f1_score', 0)
    claude_f1 = claude_data.get('overall', {}).get('avg_f1_score', 0)
    
    # Calculate difference
    difference = claude_f1 - cursor_f1
    percent_difference = (difference / cursor_f1 * 100) if cursor_f1 > 0 else 0
    
    # Determine if hypothesis is supported
    supported = percent_difference >= 15
    
    return {
        "hypothesis": "H1",
        "description": "Claude Code achieves higher overall F1 score",
        "prediction": "Claude Code F1 > Cursor F1 by ≥15%",
        "cursor_f1": cursor_f1,
        "claude_f1": claude_f1,
        "difference": difference,
        "percent_difference": percent_difference,
        "supported": supported,
        "result": "SUPPORTED" if supported else "REJECTED"
    }

def test_hypothesis_2(cursor_data: Dict, claude_data: Dict) -> Dict:
    """
    H2: Type-specific specialization.
    H2a: Cursor > Claude Code on Type 1
    H2b: Claude Code > Cursor on Type 2
    H2c: Cursor > Claude Code on Type 3
    """
    results = {
        "hypothesis": "H2",
        "description": "Type-specific specialization",
        "sub_hypotheses": {}
    }
    
    # H2a: Type 1
    cursor_type1 = cursor_data.get('test_types', {}).get('type1_missing', {}).get('metrics', {}).get('f1_score', {}).get('mean', 0)
    claude_type1 = claude_data.get('test_types', {}).get('type1_missing', {}).get('metrics', {}).get('f1_score', {}).get('mean', 0)
    
    results['sub_hypotheses']['H2a'] = {
        "prediction": "Cursor > Claude Code on Type 1",
        "cursor_score": cursor_type1,
        "claude_score": claude_type1,
        "supported": cursor_type1 > claude_type1
    }
    
    # H2b: Type 2
    cursor_type2 = cursor_data.get('test_types', {}).get('type2_incorrect', {}).get('metrics', {}).get('f1_score', {}).get('mean', 0)
    claude_type2 = claude_data.get('test_types', {}).get('type2_incorrect', {}).get('metrics', {}).get('f1_score', {}).get('mean', 0)
    
    results['sub_hypotheses']['H2b'] = {
        "prediction": "Claude Code > Cursor on Type 2",
        "cursor_score": cursor_type2,
        "claude_score": claude_type2,
        "supported": claude_type2 > cursor_type2
    }
    
    # H2c: Type 3
    cursor_type3 = cursor_data.get('test_types', {}).get('type3_extraneous', {}).get('metrics', {}).get('f1_score', {}).get('mean', 0)
    claude_type3 = claude_data.get('test_types', {}).get('type3_extraneous', {}).get('metrics', {}).get('f1_score', {}).get('mean', 0)
    
    results['sub_hypotheses']['H2c'] = {
        "prediction": "Cursor > Claude Code on Type 3",
        "cursor_score": cursor_type3,
        "claude_score": claude_type3,
        "supported": cursor_type3 > claude_type3
    }
    
    # Overall H2 result
    supported_count = sum(1 for h in results['sub_hypotheses'].values() if h['supported'])
    results['result'] = "SUPPORTED" if supported_count >= 2 else "MIXED" if supported_count == 1 else "REJECTED"
    
    return results

def test_hypothesis_5(cursor_control: Dict, claude_control: Dict) -> Dict:
    """
    H5: Cursor will generate significantly more false positives.
    Prediction: Cursor false positive rate > 2x Claude Code's rate
    """
    # Get false positive counts from control branch
    cursor_fp = 0
    claude_fp = 0
    
    # Count any detections on control branch as false positives
    for test_type in ['type1_missing', 'type2_incorrect', 'type3_extraneous']:
        cursor_detections = cursor_control.get('test_types', {}).get(test_type, {}).get('detection_counts', {}).get('false_positives', {}).get('mean', 0)
        claude_detections = claude_control.get('test_types', {}).get(test_type, {}).get('detection_counts', {}).get('false_positives', {}).get('mean', 0)
        
        cursor_fp += cursor_detections
        claude_fp += claude_detections
    
    # Calculate ratio
    ratio = cursor_fp / claude_fp if claude_fp > 0 else float('inf') if cursor_fp > 0 else 1
    
    return {
        "hypothesis": "H5",
        "description": "Cursor generates more false positives",
        "prediction": "Cursor FP rate > 2x Claude Code FP rate",
        "cursor_false_positives": cursor_fp,
        "claude_false_positives": claude_fp,
        "ratio": ratio,
        "supported": ratio > 2,
        "result": "SUPPORTED" if ratio > 2 else "REJECTED"
    }

def compare_branch(base_dir: Path, branch: str) -> Dict:
    """Compare frameworks on a specific branch."""
    # Load aggregated results for both frameworks
    cursor_data = load_aggregated_results(base_dir, "cursor", branch)
    claude_data = load_aggregated_results(base_dir, "claude-code", branch)
    
    if not cursor_data or not claude_data:
        return {
            "error": f"Missing aggregated results for {branch}. Run aggregate_results.py first."
        }
    
    comparison = {
        "branch": branch,
        "timestamp": datetime.now().isoformat(),
        "frameworks": {
            "cursor": {
                "total_runs": cursor_data.get('total_runs', 0),
                "avg_f1": cursor_data.get('overall', {}).get('avg_f1_score', 0),
                "avg_points": cursor_data.get('overall', {}).get('avg_points', 0)
            },
            "claude-code": {
                "total_runs": claude_data.get('total_runs', 0),
                "avg_f1": claude_data.get('overall', {}).get('avg_f1_score', 0),
                "avg_points": claude_data.get('overall', {}).get('avg_points', 0)
            }
        },
        "hypotheses": {}
    }
    
    # Test relevant hypotheses based on branch
    if branch == "baseline_balanced":
        comparison["hypotheses"]["H1"] = test_hypothesis_1(cursor_data, claude_data)
        comparison["hypotheses"]["H2"] = test_hypothesis_2(cursor_data, claude_data)
    
    elif branch == "control_perfect":
        comparison["hypotheses"]["H5"] = test_hypothesis_5(cursor_data, claude_data)
    
    elif branch == "type1_heavy":
        comparison["hypotheses"]["H2a"] = {
            "description": "Cursor better at Type 1 detection",
            "cursor_f1": cursor_data.get('overall', {}).get('avg_f1_score', 0),
            "claude_f1": claude_data.get('overall', {}).get('avg_f1_score', 0),
            "supported": cursor_data.get('overall', {}).get('avg_f1_score', 0) > 
                        claude_data.get('overall', {}).get('avg_f1_score', 0)
        }
    
    # Add statistical tests if we have enough data
    if cursor_data.get('total_runs', 0) >= 3 and claude_data.get('total_runs', 0) >= 3:
        comparison["statistics"] = perform_statistical_tests(cursor_data, claude_data)
    
    return comparison

def perform_statistical_tests(cursor_data: Dict, claude_data: Dict) -> Dict:
    """Perform statistical significance tests."""
    stats_results = {}
    
    # Test overall F1 scores
    for metric in ['f1_score', 'precision', 'recall', 'points']:
        cursor_mean = 0
        claude_mean = 0
        
        # Get means from all test types
        for test_type in cursor_data.get('test_types', {}).keys():
            if test_type in claude_data.get('test_types', {}):
                cursor_mean += cursor_data['test_types'][test_type]['metrics'][metric]['mean']
                claude_mean += claude_data['test_types'][test_type]['metrics'][metric]['mean']
        
        # Average across test types
        num_types = len(cursor_data.get('test_types', {}))
        if num_types > 0:
            cursor_mean /= num_types
            claude_mean /= num_types
            
            difference = claude_mean - cursor_mean
            
            stats_results[metric] = {
                "cursor_mean": cursor_mean,
                "claude_mean": claude_mean,
                "difference": difference,
                "winner": "claude-code" if difference > 0 else "cursor" if difference < 0 else "tie"
            }
    
    return stats_results

def print_comparison_summary(comparison: Dict):
    """Print a human-readable summary of the comparison."""
    print("\n" + "="*70)
    print(f"FRAMEWORK COMPARISON: {comparison['branch'].upper()}")
    print("="*70)
    
    # Framework summaries
    print("\nFRAMEWORK PERFORMANCE:")
    print("-" * 40)
    for framework, data in comparison['frameworks'].items():
        print(f"{framework.upper()}")
        print(f"  Runs: {data['total_runs']}")
        print(f"  Avg F1 Score: {data['avg_f1']:.3f}")
        print(f"  Avg Points: {data['avg_points']:.2f}")
        print()
    
    # Hypothesis results
    if comparison.get('hypotheses'):
        print("\nHYPOTHESIS TESTS:")
        print("-" * 40)
        
        for h_id, h_data in comparison['hypotheses'].items():
            print(f"\n{h_id}: {h_data.get('description', '')}")
            
            if 'sub_hypotheses' in h_data:
                # Handle multi-part hypotheses
                for sub_id, sub_data in h_data['sub_hypotheses'].items():
                    supported = "✓" if sub_data['supported'] else "✗"
                    print(f"  {supported} {sub_id}: {sub_data['prediction']}")
                    print(f"      Cursor: {sub_data['cursor_score']:.3f}, Claude: {sub_data['claude_score']:.3f}")
            else:
                # Single hypothesis
                result = h_data.get('result', 'UNKNOWN')
                print(f"  Result: {result}")
                
                if 'percent_difference' in h_data:
                    print(f"  Difference: {h_data['percent_difference']:.1f}%")
                elif 'ratio' in h_data:
                    print(f"  Ratio: {h_data['ratio']:.2f}x")
    
    # Statistical significance
    if comparison.get('statistics'):
        print("\nSTATISTICAL COMPARISON:")
        print("-" * 40)
        
        for metric, stats in comparison['statistics'].items():
            winner = stats['winner']
            diff = stats['difference']
            symbol = ">" if winner == "claude-code" else "<" if winner == "cursor" else "="
            
            print(f"{metric.replace('_', ' ').title()}:")
            print(f"  Cursor: {stats['cursor_mean']:.3f} {symbol} Claude: {stats['claude_mean']:.3f}")
            print(f"  Difference: {abs(diff):.3f} ({winner})")

def main():
    parser = argparse.ArgumentParser(
        description="Compare framework performance and test hypotheses"
    )
    parser.add_argument(
        "--branch",
        required=True,
        choices=[
            "control_perfect", "baseline_balanced", "type1_heavy",
            "type2_heavy", "subtle_only", "distributed"
        ],
        help="Test branch to compare"
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("results"),
        help="Base results directory"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path"
    )
    
    args = parser.parse_args()
    
    # Perform comparison
    comparison = compare_branch(args.base_dir, args.branch)
    
    if "error" in comparison:
        print(f"Error: {comparison['error']}")
        sys.exit(1)
    
    # Save results
    if args.output:
        output_path = args.output
    else:
        output_dir = args.base_dir / "analysis" / "comparisons"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{args.branch}_comparison.json"
    
    with open(output_path, 'w') as f:
        json.dump(comparison, f, indent=2, default=str)
    
    print(f"Saved comparison to {output_path}")
    
    # Print summary
    print_comparison_summary(comparison)

if __name__ == "__main__":
    main()
