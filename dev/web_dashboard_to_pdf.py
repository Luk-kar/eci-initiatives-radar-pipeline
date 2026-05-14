from playwright.sync_api import sync_playwright

port = 5500

url = f"http://localhost:{port}"
# from root
output_pdf = "page_to_export/goal_dashboard.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")

    # Get the exact height and width of the rendered page content
    dimensions = page.evaluate("""() => {
        return {
            width: document.documentElement.scrollWidth,
            height: document.documentElement.scrollHeight
        }
    }""")

    # Pass those dimensions to explicitly create a custom single-page size
    page.pdf(
        path=output_pdf,
        width=f"{dimensions['width']}px",
        height=f"{dimensions['height']}px",
        print_background=True,
        page_ranges="1",  # Ensures no blank overflow pages are added
    )
    browser.close()
