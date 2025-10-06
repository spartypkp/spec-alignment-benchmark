# Specification Alignment Benchmark

**A Framework Comparison Study for AI Coding Assistants**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![Status](https://img.shields.io/badge/status-Results%20Available-success)]()
[![Data](https://img.shields.io/badge/raw%20data-included-green)]()

## Executive Summary

This benchmark explores: **"Do different AI coding frameworks detect specification misalignments differently when using the same underlying language model?"**

Unlike existing benchmarks comparing AI models (GPT-4 vs Claude vs Gemini), we compare **frameworks** (Cursor vs Claude Code) while holding the model constant (Claude 4.5 Sonnet). This isolates framework-specific capabilities like search strategies, context management, and code understanding.

## Key Findings

**240 test runs completed** (120 per framework, 5 runs per condition)

### Main Result: No Overall Performance Difference
- **Cursor Mean F1**: 0.50
- **Claude Code Mean F1**: 0.48
- **Statistical Difference**: None (p = 0.73)

**However**, performance varies significantly by misalignment type:

### Type-Specific Performance Patterns

| Type | Cursor F1 | Claude Code F1 | Pattern |
|------|-----------|----------------|---------|
| **Type 1** (Missing) | 0.39 | 0.36 | Cursor slightly better |
| **Type 2** (Incorrect) | 0.42 | 0.58 | **Claude Code stronger** (p=0.03) |
| **Type 3** (Extraneous) | 0.77 | 0.60 | **Cursor stronger** (p=0.04) |

**Key Insight**: While neither framework has an overall advantage, they show different strengths:
- **Cursor** excels at finding extraneous code (Type 3) and slightly better at detecting missing features (Type 1)
- **Claude Code** performs better at identifying incorrect implementations (Type 2)

**Next Steps**: These patterns emerged from a pilot study (n=5 per condition). We plan to replicate with larger sample sizes (n≥30) to confirm these type-specific differences and establish more robust statistical evidence.

### Detection Rates

- **Type 1 Detection**: Cursor 37%, Claude Code 45% (both struggle)
- **Type 2 Detection**: Cursor 71%, Claude Code 73% (moderate success)
- **Type 3 Detection**: Cursor 72%, Claude Code 71% (best performance)
- **False Positive Rate**: Cursor 42%, Claude Code 47% (concerning)

## Study Design & Limitations

This study used a controlled experimental design with important characteristics to note:

### Experimental Design
- **Sample size**: 5 runs per condition (240 total runs)
- **Control variables**: Same model (Claude 4.5 Sonnet), same prompts, same codebase
- **Test branches**: 6 branches with varying misalignment distributions
- **Ground truth**: 38 carefully planted misalignments validated by specification

### Important Considerations

**Sample Size**: The current n=5 per condition provides initial insights but is smaller than typical for robust statistical conclusions. Planned replication with n≥30 will provide stronger evidence for the observed type-specific patterns.

**Statistical Testing**: The Type 2 and Type 3 differences (p=0.03, p=0.04) are at the threshold of significance. With multiple comparisons, these should be interpreted as promising patterns worthy of confirmation rather than definitive findings.

**Scope**: This benchmark focuses on a single todo application with medium complexity. Results may vary with:
- Enterprise-scale codebases
- Different application domains  
- Other programming languages
- Different model versions

**Generalizability**: Framework performance likely depends on the specific use case, codebase characteristics, and type of misalignment most relevant to your work.

### What This Benchmark Demonstrates
- Framework architecture influences detection capabilities even with identical models
- Type-specific performance patterns exist and are measurable
- A methodology for systematic framework comparison
- Baseline performance data for specification alignment tasks

## What We Tested

### The Three Fundamental Misalignment Types

| Type | Description | Example |
|------|-------------|---------|
| **Type 1** | Missing Implementation | Spec requires JWT auth, code has none |
| **Type 2** | Incorrect Implementation | Spec: 15-min expiry, Code: 60-min |
| **Type 3** | Extraneous Code | Code has admin panel, spec doesn't mention it |

### Test Design: 38 Planted Misalignments

A todo application with specification misalignments across 6 test branches:

| Branch | Type 1 | Type 2 | Type 3 | Total | Purpose |
|--------|--------|--------|--------|-------|---------|
| `control_perfect` | 0 | 0 | 0 | 0 | False positive baseline |
| `baseline_balanced` | 3 | 3 | 2 | 8 | Overall capability |
| `type1_heavy` | 6 | 1 | 1 | 8 | Type 1 focus |
| `type2_heavy` | 1 | 6 | 1 | 8 | Type 2 focus |
| `subtle_only` | 2 | 2 | 2 | 6 | Complex issues |
| `distributed` | 3 | 3 | 2 | 8 | Scattered across files |

## Performance Insights

**Detection patterns across 240 test runs:**

1. **Type-specific specialization observed** 
   - Cursor: Strong at Type 3 (extraneous code, F1=0.77), competitive at Type 1 (missing, F1=0.39)
   - Claude Code: Strong at Type 2 (incorrect implementation, F1=0.58), competitive at other types

2. **Type 3 is most detectable** - Both frameworks achieved ~70% accuracy finding extraneous code not mentioned in specifications

3. **Type 1 is most challenging** - Missing implementations harder to detect (~40% F1 for both frameworks)

4. **Complexity impacts performance** - Subtle/distributed issues reduce detection rates significantly (0.26-0.34 F1 on subtle_only branch vs 0.60-0.70 on baseline)

5. **False positives occur** - Even on perfect code (control_perfect), frameworks flagged some non-issues (42-47% FP rate overall)

### Practical Implications

**Choose based on your primary use case:**
- **Finding unauthorized features/code bloat**: Cursor shows stronger performance (Type 3)
- **Validating implementation correctness**: Claude Code shows stronger performance (Type 2)  
- **Comprehensive auditing**: Both frameworks show similar overall capability; type-specific strengths matter more than overall scores

**Human oversight recommended**: Both frameworks show notable false positive rates, making human review essential for production use.

## Repository Structure

```
spec-alignment-benchmark/
├── benchmark/                    # Test definitions
│   ├── prompts/                 # 4 test prompts
│   │   ├── type1-missing.md    
│   │   ├── type2-incorrect.md  
│   │   ├── type3-extraneous.md 
│   │   └── combined-all-types.md
│   ├── branches/                # 6 branches with ground truth
│   │   └── [branch]/           
│   │       ├── ground-truth-type1.json
│   │       ├── ground-truth-type2.json    
│   │       ├── ground-truth-type3.json    
│   │       └── ground-truth-combined.json 
│   └── hypotheses.md
│
├── results/
│   ├── raw/                    # All 240 test runs
│   │   ├── cursor/             # 120 Cursor runs
│   │   └── claude-code/        # 120 Claude Code runs
│   ├── comprehensive_analysis_report.pdf
│   └── simple_analysis_results.json
│
├── scripts/                     # Analysis tools
│   ├── generate_analysis_pdf.py
│   ├── simple_analyze.py
│   └── test_runner.py
│
└── specs/                       # Documentation
    ├── benchmark-specification.md
    └── repository-specification.md
```

## Reproduce the Analysis

### Prerequisites
```bash
git clone https://github.com/spartypkp/spec-alignment-benchmark
cd spec-alignment-benchmark
pip install -r requirements.txt
```

### Analyze Existing Data
```bash
# Generate comprehensive PDF report
python scripts/generate_analysis_pdf.py

# Run simple analysis
python scripts/simple_analyze.py

# View raw data
ls results/raw/cursor/
ls results/raw/claude-code/
```

### Run Your Own Tests

1. **Get the test repository**: 
   - https://github.com/spartypkp/example-todo-app
   
2. **Use the prompts**:
   ```bash
   cat benchmark/prompts/type1-missing.md
   cat benchmark/prompts/type2-incorrect.md
   cat benchmark/prompts/type3-extraneous.md
   cat benchmark/prompts/combined-all-types.md
   ```

3. **Check against ground truth**:
   ```bash
   cat benchmark/branches/baseline_balanced/ground-truth-combined.json
   ```

## Understanding the Data

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

## Future Research Directions

To improve scientific rigor, future iterations should:

**Statistical improvements:**
- Increase sample size to n≥30 per condition
- Apply proper multiple comparison corrections
- Use non-parametric tests for non-normal data
- Validate ground truth with multiple independent raters

**Methodological enhancements:**
- Blind evaluation procedures
- Documented, standardized prompting protocols
- Multiple application domains
- Different model versions
- Additional frameworks (Windsurf, GitHub Copilot, Aider)

**Scope expansion:**
- Enterprise-scale codebases
- Multiple programming languages
- Different complexity levels
- Real-world specification documents

## Using This Benchmark

**This benchmark is useful for:**
- Understanding framework behavior patterns in specification alignment tasks
- Comparing type-specific detection capabilities
- Informing framework selection based on your primary use case
- Establishing baseline performance expectations
- Generating hypotheses for deeper investigation

**Keep in mind:**
- Results are from a pilot study; larger replication planned to confirm patterns
- Performance may vary with different codebases, domains, and model versions
- Framework-specific strengths matter more than overall scores
- Human review remains essential regardless of framework choice

## Contributing

We welcome contributions that address study limitations:
- Larger-scale replications
- Additional frameworks
- Improved ground truth validation
- Statistical methodology refinements

## Learn More

- [Full Benchmark Specification](specs/benchmark-specification.md)
- [Repository Specification](specs/repository-specification.md)
- [Hypotheses Document](benchmark/hypotheses.md)
- [Results README](results/README.md)

## License

MIT License - See [LICENSE](LICENSE) file

## Acknowledgments

This benchmark addresses a gap in AI tool evaluation by comparing frameworks rather than models, providing empirical data on type-specific performance patterns in specification alignment tasks. While conducted as a pilot study, it establishes methodology and reveals meaningful performance differences that warrant further investigation with larger sample sizes.

---

**Citation**: 
```
Specification Alignment Benchmark v1.0.0 (2025)
https://github.com/spartypkp/spec-alignment-benchmark
Pilot study results (n=5 per condition); larger replication planned
```
