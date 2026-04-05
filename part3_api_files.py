"""
Product Explorer & Error-Resilient Logger
Complete solution for all 4 tasks.
"""

import requests
from datetime import datetime

# ─────────────────────────────────────────────
# LOGGING UTILITY
# ─────────────────────────────────────────────

LOG_FILE = "error_log.txt"

def log_error(location: str, error_type: str, message: str) -> None:
    """Append a timestamped error entry to error_log.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {location}: {error_type} — {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


# ─────────────────────────────────────────────
# TASK 1 — FILE READ & WRITE BASICS
# ─────────────────────────────────────────────

def task1_write_and_read() -> None:
    print("\n" + "=" * 60)
    print("TASK 1 — FILE READ & WRITE BASICS")
    print("=" * 60)

    notes_file = "python_notes.txt"

    # ── Part A: Write ──
    initial_lines = [
        "Topic 1: Variables store data. Python is dynamically typed.\n",
        "Topic 2: Lists are ordered and mutable.\n",
        "Topic 3: Dictionaries store key-value pairs.\n",
        "Topic 4: Loops automate repetitive tasks.\n",
        "Topic 5: Exception handling prevents crashes.\n",
    ]

    with open(notes_file, "w", encoding="utf-8") as f:
        f.writelines(initial_lines)
    print("File written successfully.")

    # Append two additional lines
    extra_lines = [
        "Topic 6: Functions promote code reuse and modularity.\n",
        "Topic 7: File I/O allows programs to persist data beyond runtime.\n",
    ]
    with open(notes_file, "a", encoding="utf-8") as f:
        f.writelines(extra_lines)
    print("Lines appended.")

    # ── Part B: Read ──
    with open(notes_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("\n--- File Contents ---")
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line.rstrip()}")

    print(f"\nTotal lines: {len(lines)}")

    # Keyword search
    keyword = input("\nEnter a keyword to search: ").strip()
    matches = [line.rstrip() for line in lines if keyword.lower() in line.lower()]
    if matches:
        print(f"\nLines containing '{keyword}':")
        for m in matches:
            print(" ", m)
    else:
        print(f"No lines found containing '{keyword}'.")


# ─────────────────────────────────────────────
# TASK 2 — API INTEGRATION
# ─────────────────────────────────────────────

BASE_URL = "https://dummyjson.com/products"


def fetch_products(limit: int = 20) -> list[dict]:
    """Step 1: Fetch and display products as a formatted table."""
    url = f"{BASE_URL}?limit={limit}"
    try:
        response = requests.get(url, timeout=5)
        products = response.json().get("products", [])

        # Print formatted table
        header = f"{'ID':<4} | {'Title':<30} | {'Category':<15} | {'Price':>8} | {'Rating'}"
        print("\n" + header)
        print("-" * len(header))
        for p in products:
            print(
                f"{p['id']:<4} | {p['title'][:30]:<30} | "
                f"{p['category'][:15]:<15} | "
                f"${p['price']:>7.2f} | {p['rating']}"
            )
        return products

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("fetch_products", "ConnectionError", "Failed to connect to dummyjson.com")
        return []
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("fetch_products", "Timeout", "Request to dummyjson.com timed out")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("fetch_products", "Exception", str(e))
        return []


def filter_and_sort(products: list[dict]) -> None:
    """Step 2: Filter rating >= 4.5, sort by price descending."""
    filtered = [p for p in products if p.get("rating", 0) >= 4.5]
    filtered.sort(key=lambda p: p["price"], reverse=True)

    print("\n--- Products with Rating ≥ 4.5 (sorted by price, high→low) ---")
    for p in filtered:
        print(f"  [{p['rating']}★] {p['title'][:35]:<35} ${p['price']:.2f}")


def fetch_laptops() -> None:
    """Step 3: Fetch all laptops by category."""
    url = f"{BASE_URL}/category/laptops"
    try:
        response = requests.get(url, timeout=5)
        laptops = response.json().get("products", [])

        print("\n--- Laptops ---")
        for laptop in laptops:
            print(f"  {laptop['title']:<40} ${laptop['price']:.2f}")

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("fetch_laptops", "ConnectionError", "Failed to fetch laptops")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("fetch_laptops", "Timeout", "Laptop fetch timed out")
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("fetch_laptops", "Exception", str(e))


def post_custom_product() -> None:
    """Step 4: POST a simulated custom product."""
    url = f"{BASE_URL}/add"
    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API",
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        print("\n--- POST Response (Simulated) ---")
        print(response.json())

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("post_custom_product", "ConnectionError", "POST request failed")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("post_custom_product", "Timeout", "POST request timed out")
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("post_custom_product", "Exception", str(e))


def task2_api_integration() -> None:
    print("\n" + "=" * 60)
    print("TASK 2 — API INTEGRATION")
    print("=" * 60)

    products = fetch_products(limit=20)
    if products:
        filter_and_sort(products)
    fetch_laptops()
    post_custom_product()


# ─────────────────────────────────────────────
# TASK 3 — EXCEPTION HANDLING
# ─────────────────────────────────────────────

def safe_divide(a, b):
    """Part A: Guarded calculator."""
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


def read_file_safe(filename: str) -> str | None:
    """Part B: Guarded file reader."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    finally:
        print("File operation attempt complete.")


def lookup_product_loop() -> None:
    """Part D: Input validation loop for product lookup."""
    print("\n--- Product Lookup (type 'quit' to exit) ---")
    while True:
        user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()

        if user_input.lower() == "quit":
            print("Exiting product lookup.")
            break

        # Validate integer
        try:
            product_id = int(user_input)
        except ValueError:
            print("  ⚠ Please enter a valid integer.")
            continue

        if not (1 <= product_id <= 100):
            print("  ⚠ ID must be between 1 and 100.")
            continue

        # Make API call
        try:
            response = requests.get(f"{BASE_URL}/{product_id}", timeout=5)
        except requests.exceptions.ConnectionError:
            print("  Connection failed. Please check your internet.")
            log_error("lookup_product", "ConnectionError", "Failed to reach dummyjson.com")
            continue
        except requests.exceptions.Timeout:
            print("  Request timed out. Try again later.")
            log_error("lookup_product", "Timeout", "Lookup timed out")
            continue
        except Exception as e:
            print(f"  Unexpected error: {e}")
            log_error("lookup_product", "Exception", str(e))
            continue

        if response.status_code == 404:
            print("  Product not found.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {product_id}")
        elif response.status_code == 200:
            data = response.json()
            print(f"  ✔ {data['title']}  —  ${data['price']:.2f}")
        else:
            print(f"  Unexpected status code: {response.status_code}")


def task3_exception_handling() -> None:
    print("\n" + "=" * 60)
    print("TASK 3 — EXCEPTION HANDLING")
    print("=" * 60)

    # Part A
    print("\n--- Part A: safe_divide ---")
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(safe_divide("ten", 2))

    # Part B
    print("\n--- Part B: read_file_safe ---")
    content = read_file_safe("python_notes.txt")
    if content:
        print(f"  (File read OK — {len(content.splitlines())} lines)")
    read_file_safe("ghost_file.txt")

    # Part C is embedded in Task 2's API functions (try-except on every request).

    # Part D
    lookup_product_loop()


# ─────────────────────────────────────────────
# TASK 4 — LOGGING TO FILE
# ─────────────────────────────────────────────

def task4_logging() -> None:
    print("\n" + "=" * 60)
    print("TASK 4 — LOGGING TO FILE")
    print("=" * 60)

    # ── Trigger 1: ConnectionError via unreachable host ──
    print("\nTriggering ConnectionError log entry...")
    try:
        requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
    except requests.exceptions.ConnectionError as e:
        print("  Connection failed. Please check your internet.")
        log_error("fetch_products", "ConnectionError", str(e)[:80])
    except requests.exceptions.Timeout:
        print("  Request timed out.")
        log_error("fetch_products", "Timeout", "Unreachable host timed out")
    except Exception as e:
        log_error("fetch_products", "Exception", str(e)[:80])

    # ── Trigger 2: HTTP 404 for non-existent product ──
    print("Triggering HTTP 404 log entry...")
    try:
        response = requests.get(f"{BASE_URL}/999", timeout=5)
        if response.status_code != 200:
            log_error(
                "lookup_product",
                "HTTPError",
                f"{response.status_code} Not Found for product ID 999",
            )
            print(f"  Logged HTTP {response.status_code} for product ID 999.")
    except requests.exceptions.ConnectionError:
        print("  Connection failed.")
        log_error("lookup_product", "ConnectionError", "Could not reach server for ID 999")
    except Exception as e:
        log_error("lookup_product", "Exception", str(e))

    # ── Print the full log ──
    print("\n--- error_log.txt ---")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("  (No log entries yet.)")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    task1_write_and_read()
    task2_api_integration()
    task3_exception_handling()
    task4_logging()