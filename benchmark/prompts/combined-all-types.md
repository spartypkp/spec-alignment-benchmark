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
      "section": "16.2",
      "reasoning": "User activity logging system not implemented anywhere in codebase"
    },
    {
      "section": "17.1",
      "reasoning": "Automated testing endpoints specified but completely absent"
    }
  ],
  "type2_incorrect": [
    {
      "section": "18.3",
      "reasoning": "Cache TTL set to 3600 seconds instead of specified 300 seconds",
      "files": ["src/lib/cache.ts"]
    },
    {
      "section": "19.2",
      "reasoning": "API versioning uses header instead of URL path as specified",
      "files": ["src/middleware/version.ts", "src/app/api/route.ts"]
    }
  ],
  "type3_extraneous": [
    {
      "file": "src/components/ThemeToggle.tsx",
      "reasoning": "Dark/light theme toggle component not mentioned in requirements"
    },
    {
      "file": "src/app/api/webhooks/route.ts",
      "reasoning": "Webhook endpoint not specified in API documentation"
    },
    {
      "file": "src/lib/events.ts",
      "reasoning": "Event system implementation not mentioned in specification"
    }
  ]
}
```

**Format Requirements**:
- **Type 1**: Array of objects with `section` (number only) and `reasoning`
- **Type 2**: Array of objects with `section`, `reasoning`, and `files` array
- **Type 3**: Array of objects with `file` (single path) and `reasoning`
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
