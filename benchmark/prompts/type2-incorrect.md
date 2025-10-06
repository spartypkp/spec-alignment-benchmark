# Type 2 Detection: Incorrect Implementation

Copy and paste this entire prompt exactly as shown:

---

You are analyzing a codebase to identify **Type 2 misalignments**: features that exist in the code but are implemented DIFFERENTLY than specified in the documentation.

## Your Task

1. Read the specification document at: `specs/project-specification.md`
2. Find features that are implemented in the code
3. Compare the implementation details against the specification
4. Identify where implementations differ from specifications

## Definition of Type 2 (Incorrect)

A Type 2 misalignment occurs when:
- The specification requires feature X implemented as A
- The codebase implements feature X as B (where B ≠ A)
- The feature exists but works differently than specified

Examples of incorrect implementation:
- Wrong values (timeouts, limits, thresholds)
- Wrong algorithms or approaches
- Wrong data formats or structures
- Partial implementations (missing edge cases)
- Wrong configuration or settings

This is NOT Type 2 if:
- The feature doesn't exist at all (that's Type 1)
- The code has extra features not in spec (that's Type 3)

## Examples

**Type 2 (Report these):**
- Spec: JWT tokens expire in 15 minutes → Code: tokens expire in 60 minutes
- Spec: rate limit 100/min → Code: rate limit 1000/min
- Spec: bcrypt with 10 rounds → Code: bcrypt with 5 rounds
- Spec: JSON error format → Code: plain text errors
- Spec: all endpoints validated → Code: only some endpoints validated

**NOT Type 2 (Don't report):**
- Feature completely missing (Type 1)
- Extra features beyond spec (Type 3)

## Output Format

Output your findings as a JSON object with this exact structure:

```json
{
  "misalignments": [
    {
      "section": "13.3",
      "reasoning": "Spec requires pagination with 20 items per page, but code returns 50 items per page",
      "files": ["src/app/api/list/route.ts"]
    },
    {
      "section": "14.1",
      "reasoning": "Spec requires SHA-256 hashing for data integrity, but code uses MD5 hashing",
      "files": ["src/lib/crypto.ts", "src/services/hash-service.ts"]
    },
    {
      "section": "15.4",
      "reasoning": "Spec requires UTC timezone for all timestamps, but code uses local server time",
      "files": ["src/models/base.ts"]
    }
  ]
}
```

**Required fields**:
- `section`: The section NUMBER from the specification (e.g., "13.3", "14.1", "15.4")
- `reasoning`: Brief explanation of what the spec requires vs what the code does
- `files`: Array of relative file paths where the incorrect implementation exists

**Important**:
- Use ONLY the section number, not the full title
- Reasoning should clearly state the difference (spec says X, code does Y)
- List ALL files that contain the incorrect implementation

## Important Notes

- Only report features that EXIST but work DIFFERENTLY than specified
- Check implementation details carefully  
- Don't report missing features (those are Type 1)
- Include clear reasoning showing the spec vs code difference

Begin your analysis now. Focus ONLY on Type 2 (incorrect) misalignments.
