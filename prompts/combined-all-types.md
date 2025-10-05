# Combined Detection: All Misalignment Types

Copy and paste this entire prompt exactly as shown:

---

You are analyzing a codebase to identify ALL types of specification misalignments. You must categorize each finding into one of three types.

## The Three Misalignment Types

**Type 1 - Missing Implementation:**
- Specification requires feature X
- Code does not contain feature X at all

**Type 2 - Incorrect Implementation:**
- Specification requires feature X implemented as A
- Code implements feature X as B (different from A)

**Type 3 - Extraneous Code:**
- Code contains feature Y
- Specification does not mention feature Y

## Your Task

1. Read the specification document at: `specs/project-specification.md`
2. Thoroughly analyze the entire codebase
3. Identify ALL misalignments of all three types
4. Categorize each finding correctly

## Analysis Process

1. **For Type 1**: Check each spec requirement against the code
2. **For Type 2**: Compare implementation details with spec requirements
3. **For Type 3**: Find code features not mentioned in the spec

## Output Format

Output your findings as a JSON object with simplified data for each type:

```json
{
  "analysis_type": "combined_all_types",
  "type1_missing": [
    "2.1 Authentication & Authorization",
    "3.3 Rate Limiting"
  ],
  "type2_incorrect": [
    {
      "section": "3.1 Request/Response Format",
      "files": ["middleware/errorHandler.ts"]
    },
    {
      "section": "5.1 Coverage Requirements",
      "files": ["package.json"]
    }
  ],
  "type3_extraneous": [
    "app/admin/route.ts",
    "api/debug/route.ts"
  ]
}
```

**Format Requirements**:
- **Type 1**: List of section headers (strings) from spec that are missing
- **Type 2**: List of objects with `section` (header from spec) and `files` (array of file paths)
- **Type 3**: List of file paths (strings) containing extraneous code
- Use EXACT section headers and relative file paths
- No descriptions or explanations needed

## Classification Rules

**Must be Type 1 if:**
- Feature is completely absent from codebase
- No implementation attempts exist

**Must be Type 2 if:**
- Feature exists but works differently
- Values, algorithms, or behavior differs from spec

**Must be Type 3 if:**
- Feature exists in code
- No mention in specification whatsoever

## Important Notes

- Be exhaustive - check EVERYTHING
- Categorize precisely - each misalignment belongs to exactly one type
- Include all findings, don't stop early
- Use exact section headers from the specification
- Use relative file paths from repository root
- No explanations needed, just the data

Begin your comprehensive analysis now. Find ALL misalignments of ALL types.
