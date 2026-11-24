async def run_test(page, output_dir, page_url):
    from playwright.async_api import TimeoutError as PlaywrightTimeoutError
    await page.set_viewport_size({"width":375,"height":667})
    try:
        await page.wait_for_selector('[data-testid="trips-screen"]', timeout=10000)
        print('PASS: trips screen loaded')
        await page.wait_for_timeout(700)
        body = await page.locator('body').inner_text()
        if 'Your ride is on its way' in body or 'No past rides just yet.' in body:
            print('PASS: trips history state rendered')
        else:
            print('FINDING: trips screen missing expected booking/empty state')
        # profile via tab label
        await page.get_by_text('Profile', exact=True).last.click(force=True)
        await page.wait_for_selector('[data-testid="profile-screen"]', timeout=8000)
        assert await page.get_by_text('Preferences', exact=True).count() > 0
        assert await page.get_by_text('Continue with Google', exact=True).count() > 0
        print('PASS: profile and sign-in entry rendered')
    except AssertionError as e:
        print(f'FINDING: assertion failed: {e}')
    except Exception as e:
        print(f'FINDING: flow error: {e}')
    error_text = await page.evaluate("""() => { const errorElements = Array.from(document.querySelectorAll('.error, [class*="error"], [id*="error"]')); return errorElements.map(el => el.textContent).join(', '); }""")
    if error_text:
        print(f'Found error message: {error_text}')
    else:
        print('No error messages found on the page')
