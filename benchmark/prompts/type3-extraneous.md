# Type 3 Detection: Extraneous Code

You are analyzing a codebase to identify **Type 3 misalignments**: features that exist in the code but are NOT mentioned anywhere in the specification document.

## Your Task

1. Read the specification document at: `specs/project-specification.md`
2. Explore the codebase to find all implemented features
3. Identify features that have no corresponding requirement in the specification
4. Report code that exists without specification backing

## Definition of Type 3 (Extraneous)

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

**Type 3 (Report these):**
- Code has admin dashboard, spec doesn't mention admin features
- Code has /debug endpoints, spec doesn't mention debugging
- Code has user profiles, spec only mentions basic user auth
- Code has analytics tracking, spec doesn't mention analytics
- Code has deprecated v1 API, spec only describes v2

**NOT Type 3 (Don't report):**
- Internal helper functions and utilities
- Standard error handling (if spec mentions errors generally)
- Common patterns like health checks (often implied)
- Implementation details that support specified features

## Output Format

Output your findings as a JSON object listing each extraneous file:

```json
{
  "misalignments": [
    {
      "file": "src/app/metrics/page.tsx",
      "reasoning": "Analytics dashboard page not mentioned anywhere in specification"
    },
    {
      "file": "src/components/charts/MetricsChart.tsx",
      "reasoning": "Metrics visualization component for unspecified analytics feature"
    },
    {
      "file": "src/lib/websocket.ts",
      "reasoning": "WebSocket implementation for real-time updates not specified"
    },
    {
      "file": "src/app/api/ws/route.ts",
      "reasoning": "WebSocket API endpoint not mentioned in requirements"
    },
    {
      "file": "src/app/debug/route.ts",
      "reasoning": "Debug console endpoint not specified in API documentation"
    }
  ]
}
```

**Required fields**:
- `file`: The relative file path of the extraneous code
- `reasoning`: Brief explanation of what this file does and why it's extraneous

**Important**:
- List each file separately (don't group files)
- Use exact relative paths from repository root
- Keep reasoning concise but specific about why the file is extraneous
- Only include files that represent features/endpoints not in spec

## Important Notes

- Focus on significant extraneous code, not implementation details
- Check the ENTIRE specification before reporting as extraneous
- Report actual features/endpoints/capabilities, not just helper code
- List each extraneous file separately with its own reasoning
- Include clear reasoning for why each file is extraneous

Begin your analysis now. Focus ONLY on Type 3 (extraneous) misalignments.
