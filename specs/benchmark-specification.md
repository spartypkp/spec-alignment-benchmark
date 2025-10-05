# Framework Benchmark: Cursor vs Claude Code

**Version:** 0.1.0
**Created:** October 5, 2025
**Purpose:** Compare AI coding assistant frameworks (not models) on specification alignment tasks
**Model:** Claude 3.5 Sonnet (held constant across frameworks)

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

**Structure** (5-7 files):
```
todo-app/
├── todo-spec.md          # The specification document
├── README.md             # Basic project info
├── app.py                # Main application
├── models.py             # Data models
├── api.py                # API routes
├── auth.py               # Authentication (partial)
└── tests/
    └── test_api.py       # Basic tests (incomplete)
```

### 3.2 Test Branch Structure

Each test branch contains a specific mix of the three misalignment types:

**Example Test Branch Configuration:**

```
Branch: test-set-1
├── Type 1 Misalignments (Missing): 3 instances
│   - JWT authentication not implemented
│   - Rate limiting completely absent
│   - API documentation missing
│
├── Type 2 Misalignments (Incorrect): 3 instances  
│   - Token expiry time wrong (60min instead of 15min)
│   - Error format inconsistent with spec
│   - Database operations without required transactions
│
└── Type 3 Misalignments (Extraneous): 2 instances
    - Admin dashboard (not in spec)
    - Debug endpoints (not in spec)
```

Each branch has a `ground-truth.json` file documenting exact misalignments.

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

We use **FOUR** distinct prompts to test misalignment detection:

**Prompt 1: Type 1 Detection (Missing Implementation)**
- Focus: Find features in spec that are completely missing from code
- Output: List of missing features

**Prompt 2: Type 2 Detection (Incorrect Implementation)**
- Focus: Find features that exist but are implemented differently than specified
- Output: List of incorrect implementations with differences

**Prompt 3: Type 3 Detection (Extraneous Code)**
- Focus: Find features in code that are not mentioned in the specification
- Output: List of undocumented features

**Prompt 4: Combined Detection (All Types)**
- Focus: Comprehensive analysis finding all three misalignment types
- Output: Categorized list of all misalignments

Each prompt is run independently on the same test branch.

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
  runs_per_framework: 5 minimum (10 preferred)
  total_runs: 10 minimum (20 preferred)

randomization:
  - Alternate starting framework
  - Vary time of day
  - Use fresh sessions

controls:
  - Same model version (Claude 3.5 Sonnet)
  - Identical prompts
  - Same test environment
  - No framework-specific optimizations
```

### 5.2 Statistical Analysis

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

### 5.3 Reporting Format

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

### 7.1 Phase 1: Proof of Concept (This Week)

**Day 1-2: Setup**
- [ ] Create todo app with planted gaps
- [ ] Write clear specification document
- [ ] Prepare identical prompts
- [ ] Set up measurement framework

**Day 3-4: Execution**
- [ ] Run 5 tests on Cursor
- [ ] Run 5 tests on Claude Code
- [ ] Collect all metrics
- [ ] Document observations

**Day 5: Analysis**
- [ ] Calculate statistics
- [ ] Create visualizations
- [ ] Write findings report
- [ ] Share initial results

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

## 10. Open Source Plan

### 10.1 Repository Contents

```
framework-benchmarks/
├── README.md                  # Quick start guide
├── METHODOLOGY.md            # This document
├── test-cases/               # All test repositories
├── results/                  # Raw and processed data
├── analysis/                 # Jupyter notebooks
└── scripts/                  # Automation tools
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