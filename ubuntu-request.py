import requests
import os
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url):
    """Extract filename from URL or generate one if not available."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_image.jpg"

def is_duplicate(file_content, saved_files_hashes):
    """Check if the image has already been downloaded using a hash."""
    file_hash = hashlib.sha256(file_content).hexdigest()
    if file_hash in saved_files_hashes:
        return True
    saved_files_hashes.add(file_hash)
    return False

def fetch_image(url, saved_files_hashes):
    """Fetch and save image from a URL with assignment + challenge features."""
    try:
        # Respect: Identify ourselves to the wider community
        headers = {"User-Agent": "UbuntuImageFetcher/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors

        # Check content type (security precaution)
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped {url} (not an image, Content-Type={content_type})")
            return

        # Prevent duplicate downloads
        if is_duplicate(response.content, saved_files_hashes):
            print(f"✗ Skipped duplicate: {url}")
            return

        # Extract filename
        filename = get_filename_from_url(url)
        filepath = os.path.join("Fetched_Images", filename)

        # Handle duplicate filenames by renaming
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join("Fetched_Images", f"{base}_{counter}{ext}")
            counter += 1

        # Save in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred while fetching {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get one or more URLs
    urls = input("Please enter image URL(s) (comma-separated): ").split(",")

    # Create directory if not exists
    os.makedirs("Fetched_Images", exist_ok=True)

    # Track hashes to avoid duplicate downloads
    saved_files_hashes = set()

    # Process each URL
    for url in map(str.strip, urls):
        if url:
            fetch_image(url, saved_files_hashes)

    print("\nConnection strengthened. Community enriched.")
    print('"A person is a person through other persons." – Ubuntu Philosophy')

if __name__ == "__main__":
    main()
