#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.error import URLError
import sys
from pathlib import Path

# List of URLs containing domain lists, one per line
DOMAIN_LIST_URLS = [
    "https://raw.githubusercontent.com/GhostRooter0953/discord-voice-ips/refs/heads/master/voice_domains/discord-voice-domains-list",
]

# URL of the main nftset file
NFTSET_URL = "https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-dnsmasq-nfset.lst"

def download_file(url):
    """Download a file from URL and return its contents as string."""
    try:
        with urlopen(url) as response:
            return response.read().decode('utf-8')
    except URLError as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return None

def get_existing_domains(content):
    """Extract existing domains from nftset content."""
    domains = set()
    for line in content.splitlines():
        if line.startswith('nftset=/'):
            # Extract domain from nftset=/domain.com/4#inet#fw4#vpn_domains
            domain = line.split('/')[1]
            domains.add(domain)
    return domains

def format_domain(domain):
    """Format domain into nftset format."""
    return f"nftset=/{domain.strip()}/4#inet#fw4#vpn_domains"

def main():
    # Download the main nftset file
    nftset_content = download_file(NFTSET_URL)
    if nftset_content is None:
        print("Failed to download main nftset file. Exiting.", file=sys.stderr)
        sys.exit(1)

    # Get existing domains to avoid duplicates
    existing_domains = get_existing_domains(nftset_content)
    
    # Store all lines from the original file
    original_lines = nftset_content.splitlines()
    
    # Process each domain list URL
    new_domains = set()
    for url in DOMAIN_LIST_URLS:
        content = download_file(url)
        if content is None:
            continue
            
        # Process each domain in the file
        for domain in content.splitlines():
            domain = domain.strip()
            if domain and domain not in existing_domains:
                new_domains.add(domain)
                existing_domains.add(domain)  # Prevent duplicates across files

    # Add new formatted entries
    new_lines = original_lines + [format_domain(domain) for domain in sorted(new_domains)]
    
    # Write the updated content to a new file
    output_file = Path('inside-dnsmasq-nfset.lst')
    try:
        output_file.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
        print(f"Successfully processed {len(new_domains)} new domains")
        print(f"Output written to {output_file}")
    except IOError as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
