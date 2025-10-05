# Prompt Library for Specification Alignment Benchmark

## Overview

This directory contains the four prompts used to test AI coding assistant frameworks on specification alignment detection. Each prompt targets specific misalignment types or combines them.

## The Three Misalignment Types

1. **Type 1 - Missing**: Spec requires X, code doesn't have X
2. **Type 2 - Incorrect**: Spec requires X as A, code implements X as B  
3. **Type 3 - Extraneous**: Code has Y, spec doesn't mention Y

## Prompts

### Individual Type Detection
- `type1-missing.md` - Detects missing implementations only
- `type2-incorrect.md` - Detects incorrect implementations only
- `type3-extraneous.md` - Detects extraneous code only

### Combined Detection
- `combined-all-types.md` - Detects all three types in one pass

## Test Protocol

For each test branch:
1. Run all 4 prompts separately with fresh context
2. Save outputs as JSON
3. Compare against ground truth
4. Calculate precision and recall for each type

## Important Path Structure

The specification document must be located at: `specs/project-specification.md`

This path is hardcoded in all prompts. Ensure your test repository follows this structure:
```
test-repo/
└── specs/
    └── project-specification.md
```

## Usage Instructions

1. **Setup**: Load test repository branch in framework
2. **Copy**: Copy entire prompt exactly as written
3. **Paste**: Paste into framework without modification
4. **Execute**: Let framework analyze without intervention
5. **Save**: Save JSON output for analysis

## Important Rules

- **NO modifications** to prompts between frameworks
- **NO additional context** or hints
- **NO intervention** during execution
- **Fresh context** for each prompt (no carryover)

## Output Format

All prompts produce structured JSON with:
- Categorized findings by type
- Confidence scores (1-5)
- File references
- Summary statistics

This ensures consistent, comparable outputs across frameworks.