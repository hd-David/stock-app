# Testing Checklist for Static Files Optimization

## Pre-Testing Setup

1. **Set Environment Variable**
   ```bash
   export API_KEY="your_alpha_vantage_api_key"
   ```

2. **Start the Application**
   ```bash
   python app.py
   ```

3. **Open Browser**
   Navigate to: `http://localhost:5000`

## Visual Testing Checklist

### Landing Page (Not Logged In)
- [ ] Page loads without errors
- [ ] "C$50 Finance" title displays correctly
- [ ] "Get Started" and "Login" buttons are styled properly
- [ ] Trending stocks cards display with icons
- [ ] Stock prices and change indicators show
- [ ] Font Awesome icons render (chart-line, caret-up/down)
- [ ] Responsive layout works on mobile view

### Login Page (`/login`)
- [ ] Page loads without errors
- [ ] Login form displays correctly
- [ ] Background styling is intact
- [ ] "Remember me" checkbox works
- [ ] "Secure login" button is styled
- [ ] Links to "Recover Password" and "Register Account" work
- [ ] Form validation works

### Registration Page (`/register`)
- [ ] Page loads without errors
- [ ] Registration form displays correctly
- [ ] All form fields are properly styled
- [ ] Form validation works
- [ ] Submit button is styled correctly

### Portfolio Page (Logged In - `/`)
- [ ] Page loads without errors
- [ ] Sidebar navigation appears
- [ ] Navigation icons display (home, search, shopping-cart, etc.)
- [ ] "Active" navigation item is highlighted
- [ ] Top header shows cash balance with wallet icon
- [ ] "Logout" button is visible and styled
- [ ] Portfolio table displays correctly
- [ ] Panel collapse/expand buttons work
- [ ] Panel fullscreen button works
- [ ] Table styling is intact (borders, hover effects)

### Quote Page (`/quote`)
- [ ] Page loads without errors
- [ ] Quote form displays correctly
- [ ] Form fields are styled
- [ ] Submit button works
- [ ] Form validation functions

### Quote Results (`/quote` after submission)
- [ ] Results page loads without errors
- [ ] Stock information displays correctly
- [ ] Pricing calculations show properly

### Buy Page (`/buy`)
- [ ] Page loads without errors
- [ ] Buy form displays correctly
- [ ] Form fields are accessible
- [ ] Submit functionality works

## Browser Console Check

Open browser developer tools (F12) and check the Console tab:

### Expected (No Errors)
- [ ] No 404 errors for missing CSS files
- [ ] No 404 errors for missing JS files
- [ ] No 404 errors for missing font files
- [ ] No JavaScript errors

### Common Issues to Look For
If you see errors, check:
- `Failed to load resource: 404` - File not found
- `Uncaught ReferenceError` - Missing JavaScript library
- `Failed to decode downloaded font` - Font file missing

## Network Tab Check

In browser developer tools, go to Network tab:

### Check What's Loading
- [ ] `vendors.bundle.css` loads successfully
- [ ] `app.bundle.css` loads successfully
- [ ] `page-login.css` loads (on login page)
- [ ] `cust-theme-3.css` loads successfully
- [ ] `vendors.bundle.js` loads successfully
- [ ] `app.bundle.js` loads successfully
- [ ] Font files load (fa-light-300, fa-solid-900, etc.)

### Performance Check
Before optimization:
- Total size: ~1.5MB (compressed)
- Requests: 10-15

After optimization:
- Total size: ~600KB (compressed)
- Requests: 8-10

## Functionality Testing

### Navigation
- [ ] All navigation menu items work
- [ ] Mobile hamburger menu works (on small screens)
- [ ] Hover effects work on menu items
- [ ] Active page is highlighted correctly

### Interactive Elements
- [ ] Buttons have proper hover effects
- [ ] Form inputs focus correctly
- [ ] Dropdowns work (if any)
- [ ] Tooltips display (on panel buttons)
- [ ] Panels can be collapsed/expanded
- [ ] Panels can be fullscreened

### Responsive Design
Test at these breakpoints:
- [ ] Desktop (1920px+): Full sidebar, all features visible
- [ ] Laptop (1366px): Sidebar visible, content adjusts
- [ ] Tablet (768px): Sidebar collapses, hamburger menu appears
- [ ] Mobile (375px): Mobile-optimized layout

## Font Awesome Icons Check

Verify these icons display correctly:
- [ ] `fa-home` - Home/Portfolio icon
- [ ] `fa-search` - Quote/Search icon
- [ ] `fa-shopping-cart` - Buy icon
- [ ] `fa-money-bill-wave` - Sell icon
- [ ] `fa-history` - History icon
- [ ] `fa-wallet` - Cash balance icon
- [ ] `fa-chart-line` - Stock indicators
- [ ] `fa-caret-up` / `fa-caret-down` - Price movement
- [ ] `fa-bars` - Mobile menu icon

## Cross-Browser Testing

Test in multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (if on Mac)
- [ ] Edge

## Performance Testing (Optional)

### Lighthouse Audit
1. Open Chrome DevTools
2. Go to Lighthouse tab
3. Run audit for Performance
4. Check scores:
   - [ ] Performance: 80+ (good), 90+ (excellent)
   - [ ] First Contentful Paint: < 2s
   - [ ] Largest Contentful Paint: < 2.5s

### Load Time Comparison
Use browser Network tab to measure:
- Before optimization: ~2-3s (depending on connection)
- After optimization: ~1-1.5s (33-50% improvement)

## Known Issues (Not Related to Optimization)

These are existing issues and are NOT caused by the optimization:
- History page returns "TODO" apology
- Some form validation messages might need styling

## Rollback (If Needed)

If you encounter critical issues:

1. **Check Git History**
   ```bash
   git log --oneline
   ```

2. **Revert Changes**
   ```bash
   git revert <commit-hash>
   ```

3. **Or Restore from Backup**
   If you have a backup of the static folder before optimization

## Reporting Issues

If you find issues with the optimization:

1. **Document the Issue**
   - What page/feature is affected?
   - What error appears in the console?
   - What's the expected vs actual behavior?

2. **Check STATIC_FILES.md**
   - Is the referenced file listed as removed?
   - Should it have been kept?

3. **Create GitHub Issue**
   Include:
   - Steps to reproduce
   - Browser and version
   - Console error messages
   - Screenshots if applicable

## Success Criteria

All items should be checked (✓) for optimization to be considered successful:

### Critical (Must Pass)
- [ ] All pages load without 404 errors
- [ ] Navigation works completely
- [ ] Forms can be submitted
- [ ] Icons display correctly
- [ ] Responsive design works

### Important (Should Pass)
- [ ] No JavaScript console errors
- [ ] Hover effects work
- [ ] Panel controls function
- [ ] Performance improvement evident

### Nice to Have
- [ ] Lighthouse score improved
- [ ] Page load time reduced by 30%+
- [ ] Bandwidth usage reduced

## Completion

Date tested: _______________

Tested by: _______________

Result: ⬜ Pass ⬜ Fail (with notes)

Notes:
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________
