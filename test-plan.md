# Test Plan & Exploration Report — Parkly QA Assignment

## 1. Testing Approach & Strategy

### What did I choose to test (and why)?
I chose to perform a comprehensive, full-coverage exploratory sweep of the Parkly application. While focusing heavily on the **core business flows** and **data integrity** (Authentication, Parking Session Management, and User Management), I also took the initiative to document UI/UX and accessibility issues. 
*Why?* A robust QA automation strategy shouldn't just look for crashes; it should ensure the product is secure, logically sound, and user-friendly. By going deep into edge cases, we can catch logic flaws before they reach production.

### How did I structure my testing approach?
The testing was structured systematically into three phases to ensure maximum coverage:
1. **External Boundary Testing (Unauthenticated):** Verifying routing, unprotected access to dashboard/history, and login form validation.
2. **Internal Core Flow Testing (Authenticated):** Logging in as an admin and testing the "Happy Path" (starting a session, ending a session, verifying it appears in history).
3. **Edge Case & Fuzz Testing (Going Wild):** Applying domain-specific negative testing. For a parking app, this means testing negative slot numbers, duplicate license plates, unusually long strings, and unsupported file uploads.

### What did I consider important?
- **Business Logic Risks:** Ensuring a user cannot start overlapping sessions for the same car.
- **Financial/Data Risks:** Verifying the "End Parking" (payment) flow works smoothly and that invalid data (negative slots, letters in plates) cannot be saved to the database.
- **Security & Authorization:** Ensuring an active admin cannot accidentally delete themselves.
- **Overall Quality:** Documenting broken links, missing assets, and accessibility issues.

---

## 2. Representative Test Cases

### Test Case 01: Start a valid parking session (Happy Path)
- **Preconditions:** User is logged in as Admin.
- **Steps:** 
  1. Navigate to Dashboard.
  2. Enter valid 8-digit plate (e.g., `82736451`).
  3. Enter valid slot (e.g., `10`).
  4. Click "התחל חניה" (Start Parking).
- **Expected Result:** Session starts, appears in the active sessions table, and no console errors are thrown.

### Test Case 02: Duplicate concurrent parking sessions (Negative)
- **Preconditions:** User is logged in as Admin. Vehicle `11111111` is currently parked in slot `10`.
- **Steps:**
  1. Navigate to Dashboard.
  2. Enter plate `11111111` and slot `11`.
  3. Click "התחל חניה".
- **Expected Result:** System throws a validation error preventing the same car from parking in two slots simultaneously.

### Test Case 03: Image upload validation (Negative)
- **Preconditions:** User is logged in as Admin.
- **Steps:**
  1. On the Dashboard, interact with the Image Upload input.
  2. Attempt to select and upload a `.txt` or `.pdf` file.
- **Expected Result:** The file picker restricts selection to `image/*` formats.

---

## 3. Comprehensive Bug Report

By extensively exploring the application, I identified **15 distinct bugs**. Below is the full breakdown:

### High Severity (Critical Logic & Security Flaws)
1. **Broken "Forgot Password" Link:** The link on the login page points to a cat picture (`cataas.com/cat`) instead of a recovery flow.
2. **Deferred Login Failure Feedback:** Entering invalid credentials causes a page reload without an error. Messages only appear **after** a subsequent successful login.
3. **Admin Self-Deletion Vulnerability:** An admin can delete their own account while logged in.
4. **Negative Parking Slot Numbers Accepted:** The system allows starting a session with a negative slot number (e.g., `-5`).
5. **Critical License Plate Validation Failure:** The system accepts and saves plates that are shorter than 8 digits, longer than 8 digits, or contain alphabetical characters.
6. **Payment Logic String Error:** Ending a session with certain data shows `(חיוב: error)` instead of a numeric value.
7. **History Images Path Encoding (404):** Images fail to load due to Windows-style backslashes (`%5C`) in URLs.
8. **Missing Rate Limiting (Brute Force Vulnerability):** Discovered via backend API testing. The `/login` endpoint allows unlimited consecutive failed login attempts without returning HTTP 429 or blocking the user.

### Medium Severity (Validation & UI Issues)
9. **Alphabetical and Special Characters in Slot:** The slot field accepts English letters, Hebrew letters, and special characters (e.g., `abc`, `אבג`, `!@#`).
10. **Duplicate Parking Sessions Allowed:** Starting a second session for an already parked vehicle is allowed (concatenates slot IDs).
11. **Broken Application Routes (404):** Direct access to protected routes like `/dashboard` returns a raw 404 instead of a redirect.
12. **Timestamp Microsecond Overlap:** ISO timestamps with microseconds break the UI layout in the "Start Time" column.
13. **Image Upload Missing Accept Attribute:** The file input lacks `accept="image/*"`, allowing non-image file uploads.

### Low Severity (Accessibility)
14. **Missing Label for Password Toggle:** The "Show Password" button lacks an `aria-label` for screen readers.
15. **Missing Favicon:** The application throws a 404 console error for `favicon.ico`.

---

## 4. UI & Branding Feedback
In addition to the formal bugs above, I noted a minor branding issue that should be addressed by the design/frontend team:
- **Directionality Issue in Logo:** The logo text on the login page is rendered backwards (`(:Parkly` instead of `Parkly:)`), likely due to CSS RTL/LTR text-direction inheritance.
