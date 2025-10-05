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

Output your findings as a JSON object with section headers and the files containing incorrect implementations:

```json
{
  "analysis_type": "type2_incorrect",
  "type2_incorrect": [
    {
      "section": "3.1 Request/Response Format",
      "files": ["middleware/errorHandler.ts", "lib/apiResponse.ts"]
    },
    {
      "section": "5.1 Coverage Requirements",
      "files": ["package.json"]
    }
  ]
}
```

**Important**:
- Use EXACT section headers from the specification
- List ALL files that contain the incorrect implementation
- Use relative file paths from the repository root
- Do NOT include explanations of what's wrong
- Only the section header and file paths are needed

## Important Notes

- Only report features that EXIST but work DIFFERENTLY than specified
- Check implementation details carefully  
- Don't report missing features (those are Type 1)
- Return exact section headers and file paths only

Begin your analysis now. Focus ONLY on Type 2 (incorrect) misalignments.
