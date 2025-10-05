# Framework Benchmark Hypotheses

## Overview
This document defines the scientific hypotheses being tested comparing **Cursor** and **Claude Code** on specification alignment detection tasks. Both frameworks will use Claude 4.5 Sonnet, allowing us to isolate framework-specific capabilities.

## Framework Characteristics
- **Cursor**: IDE-integrated, emphasizes code context, file-aware, tends toward completeness
- **Claude Code**: Chat-based, emphasizes reasoning, explanation-focused, tends toward precision

---

## Primary Hypotheses

### H1: Overall Detection Capability
**Statement**: "Claude Code will achieve significantly higher overall F1 score than Cursor across all misalignment types."

**Prediction**: Claude Code F1 score > Cursor F1 score by ≥15%

**Reasoning**: Claude Code's chat-based interface may encourage more systematic analysis, while Cursor's IDE integration might lead to premature focus on specific files.

**Null Hypothesis (H0)**: No significant difference in overall F1 scores (p > 0.05)

**Metrics**:
- Primary: Combined F1 score across all types
- Secondary: Total true positives, false positives, false negatives

**Tested By**: All branches, particularly baseline_balanced

---

### H2: Type-Specific Specialization
**Statement**: "Cursor and Claude Code will show opposite strengths across misalignment types."

**Specific Predictions**:
- **H2a**: Cursor > Claude Code on Type 1 (missing implementations)
  - *Reasoning*: Cursor's file tree visibility makes missing components more obvious
- **H2b**: Claude Code > Cursor on Type 2 (incorrect implementations)  
  - *Reasoning*: Claude Code's reasoning focus better identifies subtle logic errors
- **H2c**: Cursor > Claude Code on Type 3 (extraneous code)
  - *Reasoning*: Cursor's file explorer makes unexpected files immediately visible

**Null Hypothesis (H0)**: No interaction effect between framework and misalignment type

**Metrics**:
- Type-specific precision and recall
- Interaction effect in 2-way ANOVA (framework × type)

**Tested By**: type1_heavy, type2_heavy, (optional: type3_heavy)

**Expected Outcome**: Significant interaction effect (p < 0.01) with opposite performance patterns

---

### H3: Complexity Degradation
**Statement**: "Claude Code will show less performance degradation than Cursor as misalignment subtlety increases."

**Prediction**: 
- Obvious misalignments: Cursor ≈ Claude Code (within 5%)
- Subtle misalignments: Claude Code > Cursor by ≥20%

**Reasoning**: Claude Code's systematic reasoning approach should maintain effectiveness on subtle issues, while Cursor's visual/file-based approach may miss non-obvious problems.

**Null Hypothesis (H0)**: Performance degradation from obvious to subtle is equal for both frameworks

**Metrics**:
- Accuracy difference between obvious_only and subtle_only branches
- Slope of performance degradation

**Tested By**: subtle_only compared to baseline_balanced

---

### H4: Context Distribution Effect
**Statement**: "Cursor will outperform Claude Code when misalignments are distributed across many files."

**Prediction**:
- Concentrated (2-3 files): Claude Code > Cursor by ~10%
- Distributed (8+ files): Cursor > Claude Code by ~15%

**Reasoning**: Cursor's file tree and IDE integration provide better navigation for distributed issues, while Claude Code excels at deep analysis of focused areas.

**Null Hypothesis (H0)**: No difference in how frameworks handle concentrated vs distributed misalignments

**Metrics**:
- F1 score difference between baseline_balanced and distributed
- File coverage (% of files with misalignments that were examined)

**Tested By**: distributed branch compared to baseline_balanced

---

### H5: False Positive Generation
**Statement**: "Cursor will generate significantly more false positives than Claude Code."

**Prediction**: Cursor false positive rate > 2x Claude Code's rate

**Reasoning**: Cursor's emphasis on completeness and file scanning may lead to over-reporting, while Claude Code's reasoning-first approach should reduce spurious detections.

**Null Hypothesis (H0)**: No significant difference in false positive rates between frameworks

**Metrics**:
- False positive rate (FP / (FP + TN))
- Precision scores
- Control branch detections (any detection = false positive)

**Tested By**: 
- **Primary**: control_perfect branch (pure false positive test)
- **Secondary**: All branches, aggregated analysis

---

## Statistical Analysis Plan

### Required Sample Sizes
- Minimum: 3 runs per test per branch = 60 data points per framework
- Recommended: 5 runs per test per branch = 100 data points per framework

### Primary Analyses
1. **Overall Comparison**: Paired t-test on combined F1 scores
2. **Type-Specific**: 2-way repeated measures ANOVA (framework × type)
3. **Complexity**: Linear regression on subtlety scores
4. **Distribution**: Paired t-test on concentrated vs distributed

### Effect Size Interpretation
- Small: d = 0.2 (potentially meaningful)
- Medium: d = 0.5 (practically significant)
- Large: d = 0.8 (major difference)

### Significance Threshold
- α = 0.05 for all hypothesis tests
- Bonferroni correction for multiple comparisons when needed

---

## Success Criteria

The benchmark will be considered successful if:
1. At least one hypothesis shows statistically significant results
2. Effect sizes are medium or large for significant findings
3. Results are consistent across multiple runs (low variance)
4. Findings provide actionable insights for tool selection

---

## Reporting Template

For each hypothesis:
```
H[X] Result: [SUPPORTED/REJECTED/MIXED]
Statistical Test: [test type]
Cursor: M = X.XX (SD = X.XX)
Claude Code: M = X.XX (SD = X.XX)  
Difference: X.XX, p = X.XXX, d = X.XX
Interpretation: [practical meaning]
Recommendation: [actionable insight]
```

---

## Summary of Predictions

### Overall Winner
**Prediction**: Claude Code will be the overall winner with ~15% higher F1 score

### Specific Strengths
**Cursor Strengths**:
- Better at Type 1 (missing implementations) - file visibility advantage
- Better at Type 3 (extraneous code) - unexpected files stand out
- Superior on distributed misalignments - IDE navigation advantage
- Higher false positive rate (completeness over precision)

**Claude Code Strengths**:
- Better at Type 2 (incorrect implementations) - reasoning advantage  
- Superior on subtle misalignments - systematic analysis
- Better precision (fewer false positives)
- More consistent performance across complexity levels

### Decision Tree for Users
```
If your main concern is:
- Finding ALL issues → Cursor (accepts false positives)
- Finding CORRECT issues → Claude Code (higher precision)
- Reviewing large codebases → Cursor (better navigation)
- Understanding complex logic → Claude Code (better reasoning)
```

### Risk of Being Wrong
If these predictions are incorrect, it likely means:
1. IDE integration matters less than expected
2. Both frameworks use similar underlying search strategies
3. The model (Claude 3.5 Sonnet) dominates framework differences
4. Our assumptions about framework design are outdated

Any outcome provides valuable insights for the community.
