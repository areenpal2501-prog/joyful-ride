async def run_test(page, output_dir, page_url):
    import os
    from playwright.async_api import TimeoutError as PlaywrightTimeoutError

    await page.set_viewport_size({"width": 375, "height": 667})
    try:
        await page.wait_for_selector('[data-testid="home-screen"]', timeout=12000)
        print('PASS: home screen loaded')
        await page.screenshot(path='/app/test_reports/screens/automation_output/20261124_073416_50e1506e09c1/home.jpeg', type="jpeg", quality=40, full_page=False)

        await page.get_by_text('Sightseeing', exact=True).click(force=True)
        await page.wait_for_selector('[data-testid="explore-screen"]', timeout=8000)
        await page.wait_for_timeout(800)
        assert await page.get_by_text('Sunset Harbor', exact=True).count() > 0
        print('PASS: explore loaded destinations')

        await page.get_by_text('Sunset Harbor', exact=True).last.click(force=True)
        await page.wait_for_timeout(500)
        await page.wait_for_selector('[data-testid="confirm-ride-button"]', timeout=8000)
        assert await page.get_by_text('Book your ride', exact=True).count() > 0
        print('PASS: destination opened booking')

        pickup = page.locator('input').first
        dropoff = page.locator('input').nth(1)
        await pickup.fill('TEST Downtown')
        await dropoff.fill('TEST Sunset Harbor')
        await page.wait_for_timeout(1200)
        button = page.locator('[data-testid="confirm-ride-button"]')
        assert await button.is_enabled()
        print('PASS: estimate enabled confirmation')
        await button.scroll_into_view_if_needed()
        await button.click(force=True)
        await page.wait_for_selector('[data-testid="trip-screen"]', timeout=10000)
        assert await page.get_by_text('Maya Chen', exact=True).count() > 0
        assert await page.get_by_text('Driver confirmed', exact=True).count() > 0
        print('PASS: booking opened live trip')

        await page.get_by_role('button', name='chevron-down').click(force=True)
        await page.wait_for_selector('[data-testid="home-screen"]', timeout=8000)
        # navigate trips tab by visible tab label
        await page.get_by_text('Trips', exact=True).last.click(force=True)
        await page.wait_for_selector('[data-testid="trips-screen"]', timeout=8000)
        assert await page.get_by_text('Your ride is on its way', exact=True).count() > 0
        print('PASS: trips shows persisted active booking')

    except AssertionError as e:
        print(f'FINDING: assertion failed: {e}')
    except Exception as e:
        print(f'FINDING: flow error: {e}')
        try:
            await page.screenshot(path='/app/test_reports/screens/automation_output/20261124_073416_50e1506e09c1/failure.jpeg', type="jpeg", quality=40, full_page=False)
        except Exception:
            pass

    error_text = await page.evaluate("""() => { const errorElements = Array.from(document.querySelectorAll('.error, [class*='error'], [id*='error']')); return errorElements.map(el => el.textContent).join(', '); }""")
    if error_text:
        print(f'Found error message: {error_text}')
    else:
        print('No error messages found on the page')
