import csv
from robocorp.tasks import task
from robocorp import browser
from robocorp import storage
from RPA.PDF import PDF
from pathlib import Path
from RPA.Archive import Archive
from datetime import datetime

OUTPUT = Path("output")
FILES = Path("output/files")
SCREENSHOTS = Path("output/screenshots")
RECEIPTS = Path("output/receipts")
ARCHIVE = Path("output/archive")
OUTPUT.mkdir(exist_ok=True)
FILES.mkdir(exist_ok=True)
SCREENSHOTS.mkdir(exist_ok=True)
RECEIPTS.mkdir(exist_ok=True)
ARCHIVE.mkdir(exist_ok=True)

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    open_robot_order_website()
    close_website_modal()
    orders = get_orders()
    for order in orders:
        fill_in_the_form(order)
        ss_path = screenshot_robot(order["Order number"])
        pdf_path = store_receipt_as_pdf(order["Order number"])
        embed_screenshot_to_receipt(ss_path, pdf_path)
        order_another_robot()
        close_website_modal()
    archive_receipts()

def open_robot_order_website():
    """Navigates to the given URL."""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def close_website_modal():
    """Closes modal if exists."""
    page = browser.page()
    modal_buttons = page.locator("button:has-text('I guess so...')")
    if modal_buttons.count() > 0:
        modal_buttons.first.click()
        print("Modal closed.")

def get_orders():
    """Download orders .csv-file."""
    csv_path = FILES/"orders.csv"
    storage.get_file("orders.csv", path=csv_path, exist_ok=True)
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def fill_in_the_form(order):
    """Fills in the form."""
    page = browser.page()
    page.select_option("#head", order["Head"])
    page.check(f"#id-body-{order['Body']}")
    page.locator("[placeholder='Enter the part number for the legs']").fill(order["Legs"])
    page.fill("#address", order["Address"])
    for i in range(3):
        page.click("#order")
        page.wait_for_timeout(500)
        if not page.locator("text=/error/i").first.is_visible(timeout=1000):
            return
    raise RuntimeError("Clicking Order-button has failed 3 times in a row.")

def screenshot_robot(order_number):
    """Screenshot the robot and the receipt."""
    page = browser.page()
    ss_path = SCREENSHOTS/f"{order_number}.png"
    preview = page.locator("#robot-preview")
    preview.wait_for(state="visible")
    page.screenshot(path=ss_path)
    return ss_path

def store_receipt_as_pdf(order_number):
    """Store receipt as PDF."""
    pdf = PDF()
    receipt_path = RECEIPTS/f"Receipt_order_{order_number}.pdf"
    pdf.html_to_pdf(f"Receipt_order_{order_number}", receipt_path)
    return receipt_path

def embed_screenshot_to_receipt(screenshot, pdf_file):
    """Embed screenshot to the receipt PDF."""
    pdf = PDF()
    pdf.add_files_to_pdf([screenshot], pdf_file, append=True)

def order_another_robot():
    """Simple function to click ordering another robot."""
    page = browser.page()
    page.click("#order-another")

def archive_receipts():
    """Archives saved receipts."""
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    Archive().archive_folder_with_zip(folder=str(RECEIPTS), archive_name=str(ARCHIVE/f"receipts_{stamp}.zip"))