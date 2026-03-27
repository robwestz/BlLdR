# Skill: Pagination

## When to Use
Displaying a large list of items that cannot or should not load all at once.

## Steps
1. Choose pagination strategy: offset for small stable datasets (<10k items), cursor for large or real-time datasets
2. Set a default page size (10, 25, or 50 items) — expose it as a config, not a hardcoded value
3. Persist current page and page size in the URL query string (`?page=2&size=25`)
4. For offset pagination: fetch `LIMIT size OFFSET (page - 1) * size` from the data source
5. For cursor pagination: store and send the last item's cursor token; never expose raw offsets
6. Display total item count and current range ("Showing 26–50 of 312")
7. Choose UI pattern: numbered pages for browsable content, "Load more" or infinite scroll for feeds
8. Handle the empty-last-page case: if the current page has 0 items and page > 1, redirect to page 1
9. Disable Previous on page 1 and Next when no more items exist

## Verification
- [ ] Refreshing the page lands on the same page and page size
- [ ] Sharing the URL opens the same page for another user
- [ ] Next button is disabled on the last page
- [ ] Previous button is disabled on page 1
- [ ] Empty page redirects rather than showing a blank list
- [ ] Page size change resets to page 1

## Common Mistakes
- Hardcoding page size: Makes it impossible to tune per context → make it a config constant
- Offset pagination on live data: Rows shift between pages causing duplicates or skips → use cursor pagination
- Not persisting page in URL: Back button loses position → always sync to query string
- Showing "Load more" with a total count: Contradicts infinite-feel UX → pick one pattern and commit
