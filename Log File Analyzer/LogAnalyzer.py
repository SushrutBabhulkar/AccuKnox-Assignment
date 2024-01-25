import re
from collections import Counter

# Function to parse log entries and extract relevant information
def parse_log_entry(log_entry):
    match = re.match(r'(\d+\.\d+\.\d+\.\d+) - - \[.*\] "(\w+) ([^"]+).*" (\d+) \d+ "([^"]+)" "([^"]+)"', log_entry)
    
    if match:
        ip_address, method, requested_page, status_code, referrer, user_agent = match.groups()
        return ip_address, method, requested_page, status_code, referrer, user_agent
    return None

#Function to analyze logs and genrate report
def analyze_logs(log_file):
    with open(log_file, 'r') as f:
        logs = f.readlines()

    
    status_codes = Counter()
    requested_pages = Counter()
    ip_addresses = Counter()
    os_types = Counter()

    
    def simplify_os(os_info):
        return os_info.strip() if os_info else "Unknown"

    # Analyze each log entry
    for log_entry in logs:
        parsed_entry = parse_log_entry(log_entry)
        if parsed_entry:
            ip_address, _, requested_page, status_code, _, user_agent = parsed_entry

            status_codes[status_code] += 1

            requested_pages[requested_page] += 1

            ip_addresses[ip_address] += 1

            
            if user_agent and 'Mozilla' in user_agent:
                os_info_match = re.search(r'\((.*?)\)', user_agent)
                os_info_parts = os_info_match.group(1).split(';')[1:] if os_info_match else []
                os_info = os_info_parts[0] if os_info_parts else None
                simplified_os = simplify_os(os_info)
                os_types[simplified_os] += 1

    print("---Summary report ---")
    print("Number of 404 errors:", status_codes['404'])
    print("Number of successful requests (Status code 200):", status_codes['200'])
    print("\nTop 3 requested pages:")
    for page, count in requested_pages.most_common(3):
        print(f"{page}: {count} requests")

    print("\nTop 3 IP addresses with most requests:")
    for ip, count in ip_addresses.most_common(3):
        print(f"{ip}: {count} requests")

    print("\nTop 3 OS types:")
    for os_type, count in os_types.most_common(3):
        print(f"{os_type}: {count} requests")

analyze_logs('logs.txt')

