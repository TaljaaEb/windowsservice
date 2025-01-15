import socket

def get_ip_from_dns(dns_name):
    ip_address = socket.gethostbyname(dns_name)
    return ip_address

# Example usage:
ip = get_ip_from_dns('www.somestorename.com')
print(f'IP address of www.somestorename.com: {ip}')
