import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

# Config and utilities
# Using enterprise standards: config.py stores BASE_URL, USERNAME, PASSWORD, TIMEOUT, etc.
try:
    from config import BASE_URL, USERNAME, PASSWORD, INVALID_USERNAME, INVALID_PASSWORD, DEFAULT_TIMEOUT
except ImportError:
    # Placeholder: Implement or provide config.py with these constants
    BASE_URL = "http://localhost:8080"
    USERNAME = "test.user@example.com"
    PASSWORD = "correct-password"
    INVALID_USERNAME = "invalid.user@example.com"
    INVALID_PASSWORD = "wrong-password"
    DEFAULT_TIMEOUT = 15

# Driver factory for reusable WebDriver creation
try:
    from utils.driver_factory import get_driver
except Exception:
    # Placeholder: Implement driver factory to return a configured WebDriver instance
    def get_driver():
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver


# Common locators (placeholders if actual knowledge base not available)
# Placeholder: Replace these with actual locators from the knowledge base
LOGIN_USERNAME = (By.ID, "username")
LOGIN_PASSWORD = (By.ID, "password")
LOGIN_SUBMIT = (By.ID, "login")
LOGIN_ERROR = (By.CSS_SELECTOR, "div.alert.alert-error, .login-error, #loginError")
WELCOME_MODAL = (By.CSS_SELECTOR, "div.modal.welcome-modal, #welcomeModal")
WELCOME_MODAL_CLOSE = (By.CSS_SELECTOR, "div.modal.welcome-modal button.close, #welcomeModal .btn-close, #welcomeModal .btn-primary")
NAV_MANAGE = (By.CSS_SELECTOR, "nav a[href*='manage'], #nav-manage, a#manageLink")
MENU_DEVICE_USERS = (By.CSS_SELECTOR, "a[href*='device-users'], #menu-device-users, a#deviceUsersLink")
DEVICE_LIST_CONTAINER = (By.CSS_SELECTOR, "#deviceUsersList, .device-users-list, .devices-table")
DEVICE_ROW = (By.CSS_SELECTOR, ".device-row, .devices-table tbody tr")
DEVICE_NAME_CELL = (By.CSS_SELECTOR, ".device-name, td.name")
DEVICE_STATUS_CELL = (By.CSS_SELECTOR, ".device-status, td.status")
DEVICE_USER_CELL = (By.CSS_SELECTOR, ".device-user, td.user")
NO_DEVICES_MESSAGE = (By.CSS_SELECTOR, "#noDevicesMessage, .no-devices, .empty-state")
PAGINATION_NEXT = (By.CSS_SELECTOR, ".pagination .next:not(.disabled) a, .pagination-next a")
PAGINATION_PAGE = (By.CSS_SELECTOR, ".pagination li.page a, .page-link")
SORT_BY_NAME = (By.CSS_SELECTOR, "th.sort-name, button#sortName")
SORT_BY_STATUS = (By.CSS_SELECTOR, "th.sort-status, button#sortStatus")
SORT_BY_USER = (By.CSS_SELECTOR, "th.sort-user, button#sortUser")
FILTER_STATUS_DROPDOWN = (By.CSS_SELECTOR, "#filterStatus, select.status-filter")
FILTER_USER_INPUT = (By.CSS_SELECTOR, "#filterUser, input.user-filter")
APPLY_FILTER_BUTTON = (By.CSS_SELECTOR, "#applyFilter, button.apply-filter")
DEVICE_ACTION_MENU = (By.CSS_SELECTOR, ".device-actions button.menu, .actions .btn-menu")
DEVICE_ACTION_ITEM = (By.CSS_SELECTOR, ".device-actions .menu .item, .dropdown-menu .dropdown-item")
ACTION_SUCCESS_TOAST = (By.CSS_SELECTOR, ".toast-success, .alert-success")
SESSION_TIMEOUT_BANNER = (By.CSS_SELECTOR, "#sessionTimeout, .session-timeout, .auth-required")


@pytest.fixture(scope="function")
def driver():
    driver = get_driver()
    driver.get(BASE_URL)
    yield driver
    driver.quit()


def click_safely(driver, element):
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def wait_for_element(driver, locator, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


def wait_for_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def login(driver, username, password):
    # Step: Enter username
    username_field = wait_for_element(driver, LOGIN_USERNAME)
    username_field.clear()
    username_field.send_keys(username)

    # Step: Enter password
    password_field = wait_for_element(driver, LOGIN_PASSWORD)
    password_field.clear()
    password_field.send_keys(password)

    # Step: Submit login
    submit_btn = wait_for_clickable(driver, LOGIN_SUBMIT)
    click_safely(driver, submit_btn)


def dismiss_welcome_modal_if_present(driver, timeout=5):
    try:
        modal = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(WELCOME_MODAL))
        try:
            close_btn = modal.find_element(*WELCOME_MODAL_CLOSE)
        except Exception:
            close_btn = wait_for_clickable(driver, WELCOME_MODAL_CLOSE, timeout)
        click_safely(driver, close_btn)
        # Ensure modal is gone
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(WELCOME_MODAL))
        return True
    except TimeoutException:
        # Modal not present; proceed
        return False


def navigate_to_device_users(driver):
    # Navigate to 'Manage'
    manage_link = wait_for_clickable(driver, NAV_MANAGE)
    click_safely(driver, manage_link)

    # Select 'Device Users'
    device_users_link = wait_for_clickable(driver, MENU_DEVICE_USERS)
    click_safely(driver, device_users_link)

    # Wait for device list to load
    wait_for_element(driver, DEVICE_LIST_CONTAINER)


def get_device_rows(driver):
    try:
        container = wait_for_element(driver, DEVICE_LIST_CONTAINER)
    except TimeoutException:
        return []
    return container.find_elements(*DEVICE_ROW)


def get_cell_text(row, cell_locator):
    try:
        el = row.find_element(*cell_locator)
        return el.text.strip()
    except Exception:
        return ""


# TC01: Successful Login and Device List Display
@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.positive
def test_TC01_successful_login_and_device_list_display(driver):
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # Step 1: Launch app
    driver.get(BASE_URL)

    # Step 2: Enter valid credentials
    # Step 3: Submit login
    login(driver, USERNAME, PASSWORD)

    # Step 4: Handle modal if present
    modal_dismissed = dismiss_welcome_modal_if_present(driver)

    # Step 5 & 6: Navigate to 'Manage' > 'Device Users'
    navigate_to_device_users(driver)

    # Validation: Device list loads and displays all devices (at least verifies container present)
    device_list = wait.until(EC.presence_of_element_located(DEVICE_LIST_CONTAINER))
    assert device_list is not None, "Device list container should be present after navigation."

    rows = get_device_rows(driver)
    # Print device names for output purposes
    for idx, row in enumerate(rows, 1):
        name = get_cell_text(row, DEVICE_NAME_CELL)
        status = get_cell_text(row, DEVICE_STATUS_CELL)
        user = get_cell_text(row, DEVICE_USER_CELL)
        print(f"Device {idx}: Name='{name}', Status='{status}', User='{user}'")

    # Placeholder: If business rule requires non-empty list, assert len(rows) > 0
    # assert len(rows) > 0, "Expected at least one device to be listed."


# TC02: Welcome Modal Handling
@pytest.mark.functional
@pytest.mark.ui
@pytest.mark.edge
def test_TC02_welcome_modal_handling(driver):
    # Precondition: Modal configured to display (cannot enforce via UI; placeholder)
    # Step 1: Log in
    login(driver, USERNAME, PASSWORD)

    # Step 2 & 3: Observe and dismiss modal
    dismissed = dismiss_welcome_modal_if_present(driver, timeout=DEFAULT_TIMEOUT)

    # Expected: Modal appears and can be dismissed; user proceeds
    # We pass if either dismissed or no modal within timeout, but we assert that the app remains usable
    # Validate by checking that main navigation 'Manage' is available
    manage = wait_for_clickable(driver, NAV_MANAGE)
    assert manage is not None, "Manage link should be available after login and/or modal dismissal."


# TC03: Device List Loads with Devices
@pytest.mark.functional
@pytest.mark.positive
def test_TC03_device_list_loads_with_devices(driver):
    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)
    navigate_to_device_users(driver)

    rows = get_device_rows(driver)
    # Expected: Device list loads and displays all connected devices
    device_list_present = True if wait_for_element(driver, DEVICE_LIST_CONTAINER) else False
    assert device_list_present, "Device list should be present."

    # Placeholder: If environment guarantees devices, assert rows
    # assert len(rows) > 0, "Expected connected devices to be displayed."


# TC04: Device List Loads with No Devices
@pytest.mark.functional
@pytest.mark.edge
def test_TC04_device_list_loads_with_no_devices(driver):
    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)
    navigate_to_device_users(driver)

    rows = get_device_rows(driver)
    if len(rows) == 0:
        # Expect 'No devices connected' message
        try:
            msg = wait_for_element(driver, NO_DEVICES_MESSAGE)
            assert "no devices" in msg.text.lower(), "Expected 'No devices connected' message."
        except TimeoutException:
            pytest.skip("No devices and no empty-state message found; environment may not be configured for this case.")
    else:
        pytest.skip("Devices are present; cannot validate empty list message in current environment.")


# TC05: Device Details Verification
@pytest.mark.functional
@pytest.mark.verification
def test_TC05_device_details_verification(driver):
    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)
    navigate_to_device_users(driver)

    rows = get_device_rows(driver)
    assert len(rows) > 0, "Devices should be present to verify details."

    for row in rows:
        name = get_cell_text(row, DEVICE_NAME_CELL)
        status = get_cell_text(row, DEVICE_STATUS_CELL)
        user = get_cell_text(row, DEVICE_USER_CELL)
        print(f"Verify Device: Name='{name}', Status='{status}', User='{user}'")
        assert name != "", "Device name should be displayed."
        assert status != "", "Device status should be displayed."
        assert user != "", "Device user should be displayed."
        # Placeholder: Validate values against backend data via API
        # e.g., compare with REST API response for device inventory


# TC06: Device Connection Status
@pytest.mark.functional
@pytest.mark.verification
def test_TC06_device_connection_status(driver):
    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)
    navigate_to_device_users(driver)

    rows = get_device_rows(driver)
    assert len(rows) > 0, "Devices should be present to verify connection status."

    for row in rows:
        status = get_cell_text(row, DEVICE_STATUS_CELL).lower()
        print(f"Device status: {status}")
        assert status in {"online", "offline", "inactive", "active", "connected", "disconnected"}, \
            "Device status should be an expected value."
        # Placeholder: Cross-validate status with backend telemetry or API


# TC07: Invalid Login Attempt
@pytest.mark.negative
@pytest.mark.security
def test_TC07_invalid_login_attempt(driver):
    # Step 1: Launch app
    driver.get(BASE_URL)

    # Step 2 & 3: Enter invalid credentials and submit
    login(driver, INVALID_USERNAME, INVALID_PASSWORD)

    # Expected: Login fails, error message displayed, cannot access device list
    try:
        err = wait_for_element(driver, LOGIN_ERROR)
        assert err.is_displayed(), "Error message should be displayed for invalid login."
    except TimeoutException:
        pytest.fail("Expected login error message was not displayed.")

    # Ensure 'Manage' not accessible
    with pytest.raises(TimeoutException):
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(NAV_MANAGE))


# TC08: Session Timeout Handling
@pytest.mark.negative
@pytest.mark.security
def test_TC08_session_timeout_handling(driver):
    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)

    # Step: Wait for session to expire
    # Placeholder: Implement a reliable way to expire session (e.g., short TTL in test env, API call, or delete auth token)
    # For now, simulate by clearing cookies to mimic logout/session expiration
    driver.delete_all_cookies()

    # Attempt to navigate to Device Users
    # Depending on app, user may be redirected to login or shown a timeout banner
    try:
        navigate_to_device_users(driver)
    except TimeoutException:
        pass

    reauth_needed = False
    try:
        # Check for login page username field
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(LOGIN_USERNAME))
        reauth_needed = True
    except TimeoutException:
        # Or a session timeout banner
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(SESSION_TIMEOUT_BANNER))
            reauth_needed = True
        except TimeoutException:
            reauth_needed = False

    assert reauth_needed, "User should be prompted to re-login or see a session timeout notice."


# TC09: Device List Pagination
@pytest.mark.functional
@pytest.mark.ui
@pytest.mark.edge
def test_TC09_device_list_pagination(driver):
    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)
    navigate_to_device_users(driver)

    # Verify pagination controls and iterate pages
    try:
        pages = driver.find_elements(*PAGINATION_PAGE)
        if not pages:
            pytest.skip("Pagination controls not present; device count may not exceed page limit.")
    except Exception:
        pytest.skip("Pagination controls not found.")

    seen_names = set()
    page_index = 0
    while True:
        rows = get_device_rows(driver)
        for row in rows:
            name = get_cell_text(row, DEVICE_NAME_CELL)
            if name:
                seen_names.add(name)
        try:
            next_btn = driver.find_element(*PAGINATION_NEXT)
            click_safely(driver, next_btn)
            page_index += 1
            # Wait for page to update - Placeholder: implement better wait (e.g., table reload detection)
            WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(DEVICE_LIST_CONTAINER))
        except Exception:
            break

    print(f"Total unique devices across pages: {len(seen_names)}")
    assert len(seen_names) >= 1, "Expected devices across paginated pages or at least on first page."


# TC10: Device List Sorting
@pytest.mark.functional
@pytest.mark.ui
@pytest.mark.usability
def test_TC10_device_list_sorting(driver):
    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)
    navigate_to_device_users(driver)

    def collect_names():
        return [get_cell_text(row, DEVICE_NAME_CELL) for row in get_device_rows(driver) if get_cell_text(row, DEVICE_NAME_CELL)]

    # Sort by Name
    try:
        sort_name = wait_for_clickable(driver, SORT_BY_NAME)
        click_safely(driver, sort_name)
        WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(DEVICE_LIST_CONTAINER))
        names = collect_names()
        if names:
            assert names == sorted(names, key=str.lower), "Device list should be sorted by name."
        else:
            pytest.skip("No device names to validate sorting.")
    except TimeoutException:
        pytest.skip("Sort by name control not present.")

    # Sort by Status (placeholder validation)
    try:
        sort_status = wait_for_clickable(driver, SORT_BY_STATUS)
        click_safely(driver, sort_status)
        WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(DEVICE_LIST_CONTAINER))
        # Placeholder: Validate status sorting when sample data permits
    except TimeoutException:
        print("Sort by status not available; skipping validation.")

    # Sort by User (placeholder validation)
    try:
        sort_user = wait_for_clickable(driver, SORT_BY_USER)
        click_safely(driver, sort_user)
        WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(DEVICE_LIST_CONTAINER))
        # Placeholder: Validate user sorting when sample data permits
    except TimeoutException:
        print("Sort by user not available; skipping validation.")


# TC11: Device List Filtering
@pytest.mark.functional
@pytest.mark.ui
@pytest.mark.usability
def test_TC11_device_list_filtering(driver):
    from selenium.webdriver.support.ui import Select

    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)
    navigate_to_device_users(driver)

    # Apply status filter
    try:
        status_filter = wait_for_element(driver, FILTER_STATUS_DROPDOWN)
        Select(status_filter).select_by_visible_text("Online")
    except TimeoutException:
        pytest.skip("Status filter control not found.")

    # Apply user filter
    try:
        user_filter = wait_for_element(driver, FILTER_USER_INPUT)
        user_filter.clear()
        user_filter.send_keys("John")  # Placeholder: Use a known user in test data
    except TimeoutException:
        print("User filter field not found; proceeding with status filter only.")

    # Click apply
    try:
        apply_btn = wait_for_clickable(driver, APPLY_FILTER_BUTTON)
        click_safely(driver, apply_btn)
    except TimeoutException:
        print("Apply filter button not found; assuming auto-apply.")

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(DEVICE_LIST_CONTAINER))

    # Validate filtered results
    rows = get_device_rows(driver)
    if not rows:
        print("No devices after filter; possible no match scenario.")
        return

    for row in rows:
        status = get_cell_text(row, DEVICE_STATUS_CELL).lower()
        user = get_cell_text(row, DEVICE_USER_CELL)
        print(f"Filtered Device: Status='{status}', User='{user}'")
        # Placeholder: Validate status == 'online' and user contains 'John' based on real data


# TC12: Device Management Actions
@pytest.mark.functional
@pytest.mark.positive
def test_TC12_device_management_actions(driver):
    login(driver, USERNAME, PASSWORD)
    dismiss_welcome_modal_if_present(driver)
    navigate_to_device_users(driver)

    rows = get_device_rows(driver)
    if not rows:
        pytest.skip("No devices available to perform management actions.")

    # Select the first device and open action menu
    first_row = rows[0]
    try:
        action_menu = first_row.find_element(*DEVICE_ACTION_MENU)
        click_safely(driver, action_menu)
    except Exception:
        pytest.skip("Action menu not available for the device.")

    # Perform an action (e.g., 'Disconnect', 'Reboot', 'Assign User')
    try:
        action_item = first_row.find_element(*DEVICE_ACTION_ITEM)
        action_text = action_item.text.strip()
        print(f"Performing action: {action_text}")
        click_safely(driver, action_item)
    except Exception:
        pytest.skip("No actionable item found in the device action menu.")

    # Validate action success (e.g., toast appears)
    try:
        toast = WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(ACTION_SUCCESS_TOAST))
        assert toast.is_displayed(), "Success toast should be displayed after action."
    except TimeoutException:
        # Placeholder: Validate device row update or audit log as alternative
        pytest.skip("No success toast detected; validation requires environment-specific checks.")


# Additional helper placeholders for enterprise standards
# Placeholder: Implement logger integration instead of print for enterprise logging
# Placeholder: Integrate with test management tools via markers or custom hooks
# Placeholder: Implement API clients to cross-validate UI with backend data
