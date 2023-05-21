import socket

def send_command(host, port, command, source_path, dest_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        message = f"{command},{source_path},{dest_path}"
        client_socket.sendall(message.encode())

        print(f"Command '{command}' sent to server")

if __name__ == '__main__':
    host = 'localhost'
    port = 8111

    # In another terminal, use the below code to send a command to the server
    command = 'encrypt'  # or 'decrypt'
    source_path = r'C:\Users\file0.pdf'
    dest_path = r'C:\Users\file0.pdf.enc'
    send_command(host, port, command, source_path, dest_path)
