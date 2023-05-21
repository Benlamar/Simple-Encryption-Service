import socket
import os
from cryptography.fernet import Fernet

KEY_FILE = 'encryption_key.key'

def generate_key():
    if os.path.isfile(KEY_FILE):
        print("Key file already exists.")
        return

    key = Fernet.generate_key()
    try:
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    except Exception as e:
        print(f"Failed to generate {e}")

    print(f"Key generated and saved to {KEY_FILE}")

def load_key():
    if not os.path.isfile(KEY_FILE):
        generate_key()
    try:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
        return key
    except Exception as e:
        print(f"Cannot read key file{e}")
        return None
        
def encrypt_file(file_path):
    key = load_key()

    if not key:
        print("Cannot load key")
        return
    with open(file_path, 'rb') as file:
        data = file.read()

    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)

    return encrypted_data

def decrypt_file(encrypted_data):
    key = load_key()

    if not key:
        print("Cannot load key")
        return
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    return decrypted_data

def run_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}...")

        while True:
            conn, addr = server_socket.accept()
            data = conn.recv(1024)

            command, source_path, dest_path = data.decode().split(',')

            if command == 'encrypt':
                encrypted_data = encrypt_file(source_path)
                with open(dest_path, 'wb') as file:
                    file.write(encrypted_data)
                print(f"File encrypted and saved to {dest_path}")

            elif command == 'decrypt':
                with open(source_path, 'rb') as file:
                    encrypted_data = file.read()

                decrypted_data = decrypt_file(encrypted_data)
                with open(dest_path, 'wb') as file:
                    file.write(decrypted_data)
                print(f"File decrypted and saved to {dest_path}")

        print("Connection closed")

# def send_command(host, port, command, source_path, dest_path):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#         client_socket.connect((host, port))

#         message = f"{command};{source_path};{dest_path}"
#         client_socket.sendall(message.encode())

#         print(f"Command '{command}' sent to server")


if __name__ == '__main__':
    host = 'localhost'
    port = 8111

    # Run the server in one terminal
    run_server(host, port)

    # In another terminal, use the below code to send a command to the server
    # command = 'encrypt'  # or 'decrypt'
    # source_path = 'path_to_source_file'
    # dest_path = 'path_to_destination_file'
    # key = b'encryption_key'
    # send_command(host, port, command, source_path, dest_path, key)
