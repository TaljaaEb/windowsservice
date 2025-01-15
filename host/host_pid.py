import socketserver

class MyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip().decode('utf-8')
        print(f"Received data: {data}")
        
        # Split by delimiter (e.g., comma)
        params = data.split(',')
        if len(params) == 7:
            self.construct_sql_statement(params)
        else:
            print("Invalid number of parameters")

    def construct_sql_statement(self, params):
        # Create a SQL query from the received parameters
        sql = f"SELECT * FROM {params[0]} WHERE {params[1]} = {params[2]} AND {params[3]} = {params[4]} AND {params[5]} = {params[6]}"
        print(f"Constructed SQL statement: {sql}")
        self.execute_sql_and_send_result(sql)

    def execute_sql_and_send_result(self, sql):
        # Simulate executing the SQL and sending back results
        print(f"Executing SQL: {sql}")
        # Normally, you would interact with a real database, but here we simulate
        result = "Sample result based on SQL query"
        self.request.sendall(result.encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080
    server = socketserver.TCPServer((HOST, PORT), MyRequestHandler)
    print(f"Server running on {HOST}:{PORT}")
    server.serve_forever()
