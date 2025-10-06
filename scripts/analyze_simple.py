#!/usr/bin/env python3
"""
Simple, focused analyzer for Cursor benchmark results.
Produces ONE clear PDF with meaningful metrics and insights.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import statistics
from datetime import datetime
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
import numpy as np


def load_json(filepath: Path) -> Dict:
    """Load JSON safely."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}


def normalize_output(raw_output: Dict, test_type: str) -> Dict:
    """Normalize Cursor's output format."""
    if 'type1_missing' in raw_output:
        return raw_output
    
    normalized = {'type1_missing': [], 'type2_incorrect': [], 'type3_extraneous': []}
    
    if 'misalignments' in raw_output:
        misalignments = raw_output['misalignments']
        
        if test_type == 'type1':
            normalized['type1_missing'] = [
                item.get('section', '') for item in misalignments if 'section' in item
            ]
        elif test_type == 'type2':
            normalized['type2_incorrect'] = misalignments
        elif test_type == 'type3':
            normalized['type3_extraneous'] = [
                item.get('file', '') for item in misalignments if 'file' in item
            ]
    
    return normalized


def calculate_metrics(detected: List, expected: List) -> Dict:
    """Calculate precision, recall, F1, and confusion matrix values."""
    if not detected and not expected:
        return {'precision': 1.0, 'recall': 1.0, 'f1': 1.0, 'tp': 0, 'fp': 0, 'fn': 0}
    
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


def analyze_all():
    """Analyze all test results and return comprehensive data."""
    branches = ['control_perfect', 'baseline_balanced', 'type1_heavy', 
                'type2_heavy', 'subtle_only', 'distributed']
    
    # Store all metrics
    all_metrics = {
        'type1': {'precision': [], 'recall': [], 'f1': [], 'tp': 0, 'fp': 0, 'fn': 0},
        'type2': {'precision': [], 'recall': [], 'f1': [], 'tp': 0, 'fp': 0, 'fn': 0},
        'type3': {'precision': [], 'recall': [], 'f1': [], 'tp': 0, 'fp': 0, 'fn': 0}
    }
    
    branch_metrics = {branch: {'precision': [], 'recall': [], 'f1': []} for branch in branches}
    branch_type_metrics = {branch: {'type1': [], 'type2': [], 'type3': []} for branch in branches}
    
    # Track what's consistently missed
    missed_items = defaultdict(lambda: defaultdict(int))
    false_positive_items = defaultdict(lambda: defaultdict(int))
    
    for branch in branches:
        base_path = Path(f"results/raw/cursor/{branch}")
        ground_truth_base = Path(f"benchmark/branches/{branch}")
        
        if not base_path.exists():
            continue
        
        for test_type in ['type1', 'type2', 'type3']:
            test_dir = base_path / test_type
            gt_file = ground_truth_base / f"ground-truth-{test_type}.json"
            
            if not test_dir.exists() or not gt_file.exists():
                continue
            
            ground_truth = load_json(gt_file)
            
            for run_file in sorted(test_dir.glob("run*.json")):
                raw_data = load_json(run_file)
                if not raw_data or not ground_truth:
                    continue
                
                normalized = normalize_output(raw_data, test_type)
                
                # Get detected and expected based on type
                if test_type == 'type1':
                    detected = normalized['type1_missing']
                    expected = ground_truth.get('expected_sections', [])
                elif test_type == 'type2':
                    detected = [item.get('section', '') for item in normalized['type2_incorrect']]
                    expected = ground_truth.get('expected_sections', [])
                elif test_type == 'type3':
                    detected = normalized['type3_extraneous']
                    expected = ground_truth.get('expected_files', [])
                
                metrics = calculate_metrics(detected, expected)
                
                # Store metrics
                all_metrics[test_type]['precision'].append(metrics['precision'])
                all_metrics[test_type]['recall'].append(metrics['recall'])
                all_metrics[test_type]['f1'].append(metrics['f1'])
                all_metrics[test_type]['tp'] += metrics['tp']
                all_metrics[test_type]['fp'] += metrics['fp']
                all_metrics[test_type]['fn'] += metrics['fn']
                
                branch_metrics[branch]['precision'].append(metrics['precision'])
                branch_metrics[branch]['recall'].append(metrics['recall'])
                branch_metrics[branch]['f1'].append(metrics['f1'])
                
                branch_type_metrics[branch][test_type].append(metrics['f1'])
                
                # Track missed items
                detected_set = set(detected) if isinstance(detected, list) else set()
                expected_set = set(expected)
                for item in (expected_set - detected_set):
                    missed_items[test_type][item] += 1
                for item in (detected_set - expected_set):
                    false_positive_items[test_type][item] += 1
    
    return all_metrics, branch_metrics, branch_type_metrics, missed_items, false_positive_items


def create_pdf_report(output_path: str = "cursor_analysis.pdf"):
    """Create a focused PDF report with meaningful metrics."""
    
    print("Analyzing results...")
    all_metrics, branch_metrics, branch_type_metrics, missed_items, false_positive_items = analyze_all()
    
    # Calculate overall statistics first (needed for page 1)
    overall_precision = statistics.mean([statistics.mean(all_metrics[t]['precision']) 
                                        for t in ['type1', 'type2', 'type3']])
    overall_recall = statistics.mean([statistics.mean(all_metrics[t]['recall']) 
                                     for t in ['type1', 'type2', 'type3']])
    overall_f1 = statistics.mean([statistics.mean(all_metrics[t]['f1']) 
                                  for t in ['type1', 'type2', 'type3']])
    
    print(f"Generating PDF report: {output_path}")
    
    # Set up clean matplotlib style
    plt.rcParams['font.size'] = 9
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.2
    
    with PdfPages(output_path) as pdf:
        # PAGE 1: Context and Introduction
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle('Cursor Specification Alignment Detection Analysis', fontsize=16, y=0.98)
        
        # Remove axes for text page
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        context_text = """
WHAT WE'RE TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We're testing if Cursor can detect misalignments between code and specifications.
Using the same model (Claude 3.5 Sonnet) across all tests to isolate framework capabilities.

THE THREE TYPES OF MISALIGNMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type 1 - Missing Implementation: Spec requires feature X, code doesn't have it
    Example: Spec requires JWT auth, code has no authentication

Type 2 - Incorrect Implementation: Spec requires X as A, code implements X as B  
    Example: Spec requires 15-min tokens, code has 60-min tokens

Type 3 - Extraneous Code: Code has feature Y, spec doesn't mention Y
    Example: Code has admin dashboard, spec has no admin features

TEST STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 6 test branches with different misalignment distributions
• 5 runs per test for statistical validity  
• 120 total tests (6 branches × 4 test types × 5 runs)
• Each test asks Cursor to find specific types of misalignments

TEST BRANCHES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
control_perfect:    No misalignments (tests for false positives)
baseline_balanced:  3 Type1, 3 Type2, 2 Type3 (balanced test)
type1_heavy:        6 Type1, 1 Type2, 1 Type3 (missing features focus)
type2_heavy:        1 Type1, 6 Type2, 1 Type3 (incorrect implementations focus)
subtle_only:        Subtle, hard-to-find misalignments
distributed:        Misalignments spread across many files
        """
        
        ax.text(0.1, 0.5, context_text, fontsize=9, family='monospace', 
                verticalalignment='center', transform=ax.transAxes)
        
        # Add quick summary at bottom
        summary_box = f"""
┌─────────────────────────────────────────────────────────────────────┐
│ QUICK RESULTS:  Overall F1: {overall_f1:.1%}  •  Precision: {overall_precision:.1%}  •  Recall: {overall_recall:.1%}    │
│ Best Detection: Type 3 ({statistics.mean(all_metrics['type3']['f1']):.1%})  •  Weakest: Type 1 ({statistics.mean(all_metrics['type1']['f1']):.1%})         │
└─────────────────────────────────────────────────────────────────────┘
        """
        ax.text(0.5, 0.1, summary_box, fontsize=8, family='monospace',
                ha='center', transform=ax.transAxes)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # PAGE 2: Core Performance Metrics
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle('Performance Metrics', fontsize=14, y=0.98)
        
        # Chart 1: Precision, Recall, F1 by Type
        ax1 = plt.subplot(4, 1, 1)
        types = ['Type 1\n(Missing)', 'Type 2\n(Incorrect)', 'Type 3\n(Extraneous)']
        
        precision_means = [statistics.mean(all_metrics[t]['precision']) for t in ['type1', 'type2', 'type3']]
        recall_means = [statistics.mean(all_metrics[t]['recall']) for t in ['type1', 'type2', 'type3']]
        f1_means = [statistics.mean(all_metrics[t]['f1']) for t in ['type1', 'type2', 'type3']]
        
        x = np.arange(len(types))
        width = 0.25
        
        bars1 = ax1.bar(x - width, precision_means, width, label='Precision', color='#3498db')
        bars2 = ax1.bar(x, recall_means, width, label='Recall', color='#e74c3c')
        bars3 = ax1.bar(x + width, f1_means, width, label='F1 Score', color='#2ecc71')
        
        ax1.set_ylabel('Score')
        ax1.set_title('Detection Performance by Misalignment Type')
        ax1.set_xticks(x)
        ax1.set_xticklabels(types)
        ax1.legend()
        ax1.set_ylim([0, 1])
        
        # Add value labels
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{height:.2f}', ha='center', va='bottom', fontsize=7)
        
        # Chart 2: Confusion Matrix Visualization
        ax2 = plt.subplot(4, 3, 4)
        ax3 = plt.subplot(4, 3, 5)
        ax4 = plt.subplot(4, 3, 6)
        
        for ax, t, title in [(ax2, 'type1', 'Type 1'), (ax3, 'type2', 'Type 2'), (ax4, 'type3', 'Type 3')]:
            tp = all_metrics[t]['tp']
            fp = all_metrics[t]['fp']
            fn = all_metrics[t]['fn']
            total = tp + fp + fn
            
            if total > 0:
                sizes = [tp, fp, fn]
                labels = [f'TP\n{tp}', f'FP\n{fp}', f'FN\n{fn}']
                colors = ['#2ecc71', '#e74c3c', '#95a5a6']
                explode = (0.05, 0.05, 0.05)
                
                ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                      autopct='%1.0f%%', shadow=False, startangle=90)
                ax.set_title(f'{title} Detection Breakdown')
        
        # Chart 3: Variance Analysis (Boxplot)
        ax5 = plt.subplot(4, 1, 3)
        
        type1_f1s = all_metrics['type1']['f1']
        type2_f1s = all_metrics['type2']['f1']
        type3_f1s = all_metrics['type3']['f1']
        
        bp = ax5.boxplot([type1_f1s, type2_f1s, type3_f1s],
                         labels=['Type 1', 'Type 2', 'Type 3'],
                         patch_artist=True,
                         medianprops=dict(color='red', linewidth=2))
        
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.5)
        
        ax5.set_ylabel('F1 Score')
        ax5.set_title('F1 Score Distribution Across All Runs')
        ax5.set_ylim([0, 1.05])
        
        # Add mean line
        means = [statistics.mean(type1_f1s), statistics.mean(type2_f1s), statistics.mean(type3_f1s)]
        ax5.plot(range(1, 4), means, 'D', color='darkred', markersize=6, label='Mean')
        ax5.legend()
        
        # Chart 4: Performance Consistency (Standard Deviation)
        ax6 = plt.subplot(4, 1, 4)
        
        stds = [statistics.stdev(type1_f1s) if len(type1_f1s) > 1 else 0,
                statistics.stdev(type2_f1s) if len(type2_f1s) > 1 else 0,
                statistics.stdev(type3_f1s) if len(type3_f1s) > 1 else 0]
        
        bars = ax6.bar(range(3), stds, color=['#3498db', '#e74c3c', '#2ecc71'])
        ax6.set_ylabel('Standard Deviation')
        ax6.set_title('Performance Consistency (Lower is More Consistent)')
        ax6.set_xticks(range(3))
        ax6.set_xticklabels(['Type 1', 'Type 2', 'Type 3'])
        ax6.set_ylim([0, max(stds) * 1.2 if stds else 0.5])
        
        for bar, val in zip(bars, stds):
            ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,
                    f'{val:.3f}', ha='center', va='bottom')
        
        plt.tight_layout(rect=[0, 0.02, 1, 0.96])
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # PAGE 3: Branch Analysis and Patterns
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle('Performance Patterns Across Test Branches', fontsize=14, y=0.98)
        
        # Chart 1: Branch Performance Heatmap
        ax1 = plt.subplot(3, 1, 1)
        
        branches = list(branch_type_metrics.keys())
        heatmap_data = []
        for branch in branches:
            row = []
            for t in ['type1', 'type2', 'type3']:
                scores = branch_type_metrics[branch][t]
                row.append(statistics.mean(scores) if scores else 0)
            heatmap_data.append(row)
        
        im = ax1.imshow(heatmap_data, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')
        
        ax1.set_xticks(range(3))
        ax1.set_xticklabels(['Type 1', 'Type 2', 'Type 3'])
        ax1.set_yticks(range(len(branches)))
        ax1.set_yticklabels(branches)
        ax1.set_title('F1 Score Heatmap: Branch × Type')
        
        # Add text annotations
        for i in range(len(branches)):
            for j in range(3):
                text = ax1.text(j, i, f'{heatmap_data[i][j]:.2f}',
                              ha="center", va="center", color="black", fontsize=8)
        
        plt.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
        
        # Chart 2: Precision vs Recall Scatter
        ax2 = plt.subplot(3, 1, 2)
        
        colors_map = {'control_perfect': '#8e44ad', 'baseline_balanced': '#3498db', 
                     'type1_heavy': '#e74c3c', 'type2_heavy': '#f39c12',
                     'subtle_only': '#95a5a6', 'distributed': '#34495e'}
        
        for branch in branches:
            if branch_metrics[branch]['precision'] and branch_metrics[branch]['recall']:
                avg_precision = statistics.mean(branch_metrics[branch]['precision'])
                avg_recall = statistics.mean(branch_metrics[branch]['recall'])
                ax2.scatter(avg_recall, avg_precision, s=100, alpha=0.7,
                          color=colors_map[branch], label=branch)
        
        ax2.set_xlabel('Recall (Completeness)')
        ax2.set_ylabel('Precision (Accuracy)')
        ax2.set_title('Precision-Recall Trade-off by Branch')
        ax2.set_xlim([0, 1.05])
        ax2.set_ylim([0, 1.05])
        ax2.legend(fontsize=7, loc='best')
        ax2.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=1)
        ax2.grid(True, alpha=0.3)
        
        # Chart 3: Detection Rate Over Runs
        ax3 = plt.subplot(3, 1, 3)
        
        # Show performance stability for baseline_balanced
        baseline_data = {
            'type1': branch_type_metrics.get('baseline_balanced', {}).get('type1', []),
            'type2': branch_type_metrics.get('baseline_balanced', {}).get('type2', []),
            'type3': branch_type_metrics.get('baseline_balanced', {}).get('type3', [])
        }
        
        if any(baseline_data.values()):
            runs = range(1, max(len(v) for v in baseline_data.values()) + 1)
            for t, scores in baseline_data.items():
                if scores:
                    ax3.plot(range(1, len(scores) + 1), scores, marker='o', 
                            label=t.upper(), linewidth=1.5)
        
        ax3.set_xlabel('Run Number')
        ax3.set_ylabel('F1 Score')
        ax3.set_title('Performance Consistency: Baseline Balanced Branch')
        ax3.set_ylim([0, 1.05])
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout(rect=[0, 0.02, 1, 0.96])
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # PAGE 4: Detection Patterns and Insights
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle('Detection Patterns and Common Issues', fontsize=14, y=0.98)
        
        ax = plt.subplot(1, 1, 1)
        ax.axis('off')
        
        # Most commonly missed items
        top_missed_type1 = sorted(missed_items['type1'].items(), key=lambda x: x[1], reverse=True)[:3]
        top_missed_type2 = sorted(missed_items['type2'].items(), key=lambda x: x[1], reverse=True)[:3]
        top_missed_type3 = sorted(missed_items['type3'].items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Most common false positives
        top_fp_type1 = sorted(false_positive_items['type1'].items(), key=lambda x: x[1], reverse=True)[:3]
        top_fp_type2 = sorted(false_positive_items['type2'].items(), key=lambda x: x[1], reverse=True)[:3]
        top_fp_type3 = sorted(false_positive_items['type3'].items(), key=lambda x: x[1], reverse=True)[:3]
        
        insights_text = f"""
OVERALL PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Overall Precision: {overall_precision:.1%}  (When Cursor reports something, it's correct this often)
  Overall Recall:    {overall_recall:.1%}  (Cursor finds this percentage of actual issues)
  Overall F1 Score:  {overall_f1:.1%}  (Harmonic mean balancing precision and recall)

PERFORMANCE BY TYPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Type 1 (Missing):    F1={statistics.mean(all_metrics['type1']['f1']):.1%}  P={statistics.mean(all_metrics['type1']['precision']):.1%}  R={statistics.mean(all_metrics['type1']['recall']):.1%}
  Type 2 (Incorrect):  F1={statistics.mean(all_metrics['type2']['f1']):.1%}  P={statistics.mean(all_metrics['type2']['precision']):.1%}  R={statistics.mean(all_metrics['type2']['recall']):.1%}
  Type 3 (Extraneous): F1={statistics.mean(all_metrics['type3']['f1']):.1%}  P={statistics.mean(all_metrics['type3']['precision']):.1%}  R={statistics.mean(all_metrics['type3']['recall']):.1%}

CONSISTENCY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Most Consistent:  Type 3 (σ={statistics.stdev(all_metrics['type3']['f1']) if len(all_metrics['type3']['f1']) > 1 else 0:.3f})
  Least Consistent: Type 1 (σ={statistics.stdev(all_metrics['type1']['f1']) if len(all_metrics['type1']['f1']) > 1 else 0:.3f})

COMMONLY MISSED PATTERNS (Top 3 per type)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Type 1: {', '.join([f"{item[0]} ({item[1]}x)" for item in top_missed_type1]) if top_missed_type1 else 'None'}
  Type 2: {', '.join([f"{item[0]} ({item[1]}x)" for item in top_missed_type2]) if top_missed_type2 else 'None'}
  Type 3: {', '.join([f"{item[0].split('/')[-1] if '/' in item[0] else item[0]} ({item[1]}x)" for item in top_missed_type3]) if top_missed_type3 else 'None'}

FALSE POSITIVE PATTERNS (Top 3 per type)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Type 1: {', '.join([f"{item[0]} ({item[1]}x)" for item in top_fp_type1]) if top_fp_type1 else 'None'}
  Type 2: {', '.join([f"{item[0]} ({item[1]}x)" for item in top_fp_type2]) if top_fp_type2 else 'None'}
  Type 3: {', '.join([f"{item[0].split('/')[-1] if '/' in item[0] else item[0]} ({item[1]}x)" for item in top_fp_type3]) if top_fp_type3 else 'None'}

KEY INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Precision vs Recall: Cursor tends toward {('higher precision' if overall_precision > overall_recall else 'higher recall')}
• Best Detection: Type 3 (Extraneous) with {statistics.mean(all_metrics['type3']['f1']):.1%} F1
• Weakest Detection: Type 1 (Missing) with {statistics.mean(all_metrics['type1']['f1']):.1%} F1
• Branch Performance: {'Baseline_balanced' if statistics.mean(branch_metrics.get('baseline_balanced', {}).get('f1', [0])) > 0.5 else 'Struggles with'} performs best
• Consistency: {'Reliable' if max(statistics.stdev(all_metrics[t]['f1']) if len(all_metrics[t]['f1']) > 1 else 0 for t in ['type1', 'type2', 'type3']) < 0.15 else 'Variable'} performance across runs
        """
        
        ax.text(0.05, 0.5, insights_text, fontsize=8, family='monospace',
                verticalalignment='center', transform=ax.transAxes)
        
        # Add timestamp
        ax.text(0.5, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                transform=ax.transAxes, ha='center', fontsize=8, style='italic')
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # PAGE 5: Executive Summary
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle('Executive Summary', fontsize=16, y=0.98)
        
        # Create a clean summary visualization
        ax = plt.subplot(1, 1, 1)
        ax.axis('off')
        
        # Calculate key stats
        type1_f1 = statistics.mean(all_metrics['type1']['f1'])
        type2_f1 = statistics.mean(all_metrics['type2']['f1'])
        type3_f1 = statistics.mean(all_metrics['type3']['f1'])
        
        type1_precision = statistics.mean(all_metrics['type1']['precision'])
        type2_precision = statistics.mean(all_metrics['type2']['precision'])
        type3_precision = statistics.mean(all_metrics['type3']['precision'])
        
        type1_recall = statistics.mean(all_metrics['type1']['recall'])
        type2_recall = statistics.mean(all_metrics['type2']['recall'])
        type3_recall = statistics.mean(all_metrics['type3']['recall'])
        
        # Create a traffic light style summary
        summary_text = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CURSOR PERFORMANCE SUMMARY                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║  Overall Performance:  F1 Score: {overall_f1:.1%}  •  Precision: {overall_precision:.1%}  •  Recall: {overall_recall:.1%}    ║
║                                                                                ║
╠════════════════╤═══════════════╤═══════════════╤═══════════════╤═════════════╣
║ Misalignment   │   F1 Score    │   Precision   │    Recall     │   Rating    ║
╠════════════════╪═══════════════╪═══════════════╪═══════════════╪═════════════╣
║ Type 1 Missing │     {type1_f1:5.1%}     │     {type1_precision:5.1%}     │     {type1_recall:5.1%}     │    {'POOR' if type1_f1 < 0.4 else 'FAIR' if type1_f1 < 0.6 else 'GOOD'}     ║
║ Type 2 Incorrect│     {type2_f1:5.1%}     │     {type2_precision:5.1%}     │     {type2_recall:5.1%}     │    {'POOR' if type2_f1 < 0.4 else 'FAIR' if type2_f1 < 0.6 else 'GOOD'}     ║
║ Type 3 Extra   │     {type3_f1:5.1%}     │     {type3_precision:5.1%}     │     {type3_recall:5.1%}     │    {'GOOD' if type3_f1 > 0.6 else 'FAIR' if type3_f1 > 0.4 else 'POOR'}     ║
╚════════════════╧═══════════════╧═══════════════╧═══════════════╧═════════════╝


                               USE CASE RECOMMENDATIONS
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  RECOMMENDED FOR:                      USE WITH CAUTION:
  • Finding extraneous code              • Verifying completeness
  • Code cleanup tasks                   • Critical missing features
  • Basic sanity checks                  • Subtle implementation errors
  • Obvious implementation errors        • Distributed issues
  
  NOT RECOMMENDED FOR:
  • Sole verification method
  • Finding all missing requirements
  • Complex, distributed systems


                                  RELIABILITY PROFILE
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Performance Consistency:  {'STABLE' if max(statistics.stdev(all_metrics[t]['f1']) if len(all_metrics[t]['f1']) > 1 else 0 for t in ['type1', 'type2', 'type3']) < 0.15 else 'VARIABLE' if max(statistics.stdev(all_metrics[t]['f1']) if len(all_metrics[t]['f1']) > 1 else 0 for t in ['type1', 'type2', 'type3']) < 0.25 else 'UNSTABLE'}
  False Positive Rate:      {'LOW' if overall_precision > 0.7 else 'MODERATE' if overall_precision > 0.5 else 'HIGH'}  
  Coverage:                 {'GOOD' if overall_recall > 0.7 else 'PARTIAL' if overall_recall > 0.5 else 'LIMITED'}


                                     KEY INSIGHT
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Cursor excels at finding code that shouldn't exist ({type3_f1:.0%} F1) but struggles
  to identify what's missing ({type1_f1:.0%} F1). Best used as a complementary tool
  for code review, not as the sole verification method.
"""
        
        # Display the formatted summary
        ax.text(0.5, 0.5, summary_text, fontsize=8.5, family='monospace',
                ha='center', va='center', transform=ax.transAxes)
        
        # Add a simple visual indicator at the bottom
        bottom_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  •  Based on {sum(len(all_metrics[t]['f1']) for t in ['type1', 'type2', 'type3'])} test runs"
        ax.text(0.5, 0.02, bottom_text, fontsize=8, ha='center', 
                transform=ax.transAxes, style='italic', color='gray')
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # Set PDF metadata
        d = pdf.infodict()
        d['Title'] = 'Cursor Framework Specification Alignment Analysis'
        d['Author'] = 'Benchmark Analysis System'
        d['Subject'] = 'Performance analysis of Cursor on specification alignment detection'
        d['CreationDate'] = datetime.now()
    
    print(f"✓ PDF report generated: {output_path}")
    
    # Print summary to console
    print("\nSummary:")
    print(f"  Overall Precision: {overall_precision:.1%}")
    print(f"  Overall Recall: {overall_recall:.1%}")
    print(f"  Overall F1: {overall_f1:.1%}")
    print(f"  Type 1 (Missing): F1={statistics.mean(all_metrics['type1']['f1']):.1%}")
    print(f"  Type 2 (Incorrect): F1={statistics.mean(all_metrics['type2']['f1']):.1%}")  
    print(f"  Type 3 (Extraneous): F1={statistics.mean(all_metrics['type3']['f1']):.1%}")


if __name__ == "__main__":
    create_pdf_report("cursor_analysis.pdf")