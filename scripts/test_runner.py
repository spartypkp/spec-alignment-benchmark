#!/usr/bin/env python3
"""
Test runner to organize and track benchmark test execution.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, List, Optional
import subprocess

class TestRunner:
    """Manages test execution and tracking."""
    
    def __init__(self, base_dir: Path = Path(".")):
        self.base_dir = base_dir
        self.results_dir = base_dir / "results"
        self.benchmark_dir = base_dir / "benchmark"
        self.progress_file = self.results_dir / "progress.json"
        self.log_file = self.results_dir / "test_runs.log"
        
        # Test configuration
        self.branches = [
            "control_perfect",
            "baseline_balanced",
            "type1_heavy",
            "type2_heavy",
            "subtle_only",
            "distributed"
        ]
        
        self.test_types = [
            "type1",
            "type2",
            "type3",
            "combined"
        ]
        
        self.frameworks = ["cursor", "claude-code"]
        
        # Load or initialize progress
        self.progress = self.load_progress()
    
    def load_progress(self) -> Dict:
        """Load progress from file or create new."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        
        # Initialize empty progress
        progress = {}
        for framework in self.frameworks:
            progress[framework] = {}
            for branch in self.branches:
                progress[framework][branch] = {
                    test_type: [] for test_type in self.test_types
                }
        return progress
    
    def save_progress(self):
        """Save progress to file."""
        self.results_dir.mkdir(parents=True, exist_ok=True)
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def log_run(self, framework: str, branch: str, test_type: str, 
                run_number: int, status: str, notes: str = ""):
        """Log a test run to the log file."""
        self.results_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | {framework} | {branch} | {test_type} | run_{run_number} | {status} | {notes}\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
    
    def get_next_run_number(self, framework: str, branch: str, test_type: str) -> int:
        """Get the next run number for a test."""
        completed_runs = self.progress[framework][branch][test_type]
        if not completed_runs:
            return 1
        return max(completed_runs) + 1
    
    def record_test_output(self, framework: str, branch: str, test_type: str,
                          run_number: int, output: Dict) -> Path:
        """Save test output to the raw results directory."""
        # Create output directory
        output_dir = self.results_dir / "raw" / framework / branch
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{branch}_{test_type}_run{run_number}_{timestamp}.json"
        output_path = output_dir / filename
        
        # Save output
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Saved output to {output_path}")
        return output_path
    
    def score_result(self, output_path: Path, framework: str, branch: str, 
                    test_type: str, run_number: int) -> Path:
        """Score a test result against ground truth."""
        # Determine ground truth file
        gt_file = self.benchmark_dir / "branches" / branch / f"ground-truth-{test_type}.json"
        
        if not gt_file.exists():
            print(f"Warning: Ground truth file not found: {gt_file}")
            return None
        
        # Create scored output directory
        scored_dir = self.results_dir / "processed" / framework / branch
        scored_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate scored filename
        scored_filename = f"{branch}_{test_type}_run{run_number}_scored.json"
        scored_path = scored_dir / scored_filename
        
        # Run scoring script
        cmd = [
            sys.executable,
            str(self.base_dir / "scripts" / "score_result.py"),
            str(output_path),
            str(gt_file)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse the JSON output
            json_output = result.stdout.split('\n')
            # Find where JSON starts (after any print statements)
            json_start = 0
            for i, line in enumerate(json_output):
                if line.startswith('{'):
                    json_start = i
                    break
            
            # Extract just the JSON part
            json_lines = []
            bracket_count = 0
            for line in json_output[json_start:]:
                json_lines.append(line)
                bracket_count += line.count('{') - line.count('}')
                if bracket_count == 0 and json_lines:
                    break
            
            scored_data = json.loads('\n'.join(json_lines))
            
            # Save scored result
            with open(scored_path, 'w') as f:
                json.dump(scored_data, f, indent=2)
            
            print(f"Scored result saved to {scored_path}")
            
            # Print score summary
            scores = scored_data['scores']
            if 'combined' in scores:
                print(f"  Combined F1: {scores['combined']['avg_f1']:.3f}")
            else:
                print(f"  F1 Score: {scores['f1_score']:.3f}")
            
            return scored_path
            
        except subprocess.CalledProcessError as e:
            print(f"Error scoring result: {e}")
            print(f"stderr: {e.stderr}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing scoring output: {e}")
            return None
    
    def register_completed_test(self, framework: str, branch: str, 
                                test_type: str, run_number: int):
        """Register a test as completed."""
        if run_number not in self.progress[framework][branch][test_type]:
            self.progress[framework][branch][test_type].append(run_number)
            self.save_progress()
    
    def show_progress(self):
        """Display current progress."""
        print("\n" + "="*70)
        print("TEST PROGRESS SUMMARY")
        print("="*70)
        
        total_expected = len(self.branches) * len(self.test_types) * 5  # 5 runs each
        
        for framework in self.frameworks:
            print(f"\n{framework.upper()}")
            print("-" * 40)
            
            total_completed = 0
            
            for branch in self.branches:
                branch_completed = 0
                branch_details = []
                
                for test_type in self.test_types:
                    runs = self.progress[framework][branch][test_type]
                    branch_completed += len(runs)
                    if runs:
                        branch_details.append(f"{test_type}({len(runs)})")
                
                total_completed += branch_completed
                
                status_symbol = "✓" if branch_completed >= 20 else "○"  # 4 types × 5 runs
                print(f"  {status_symbol} {branch:20} {branch_completed}/20 runs")
                if branch_details:
                    print(f"      Completed: {', '.join(branch_details)}")
            
            percentage = (total_completed / total_expected) * 100
            print(f"\n  Total Progress: {total_completed}/{total_expected} ({percentage:.1f}%)")
        
        print()
    
    def get_missing_tests(self, framework: str, max_runs: int = 5) -> List[Dict]:
        """Get list of tests that still need to be run."""
        missing = []
        
        for branch in self.branches:
            for test_type in self.test_types:
                completed_runs = self.progress[framework][branch][test_type]
                needed_runs = max_runs - len(completed_runs)
                
                if needed_runs > 0:
                    missing.append({
                        "branch": branch,
                        "test_type": test_type,
                        "completed": len(completed_runs),
                        "needed": needed_runs,
                        "next_run": self.get_next_run_number(framework, branch, test_type)
                    })
        
        return missing
    
    def show_next_tests(self, framework: str, limit: int = 5):
        """Show the next tests to run."""
        missing = self.get_missing_tests(framework)
        
        if not missing:
            print(f"\nAll tests completed for {framework}!")
            return
        
        print(f"\nNext tests to run for {framework}:")
        print("-" * 50)
        
        # Prioritize by branch order, then test type
        priority_order = []
        for branch in self.branches:
            for test_type in self.test_types:
                for test in missing:
                    if test['branch'] == branch and test['test_type'] == test_type:
                        priority_order.append(test)
        
        for i, test in enumerate(priority_order[:limit], 1):
            print(f"{i}. {test['branch']} - {test['test_type']} (run {test['next_run']})")
            print(f"   Status: {test['completed']}/{test['completed'] + test['needed']} completed")
    
    def validate_output(self, output: Dict, test_type: str) -> bool:
        """Validate that output has expected structure."""
        if test_type == "combined":
            expected_keys = ["type1_missing", "type2_incorrect", "type3_extraneous"]
            for key in expected_keys:
                if key not in output:
                    print(f"Warning: Missing expected key '{key}' in output")
                    return False
        else:
            expected_key = f"{test_type}_" + {
                "type1": "missing",
                "type2": "incorrect",
                "type3": "extraneous"
            }[test_type]
            
            if expected_key not in output:
                print(f"Warning: Missing expected key '{expected_key}' in output")
                return False
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Test runner for benchmark execution"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Progress command
    progress_parser = subparsers.add_parser('progress', help='Show test progress')
    
    # Next command
    next_parser = subparsers.add_parser('next', help='Show next tests to run')
    next_parser.add_argument('framework', choices=['cursor', 'claude-code'])
    next_parser.add_argument('--limit', type=int, default=5, help='Number of tests to show')
    
    # Record command
    record_parser = subparsers.add_parser('record', help='Record a test result')
    record_parser.add_argument('framework', choices=['cursor', 'claude-code'])
    record_parser.add_argument('branch', choices=[
        'control_perfect', 'baseline_balanced', 'type1_heavy',
        'type2_heavy', 'subtle_only', 'distributed'
    ])
    record_parser.add_argument('test_type', choices=['type1', 'type2', 'type3', 'combined'])
    record_parser.add_argument('output_file', type=Path, help='JSON output file from framework')
    record_parser.add_argument('--run', type=int, help='Run number (auto if not specified)')
    record_parser.add_argument('--score', action='store_true', help='Also score the result')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate output format')
    validate_parser.add_argument('output_file', type=Path, help='JSON output file to validate')
    validate_parser.add_argument('test_type', choices=['type1', 'type2', 'type3', 'combined'])
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    runner = TestRunner()
    
    if args.command == 'progress':
        runner.show_progress()
    
    elif args.command == 'next':
        runner.show_next_tests(args.framework, args.limit)
    
    elif args.command == 'record':
        # Load output file
        try:
            with open(args.output_file, 'r') as f:
                output = json.load(f)
        except Exception as e:
            print(f"Error loading output file: {e}")
            sys.exit(1)
        
        # Validate output
        if not runner.validate_output(output, args.test_type):
            print("Output validation failed. Continue anyway? (y/n)")
            if input().lower() != 'y':
                sys.exit(1)
        
        # Get run number
        run_number = args.run or runner.get_next_run_number(
            args.framework, args.branch, args.test_type
        )
        
        # Record the output
        output_path = runner.record_test_output(
            args.framework, args.branch, args.test_type, run_number, output
        )
        
        # Score if requested
        if args.score:
            scored_path = runner.score_result(
                output_path, args.framework, args.branch, args.test_type, run_number
            )
            if scored_path:
                runner.register_completed_test(
                    args.framework, args.branch, args.test_type, run_number
                )
                runner.log_run(
                    args.framework, args.branch, args.test_type, run_number,
                    "completed", "Scored successfully"
                )
            else:
                runner.log_run(
                    args.framework, args.branch, args.test_type, run_number,
                    "error", "Scoring failed"
                )
        else:
            runner.register_completed_test(
                args.framework, args.branch, args.test_type, run_number
            )
            runner.log_run(
                args.framework, args.branch, args.test_type, run_number,
                "recorded", "Output saved"
            )
    
    elif args.command == 'validate':
        # Load and validate output file
        try:
            with open(args.output_file, 'r') as f:
                output = json.load(f)
            
            if runner.validate_output(output, args.test_type):
                print(f"✓ Output is valid for {args.test_type} test")
            else:
                print(f"✗ Output is invalid for {args.test_type} test")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error validating file: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
