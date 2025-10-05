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

Output your findings as a JSON object containing ONLY the section headers from the specification that have missing implementations:

```json
{
  "analysis_type": "type1_missing",
  "type1_missing": [
    "2.1 Authentication & Authorization",
    "3.3 Rate Limiting",
    "6.1 API Documentation"
  ]
}
```

**Important**: 
- List ONLY the section headers (e.g., "2.1 Authentication & Authorization")
- Use the EXACT section headers as they appear in the specification
- Do NOT include descriptions or explanations
- Order doesn't matter

## Important Notes

- Only report features that are COMPLETELY MISSING
- Be thorough - check the entire codebase before concluding something is missing
- Check common locations and alternative implementations before reporting
- Return the exact section headers from the specification

Begin your analysis now. Focus ONLY on Type 1 (missing) misalignments.
