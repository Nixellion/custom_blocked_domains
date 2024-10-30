#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.error import URLError
import sys

# List of URLs to process
URLS = [
    "https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/Discord.lst",
    "https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/Meta.lst",
    "https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/Twitter.lst"
]

def download_and_process_url(url):
    """Download content from URL and format each line."""
    try:
        with urlopen(url) as response:
            content = response.read().decode('utf-8')
            
            # Process each non-empty line
            for line in content.splitlines():
                line = line.strip()
                if line:
                    formatted_line = "        list entry '{}'".format(line)
                    print(formatted_line)
                    
    except URLError as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error processing {url}: {e}", file=sys.stderr)
        return False
    
    return True

def main():
    if not URLS:
        print("No URLs specified. Please add URLs to the URLS list.", file=sys.stderr)
        sys.exit(1)
    
    success_count = 0
    for url in URLS:
        if download_and_process_url(url):
            success_count += 1
    
    total_urls = len(URLS)
    print(f"\nProcessed {success_count} out of {total_urls} URLs successfully", file=sys.stderr)
    
    if success_count != total_urls:
        sys.exit(1)

if __name__ == "__main__":
    main()