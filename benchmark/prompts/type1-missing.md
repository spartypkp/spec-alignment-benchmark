# Type 1 Detection: Missing Implementation

Copy and paste this entire prompt exactly as shown:

---

You are analyzing a codebase to identify **Type 1 misalignments**: features that are specified in the documentation but are completely MISSING from the implementation.

## Your Task

1. Read the specification document at: `specs/project-specification.md`
2. Systematically check if each specified feature exists in the codebase
3. Identify features that are completely absent from the code

## Definition of Type 1 (Missing)

A Type 1 misalignment occurs when:
- The specification explicitly requires feature X
- The codebase contains NO implementation of feature X whatsoever
- There is no code attempting to provide that functionality

This is NOT Type 1 if:
- The feature exists but works differently (that's Type 2)
- The feature is partially implemented (that's Type 2)
- The feature is commented out but code exists (that's Type 2)

## Examples

**Type 1 (Report these):**
- Spec requires JWT auth, code has no authentication at all
- Spec requires rate limiting, no rate limiting code exists
- Spec requires API documentation, no docs exist

**NOT Type 1 (Don't report):**
- Spec requires 15-min tokens, code has 60-min tokens
- Spec requires JSON logs, code uses plain text logs
- Spec requires 80% coverage, code has 30% coverage

## Output Format

Output your findings as a JSON object with this exact structure:

```json
{
  "misalignments": [
    {
      "section": "4.1",
      "reasoning": "Password field exists but no validation for 6-character minimum is implemented in either client or server code"
    },
    {
      "section": "3.1",
      "reasoning": "Sessions are created but no expiry logic found in auth.ts or login route"
    },
    {
      "section": "2.4",
      "reasoning": "Dashboard exists but statistics bar component is completely missing"
    }
  ]
}
```

**Required fields**:
- `section`: The section NUMBER from the specification (e.g., "4.1", "3.1", "2.4")
- `reasoning`: Brief explanation of what is missing and why you concluded it's absent

**Important**: 
- Use ONLY the section number, not the full title
- Keep reasoning concise but specific
- Be certain the feature is COMPLETELY missing before reporting

## Important Notes

- Only report features that are COMPLETELY MISSING
- Be thorough - check the entire codebase before concluding something is missing
- Check common locations and alternative implementations before reporting
- Include clear reasoning for each finding

Begin your analysis now. Focus ONLY on Type 1 (missing) misalignments.
