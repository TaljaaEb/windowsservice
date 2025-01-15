import socket

def get_ip_from_dns(dns_name):
    ip_address = socket.gethostbyname(dns_name)
    return ip_address

# Example usage:
ip = get_ip_from_dns('www.somestorename.com')
print(f'IP address of www.somestorename.com: {ip}')


import socket

def connect_to_backend(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        return s
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return None

# Example usage:
s = connect_to_backend(ip, 5000)
if s:
    print("Connected to backend")
    # You can now send/receive data
