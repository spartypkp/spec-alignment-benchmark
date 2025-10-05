# Specification Alignment Benchmark Methodology

## Core Concept

We test how well AI coding assistant frameworks (Cursor, Claude Code) can detect misalignments between code and specifications when using the same AI model (Claude 3.5 Sonnet).

## The Three Misalignment Types

Every possible specification misalignment falls into one of these three categories:

### Type 1: Missing Implementation
- **Definition**: Spec requires X, code doesn't have X
- **Example**: Spec requires JWT authentication, code has no authentication

### Type 2: Incorrect Implementation  
- **Definition**: Spec requires X implemented as A, code implements X as B
- **Example**: Spec requires 15-minute token expiry, code has 60-minute expiry

### Type 3: Extraneous Code
- **Definition**: Code has Y, spec doesn't mention Y
- **Example**: Code has admin dashboard, spec doesn't mention admin features

## Test Structure

### Repository Organization

```
todo-app-repo/                    # Separate repository with test code
├── specs/
│   └── project-specification.md  # The specification (same path in all branches)
├── main branch                   # Perfectly aligned code and spec
├── test-set-1 branch            # Planted misalignments (mix of types)
├── test-set-2 branch            # Different misalignments
└── test-set-3 branch            # Edge cases and subtle misalignments

spec-alignment-benchmark/         # This repository with methodology
├── prompts/                      # The 4 test prompts
├── results/                      # Test outputs
├── scripts/                      # Analysis tools
└── docs/                         # Documentation
```

### The Four Tests

For each test branch, we run 4 separate prompts:

1. **Type 1 Detection**: Find missing implementations only
2. **Type 2 Detection**: Find incorrect implementations only
3. **Type 3 Detection**: Find extraneous code only
4. **Combined Detection**: Find all three types in one pass

## Test Process

### 1. Setup Phase
- Create test branches with known misalignments
- Document exact misalignments in `ground-truth.json`
- Remove ground truth before testing (blind test)

### 2. Execution Phase
For each framework (Cursor, Claude Code):
- Load test branch
- Run each of the 4 prompts separately
- Fresh context for each prompt (no carryover)
- Save JSON outputs

### 3. Scoring Phase
- Compare outputs against ground truth
- Calculate precision and recall for each type
- Measure false positive rate
- Generate statistical analysis

## Measurement Metrics

### Per Type Metrics
- **Detection Rate**: How many misalignments of this type were found?
- **Precision**: Of the things reported, how many were correct?
- **Recall**: Of the actual misalignments, how many were found?
- **F1 Score**: Harmonic mean of precision and recall

### Overall Metrics
- **Total Accuracy**: All misalignments found / Total misalignments
- **Type Classification**: Are misalignments categorized correctly?
- **False Positive Rate**: How many non-existent issues reported?
- **Completeness**: Does it find everything or stop early?

## Why This Methodology?

### Scientific Rigor
- **Controlled Variables**: Same model, same prompts, same test cases
- **Isolated Testing**: Each type tested separately AND together
- **Known Ground Truth**: Exact answer key for objective scoring
- **Multiple Runs**: Statistical validity through repetition

### Practical Value
- **Real-World Task**: Specification alignment is a common developer need
- **Clear Categories**: Three types cover all possible misalignments
- **Actionable Results**: Shows specific strengths/weaknesses
- **Fair Comparison**: No framework-specific advantages

## Key Principles

1. **Simplicity**: Only 3 fundamental misalignment types
2. **Completeness**: These 3 types cover every possible case
3. **Objectivity**: Clear ground truth enables objective scoring
4. **Reproducibility**: Anyone can run the same tests
5. **Fairness**: Identical conditions for both frameworks

## Expected Insights

This benchmark will reveal:
- Which framework better detects missing features (Type 1)
- Which framework better identifies incorrect implementations (Type 2)
- Which framework better finds extraneous code (Type 3)
- Whether combined detection differs from individual detection
- How search strategies differ between frameworks
- Which framework has better precision vs recall trade-offs

## Next Steps

1. **Create Test Repository**: Build app with perfect alignment first
2. **Plant Misalignments**: Create test branches with known issues
3. **Run Tests**: Execute all prompts on both frameworks
4. **Analyze Results**: Score against ground truth
5. **Share Findings**: Publish results and methodology

This methodology provides the first rigorous comparison of AI coding frameworks (not models) on a practical development task.
