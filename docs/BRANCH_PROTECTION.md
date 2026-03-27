# Branch Protection Recommendations

Configure branch protection on `main` (or your default branch):

1. Require a pull request before merging.
2. Require status checks to pass before merging.
3. Select required checks:
   - `Backend Quality`
   - `Frontend Quality`
4. Require branches to be up to date before merging.
5. Require at least 1 approving review.
6. Dismiss stale pull request approvals when new commits are pushed.
7. Restrict who can push directly to the protected branch (optional but recommended).

This ensures code is reviewed and CI validated before integration.
