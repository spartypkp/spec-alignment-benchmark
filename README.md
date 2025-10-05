# Specification Alignment Benchmark

A benchmark for testing AI coding assistant frameworks (Cursor, Claude Code, etc.) on their ability to detect misalignments between code and specifications.

## 🎯 What This Does

This benchmark tests how well AI coding frameworks can find three types of specification misalignments:

1. **Type 1 - Missing**: Features in the spec but not in code
2. **Type 2 - Incorrect**: Features implemented differently than specified  
3. **Type 3 - Extraneous**: Features in code but not in the spec

By using the same AI model (Claude 3.5 Sonnet) across different frameworks, we isolate and measure framework-specific capabilities like search, context management, and code understanding.

## 🚀 Quick Start

### 1. Try the Example

```bash
# Score a sample output against ground truth
python3 scripts/score.py examples/sample-llm-output.json examples/sample-ground-truth.json
```

You'll see precision, recall, and F1 scores for each misalignment type.

### 2. Run Your Own Test

**Step 1**: Create a test repository with planted misalignments and a ground truth file:

```json
{
  "type1_missing": ["2.1 Authentication & Authorization"],
  "type2_incorrect": [
    {"section": "3.1 Error Handling", "files": ["middleware/errors.ts"]}
  ],
  "type3_extraneous": ["app/admin/route.ts"]
}
```

**Step 2**: Load the test repo in your framework (Cursor, Claude Code, etc.)

**Step 3**: Copy and run each prompt from `prompts/`:
- `type1-missing.md` - Find missing features
- `type2-incorrect.md` - Find incorrect implementations
- `type3-extraneous.md` - Find extra code
- `combined-all-types.md` - Find all three types

**Step 4**: Score the results:

```bash
python3 scripts/score.py output.json ground-truth.json
```

## 📊 How Scoring Works

The benchmark uses simple, objective scoring:

- **Type 1 & 3**: Simple set intersection (did they find the right sections/files?)
- **Type 2**: Section + file matching (right section + at least one correct file)
- **Scoring**: +1 for correct, -0.25 for false positive, 0 for missed

No fuzzy matching, no subjective interpretation - just exact string comparison.

## 📁 Repository Structure

```
spec-alignment-benchmark/
├── prompts/          # The 4 test prompts
├── scripts/          # Scoring and validation tools
├── examples/         # Sample inputs and outputs
├── docs/            # Detailed documentation
└── specs/           # Methodology and design docs
```

## 🔬 The Three Misalignment Types

### Type 1: Missing Implementation
**What**: Spec says "must have X", code doesn't have X  
**Example**: Spec requires JWT auth, code has no auth  
**Output**: List of missing section headers

### Type 2: Incorrect Implementation  
**What**: Spec says "X should work like A", code implements X as B  
**Example**: Spec requires 15-min token expiry, code has 60-min  
**Output**: Section headers + files with wrong implementation

### Type 3: Extraneous Code
**What**: Code has Y, spec never mentions Y  
**Example**: Code has admin panel, spec doesn't mention admin features  
**Output**: List of files containing unspecified features

## 📈 Understanding Results

```
TYPE1 Results:
  Precision: 66.7%  ← Of 3 reported, 2 were correct
  Recall:    66.7%  ← Found 2 out of 3 actual issues
  F1 Score:  0.667  ← Harmonic mean
  Score:     1.75   ← 2 correct - 0.25 penalty for false positive
```

- **High Precision**: Few false alarms
- **High Recall**: Finds most issues
- **High F1**: Good balance of both

## 🛠️ Testing Your Own Framework

1. Create test branches with known misalignments
2. Document them in `ground-truth.json`
3. Run the 4 prompts in your framework
4. Save outputs as JSON
5. Score with `score.py`
6. Compare results across frameworks

## 📖 Documentation

- [Methodology](METHODOLOGY.md) - Detailed explanation of approach
- [Test Execution Protocol](docs/test-execution-protocol.md) - Step-by-step testing guide
- [Ground Truth Format](docs/ground-truth-format.md) - How to create answer keys
- [Examples](examples/README.md) - Working examples with explanation

## 🤝 Contributing

We welcome contributions! Priority areas:
- Test repositories with different patterns
- Statistical analysis tools
- Support for more frameworks
- Visualization of results

## 📜 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

This benchmark fills a gap in AI tool evaluation by testing frameworks rather than models, helping developers choose the right tools for specification alignment tasks.