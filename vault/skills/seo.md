# Skill: SEO Implementation

## When to Use
Any project with public-facing pages.

## Steps
1. Add unique `<title>` to every page (50-60 characters)
2. Add `<meta name="description">` to every page (150-160 characters)
3. Add Open Graph tags: og:title, og:description, og:image, og:url
4. Add canonical URL tag on every page
5. Create favicon (multiple sizes: 16, 32, 180, 192, 512)
6. Generate sitemap.xml listing all public pages
7. Create robots.txt allowing crawling of public pages
8. Use semantic HTML: one h1 per page, sequential heading hierarchy
9. Add structured data (JSON-LD) for the primary entity type

## Verification
- [ ] Every page has unique title and description
- [ ] OG tags render correctly in social sharing preview
- [ ] Favicon displays in browser tab
- [ ] sitemap.xml is accessible and lists all pages
- [ ] robots.txt exists and is correct
- [ ] Only one h1 per page

## Common Mistakes
- Same title on every page: Each page needs a unique, descriptive title
- Missing og:image: Social shares without images get 80% less engagement
- Blocking crawlers in robots.txt: Default should allow, block explicitly
