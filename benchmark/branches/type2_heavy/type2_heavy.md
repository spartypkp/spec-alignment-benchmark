# Branch: type2_heavy

## Purpose
Test H2b: Whether Claude Code outperforms Cursor at detecting Type 2 (incorrect implementations). This branch heavily weights Type 2 misalignments to test each framework's ability to identify logic errors and specification deviations.

## Configuration
- **Total Misalignments**: 8
- **Type 1 (Missing)**: 1
- **Type 2 (Incorrect)**: 6
- **Type 3 (Extraneous)**: 1
- **Subtlety**: Mixed within Type 2 (1 obvious, 3 moderate, 2 subtle)

---

## Planted Misalignments

### Type 1: Missing Implementation (1)

#### 1.1 Missing Name Field Validation
- **Spec Reference**: Section 4.1 Input Validation - "Name: Required, 1-50 characters"
- **Current State**: Name field exists but no length validation
- **Files Affected**: `/src/app/(auth)/register/page.tsx`
- **Subtlety**: Moderate
- **Implementation**: Remove character limit validation for name field

---

### Type 2: Incorrect Implementations (6)

#### 2.1 Wrong Password Hash Algorithm
- **Spec Reference**: Section 3.1 Authentication - "Email/password authentication using bcryptjs"
- **Current Implementation**: Using plain SHA256 instead of bcrypt
- **Files Affected**: `/src/app/api/auth/register/route.ts`, `/src/app/api/auth/login/route.ts`
- **Subtlety**: Obvious
- **Implementation**: Replace bcrypt.hash with crypto SHA256 hashing

#### 2.2 Incorrect Session Duration
- **Spec Reference**: Section 3.1 Authentication - "Sessions stored in httpOnly cookies (7-day expiry)"
- **Current Implementation**: Sessions expire after 1 day instead of 7 days
- **Files Affected**: `/src/lib/auth.ts`
- **Subtlety**: Moderate
- **Implementation**: Change session expiry from 7 * 24 * 60 * 60 * 1000 to 24 * 60 * 60 * 1000

#### 2.3 Wrong HTTP Status Codes
- **Spec Reference**: Section 4.2 Error Handling (implied) - Standard REST status codes
- **Current Implementation**: Returns 200 for all responses, errors in body
- **Files Affected**: `/src/app/api/tasks/route.ts`, `/src/app/api/auth/login/route.ts`
- **Subtlety**: Moderate
- **Implementation**: Change all error responses to use status 200 with error in body

#### 2.4 Incorrect Database Foreign Key Handling
- **Spec Reference**: Section 8.1 Database Initialization - "FOREIGN KEY (userId) REFERENCES users(id)"
- **Current Implementation**: No CASCADE on delete, orphaned records possible
- **Files Affected**: `/src/lib/db.ts` (schema definition)
- **Subtlety**: Subtle
- **Implementation**: Remove ON DELETE CASCADE from foreign key constraints

#### 2.5 Wrong Task Update Behavior
- **Spec Reference**: Section 3.2 Task Management - "Toggle completion: Updates task state"
- **Current Implementation**: Toggle creates new task instead of updating existing
- **Files Affected**: `/src/app/api/tasks/[id]/route.ts` (PUT handler)
- **Subtlety**: Moderate
- **Implementation**: Change UPDATE query to INSERT with same ID (causing duplicates)

#### 2.6 Incorrect Checkbox State Logic
- **Spec Reference**: Section 2.4 Dashboard - "Checkbox to toggle completion"
- **Current Implementation**: Checkbox inverts all tasks instead of just one
- **Files Affected**: `/src/components/TaskItem.tsx`
- **Subtlety**: Subtle
- **Implementation**: onChange handler affects all tasks in list instead of single task

---

### Type 3: Extraneous Code (1)

#### 3.1 Theme Toggle Feature
- **Description**: Dark/light theme switcher not in specification
- **Files Affected**: `/src/components/ThemeToggle.tsx`, `/src/app/layout.tsx`
- **Subtlety**: Moderate
- **Implementation**: Add theme context and toggle button in header

---

## Ground Truth Summary

```json
{
  "test_branch": "type2_heavy",
  "specification_file": "specs/project-specification.md",
  "type1_missing": [
    "4.1 Input Validation - Name: Required, 1-50 characters"
  ],
  "type2_incorrect": [
    {
      "section": "3.1 Authentication - Email/password authentication using bcryptjs",
      "files": ["src/app/api/auth/register/route.ts", "src/app/api/auth/login/route.ts"]
    },
    {
      "section": "3.1 Authentication - Sessions stored in httpOnly cookies (7-day expiry)",
      "files": ["src/lib/auth.ts"]
    },
    {
      "section": "4.2 Error Handling - HTTP status codes",
      "files": ["src/app/api/tasks/route.ts", "src/app/api/auth/login/route.ts"]
    },
    {
      "section": "8.1 Database Initialization - Foreign key constraints",
      "files": ["src/lib/db.ts"]
    },
    {
      "section": "3.2 Task Management - Toggle completion updates task",
      "files": ["src/app/api/tasks/[id]/route.ts"]
    },
    {
      "section": "2.4 Dashboard Page - Checkbox to toggle completion",
      "files": ["src/components/TaskItem.tsx"]
    }
  ],
  "type3_extraneous": [
    "src/components/ThemeToggle.tsx"
  ]
}
```

---

## Implementation Checklist

When creating this branch:

- [ ] Create branch from main: `git checkout -b type2_heavy`
- [ ] Remove name validation (Type 1.1)
- [ ] Replace bcrypt with SHA256 (Type 2.1)
- [ ] Change session to 1 day expiry (Type 2.2)
- [ ] Use status 200 for all responses (Type 2.3)
- [ ] Remove CASCADE from foreign keys (Type 2.4)
- [ ] Make toggle create duplicates (Type 2.5)
- [ ] Make checkbox affect all tasks (Type 2.6)
- [ ] Add theme toggle feature (Type 3.1)
- [ ] Save ground-truth.json to branch
- [ ] Test that app runs (with bugs)
- [ ] Commit with message: "Plant type2_heavy misalignments"

---

## Expected Detection Patterns

**Should strongly favor Claude Code (if H2b correct):**
- Wrong hash algorithm (security logic error)
- Incorrect update behavior (subtle logic bug)
- Checkbox affecting all tasks (requires understanding component state)
- Foreign key cascade issue (database relationship logic)

**Should be detected by both:**
- Session duration difference (explicit number in spec)
- HTTP status codes (common REST pattern)

**May differentiate frameworks:**
- Theme feature (visible but not dramatic)
- Name validation missing (straightforward requirement)

This configuration tests whether Claude Code's reasoning capabilities provide advantages in detecting incorrect logic and implementation details that deviate from specifications.
