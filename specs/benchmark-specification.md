# Framework Benchmark: Cursor vs Claude Code

**Version:** 1.0.0
**Created:** October 5, 2025
**Updated:** October 5, 2025
**Status:** Implementation Complete - Ready for Testing
**Purpose:** Compare AI coding assistant frameworks (not models) on specification alignment tasks
**Model:** Claude 3.5 Sonnet (held constant across frameworks)
**Test Case:** Todo Application with planted misalignments

---

## Executive Summary

This benchmark compares how different AI coding assistant frameworks (Cursor and Claude Code) perform on identical specification alignment analysis tasks using the same underlying language model. By holding the model constant, we can isolate and measure framework-specific capabilities.

**Key Innovation**: This is the first benchmark to test frameworks rather than models, providing actionable insights for both developers choosing tools and teams building them.

---

## 1. Problem Statement

### 1.1 The Gap in Current Benchmarks

All existing benchmarks compare different AI models (GPT-4 vs Claude vs Gemini). **None compare the frameworks that wrap these models.**

Both Cursor and Claude Code can use Claude 3.5 Sonnet, yet users report dramatically different experiences. This benchmark answers: **"Which framework better amplifies the model's capabilities for specification alignment analysis?"**

### 1.2 Why This Matters

**For Developers:**
- Choose the right tool based on empirical data
- Understand tool strengths and limitations
- Optimize development workflows

**For Framework Teams:**
- Identify specific areas for improvement
- Make data-driven development decisions
- Understand competitive positioning

**For the Industry:**
- Establish framework evaluation standards
- Push innovation in tool development
- Create reproducible comparison methods

---

## 2. Benchmark Design

### 2.1 Control Variables

**Model Held Constant**: Claude 3.5 Sonnet (October 2024) in both frameworks
- Same model version for all tests
- Same user prompt (word-for-word identical)
- Same starting conditions

**Task Held Constant**: Specification alignment analysis
- Same starting codebase
- Same specification document
- Same planted gaps (known ground truth)
- Same success criteria

### 2.2 What We're Measuring

**Core Detection Capabilities**:
1. **Type 1 Detection Rate**: Can it find missing implementations?
2. **Type 2 Detection Rate**: Can it identify incorrect implementations?
3. **Type 3 Detection Rate**: Can it find extraneous code?
4. **False Positive Rate**: Does it report misalignments that don't exist?
5. **Detection Accuracy**: Precision and recall for each type

**Framework Performance**:
1. **Search Strategy**: How does it explore the codebase?
2. **Context Usage**: How well does it understand relationships?
3. **Completeness**: Does it find all misalignments or stop early?
4. **Confidence Calibration**: How accurate are its confidence scores?

### 2.3 What We're NOT Measuring

- Model capabilities (same model in both)
- Complex prompt engineering (using simple, identical prompts)
- Edge cases (starting with straightforward test)
- User interaction patterns (minimal intervention design)

---

## 3. Test Design

### 3.1 The Todo App Test Case

**Current Implementation Focus**: We are starting with a Next.js todo application as our test case. This provides sufficient complexity while remaining manageable for initial benchmark validation.

**Structure**:
```
todo-app/
├── specs/
│   └── todo-specification.md    # Complete specification document
├── src/
│   ├── app/                     # Next.js app directory
│   │   ├── api/                 # API routes
│   │   │   ├── auth/           # Authentication endpoints
│   │   │   └── tasks/          # Task CRUD endpoints
│   │   └── admin/              # Admin interface (Type 3 misalignment)
│   ├── components/             # React components
│   └── lib/                    # Utilities and validation
└── README.md                   # Project documentation
```

### 3.2 Test Branch Structure

**Implemented Test Branches** (6 total with 38 misalignments):

| Branch | Type 1 | Type 2 | Type 3 | Total | Purpose |
|--------|--------|--------|--------|-------|---------|
| **control_perfect** | 0 | 0 | 0 | 0 | False positive baseline (MUST RUN FIRST) |
| **baseline_balanced** | 3 | 3 | 2 | 8 | Overall capability testing (H1) |
| **type1_heavy** | 6 | 1 | 1 | 8 | Type 1 specialization (H2a) |
| **type2_heavy** | 1 | 6 | 1 | 8 | Type 2 specialization (H2b) |
| **subtle_only** | 2 | 2 | 2 | 6 | Complexity handling (H3) |
| **distributed** | 3 | 3 | 2 | 8 | Context distribution (H4) |

**Ground Truth Structure**: Each branch has 4 ground truth files:
- `ground-truth-type1.json` - Type 1 misalignments only
- `ground-truth-type2.json` - Type 2 misalignments only
- `ground-truth-type3.json` - Type 3 misalignments only
- `ground-truth-combined.json` - All types combined

### 3.3 Core Misalignment Types

There are exactly **THREE** fundamental types of specification misalignment:

**Type 1: Missing Implementation**
- Specification requires feature X
- Code does not contain feature X at all
- Example: Spec requires JWT authentication, code has no authentication

**Type 2: Incorrect Implementation** 
- Specification requires feature X implemented as A
- Code implements feature X as B (different from A)
- Example: Spec requires 15-minute token expiry, code has 60-minute expiry

**Type 3: Extraneous Code**
- Code contains feature Y
- Specification does not mention feature Y at all
- Example: Code has admin dashboard, spec doesn't mention admin functionality

These three types are exhaustive - every possible misalignment falls into one of these categories.

---

## 4. Test Protocol

### 4.1 Test Prompts

**Implemented Prompts** (4 total in `benchmark/prompts/`):

1. **`type1-missing.md`** - Missing Implementation Detection
   - Focuses on finding spec requirements not in code
   - Output format: JSON with section numbers

2. **`type2-incorrect.md`** - Incorrect Implementation Detection
   - Focuses on implementations that differ from spec
   - Output format: JSON with sections and affected files

3. **`type3-extraneous.md`** - Extraneous Code Detection
   - Focuses on code not mentioned in spec
   - Output format: JSON with features and files

4. **`combined-all-types.md`** - Comprehensive Detection
   - Finds all three types in one analysis
   - Output format: JSON with all three categories

Each prompt provides clear instructions and expected JSON output format.

### 4.2 Execution Protocol

**For Each Test Branch:**
1. Switch to test branch in the repository
2. For each framework (Cursor, Claude Code):
   - Run all 4 prompts independently:
     - Type 1 detection prompt
     - Type 2 detection prompt  
     - Type 3 detection prompt
     - Combined detection prompt
   - Each prompt gets fresh context (no carryover)
   - Save each output separately

**Test Sequence Per Branch:**
```
Branch: test-set-1
├── Cursor Tests
│   ├── type1_output.json
│   ├── type2_output.json
│   ├── type3_output.json
│   └── combined_output.json
└── Claude Code Tests
    ├── type1_output.json
    ├── type2_output.json
    ├── type3_output.json
    └── combined_output.json
```

**Repetition**: Run each test 3-5 times for statistical validity

### 4.3 Measurement Points

**Primary Metrics:**
- **Accuracy**: Gaps correctly identified / Total gaps
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / Total actual gaps
- **F1 Score**: Harmonic mean of precision and recall
- **Time to completion**: Minutes from start to final output
- **Confidence calibration**: How well confidence matches correctness

**Secondary Metrics:**
- Files examined
- Search patterns used
- Token consumption
- Backtracking/corrections made

---

## 5. Statistical Rigor

### 5.1 Experimental Design

```yaml
sample_size:
  runs_per_test: 5 (minimum 3)
  test_types: 4 (type1, type2, type3, combined)
  branches: 6 (control_perfect through distributed)
  total_tests_per_framework: 120 (6 branches × 4 prompts × 5 runs)
  total_tests: 240 (both frameworks)

controls:
  - Same model version (Claude 3.5 Sonnet)
  - Identical prompts from benchmark/prompts/
  - Fresh context for each test
  - No framework-specific optimizations
  - Systematic test order (control_perfect first)
```

### 5.2 Hypothesis Framework

**Five Core Hypotheses Being Tested**:

1. **H1: Overall Performance**
   - Prediction: Claude Code > Cursor by ≥15% F1 score
   - Test: baseline_balanced branch

2. **H2: Type-Specific Specialization**
   - H2a: Cursor > Claude Code on Type 1 (missing)
   - H2b: Claude Code > Cursor on Type 2 (incorrect)
   - H2c: Cursor > Claude Code on Type 3 (extraneous)
   - Tests: type1_heavy, type2_heavy branches

3. **H3: Complexity Degradation**
   - Prediction: Claude Code handles subtle issues better
   - Test: subtle_only branch

4. **H4: Context Distribution**
   - Prediction: Cursor better with distributed misalignments
   - Test: distributed branch

5. **H5: False Positive Rate**
   - Prediction: Cursor generates 2x more false positives
   - Test: control_perfect branch

### 5.3 Statistical Analysis

**Required Calculations:**
1. **Descriptive Statistics**
   - Mean ± standard deviation for each metric
   - Median and interquartile range
   - Min/max values

2. **Inferential Statistics**
   - Paired t-test (same test, both frameworks)
   - Mann-Whitney U test (if non-normal distribution)
   - Effect size (Cohen's d)

3. **Significance Thresholds**
   - p < 0.05 for statistical significance
   - Effect sizes: small (0.2), medium (0.5), large (0.8)

### 5.4 Reporting Format

```
Example Results:
Cursor: 73% ± 8% accuracy (n=5)
Claude Code: 87% ± 5% accuracy (n=5)
Difference: 14% (p=0.03, d=0.72, medium effect)
Statistical significance: Yes
Practical significance: Meaningful difference in real-world use
```

---

## 6. Scoring Framework

### 6.1 Point System

```python
# For each misalignment type:
type_scoring = {
    "correct_detection": +1.0,     # Correctly identified misalignment
    "missed": 0.0,                 # Failed to find actual misalignment
    "false_positive": -0.25,       # Reported misalignment that doesn't exist
}

# Overall accuracy metrics:
metrics = {
    "type1_precision": correct_type1 / (correct_type1 + false_positives_type1),
    "type1_recall": correct_type1 / total_type1_in_ground_truth,
    "type2_precision": correct_type2 / (correct_type2 + false_positives_type2),
    "type2_recall": correct_type2 / total_type2_in_ground_truth,
    "type3_precision": correct_type3 / (correct_type3 + false_positives_type3),
    "type3_recall": correct_type3 / total_type3_in_ground_truth,
}
```

### 6.2 Confidence Calibration

Compare reported confidence (1-5) with actual correctness:
- Well-calibrated: High confidence when correct, low when wrong
- Overconfident: High confidence but often wrong
- Underconfident: Low confidence but often right

---

## 7. Implementation Timeline

### 7.1 Implementation Status

**Completed**:
- ✅ Todo app specification created
- ✅ 6 test branches documented with misalignments
- ✅ 38 total misalignments defined
- ✅ Ground truth files created (24 total)
- ✅ Test prompts finalized (4 types)
- ✅ Scoring system implemented
- ✅ Analysis scripts created
- ✅ Visualization tools ready

**Ready for Testing**:
- [ ] Run control_perfect branch first (establish baseline)
- [ ] Execute 5 runs × 4 prompts × 6 branches × 2 frameworks
- [ ] Score and aggregate results
- [ ] Test hypotheses and generate reports

### 7.2 Success Criteria

**Minimum Viable Benchmark:**
1. Both frameworks tested with same model
2. At least 5 runs per framework
3. Statistical analysis completed
4. Clear winner or "no significant difference"
5. Reproducible methodology documented

---

## 8. Expected Outcomes

### 8.1 Possible Findings

**Scenario A: Clear Winner**
- One framework significantly outperforms (p < 0.05, large effect)
- Specific strengths and weaknesses identified
- Clear recommendations for users

**Scenario B: Different Strengths**
- Each framework excels at different gap types
- Trade-offs identified
- Context-dependent recommendations

**Scenario C: No Significant Difference**
- Both frameworks perform similarly
- Choice comes down to other factors (UX, cost, integration)
- Validates that framework choice may not matter for this task

### 8.2 Value Regardless of Outcome

Any result provides value:
- First empirical framework comparison
- Reproducible methodology for future tests
- Baseline for framework improvements
- Community resource for decision-making

---

## 9. Limitations and Future Work

### 9.1 Current Limitations

- Single task type (specification alignment)
- Single programming language/framework
- Limited complexity (simple todo app)
- Small sample size (minimum viable)

### 9.2 Future Expansions

**If Initial Results Are Valuable:**
- More complex codebases
- Different task types (implementation, refactoring, debugging)
- Additional frameworks
- Community-contributed test cases
- Automated continuous benchmarking

---

## 10. Repository Structure (Current Implementation)

```
spec-alignment-benchmark/
├── README.md                    # Quick start guide
├── METHODOLOGY.md              # Detailed methodology
├── requirements.txt            # Python dependencies
│
├── benchmark/                  # Test definitions and prompts
│   ├── branches/              # Branch-specific documentation
│   │   ├── control_perfect/  # Control branch (0 misalignments)
│   │   ├── baseline_balanced/# Balanced test (8 misalignments)
│   │   └── [4 more branches]
│   ├── prompts/              # Test prompts
│   ├── hypotheses.md         # Scientific hypotheses
│   └── test-summary.md       # Test overview
│
├── scripts/                   # Analysis tools
│   ├── score_result.py       # Individual test scoring
│   ├── test_runner.py        # Test execution management
│   ├── aggregate_results.py  # Statistical aggregation
│   ├── compare_frameworks.py # Hypothesis testing
│   └── visualize_results.py  # Chart generation
│
├── results/                   # Test outputs (created during testing)
│   ├── raw/                  # Framework outputs
│   ├── processed/            # Scored results
│   └── analysis/             # Aggregated analysis
│
└── specs/                     # Specifications
    ├── benchmark-specification.md  # This document
    └── repository-specification.md # Repository details
```

### 10.2 Contribution Guidelines

- Test case contributions welcome
- Framework additions encouraged
- Methodology improvements via PR
- Results reproduction valued

---

## Summary

This benchmark creates a new evaluation category: framework comparison with model held constant. By testing Cursor and Claude Code with the same Claude 3.5 Sonnet model on identical specification alignment tasks, we can finally answer which framework better amplifies the model's capabilities.

**Key Design Decisions:**
- Start simple (todo app) but scientifically rigorous
- Measure what matters (accuracy, speed, completeness)
- Statistical validity even with small sample
- Open methodology for community validation

**Expected Impact:**
- Empirical data for tool selection
- Specific improvement targets for frameworks
- Foundation for framework benchmark ecosystem
- Push toward better developer tools

The goal isn't to declare a "winner" but to understand trade-offs and help both users and builders make better decisions.