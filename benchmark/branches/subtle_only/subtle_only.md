# Branch: subtle_only

## Purpose
Test H3: Whether Claude Code shows less performance degradation than Cursor when all misalignments are subtle. This branch contains only hard-to-detect misalignments requiring deep analysis.

## Configuration
- **Total Misalignments**: 5
- **Type 1 (Missing)**: 1
- **Type 2 (Incorrect)**: 2
- **Type 3 (Extraneous)**: 2
- **Subtlety**: All subtle (requiring careful analysis)

---

## Planted Misalignments

### Type 1: Missing Implementations (1)

#### 1.1 Missing createdAt Field Auto-Population
- **Spec Reference**: Section 5 Data Models - User model "createdAt: string // ISO timestamp"
- **Current State**: Field exists in schema but not auto-populated on insert
- **Files Affected**: `/src/app/api/auth/register/route.ts`
- **Subtlety**: Subtle
- **Implementation**: Remove `new Date().toISOString()` assignment for createdAt

---

### Type 2: Incorrect Implementations (2)

#### 2.1 Case-Sensitive Email Comparison
- **Spec Reference**: Section 3.1 Authentication (implied) - Emails should be case-insensitive
- **Current Implementation**: Login compares emails with case sensitivity
- **Files Affected**: `/src/app/api/auth/login/route.ts`
- **Subtlety**: Subtle
- **Implementation**: Remove `.toLowerCase()` from email comparison

#### 2.2 Timezone Handling in Timestamps
- **Spec Reference**: Section 5 Data Models - "ISO timestamp" implies UTC
- **Current Implementation**: Uses local timezone instead of UTC
- **Files Affected**: `/src/lib/db.ts`
- **Subtlety**: Very subtle
- **Implementation**: Use `new Date().toString()` instead of `new Date().toISOString()`

---

### Type 3: Extraneous Code (2)

#### 3.1 Unused Utility Functions
- **Description**: Helper functions that aren't called anywhere
- **Files Affected**: `/src/lib/utils.ts`
- **Subtlety**: Subtle
- **Implementation**: Add 2-3 utility functions (formatDate, debounce) that aren't used

#### 3.2 Development Console Logs
- **Description**: Debug logging left in production code
- **Files Affected**: `/src/app/api/tasks/route.ts`, `/src/components/TaskList.tsx`
- **Subtlety**: Subtle
- **Implementation**: Add console.log statements in API and components

---

## Ground Truth Summary

```json
{
  "test_branch": "subtle_only",
  "specification_file": "specs/project-specification.md",
  "type1_missing": [
    "5 Data Models - User.createdAt auto-population"
  ],
  "type2_incorrect": [
    {
      "section": "3.1 Authentication - Email case-insensitive comparison",
      "files": ["src/app/api/auth/login/route.ts"]
    },
    {
      "section": "5 Data Models - ISO timestamp (UTC)",
      "files": ["src/lib/db.ts"]
    }
  ],
  "type3_extraneous": [
    "src/lib/utils.ts",
    "src/app/api/tasks/route.ts",
    "src/components/TaskList.tsx"
  ]
}
```

---

## Implementation Checklist

When creating this branch:

- [ ] Create branch from main: `git checkout -b subtle_only`
- [ ] Remove createdAt auto-population (Type 1.1)
- [ ] Make email comparison case-sensitive (Type 2.1)
- [ ] Use local timezone for timestamps (Type 2.2)
- [ ] Add unused utility functions (Type 3.1)
- [ ] Add console.log statements (Type 3.2)
- [ ] Save ground-truth.json to branch
- [ ] Test that app still runs normally
- [ ] Commit with message: "Plant subtle_only misalignments"

---

## Expected Detection Patterns

**All items are challenging and will test:**
- Deep specification understanding
- Knowledge of best practices
- Attention to implementation details
- Ability to infer unstated requirements

**Should favor Claude Code (if H3 correct):**
- Systematic reasoning should catch these subtle issues
- Less reliance on obvious visual cues
- Better at inferring implied requirements

**May be missed by both:**
- Input trimming (often implied, not stated)
- Timezone handling (very technical detail)
- Unused functions (requires full codebase analysis)

This configuration specifically tests performance on subtle misalignments that require careful analysis rather than surface-level scanning. The results will reveal whether Claude Code's reasoning approach maintains effectiveness when obvious visual cues are absent.
