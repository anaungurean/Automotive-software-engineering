import socket

def process_message(message):
    client_id = message[0]
    client_type = message[1]
    message_id = message[2]
    payload = message[3:]

    message_to_be_sent = "Invalid message."

    if client_type == '0':
        if message_id == '2':
            print("Owner posted a car with payload:", payload)
            message_to_be_sent = "The car was posted successfully."
        elif message_id == '1':
            print("Owner registered with payload:", payload)
            message_to_be_sent = "Owner registered successfully."
        else:
            print("This command can't be made by an owner:", message)
            message_to_be_sent = "Invalid command for owner."

    elif client_type == '1':
        if message_id == '3':
            print("Renter requested a car with payload:", payload)
            message_to_be_sent = "Car request received. We'll match you with a car soon."
        elif message_id == '0':
            print("Renter registered with payload:", payload)
            message_to_be_sent = "Renter registered successfully."
        elif message_id == '4':
            print("Renter started a rental with payload:", payload)
            message_to_be_sent = "Rental started. Enjoy your ride!"
        elif message_id == '5':
            print("Renter ended a rental with payload:", payload)
            message_to_be_sent = "Rental ended. We hope you had a great experience."
        else:
            print("This command can't be made by a renter:", message)
            message_to_be_sent = "Invalid command for renter."

    return message_to_be_sent

def validate_message(message):
    if len(message) < 4:
        return False
    client_id = message[0]
    client_type = message[1]
    message_id = message[2]
    if not (client_id.isdigit() and (client_type == '0' or client_type == '1') and message_id.isdigit() and 0 <= int(message_id) <= 5):
        return False
    return True

def main():
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print("Server is listening...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode().split(",")
                    print("Received message:", message)
                    if validate_message(message):
                        confirmation = process_message(message)
                        conn.sendall(confirmation.encode())
                    else:
                        error_message = "Invalid message format."
                        conn.sendall(error_message.encode())

if __name__ == "__main__":
    main()
