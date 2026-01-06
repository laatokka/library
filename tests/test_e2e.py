import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }

def test_home_page_title(page: Page, live_server):
    page.goto(live_server.url)
    expect(page).to_have_title("Library System")
    # Updated to look for h3 because the cotton card component uses h3 for title
    expect(page.get_by_role("heading", name="Welcome to the Library")).to_be_visible()

def test_alpine_interaction(page: Page, live_server):
    page.goto(live_server.url)
    # Check if the button exists
    button = page.get_by_role("button", name="Toggle Details")
    expect(button).to_be_visible()

    # Check that details are initially hidden
    details = page.locator("div.border.rounded")
    expect(details).not_to_be_visible()

    # Click button
    button.click()

    # Check that details are visible
    expect(details).to_be_visible()
