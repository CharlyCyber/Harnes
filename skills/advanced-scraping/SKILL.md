---
name: advanced-scraping
description: "Expert web scraping techniques using BeautifulSoup for static content and Playwright for dynamic/JS-heavy sites. Includes strategies for bypass, data extraction, and structural parsing. Use when: extracting data from websites, monitoring price changes, or building data-driven agents."
---

# Advanced Web Scraping

Extract data reliably from any website, from simple HTML to complex SPAs.

## Methodology

1. **Analyze First**: Check `robots.txt` and network tabs for hidden APIs before scraping DOM.
2. **Choose the Tool**: 
    - `BeautifulSoup` (Fast, low memory) for static HTML.
    - `Playwright` (Heavy, JS-execution) for React/Vue sites or interaction.

## Core Patterns

### 1. The Playwright "Stealth" Approach
Simulate real user behavior to avoid detection.

```python
async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(
        user_agent="Mozilla/5.0 ...",
        viewport={'width': 1920, 'height': 1080}
    )
    page = await context.new_page()
    await page.goto(url, wait_until="networkidle")
```

### 2. Structured Extraction with CSS/XPath
Be specific to avoid breaking on layout changes.

```python
# BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
items = soup.select('.ranking-table tr.item-row')
for item in items:
    name = item.find('td', class_='name').text.strip()
```

### 3. Handling Pagination & Dynamic Loading
Scroll and wait for elements.

```python
while await page.is_visible('button.load-more'):
    await page.click('button.load-more')
    await page.wait_for_timeout(1000)
```

## Anti-Blocking Strategies

- **Random Delays**: Never scrape at constant intervals.
- **Header Rotation**: Rotate User-Agents and Referers.
- **Proxy Usage**: Use rotating proxies for high-volume tasks.

## Ethical Considerations

- Respect `robots.txt`.
- Don't overwhelm servers (Rate limit your requests).
- Use local caching to avoid re-fetching unchanged data.
