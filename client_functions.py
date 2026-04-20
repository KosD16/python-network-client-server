import socket
import struct
import threading

# -------------------------------
# Λειτουργίες Πελάτη TCP και UDP
# -------------------------------

# Συνάρτηση πελάτη TCP
def tcp_client(ip_version):
    # Ρύθμιση διευθύνσεων ανάλογα με το αν χρησιμοποιείται IPv4 ή IPv6
    if ip_version == "IPv4":
        family = socket.AF_INET
        address = ("127.0.0.1", 12345)  # Διεύθυνση IPv4 και port για σύνδεση
    elif ip_version == "IPv6":
        family = socket.AF_INET6
        address = ("::1", 12345)  # Διεύθυνση IPv6 και port για σύνδεση
    else:
        print("Μη έγκυρη επιλογή.")
        return

    try:
        # Δημιουργία TCP socket
        client = socket.socket(family, socket.SOCK_STREAM)
        client.connect(address)  # Σύνδεση στον server
        print(f"Συνδεθήκατε στον διακομιστή TCP {ip_version}.")

        while True:
            # Ανάγνωση μηνύματος από τον χρήστη
            message = input("Πληκτρολογήστε μήνυμα ('exit' για τερματισμό): ")
            if message.lower() == "exit":  # Έξοδος αν πληκτρολογηθεί 'exit'
                break
            client.sendall(message.encode())  # Αποστολή του μηνύματος στον server
            response = client.recv(1024)  # Λήψη απάντησης
            print(f"Απάντηση: {response.decode()}")

    except ConnectionRefusedError:
        print("Δεν μπόρεσε να συνδεθεί με τον διακομιστή.")
    except Exception as e:
        print(f"Σφάλμα: {e}")
    finally:
        # Κλείσιμο της σύνδεσης
        client.close()
        print("Η σύνδεση έκλεισε.")

# Συνάρτηση πελάτη UDP
def udp_client(ip_version):
    # Ρύθμιση διευθύνσεων ανάλογα με το IPv4 ή IPv6
    if ip_version == "IPv4":
        family = socket.AF_INET
        address = ("127.0.0.1", 12346)  # IP και port για UDP
    elif ip_version == "IPv6":
        family = socket.AF_INET6
        address = ("::1", 12346)
    else:
        print("Μη έγκυρη επιλογή.")
        return

    try:
        # Δημιουργία UDP socket
        client = socket.socket(family, socket.SOCK_DGRAM)
        print(f"Έτοιμοι για επικοινωνία με τον UDP διακομιστή {ip_version}.")

        while True:
            # Ανάγνωση μηνύματος από τον χρήστη
            message = input("Πληκτρολογήστε μήνυμα ('exit' για τερματισμό): ")
            if message.lower() == "exit":
                break
            client.sendto(message.encode(), address)  # Αποστολή δεδομένων
            response, server_addr = client.recvfrom(1024)  # Λήψη απάντησης
            print(f"Απάντηση από {server_addr}: {response.decode()}")

    except Exception as e:
        print(f"Σφάλμα: {e}")
    finally:
        # Κλείσιμο της επικοινωνίας
        client.close()
        print("Η επικοινωνία τερματίστηκε.")

# -------------------------------
# Λειτουργίες Multicast
# -------------------------------

# Αποστολέας Multicast
def multicast_sender(ip_version):
    if ip_version == "IPv4":
        multicast_group = '224.1.1.1'  # Διεύθυνση multicast για IPv4
        port = 12347
        family = socket.AF_INET
        ttl = struct.pack('b', 2)  # TTL (Time-To-Live) = 2 για τοπικό δίκτυο
    elif ip_version == "IPv6":
        multicast_group = 'ff02::1'  # Διεύθυνση multicast για IPv6
        port = 12347
        family = socket.AF_INET6
    else:
        print("Μη έγκυρη επιλογή.")
        return

    try:
        # Δημιουργία UDP socket
        sender = socket.socket(family, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Ρύθμιση TTL για IPv4
        if ip_version == "IPv4":
            sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        print(f"Ξεκινώντας αποστολή multicast ({ip_version}) στη διεύθυνση {multicast_group}...")

        while True:
            # Ανάγνωση μηνύματος από τον χρήστη
            message = input("Πληκτρολογήστε το μήνυμα σας ('exit' για τερματισμό): ")
            if message.lower() == 'exit':
                break
            sender.sendto(message.encode(), (multicast_group, port))  # Αποστολή του μηνύματος

    except Exception as e:
        print(f"Σφάλμα: {e}")
    finally:
        # Κλείσιμο του socket
        sender.close()
        print("Τερματισμός αποστολέα multicast.")

# -------------------------------
# Λειτουργίες Broadcast για IPv4
# -------------------------------

# Αποστολέας Broadcast
def broadcast_sender():
    try:
        # Δημιουργία UDP socket για broadcast
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Ενεργοποίηση broadcast
        broadcast_address = '<broadcast>'  # Broadcast διεύθυνση
        port = 12348
        print("Ξεκινώντας αποστολή broadcast στη διεύθυνση broadcast...")

        while True:
            # Ανάγνωση μηνύματος από τον χρήστη
            message = input("Πληκτρολογήστε το μήνυμα σας ('exit' για τερματισμό): ")
            if message.lower() == 'exit':
                break
            sender.sendto(message.encode(), (broadcast_address, port))  # Αποστολή broadcast μηνύματος

    except Exception as e:
        print(f"Σφάλμα: {e}")
    finally:
        # Κλείσιμο του socket
        sender.close()
        print("Τερματισμός αποστολέα broadcast.")

# -------------------------------
# Κύρια Συνάρτηση Εκκίνησης
# -------------------------------

if __name__ == "__main__":
    # Μενού επιλογών client
    print("Επιλέξτε λειτουργία πελάτη:")
    print("1. TCP Client (IPv4)")
    print("2. TCP Client (IPv6)")
    print("3. UDP Client (IPv4)")
    print("4. UDP Client (IPv6)")
    print("5. Multicast Sender (IPv4)")
    print("6. Multicast Sender (IPv6)")
    print("7. Broadcast Sender (IPv4)")

    choice = input("Εισάγετε την επιλογή σας (1-7): ")

    # Εκκίνηση της αντίστοιχης λειτουργίας
    if choice == "1":
        tcp_client("IPv4")
    elif choice == "2":
        tcp_client("IPv6")
    elif choice == "3":
        udp_client("IPv4")
    elif choice == "4":
        udp_client("IPv6")
    elif choice == "5":
        multicast_sender("IPv4")
    elif choice == "6":
        multicast_sender("IPv6")
    elif choice == "7":
        broadcast_sender()
    else:
        print("Μη έγκυρη επιλογή. Τερματισμός.")
