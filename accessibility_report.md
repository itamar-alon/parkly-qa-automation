# Accessibility Audit Report - Pango/Parkly QA Automation

## Overview
This report summarizes the accessibility (a11y) findings for the Parkly application. Ensuring accessibility is not only a legal requirement in many jurisdictions but also a fundamental part of providing a high-quality user experience for all users, including those using assistive technologies like screen readers.

## Key Findings

### 1. Missing `aria-label` on Interactive Elements
- **Component**: Password Toggle Button (Login Page)
- **Issue**: The button that toggles password visibility does not have an `aria-label` or descriptive text.
- **Impact**: Screen reader users will only hear "button" without knowing its purpose.
- **Recommendation**: Add `aria-label="Show password"` or `aria-label="Hide password"` dynamically.

### 2. Missing `alt` Attributes on Images
- **Component**: Dashboard and History Tables
- **Issue**: Uploaded vehicle images do not have meaningful `alt` text (some are empty or missing the attribute).
- **Impact**: Users with visual impairments cannot understand the content of the images.
- **Recommendation**: Use `alt="Vehicle Image - [License Plate]"` or similar descriptive text.

### 3. Form Input Labeling
- **Component**: Parking Form (Dashboard)
- **Issue**: Some inputs rely on placeholders instead of explicitly linked `<label>` elements using the `for` attribute.
- **Impact**: When a user focuses on an input, a screen reader might not announce what the input is for if the placeholder is gone or not properly associated.
- **Recommendation**: Ensure every `<input>` has a corresponding `<label for="id">`.

### 4. Keyboard Navigation (Focus Trap/Order)
- **Issue**: The focus order when using the `Tab` key is sometimes inconsistent, especially after closing toasts or modals.
- **Impact**: Keyboard-only users may get "lost" on the page.
- **Recommendation**: Use a logical `tabindex` and ensure focus returns to a sensible element after actions.

### 5. Semantic HTML
- **Issue**: Some buttons are implemented as `<div>` or `<a>` without `role="button"`.
- **Impact**: Assistive technologies might not treat these as clickable actions.
- **Recommendation**: Use semantic `<button>` elements for all actions.

---

## Automated Testing Strategy
We have implemented a baseline accessibility suite in `tests/test_accessibility.py` to catch these issues programmatically. Future integration with `axe-core` is recommended for full WCAG 2.1 compliance scanning.
