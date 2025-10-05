# Branch: distributed

## Purpose
Test H4: Whether Cursor outperforms Claude Code when misalignments are distributed across many files. This tests how framework navigation capabilities affect detection performance.

## Configuration
- **Total Misalignments**: 7
- **Type 1 (Missing)**: 2
- **Type 2 (Incorrect)**: 3
- **Type 3 (Extraneous)**: 2
- **Distribution**: Each misalignment in a different file (7 files affected)
- **Subtlety**: Mixed (emphasis on moderate)

---

## Planted Misalignments

### Type 1: Missing Implementations (2)

#### 1.1 Missing Checkbox Component Import
- **Spec Reference**: Section 2.4 Dashboard - "Checkbox (left) to toggle completion"
- **Current State**: Checkbox component not imported/used in TaskItem
- **Files Affected**: `/src/components/TaskItem.tsx`
- **Subtlety**: Moderate
- **Implementation**: Remove checkbox import and use a button instead

#### 1.2 Missing Layout Metadata
- **Spec Reference**: Section 2.1 Landing Page - "App title: 'Welcome to TODOs'"
- **Current State**: Page title not set in metadata
- **Files Affected**: `/src/app/layout.tsx`
- **Subtlety**: Moderate
- **Implementation**: Remove metadata export with title

---

### Type 2: Incorrect Implementations (3)

#### 2.1 Wrong Button Text
- **Spec Reference**: Section 2.4 Dashboard - "Add Task" button
- **Current Implementation**: Button says "Create" instead of "Add Task"
- **Files Affected**: `/src/components/TaskInput.tsx`
- **Subtlety**: Obvious
- **Implementation**: Change button text from "Add Task" to "Create"

#### 2.2 Incorrect Route Path
- **Spec Reference**: Section 6 API Endpoints - "POST /api/auth/register"
- **Current Implementation**: Route at /api/auth/signup instead
- **Files Affected**: `/src/app/api/auth/register/route.ts`
- **Subtlety**: Moderate
- **Implementation**: Rename register folder to signup

#### 2.3 Wrong Label Text
- **Spec Reference**: Section 2.3 Registration - "Name input field"
- **Current Implementation**: Label says "Full Name" instead of "Name"
- **Files Affected**: `/src/app/(auth)/register/page.tsx`
- **Subtlety**: Moderate
- **Implementation**: Change label from "Name" to "Full Name"

---

### Type 3: Extraneous Code (2)

#### 3.1 Metrics Tracking Script
- **Description**: Analytics code not mentioned in spec
- **Files Affected**: `/src/app/page.tsx`
- **Subtlety**: Moderate
- **Implementation**: Add Google Analytics or similar tracking code

#### 3.2 API Rate Limiting Middleware
- **Description**: Rate limiting not specified
- **Files Affected**: `/middleware.ts`
- **Subtlety**: Moderate
- **Implementation**: Add rate limiting logic to middleware

---

## File Distribution Summary

Each file contains exactly one misalignment:
1. `/src/components/TaskItem.tsx` - Missing checkbox (Type 1)
2. `/src/app/layout.tsx` - Missing metadata (Type 1)
3. `/src/components/TaskInput.tsx` - Wrong button text (Type 2)
4. `/src/app/api/auth/register/route.ts` - Wrong route path (Type 2)
5. `/src/app/(auth)/register/page.tsx` - Wrong label (Type 2)
6. `/src/app/page.tsx` - Extra analytics (Type 3)
7. `/middleware.ts` - Extra rate limiting (Type 3)

---

## Ground Truth Summary

```json
{
  "test_branch": "distributed",
  "specification_file": "specs/project-specification.md",
  "type1_missing": [
    "2.4 Dashboard Page - Checkbox component",
    "2.1 Landing Page - App title metadata"
  ],
  "type2_incorrect": [
    {
      "section": "2.4 Dashboard Page - Add Task button",
      "files": ["src/components/TaskInput.tsx"]
    },
    {
      "section": "6 API Endpoints - /api/auth/register",
      "files": ["src/app/api/auth/register/route.ts"]
    },
    {
      "section": "2.3 Registration Page - Name input field",
      "files": ["src/app/(auth)/register/page.tsx"]
    }
  ],
  "type3_extraneous": [
    "src/app/page.tsx",
    "middleware.ts"
  ]
}
```

---

## Implementation Checklist

When creating this branch:

- [ ] Create branch from main: `git checkout -b distributed`
- [ ] Remove checkbox usage in TaskItem (Type 1.1)
- [ ] Remove page metadata (Type 1.2)
- [ ] Change button text to "Create" (Type 2.1)
- [ ] Rename register route to signup (Type 2.2)
- [ ] Change label to "Full Name" (Type 2.3)
- [ ] Add analytics tracking (Type 3.1)
- [ ] Add rate limiting (Type 3.2)
- [ ] Save ground-truth.json to branch
- [ ] Verify each file has exactly one change
- [ ] Test that app still runs
- [ ] Commit with message: "Plant distributed misalignments"

---

## Expected Detection Patterns

**Should favor Cursor (if H4 correct):**
- Better file navigation through IDE
- File tree makes it easier to spot affected files
- Can quickly jump between files to verify

**Should favor Claude Code:**
- None specifically (hypothesis predicts Cursor advantage)

**Critical test aspects:**
- Whether frameworks examine all 8 files
- Order of file exploration
- Completeness of coverage
- Time to find distributed issues

This configuration tests whether Cursor's IDE integration provides advantages when misalignments are spread across the codebase rather than concentrated in a few files. The wide distribution requires systematic exploration of the entire project structure.
