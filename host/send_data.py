import socket

def send_parameters_to_server(ip, port, params):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        # Send seven delimited parameters
        data = ','.join(params)
        s.sendall(data.encode('utf-8'))
        
        # Receive the response from the server
        response = s.recv(1024).decode('utf-8')
        print(f"Received response from server: {response}")

# Example usage:
params = ["table_name", "column1", "value1", "column2", "value2", "column3", "value3"]
send_parameters_to_server(ip, 8080, params)
