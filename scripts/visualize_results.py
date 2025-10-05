#!/usr/bin/env python3
"""
Generate visualizations for benchmark results.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
import argparse
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def load_comparison_data(base_dir: Path) -> Dict[str, Dict]:
    """Load all comparison data."""
    comparisons_dir = base_dir / "analysis" / "comparisons"
    data = {}
    
    if comparisons_dir.exists():
        for file in comparisons_dir.glob("*_comparison.json"):
            branch = file.stem.replace("_comparison", "")
            with open(file, 'r') as f:
                data[branch] = json.load(f)
    
    return data

def create_overall_comparison_chart(data: Dict[str, Dict], output_dir: Path):
    """Create bar chart comparing overall F1 scores across branches."""
    branches = []
    cursor_scores = []
    claude_scores = []
    
    # Extract data
    for branch in ['control_perfect', 'baseline_balanced', 'type1_heavy', 
                   'type2_heavy', 'subtle_only', 'distributed']:
        if branch in data:
            branches.append(branch.replace('_', '\n'))
            cursor_scores.append(data[branch]['frameworks']['cursor']['avg_f1'])
            claude_scores.append(data[branch]['frameworks']['claude-code']['avg_f1'])
    
    if not branches:
        print("No data available for overall comparison")
        return
    
    # Create plot
    x = np.arange(len(branches))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    bars1 = ax.bar(x - width/2, cursor_scores, width, label='Cursor', 
                   color='#4A90E2', edgecolor='black', linewidth=1)
    bars2 = ax.bar(x + width/2, claude_scores, width, label='Claude Code',
                   color='#50E3C2', edgecolor='black', linewidth=1)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')
    
    # Customize plot
    ax.set_xlabel('Test Branch', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average F1 Score', fontsize=12, fontweight='bold')
    ax.set_title('Framework Performance Comparison Across Test Branches', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(branches)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)
    
    # Add horizontal line at 0.5 for reference
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Baseline')
    
    plt.tight_layout()
    output_path = output_dir / "overall_f1_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved overall comparison chart to {output_path}")

def create_type_specific_chart(data: Dict[str, Dict], output_dir: Path):
    """Create grouped bar chart for type-specific performance."""
    # Focus on baseline_balanced for type comparison
    if 'baseline_balanced' not in data:
        print("No baseline_balanced data for type-specific comparison")
        return
    
    branch_data = data['baseline_balanced']
    
    # Extract hypothesis H2 data if available
    if 'hypotheses' not in branch_data or 'H2' not in branch_data['hypotheses']:
        print("No H2 hypothesis data available")
        return
    
    h2_data = branch_data['hypotheses']['H2']['sub_hypotheses']
    
    # Prepare data
    types = ['Type 1\n(Missing)', 'Type 2\n(Incorrect)', 'Type 3\n(Extraneous)']
    cursor_scores = [
        h2_data['H2a']['cursor_score'],
        h2_data['H2b']['cursor_score'],
        h2_data['H2c']['cursor_score']
    ]
    claude_scores = [
        h2_data['H2a']['claude_score'],
        h2_data['H2b']['claude_score'],
        h2_data['H2c']['claude_score']
    ]
    
    # Create plot
    x = np.arange(len(types))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    bars1 = ax.bar(x - width/2, cursor_scores, width, label='Cursor',
                   color='#4A90E2', edgecolor='black', linewidth=1)
    bars2 = ax.bar(x + width/2, claude_scores, width, label='Claude Code',
                   color='#50E3C2', edgecolor='black', linewidth=1)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')
    
    # Mark winners with asterisks
    for i, (c_score, cl_score) in enumerate(zip(cursor_scores, claude_scores)):
        if c_score > cl_score:
            ax.text(i - width/2, c_score + 0.02, '*', ha='center', fontsize=16, color='gold')
        elif cl_score > c_score:
            ax.text(i + width/2, cl_score + 0.02, '*', ha='center', fontsize=16, color='gold')
    
    # Customize plot
    ax.set_xlabel('Misalignment Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('F1 Score', fontsize=12, fontweight='bold')
    ax.set_title('Type-Specific Detection Performance (Baseline Balanced)',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(types)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = output_dir / "type_specific_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved type-specific chart to {output_path}")

def create_hypothesis_summary_chart(data: Dict[str, Dict], output_dir: Path):
    """Create visualization of hypothesis test results."""
    hypotheses_results = {
        'H1': {'description': 'Overall Performance', 'result': None},
        'H2a': {'description': 'Type 1 Detection', 'result': None},
        'H2b': {'description': 'Type 2 Detection', 'result': None},
        'H2c': {'description': 'Type 3 Detection', 'result': None},
        'H5': {'description': 'False Positive Rate', 'result': None}
    }
    
    # Collect hypothesis results
    for branch, branch_data in data.items():
        if 'hypotheses' in branch_data:
            for h_id, h_data in branch_data['hypotheses'].items():
                if h_id == 'H1':
                    hypotheses_results['H1']['result'] = h_data.get('result')
                elif h_id == 'H2':
                    for sub_id, sub_data in h_data.get('sub_hypotheses', {}).items():
                        if sub_id in hypotheses_results:
                            hypotheses_results[sub_id]['result'] = 'SUPPORTED' if sub_data['supported'] else 'REJECTED'
                elif h_id == 'H5':
                    hypotheses_results['H5']['result'] = h_data.get('result')
    
    # Filter out null results
    valid_hypotheses = {k: v for k, v in hypotheses_results.items() if v['result'] is not None}
    
    if not valid_hypotheses:
        print("No hypothesis results to visualize")
        return
    
    # Prepare data for visualization
    labels = []
    colors = []
    results = []
    
    for h_id, h_data in valid_hypotheses.items():
        labels.append(f"{h_id}\n{h_data['description']}")
        result = h_data['result']
        results.append(result)
        
        if result == 'SUPPORTED':
            colors.append('#4CAF50')  # Green
        elif result == 'REJECTED':
            colors.append('#F44336')  # Red
        elif result == 'MIXED':
            colors.append('#FFC107')  # Amber
        else:
            colors.append('#9E9E9E')  # Gray
    
    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, [1] * len(labels), color=colors, edgecolor='black', linewidth=1)
    
    # Add result text
    for i, (bar, result) in enumerate(zip(bars, results)):
        ax.text(0.5, bar.get_y() + bar.get_height()/2, result,
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    
    # Customize plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Test Result', fontsize=12, fontweight='bold')
    ax.set_title('Hypothesis Test Results Summary', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.grid(False)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4CAF50', edgecolor='black', label='Supported'),
        Patch(facecolor='#F44336', edgecolor='black', label='Rejected'),
        Patch(facecolor='#FFC107', edgecolor='black', label='Mixed'),
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    output_path = output_dir / "hypothesis_results.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved hypothesis results chart to {output_path}")

def create_performance_heatmap(base_dir: Path, output_dir: Path):
    """Create heatmap of performance across branches and test types."""
    # Collect all aggregated data
    frameworks = ['cursor', 'claude-code']
    branches = ['baseline_balanced', 'type1_heavy', 'type2_heavy', 'subtle_only', 'distributed']
    test_types = ['type1_missing', 'type2_incorrect', 'type3_extraneous', 'combined_all_types']
    
    for framework in frameworks:
        # Create matrix for heatmap
        matrix = []
        
        for branch in branches:
            row = []
            for test_type in test_types:
                # Try to load aggregated data
                summary_file = base_dir / "analysis" / framework / branch / f"{branch}_summary.json"
                if summary_file.exists():
                    with open(summary_file, 'r') as f:
                        data = json.load(f)
                        if test_type in data.get('test_types', {}):
                            f1_score = data['test_types'][test_type]['metrics']['f1_score']['mean']
                            row.append(f1_score)
                        else:
                            row.append(np.nan)
                else:
                    row.append(np.nan)
            matrix.append(row)
        
        # Skip if no data
        if all(all(np.isnan(val) for val in row) for row in matrix):
            continue
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Use masked array to handle NaN values
        matrix_array = np.ma.masked_invalid(matrix)
        
        im = ax.imshow(matrix_array, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
        
        # Set ticks
        ax.set_xticks(np.arange(len(test_types)))
        ax.set_yticks(np.arange(len(branches)))
        ax.set_xticklabels([t.replace('_', '\n') for t in test_types], fontsize=9)
        ax.set_yticklabels([b.replace('_', ' ') for b in branches], fontsize=9)
        
        # Rotate the tick labels for better fit
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('F1 Score', rotation=270, labelpad=20)
        
        # Add text annotations
        for i in range(len(branches)):
            for j in range(len(test_types)):
                if not np.isnan(matrix[i][j]):
                    text = ax.text(j, i, f'{matrix[i][j]:.2f}',
                                  ha="center", va="center", color="black" if matrix[i][j] > 0.5 else "white")
        
        ax.set_title(f'{framework.upper()} Performance Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        output_path = output_dir / f"{framework}_performance_heatmap.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved {framework} heatmap to {output_path}")

def create_summary_report(data: Dict[str, Dict], output_dir: Path):
    """Create a text summary report."""
    report_lines = []
    report_lines.append("="*70)
    report_lines.append("BENCHMARK RESULTS SUMMARY")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("="*70)
    report_lines.append("")
    
    # Overall winner determination
    cursor_wins = 0
    claude_wins = 0
    
    for branch, branch_data in data.items():
        cursor_f1 = branch_data['frameworks']['cursor']['avg_f1']
        claude_f1 = branch_data['frameworks']['claude-code']['avg_f1']
        
        if cursor_f1 > claude_f1:
            cursor_wins += 1
        elif claude_f1 > cursor_f1:
            claude_wins += 1
    
    report_lines.append("OVERALL RESULTS")
    report_lines.append("-"*40)
    report_lines.append(f"Branches where Cursor wins: {cursor_wins}")
    report_lines.append(f"Branches where Claude Code wins: {claude_wins}")
    
    if cursor_wins > claude_wins:
        report_lines.append("Overall Winner: CURSOR")
    elif claude_wins > cursor_wins:
        report_lines.append("Overall Winner: CLAUDE CODE")
    else:
        report_lines.append("Overall Winner: TIE")
    
    report_lines.append("")
    
    # Branch-by-branch results
    report_lines.append("BRANCH-BY-BRANCH RESULTS")
    report_lines.append("-"*40)
    
    for branch in ['control_perfect', 'baseline_balanced', 'type1_heavy', 
                   'type2_heavy', 'subtle_only', 'distributed']:
        if branch in data:
            branch_data = data[branch]
            cursor_f1 = branch_data['frameworks']['cursor']['avg_f1']
            claude_f1 = branch_data['frameworks']['claude-code']['avg_f1']
            diff = claude_f1 - cursor_f1
            
            report_lines.append(f"\n{branch.upper()}")
            report_lines.append(f"  Cursor F1: {cursor_f1:.3f}")
            report_lines.append(f"  Claude F1: {claude_f1:.3f}")
            report_lines.append(f"  Difference: {diff:+.3f} ({'Claude' if diff > 0 else 'Cursor'} better)")
    
    report_lines.append("")
    
    # Hypothesis test results
    report_lines.append("HYPOTHESIS TEST RESULTS")
    report_lines.append("-"*40)
    
    hypothesis_summary = {}
    for branch, branch_data in data.items():
        if 'hypotheses' in branch_data:
            for h_id, h_data in branch_data['hypotheses'].items():
                if h_id not in hypothesis_summary:
                    hypothesis_summary[h_id] = h_data
    
    for h_id, h_data in hypothesis_summary.items():
        report_lines.append(f"\n{h_id}: {h_data.get('description', '')}")
        report_lines.append(f"  Result: {h_data.get('result', 'UNKNOWN')}")
        
        if 'percent_difference' in h_data:
            report_lines.append(f"  Observed difference: {h_data['percent_difference']:.1f}%")
        elif 'ratio' in h_data:
            report_lines.append(f"  Observed ratio: {h_data['ratio']:.2f}x")
    
    # Save report
    report_path = output_dir / "summary_report.txt"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Saved summary report to {report_path}")
    
    # Also print to console
    print('\n'.join(report_lines))

def main():
    parser = argparse.ArgumentParser(
        description="Generate visualizations for benchmark results"
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("results"),
        help="Base results directory"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for visualizations"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all visualizations"
    )
    parser.add_argument(
        "--overall",
        action="store_true",
        help="Generate overall comparison chart"
    )
    parser.add_argument(
        "--types",
        action="store_true",
        help="Generate type-specific comparison"
    )
    parser.add_argument(
        "--hypotheses",
        action="store_true",
        help="Generate hypothesis results chart"
    )
    parser.add_argument(
        "--heatmap",
        action="store_true",
        help="Generate performance heatmaps"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate text summary report"
    )
    
    args = parser.parse_args()
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = args.base_dir / "analysis" / "comparisons" / "visualizations"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load comparison data
    data = load_comparison_data(args.base_dir)
    
    if not data:
        print("No comparison data found. Run compare_frameworks.py first.")
        sys.exit(1)
    
    # Generate requested visualizations
    if args.all or args.overall:
        create_overall_comparison_chart(data, output_dir)
    
    if args.all or args.types:
        create_type_specific_chart(data, output_dir)
    
    if args.all or args.hypotheses:
        create_hypothesis_summary_chart(data, output_dir)
    
    if args.all or args.heatmap:
        create_performance_heatmap(args.base_dir, output_dir)
    
    if args.all or args.report:
        create_summary_report(data, output_dir)
    
    if not any([args.all, args.overall, args.types, args.hypotheses, args.heatmap, args.report]):
        print("No visualization type specified. Use --all or specific flags.")
        parser.print_help()

if __name__ == "__main__":
    main()
