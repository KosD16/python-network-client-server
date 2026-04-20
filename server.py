import socket
import struct
import threading
import ssl
import logging


logging.basicConfig(filename='network_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


def create_ssl_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem') 
    return context


def tcp_ipv4_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))  
    server.listen(5) 
    print("Ο διακομιστής IPv4 TCP λειτουργεί στη θύρα 12345!")

    while True:
        conn, addr = server.accept()
        print(f"Σύνδεση από: {addr}")
        threading.Thread(target=handle_tcp_connection, args=(conn, addr), daemon=True).start()


def tcp_ipv6_server():
    server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server.bind(("::1", 12345)) 
    server.listen(5)
    print("Ο διακομιστής IPv6 TCP λειτουργεί στη θύρα 12345!")

    while True:
        conn, addr = server.accept()
        print(f"Σύνδεση από: {addr}")
        threading.Thread(target=handle_tcp_connection, args=(conn, addr), daemon=True).start()


def handle_tcp_connection(conn, addr):
    print(f"Διαχείριση σύνδεσης από {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"Η σύνδεση με τον πελάτη {addr} διακόπηκε.")
                break
            print(f"Λήψη από {addr}: {data.decode()}")
            conn.sendall(data)  
        except ConnectionError:
            break
    conn.close()
    print(f"Η σύνδεση με {addr} έκλεισε.")

def udp_ipv4_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("127.0.0.1", 12346))  
    print("Ο διακομιστής IPv4 UDP λειτουργεί στη θύρα 12346.")

    while True:
        try:
            data, addr = server.recvfrom(1024)
            print(f"Λήψη από {addr}: {data.decode()}")
            server.sendto(data, addr)  
        except Exception as e:
            print(f"Σφάλμα κατά τη λήψη ή αποστολή δεδομένων: {e}")


def udp_ipv6_server():
    server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    server.bind(("::1", 12346))  
    print("Ο διακομιστής IPv6 UDP λειτουργεί στη θύρα 12346.")

    while True:
        try:
            data, addr = server.recvfrom(1024)
            print(f"Λήψη από {addr}: {data.decode()}")
            server.sendto(data, addr)
        except Exception as e:
            print(f"Σφάλμα κατά τη λήψη ή αποστολή δεδομένων: {e}")


def multicast_receiver(ip_version):
    if ip_version == "IPv4":
        multicast_group = '224.1.1.1'  
        port = 12347
        family = socket.AF_INET
        mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    elif ip_version == "IPv6":
        multicast_group = 'ff02::1'  
        port = 12347
        family = socket.AF_INET6
        mreq = struct.pack("16sI", socket.inet_pton(socket.AF_INET6, multicast_group), 0)
    else:
        print("Μη έγκυρη επιλογή.")
        return

    try:
        receiver = socket.socket(family, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver.bind(('', port))

        if ip_version == "IPv4":
            receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        else:
            receiver.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        print(f"Δέκτης multicast ({ip_version}) λειτουργεί στη θύρα {port}...")

        while True:
            data, addr = receiver.recvfrom(1024)
            print(f"Λήψη από {addr}: {data.decode()}")

    except Exception as e:
        print(f"Σφάλμα: {e}")
    finally:
        receiver.close()
        print("Δέκτης multicast έκλεισε.")



def broadcast_receiver():
    try:
        receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver.bind(('', 12348)) 
        print("Δέκτης broadcast σε λειτουργία στη θύρα 12348...")

        while True:
            data, addr = receiver.recvfrom(1024)
            print(f"Λήψη από {addr}: {data.decode()}")

    except Exception as e:
        print(f"Σφάλμα: {e}")
    finally:
        receiver.close()
        print("Δέκτης broadcast έκλεισε.")

if __name__ == "__main__":
    print("Εκτέλεση διακομιστών για TCP, UDP, Multicast και Broadcast.")
    threading.Thread(target=tcp_ipv4_server, daemon=True).start()
    threading.Thread(target=tcp_ipv6_server, daemon=True).start()
    threading.Thread(target=udp_ipv4_server, daemon=True).start()
    threading.Thread(target=udp_ipv6_server, daemon=True).start()
    threading.Thread(target=multicast_receiver, args=("IPv4",), daemon=True).start()
    threading.Thread(target=multicast_receiver, args=("IPv6",), daemon=True).start()
    threading.Thread(target=broadcast_receiver, daemon=True).start()

    while True:
        command = input("Πληκτρολογήστε 'exit' για τερματισμό: ")
        if command.lower() == 'exit':
            break
