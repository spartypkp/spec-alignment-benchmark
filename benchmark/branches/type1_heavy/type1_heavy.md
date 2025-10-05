# Branch: type1_heavy

## Purpose
Test H2a: Whether Cursor outperforms Claude Code at detecting Type 1 (missing implementations). This branch heavily weights Type 1 misalignments to stress-test each framework's ability to identify missing features.

## Configuration
- **Total Misalignments**: 8
- **Type 1 (Missing)**: 6 
- **Type 2 (Incorrect)**: 1
- **Type 3 (Extraneous)**: 1
- **Subtlety**: Mixed within Type 1 (2 obvious, 3 moderate, 1 subtle)

---

## Planted Misalignments

### Type 1: Missing Implementations (6)

#### 1.1 Missing Authentication Middleware
- **Spec Reference**: Section 8.2 Middleware Configuration - "Protect routes using Next.js middleware"
- **Current State**: No middleware.ts file protecting dashboard routes
- **Files Affected**: `/middleware.ts` (should exist but doesn't)
- **Subtlety**: Obvious
- **Implementation**: Delete the middleware.ts file entirely

#### 1.2 Missing Logout Functionality
- **Spec Reference**: Section 2.4 Dashboard - "Logout button (functional, clears session)"
- **Current State**: Logout button exists but no API endpoint
- **Files Affected**: `/src/app/api/auth/logout/route.ts` (missing)
- **Subtlety**: Obvious
- **Implementation**: Delete the logout route handler

#### 1.3 Missing Email Validation
- **Spec Reference**: Section 4.1 Input Validation - "Email: Required, valid email format"
- **Current State**: Email field accepts any string, no format validation
- **Files Affected**: `/src/lib/validation.ts`, `/src/app/(auth)/register/page.tsx`
- **Subtlety**: Moderate
- **Implementation**: Remove email regex validation from both client and server

#### 1.4 Missing Transaction Wrapper for Bulk Operations
- **Spec Reference**: Section 4.3 Database Transactions - "Bulk operations wrapped in transactions"
- **Current State**: Database operations execute individually without transaction wrapper
- **Files Affected**: `/src/lib/db.ts`
- **Subtlety**: Subtle
- **Implementation**: Remove db.transaction() wrapper from any bulk operations

#### 1.5 Missing Error Codes
- **Spec Reference**: Section 4.2 Error Handling - "Common error codes: MISSING_FIELDS, INVALID_EMAIL, etc."
- **Current State**: Errors return messages but no error codes
- **Files Affected**: All API routes
- **Subtlety**: Moderate
- **Implementation**: Remove all error code constants and their usage

#### 1.6 Missing Empty State Message
- **Spec Reference**: Section 2.4 Task List - "Empty state: 'No tasks yet. Add your first task above!'"
- **Current State**: Shows blank list when no tasks exist
- **Files Affected**: `/src/components/TaskList.tsx`
- **Subtlety**: Moderate
- **Implementation**: Remove the empty state conditional rendering

---

### Type 2: Incorrect Implementation (1)

#### 2.1 Wrong Session Cookie Name
- **Spec Reference**: Section 3.1 Authentication - "Session cookie name: 'todo-session'"
- **Current Implementation**: Cookie named 'session' instead of 'todo-session'
- **Files Affected**: `/src/lib/auth.ts`
- **Subtlety**: Moderate
- **Implementation**: Change cookie name to just 'session'

---

### Type 3: Extraneous Code (1)

#### 3.1 Export Data Feature
- **Description**: CSV export functionality not mentioned in specification
- **Files Added**: `/src/app/api/export/route.ts`
- **Subtlety**: Moderate
- **Implementation**: Add endpoint to export tasks as CSV

---

## Ground Truth Summary

```json
{
  "test_branch": "type1_heavy",
  "specification_file": "specs/project-specification.md",
  "type1_missing": [
    "8.2 Middleware Configuration - Protect routes using Next.js middleware",
    "2.4 Dashboard Page - Logout button (functional, clears session)",
    "4.1 Input Validation - Email: Required, valid email format",
    "4.3 Database Transactions - Bulk operations wrapped in transactions",
    "4.2 Error Handling - Common error codes",
    "2.4 Dashboard Page - Empty state message"
  ],
  "type2_incorrect": [
    {
      "section": "3.1 Authentication - Session cookie name",
      "files": ["src/lib/auth.ts"]
    }
  ],
  "type3_extraneous": [
    "src/app/api/export/route.ts"
  ]
}
```

---

## Implementation Checklist

When creating this branch:

- [ ] Create branch from main: `git checkout -b type1_heavy`
- [ ] Delete middleware.ts file (Type 1.1)
- [ ] Delete logout route handler (Type 1.2)
- [ ] Remove email validation logic (Type 1.3)
- [ ] Remove transaction wrappers (Type 1.4)
- [ ] Remove error code constants (Type 1.5)
- [ ] Remove empty state message (Type 1.6)
- [ ] Change session cookie name (Type 2.1)
- [ ] Add export endpoint (Type 3.1)
- [ ] Save ground-truth.json to branch
- [ ] Test that app still runs (with reduced functionality)
- [ ] Commit with message: "Plant type1_heavy misalignments"

---

## Expected Detection Patterns

**Should strongly favor Cursor (if H2a correct):**
- Missing middleware.ts file (entire file missing)
- Missing logout route (entire route missing)
- Missing empty state (visual UI element)

**Should be detected by both:**
- Email validation (common requirement)
- Error codes (explicit in spec)

**May differentiate frameworks:**
- Transaction wrapping (subtle, backend logic)
- Cookie name difference (small detail)
- Export feature (unexpected endpoint)

This configuration will test whether Cursor's file-tree visibility and IDE integration provide advantages in detecting missing implementations.
