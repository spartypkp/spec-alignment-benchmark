# Specification Alignment Benchmark Repository

**Version:** 1.0.0  
**Created:** October 5, 2025  
**Repository:** spec-alignment-benchmark  
**Purpose:** Benchmark AI coding assistant frameworks on specification alignment detection

---

## Repository Overview

This repository contains a benchmark for comparing how well AI coding assistant **frameworks** (not models) can detect misalignments between code and specifications. By using the same underlying language model across different tools, we isolate and measure framework-specific capabilities.

### Key Innovation

Unlike existing benchmarks that compare models (GPT-4 vs Claude), this benchmark:
- Holds the model constant (Claude 3.5 Sonnet)
- Tests three fundamental misalignment types
- Uses simplified, objective scoring
- Provides reproducible methodology

---

## The Three Misalignment Types

Every possible specification misalignment falls into exactly one of these categories:

### Type 1: Missing Implementation
- **Definition**: Specification requires X, code doesn't have X
- **Example**: Spec requires JWT authentication, code has no authentication
- **Output**: List of section headers from spec

### Type 2: Incorrect Implementation
- **Definition**: Specification requires X as A, code implements X as B  
- **Example**: Spec requires 15-minute tokens, code has 60-minute tokens
- **Output**: Section headers + affected files

### Type 3: Extraneous Code
- **Definition**: Code contains Y, specification doesn't mention Y
- **Example**: Code has admin dashboard, spec doesn't mention admin features
- **Output**: List of file paths

---

## Repository Structure

```
spec-alignment-benchmark/
├── README.md                    # Quick start and overview
├── METHODOLOGY.md              # Detailed explanation of approach
│
├── prompts/                    # Test prompts for frameworks
│   ├── README.md              # Prompt usage guide
│   ├── type1-missing.md      # Detect missing implementations
│   ├── type2-incorrect.md    # Detect incorrect implementations
│   ├── type3-extraneous.md   # Detect extraneous code
│   └── combined-all-types.md # Detect all three types
│
├── scripts/                    # Analysis tools
│   ├── score.py              # Main scoring script
│   └── validate_results.py   # Validate JSON outputs
│
├── examples/                   # Example inputs and outputs
│   ├── README.md             # How scoring works
│   ├── sample-ground-truth.json
│   ├── sample-llm-output.json
│   └── scored_sample-llm-output.json
│
├── docs/                       # Documentation
│   ├── ground-truth-format.md    # Ground truth schema
│   └── test-execution-protocol.md # How to run tests
│
├── results/                    # Test results (create as needed)
│   ├── raw/                   # Framework outputs
│   │   ├── cursor/           
│   │   └── claude-code/      
│   └── processed/             # Scored results
│
└── specs/                      # Specifications
    ├── benchmark-specification.md  # Original benchmark design
    └── repository-specification.md # This document
```

---

## How It Works

### 1. Test Repository Setup

Create a separate repository with:
```
test-repository/
├── specs/
│   └── project-specification.md  # The specification document
├── app/                          # Implementation code
├── components/
├── lib/
└── ground-truth.json             # Answer key (remove before testing)
```

Create test branches with planted misalignments:
- `main`: Perfectly aligned code and spec
- `test-set-1`: Mix of Type 1, 2, and 3 misalignments
- `test-set-2`: Different misalignment patterns
- `test-set-3`: Edge cases and subtle issues

### 2. Test Execution

For each test branch and framework:
1. Load the test repository in the framework
2. Run each of the 4 prompts with fresh context:
   - `type1-missing.md`
   - `type2-incorrect.md`
   - `type3-extraneous.md`
   - `combined-all-types.md`
3. Save JSON outputs to `results/raw/[framework]/`

### 3. Scoring

```bash
# Score individual test
python3 scripts/score.py results/raw/cursor/test1.json ground-truth.json

# Output shows:
# - Precision, Recall, F1 for each type
# - True/false positives/negatives
# - Combined score
```

---

## Ground Truth Format

The ground truth is extremely simple - just the data needed for scoring:

```json
{
  "test_branch": "test-set-1",
  "specification_file": "specs/project-specification.md",
  "type1_missing": [
    "2.1 Authentication & Authorization",
    "3.3 Rate Limiting"
  ],
  "type2_incorrect": [
    {
      "section": "3.1 Request/Response Format",
      "files": ["middleware/errorHandler.ts"]
    }
  ],
  "type3_extraneous": [
    "app/admin/route.ts",
    "api/debug/route.ts"
  ]
}
```

## LLM Output Format

The prompts ask for this exact format:

### Type 1 Output
```json
{
  "analysis_type": "type1_missing",
  "type1_missing": ["2.1 Authentication & Authorization"]
}
```

### Type 2 Output  
```json
{
  "analysis_type": "type2_incorrect",
  "type2_incorrect": [
    {
      "section": "3.1 Request/Response Format",
      "files": ["middleware/errorHandler.ts"]
    }
  ]
}
```

### Type 3 Output
```json
{
  "analysis_type": "type3_extraneous",
  "type3_extraneous": ["app/admin/route.ts"]
}
```

### Combined Output
All three types in one response.

---

## Scoring System

### Scoring Algorithm

**Type 1 & Type 3**: Simple set operations
```python
true_positives = set(llm_output) & set(ground_truth)
false_positives = set(llm_output) - set(ground_truth)
precision = len(true_positives) / len(llm_output)
recall = len(true_positives) / len(ground_truth)
```

**Type 2**: Section + file matching
- Match if same section AND at least one file overlaps

**Point System**:
- Correct detection: +1 point
- False positive: -0.25 points
- Missed detection: 0 points

### Why This Design?

1. **No fuzzy matching**: Exact string comparison only
2. **Minimal data**: Only what's needed for scoring
3. **Fast comparison**: O(n) set operations
4. **Objective scoring**: No subjective interpretation
5. **Easy validation**: Anyone can verify results

---

## Running Tests

### Prerequisites

- Python 3.9+
- Access to AI coding frameworks (Cursor, Claude Code, etc.)
- Test repository with planted misalignments

### Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/[username]/spec-alignment-benchmark
cd spec-alignment-benchmark

# 2. Create results directory
mkdir -p results/raw/{cursor,claude-code}

# 3. Run tests in frameworks (manual process)
# - Load test repository in framework
# - Copy and paste each prompt
# - Save outputs to results/raw/

# 4. Score results
python3 scripts/score.py \
  results/raw/cursor/type1-output.json \
  test-repo/ground-truth.json

# 5. View example
python3 scripts/score.py \
  examples/sample-llm-output.json \
  examples/sample-ground-truth.json
```

### Test Protocol

See `docs/test-execution-protocol.md` for detailed instructions on:
- Environment setup
- Test execution steps  
- Output collection
- Quality control

---

## Key Principles

1. **Simplicity**: Only 3 fundamental misalignment types
2. **Completeness**: These 3 types cover every possible case
3. **Objectivity**: Clear ground truth enables objective scoring
4. **Reproducibility**: Anyone can run the same tests
5. **Fairness**: Identical prompts and conditions for all frameworks

---

## Contributing

We welcome contributions:

### Priority Areas

1. **Test Cases**: Create test repositories with different patterns
2. **Analysis Tools**: Improve scoring and visualization
3. **Documentation**: Clarify methods and usage
4. **Framework Support**: Add more frameworks to test

### Contribution Process

1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Participate in review

---

## Results Interpretation

### Metrics Explained

**Precision**: Of items reported, how many were correct?
- High precision = few false positives
- Low precision = many false alarms

**Recall**: Of actual misalignments, how many were found?
- High recall = found most issues
- Low recall = missed many issues

**F1 Score**: Harmonic mean of precision and recall
- Balances both metrics
- Single score for comparison

### Understanding Scores

```
Example Output:
TYPE1 Results:
  Precision: 66.7%  (2 correct out of 3 reported)
  Recall:    66.7%  (2 found out of 3 actual)
  F1 Score:  0.667
  Score:     1.75   (2 correct - 0.25 penalty)
```

This means the framework:
- Found 2/3 missing implementations
- Had 1 false positive (penalty applied)
- Achieved moderate performance on Type 1 detection

---

## FAQ

**Q: Why test frameworks instead of models?**  
A: Frameworks add search, context management, and tool use on top of models. Testing with the same model isolates these framework capabilities.

**Q: Why these three types?**  
A: They're exhaustive - every possible misalignment must be one of: missing (Type 1), wrong (Type 2), or extra (Type 3).

**Q: Why such simple outputs?**  
A: Simple outputs enable objective scoring without fuzzy matching or interpretation.

**Q: Can I test other frameworks?**  
A: Yes! Use the same prompts and ground truth format for any framework.

**Q: How many test runs are needed?**  
A: Minimum 3-5 runs per framework for statistical validity.

---

## License

MIT License - See LICENSE file

---

## Contact

- Issues: [GitHub Issues](https://github.com/[username]/spec-alignment-benchmark/issues)
- Discussions: [GitHub Discussions](https://github.com/[username]/spec-alignment-benchmark/discussions)

---

## Acknowledgments

This benchmark addresses a critical gap in AI tool evaluation. By testing frameworks rather than models, we can finally understand which tools best help developers maintain specification alignment.