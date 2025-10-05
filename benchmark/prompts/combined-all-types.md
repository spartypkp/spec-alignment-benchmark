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

Output your findings as a JSON object with all three types of misalignments:

```json
{
  "type1_missing": [
    {
      "section": "4.1",
      "reasoning": "Password validation for 6-character minimum not implemented"
    },
    {
      "section": "3.1",
      "reasoning": "Session expiry logic completely missing"
    }
  ],
  "type2_incorrect": [
    {
      "section": "2.4",
      "reasoning": "Tasks sorted oldest first (ASC) instead of newest first (DESC)",
      "files": ["src/app/api/tasks/route.ts"]
    },
    {
      "section": "4.2",
      "reasoning": "Error format missing required code field",
      "files": ["src/app/api/auth/login/route.ts", "src/app/api/auth/register/route.ts"]
    }
  ],
  "type3_extraneous": [
    {
      "feature": "Admin Dashboard",
      "reasoning": "Admin interface not mentioned in specification",
      "files": ["src/app/admin/page.tsx"]
    },
    {
      "feature": "Export API",
      "reasoning": "CSV export functionality not specified",
      "files": ["src/app/api/export/route.ts"]
    }
  ]
}
```

**Format Requirements**:
- **Type 1**: Array of objects with `section` (number only) and `reasoning`
- **Type 2**: Array of objects with `section`, `reasoning`, and `files` array
- **Type 3**: Array of objects with `feature`, `reasoning`, and `files` array
- Use section NUMBERS only (e.g., "4.1", not "4.1 Input Validation")
- Keep reasoning concise but specific

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
- Use section numbers only (not full titles)
- Use relative file paths from repository root
- Include clear, concise reasoning for each finding

Begin your comprehensive analysis now. Find ALL misalignments of ALL types.
