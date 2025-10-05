# Type 3 Detection: Extraneous Code

Copy and paste this entire prompt exactly as shown:

---

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

Output your findings as a JSON object with this exact structure:

```json
{
  "misalignments": [
    {
      "feature": "Admin Dashboard",
      "reasoning": "Complete admin interface with user management not mentioned anywhere in specification",
      "files": ["src/app/admin/page.tsx", "src/app/admin/dashboard/page.tsx"]
    },
    {
      "feature": "Task Priority System",
      "reasoning": "Priority field (low/medium/high) and filtering not specified in requirements",
      "files": ["src/components/TaskItem.tsx", "src/app/api/tasks/route.ts"]
    },
    {
      "feature": "Export Data",
      "reasoning": "CSV export endpoint not mentioned in API specification",
      "files": ["src/app/api/export/route.ts"]
    }
  ]
}
```

**Required fields**:
- `feature`: Brief name/description of the extraneous functionality
- `reasoning`: Explanation of what this feature does and why it's extraneous
- `files`: Array of relative file paths that contain this extraneous code

**Important**:
- Group related files under one feature (e.g., all admin files together)
- Keep feature names descriptive but concise
- Reasoning should confirm the feature is not mentioned in spec

## Important Notes

- Focus on significant extraneous code, not implementation details
- Check the ENTIRE specification before reporting as extraneous
- Report actual features/endpoints/capabilities, not just helper code
- Group related files under a single feature
- Include clear reasoning for why each feature is extraneous

Begin your analysis now. Focus ONLY on Type 3 (extraneous) misalignments.
