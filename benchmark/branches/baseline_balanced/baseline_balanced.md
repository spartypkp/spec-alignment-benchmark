# Branch: baseline_balanced

## Purpose
Establish baseline performance and test H1 (overall detection capability). This branch contains a balanced mix of all three misalignment types with moderate subtlety.

## Configuration
- **Total Misalignments**: 8
- **Type 1 (Missing)**: 3
- **Type 2 (Incorrect)**: 3  
- **Type 3 (Extraneous)**: 2
- **Subtlety**: Mixed (2 obvious, 4 moderate, 2 subtle)

---

## Planted Misalignments

### Type 1: Missing Implementations (3)

#### 1.1 Missing Password Validation on Registration
- **Spec Reference**: Section 4.3 Registration Page - "Password input field (minimum 6 characters)"
- **Current State**: Password field exists but no validation for 6-character minimum
- **Files Affected**: `/src/app/(auth)/register/page.tsx`, `/src/app/api/auth/register/route.ts`
- **Subtlety**: Obvious
- **Implementation**: Remove password length validation from both client and server

#### 1.2 Missing Session Expiry Implementation
- **Spec Reference**: Section 3.1 Authentication - "Sessions stored in httpOnly cookies (7-day expiry)"
- **Current State**: Sessions created but no expiry logic implemented
- **Files Affected**: `/src/lib/auth.ts`, `/src/app/api/auth/login/route.ts`
- **Subtlety**: Moderate
- **Implementation**: Remove all session expiry date setting and checking

#### 1.3 Missing Statistics Bar
- **Spec Reference**: Section 2.4 Dashboard Page - "Statistics Bar: Three metrics displayed horizontally"
- **Current State**: Dashboard exists but no statistics display
- **Files Affected**: `/src/app/dashboard/page.tsx`
- **Subtlety**: Obvious
- **Implementation**: Remove the entire statistics section showing total tasks, completed tasks, and completion percentage

---

### Type 2: Incorrect Implementations (3)

#### 2.1 Wrong Task Sort Order
- **Spec Reference**: Section 2.4 Dashboard - "Tasks sorted by creation date (newest first)"
- **Current Implementation**: Tasks sorted oldest first (ascending instead of descending)
- **Files Affected**: `/src/app/api/tasks/route.ts` (GET handler)
- **Subtlety**: Moderate
- **Implementation**: Change `ORDER BY createdAt DESC` to `ORDER BY createdAt ASC`

#### 2.2 Incorrect Error Response Format
- **Spec Reference**: Section 4.2 Error Handling - Specific JSON format with code and message
- **Current Implementation**: Returns simple `{ error: "message" }` instead of `{ error: { code: "CODE", message: "message" } }`
- **Files Affected**: `/src/app/api/auth/login/route.ts`, `/src/app/api/auth/register/route.ts`
- **Subtlety**: Moderate  
- **Implementation**: Use simplified error format without error codes

#### 2.3 Wrong Character Limit for Task Title
- **Spec Reference**: Section 3.2 Task Management - "Title: Required, 1-100 characters"
- **Current Implementation**: Validates for 50 characters maximum instead of 100
- **Files Affected**: `/src/lib/validation.ts`, `/src/components/TaskInput.tsx`
- **Subtlety**: Subtle
- **Implementation**: Change MAX_TASK_LENGTH from 100 to 50

---

### Type 3: Extraneous Code (2)

#### 3.1 Admin Dashboard Route
- **Description**: Admin interface not mentioned anywhere in specification
- **Files Added**: `/src/app/admin/page.tsx`
- **Subtlety**: Obvious
- **Implementation**: Create a basic admin page showing all users and their task counts

#### 3.2 Task Priority Feature
- **Description**: Priority field and filtering not in specification
- **Files Affected**: `/src/app/api/tasks/route.ts`, `/src/components/TaskItem.tsx`
- **Subtlety**: Subtle
- **Implementation**: Add optional priority field to task creation and display (low/medium/high)

---

## Ground Truth Summary

```json
{
  "test_branch": "baseline_balanced",
  "specification_file": "specs/project-specification.md",
  "type1_missing": [
    "4.3 Registration Page - Password validation (minimum 6 characters)",
    "3.1 Authentication - Session expiry (7-day expiry)",
    "2.4 Dashboard Page - Statistics Bar"
  ],
  "type2_incorrect": [
    {
      "section": "2.4 Dashboard Page - Task sorting",
      "files": ["src/app/api/tasks/route.ts"]
    },
    {
      "section": "4.2 Error Handling - Response format",
      "files": ["src/app/api/auth/login/route.ts", "src/app/api/auth/register/route.ts"]
    },
    {
      "section": "3.2 Task Management - Title character limit",
      "files": ["src/lib/validation.ts", "src/components/TaskInput.tsx"]
    }
  ],
  "type3_extraneous": [
    "src/app/admin/page.tsx",
    "src/components/TaskItem.tsx (priority feature)",
    "src/app/api/tasks/route.ts (priority field)"
  ]
}
```

---

## Implementation Checklist

When creating this branch:

- [ ] Create branch from main: `git checkout -b baseline_balanced`
- [ ] Remove password length validation (Type 1.1)
- [ ] Remove session expiry logic (Type 1.2)
- [ ] Remove statistics bar component (Type 1.3)
- [ ] Change task sort to ascending (Type 2.1)
- [ ] Simplify error response format (Type 2.2)
- [ ] Change task title limit to 50 (Type 2.3)
- [ ] Add admin dashboard page (Type 3.1)
- [ ] Add task priority feature (Type 3.2)
- [ ] Save ground-truth.json to branch
- [ ] Test that app still runs
- [ ] Commit with message: "Plant baseline_balanced misalignments"

---

## Expected Detection Difficulty

**Easy to Find** (Should be caught by both frameworks):
- Missing statistics bar (very visible omission)
- Admin dashboard (entire extra page)

**Moderate** (May differentiate frameworks):
- Wrong sort order (requires understanding DESC vs ASC)
- Session expiry (requires understanding auth flow)
- Error format (requires careful spec reading)

**Challenging** (Best frameworks will catch these):
- Character limit difference (50 vs 100)
- Priority feature in existing components

This balanced mix will establish a performance baseline while testing each framework's capabilities across all misalignment types.
