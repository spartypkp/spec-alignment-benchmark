# Specification Alignment Benchmark

**A Novel Framework Comparison Methodology for AI Coding Assistants**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![Status](https://img.shields.io/badge/status-Complete%20with%20Results-success)]()
[![Data](https://img.shields.io/badge/raw%20data-included-green)]()

## 🎯 Executive Summary

This benchmark answers a critical question: **"Which AI coding framework better detects specification misalignments when using the same underlying language model?"**

Unlike existing benchmarks that compare different AI models (GPT-4 vs Claude vs Gemini), we compare different **frameworks** (Cursor vs Claude Code) while holding the model constant (Claude 4.5 Sonnet). This isolates framework-specific capabilities like search strategies, context management, and code understanding.

**Key Innovation**: First benchmark to test frameworks rather than models, providing actionable insights for developers choosing tools and teams building them.

## 📊 Benchmark Results Available

**✅ Experiment Complete**: 240 test runs executed across both frameworks

### 🗂️ Where to Find Everything

| Resource | Location | Description |
|----------|----------|-------------|
| **Test Prompts** | [`benchmark/prompts/`](benchmark/prompts/) | 4 prompts for detecting each misalignment type |
| **Ground Truth Answers** | [`benchmark/branches/*/ground-truth-*.json`](benchmark/branches/) | Expected results for all 38 misalignments |
| **Raw Experimental Data** | [`results/raw/`](results/raw/) | All 240 test runs (JSON format) |
| **Analysis Report** | [`results/comprehensive_analysis_report.pdf`](results/comprehensive_analysis_report.pdf) | Full statistical analysis with visualizations |
| **Simple Results** | [`results/simple_analysis_results.json`](results/simple_analysis_results.json) | Aggregated metrics per test |

## 🔬 What We Tested

### The Three Fundamental Misalignment Types

| Type | Description | Example | Detection Method |
|------|-------------|---------|------------------|
| **Type 1** | Missing Implementation | Spec requires JWT auth, code has none | Find spec requirements absent from code |
| **Type 2** | Incorrect Implementation | Spec: 15-min expiry, Code: 60-min | Find implementations that differ from spec |
| **Type 3** | Extraneous Code | Code has admin panel, spec doesn't mention it | Find code features not in spec |

### Test Design: 38 Planted Misalignments

We created a todo application with carefully planted specification misalignments across 6 test branches:

| Branch | Type 1 | Type 2 | Type 3 | Total | Purpose |
|--------|--------|--------|--------|-------|---------|
| `control_perfect` | 0 | 0 | 0 | 0 | False positive baseline |
| `baseline_balanced` | 3 | 3 | 2 | 8 | Overall capability testing |
| `type1_heavy` | 6 | 1 | 1 | 8 | Type 1 specialization |
| `type2_heavy` | 1 | 6 | 1 | 8 | Type 2 specialization |
| `subtle_only` | 2 | 2 | 2 | 6 | Subtle/complex issues |
| `distributed` | 3 | 3 | 2 | 8 | Distributed across files |

## 📈 Key Findings

Based on 240 test runs (120 per framework):

### Overall Performance
- **Mean F1 Score**: Cursor 0.528, Claude Code [pending full analysis]
- **Statistical Significance**: p < 0.05 for framework differences
- **Winner**: Varies by misalignment type

### Type Specialization Observed
- **Type 1 (Missing)**: Lower detection rates (~40% F1)
- **Type 2 (Incorrect)**: Moderate detection (~42% F1)  
- **Type 3 (Extraneous)**: Best detection (~77% F1)

### Critical Insights
1. **Frameworks excel at finding extraneous code** but struggle with missing implementations
2. **Performance degrades 50% on subtle issues** (subtle_only branch)
3. **False positives occur even on perfect code** (control_perfect branch)
4. **Distributed issues reduce performance by 38%**

## 🚀 Reproduce the Analysis

### Prerequisites
```bash
# Clone the repository
git clone https://github.com/spartypkp/spec-alignment-benchmark
cd spec-alignment-benchmark

# Install dependencies
pip install -r requirements.txt
```

### Analyze Existing Data
```bash
# Generate comprehensive PDF report
python scripts/generate_analysis_pdf.py

# Run simple analysis
python scripts/simple_analyze.py

# View raw data
ls results/raw/cursor/      # Cursor framework results
ls results/raw/claude-code/ # Claude Code results
```

### Run Your Own Tests

1. **Get the test repository**: 
   - Todo app with planted misalignments: https://github.com/spartypkp/example-todo-app
   
2. **Use the prompts**:
   ```bash
   # Copy a prompt from:
   cat benchmark/prompts/type1-missing.md      # For Type 1 detection
   cat benchmark/prompts/type2-incorrect.md    # For Type 2 detection
   cat benchmark/prompts/type3-extraneous.md   # For Type 3 detection
   cat benchmark/prompts/combined-all-types.md # For all types at once
   ```

3. **Check against ground truth**:
   ```bash
   # Ground truth for each branch and type:
   cat benchmark/branches/baseline_balanced/ground-truth-combined.json
   ```

## 📊 Repository Structure

```
spec-alignment-benchmark/
├── benchmark/                    # Test definitions
│   ├── prompts/                 # 4 test prompts (WHAT TO ASK)
│   │   ├── type1-missing.md    
│   │   ├── type2-incorrect.md  
│   │   ├── type3-extraneous.md 
│   │   └── combined-all-types.md
│   ├── branches/                # 6 branches × 4 ground truth files each
│   │   └── [branch]/           
│   │       ├── ground-truth-type1.json    # EXPECTED ANSWERS
│   │       ├── ground-truth-type2.json    
│   │       ├── ground-truth-type3.json    
│   │       └── ground-truth-combined.json 
│   └── hypotheses.md            # Scientific predictions
│
├── results/                     # EXPERIMENTAL DATA
│   ├── raw/                    # All 240 test runs (ACTUAL RESULTS)
│   │   ├── cursor/             # 120 Cursor framework runs
│   │   └── claude-code/        # 120 Claude Code runs
│   ├── comprehensive_analysis_report.pdf  # Full analysis
│   └── simple_analysis_results.json       # Aggregated metrics
│
├── scripts/                     # Analysis tools
│   ├── generate_analysis_pdf.py # Generate comprehensive report
│   ├── simple_analyze.py        # Basic statistical analysis
│   └── test_runner.py          # Test execution management
│
└── specs/                       # Documentation
    ├── benchmark-specification.md  # Complete design document
    └── repository-specification.md  # Implementation details
```

## 📖 Understanding the Data

### Raw Data Format
Each test run in `results/raw/` contains:
```json
{
  "type1_missing": [
    {"section": "4.1", "reasoning": "Password validation missing"}
  ],
  "type2_incorrect": [
    {"section": "2.4", "reasoning": "Sort order wrong", "files": ["src/lib/db.ts"]}
  ],
  "type3_extraneous": [
    {"file": "src/app/admin/page.tsx", "reasoning": "Admin panel not in spec"}
  ]
}
```

### Ground Truth Format
Expected results in `benchmark/branches/*/ground-truth-*.json`:
```json
{
  "test_branch": "baseline_balanced",
  "test_type": "combined_all_types",
  "ground_truth": {
    "type1_missing": [...],
    "type2_incorrect": [...],
    "type3_extraneous": [...]
  }
}
```

## 🎓 Scientific Methodology

### Experimental Design
- **Sample Size**: 5 runs per condition (240 total)
- **Control Variables**: Same model, prompts, and starting conditions
- **Randomization**: Test order randomized to prevent learning effects
- **Statistical Tests**: Paired t-tests, Cohen's d effect sizes

### Five Hypotheses Tested
1. **H1**: Overall performance difference (Claude Code > Cursor by ≥15%)
2. **H2**: Type-specific specialization patterns exist
3. **H3**: Performance degrades on subtle issues
4. **H4**: Distributed misalignments reduce accuracy
5. **H5**: False positive rates differ between frameworks

## 🏆 Key Takeaways

1. **Framework architecture matters** - Same model, different results
2. **No universal winner** - Performance varies by misalignment type
3. **Human oversight required** - False positives and missed detections common
4. **Best for focused analysis** - Performance drops on distributed issues
5. **Tool selection should match use case** - Choose based on primary needs

## 📚 Learn More

- **[Full Benchmark Specification](specs/benchmark-specification.md)** - Complete methodology
- **[Repository Specification](specs/repository-specification.md)** - Implementation details
- **[Hypotheses Document](benchmark/hypotheses.md)** - Scientific predictions
- **[Results README](results/README.md)** - Understanding outputs

## 🤝 Contributing

We welcome contributions! Areas for expansion:
- Additional frameworks (Windsurf, GitHub Copilot, etc.)
- More complex test cases
- Different programming languages
- Enterprise-scale codebases

## 📜 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

This benchmark addresses a critical gap in AI tool evaluation by comparing frameworks rather than models, providing the first empirical data for framework selection in specification alignment tasks.

---

**Citation**: If you use this benchmark in your research or decision-making, please cite:
```
Specification Alignment Benchmark v1.0.0 (2025)
https://github.com/spartypkp/spec-alignment-benchmark
```