# Combined Detection: All Misalignment Types

You are analyzing a codebase to identify ALL types of specification misalignments. You must categorize each finding into one of three types.

## The Three Misalignment Types

### Type 1 - Missing Implementation
A Type 1 misalignment occurs when:
- The specification explicitly requires feature X
- The codebase contains NO implementation of feature X whatsoever
- There is no code attempting to provide that functionality

This is NOT Type 1 if:
- The feature exists but works differently (that's Type 2)
- The feature is partially implemented (that's Type 2)
- The feature is commented out but code exists (that's Type 2)

### Type 2 - Incorrect Implementation
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

### Type 3 - Extraneous Code
A Type 3 misalignment occurs when:
- The codebase contains feature Y
- The specification does not mention feature Y at all
- This is undocumented/unspecified functionality

Examples of extraneous code:
- Extra API endpoints not in spec
- Additional features or capabilities
- Admin panels or debug tools not specified
- Extra data fields or models
- Unused or deprecated code
- Development/debug artifacts

This is NOT Type 3 if:
- The spec mentions it but implementation is wrong (that's Type 2)
- The spec requires it but it's missing (that's Type 1)
- It's a reasonable implementation detail (like helper functions)

## Examples

### Type 1 Examples (Report these):
- Spec requires JWT auth, code has no authentication at all
- Spec requires rate limiting, no rate limiting code exists
- Spec requires API documentation, no docs exist

### Type 1 NOT to Report:
- Spec requires 15-min tokens, code has 60-min tokens (that's Type 2)
- Spec requires JSON logs, code uses plain text logs (that's Type 2)
- Spec requires 80% coverage, code has 30% coverage (that's Type 2)

### Type 2 Examples (Report these):
- Spec: JWT tokens expire in 15 minutes → Code: tokens expire in 60 minutes
- Spec: rate limit 100/min → Code: rate limit 1000/min
- Spec: bcrypt with 10 rounds → Code: bcrypt with 5 rounds
- Spec: JSON error format → Code: plain text errors
- Spec: all endpoints validated → Code: only some endpoints validated

### Type 2 NOT to Report:
- Feature completely missing (that's Type 1)
- Extra features beyond spec (that's Type 3)

### Type 3 Examples (Report these):
- Code has admin dashboard, spec doesn't mention admin features
- Code has /debug endpoints, spec doesn't mention debugging
- Code has user profiles, spec only mentions basic user auth
- Code has analytics tracking, spec doesn't mention analytics
- Code has deprecated v1 API, spec only describes v2

### Type 3 NOT to Report:
- Internal helper functions and utilities
- Standard error handling (if spec mentions errors generally)
- Common patterns like health checks (often implied)
- Implementation details that support specified features

## Your Task

1. Read the specification document at: `specs/project-specification.md`
2. Thoroughly analyze the entire codebase
3. Identify ALL misalignments of all three types
4. Categorize each finding correctly
5. Be exhaustive - check EVERYTHING

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

**Required fields**:
- **Type 1**: Objects with `section` (section NUMBER only) and `reasoning`
- **Type 2**: Objects with `section`, `reasoning`, and `files` array
- **Type 3**: Objects with `file` (relative file path) and `reasoning`

**Important formatting**:
- Use ONLY section numbers, not full titles (e.g., "4.1", not "4.1 Input Validation")
- Keep reasoning concise but specific
- For Type 2, list ALL files that contain the incorrect implementation
- For Type 3, list each file separately with its own reasoning
- Use exact relative paths from repository root

## Important Notes

- **Type 1**: Only report features that are COMPLETELY MISSING
- **Type 2**: Only report features that EXIST but work DIFFERENTLY than specified
- **Type 3**: Focus on significant extraneous code, not implementation details
- Be thorough - check the entire codebase before concluding something is missing
- Check common locations and alternative implementations before reporting
- Include clear reasoning for each finding showing why it's that specific type
- Be exhaustive - find ALL misalignments of ALL types
- Categorize precisely - each misalignment belongs to exactly one type

Begin your comprehensive analysis now. Find ALL misalignments of ALL types.
