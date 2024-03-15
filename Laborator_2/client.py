import socket

def create_message(client_id, client_type, message_id, payload):
    return f"{client_id},{client_type},{message_id},{payload}"

def validate_input(client_id, client_type, message_id):
    if not (client_id.isdigit() and (client_type == '0' or client_type == '1') and message_id.isdigit() and 0 <= int(message_id) <= 5):
        print("Invalid input. Please enter valid client id, client type, and message id.")
        return False
    return True

def main():
    host = '127.0.0.1'
    port = 12345

    client_id = input("Enter Client Id: ")
    client_type = input("Enter Client Type (0 for Owner, 1 for Renter): ")

    if client_type not in ['0', '1']:
        print("Invalid client type. Exiting...")
        return

    while True:
        print("Message Id:")
        print("0 : register Renter")
        print("1 : register Owner")
        print("2 : post Car")
        print("3 : request Car")
        print("4 : start Rental")
        print("5 : end Rental")

        message_id = input("Enter Message Id: ")
        if not message_id.isdigit() or not 0 <= int(message_id) <= 5:
            print("Invalid message id. Please enter a valid message id.")
            continue

        payload = input("Enter Payload: ")

        if validate_input(client_id, client_type, message_id):
            message = create_message(client_id, client_type, message_id, payload)
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((host, port))
                    print("Sending message:", message)
                    client_socket.sendall(message.encode())
                    response = client_socket.recv(1024)
                    print("Server response:", response.decode())
            except Exception as e:
                print("An error occurred while sending the message:", str(e))

        continue_sending = input("Do you want to send another message? (yes/no): ")
        if continue_sending.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
