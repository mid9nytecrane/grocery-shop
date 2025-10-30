# test_firewall.py
import socket

def test_port_access():
    try:
        # Test connection to Gmail SMTP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('smtp.gmail.com', 587))
        sock.close()
        
        if result == 0:
            print("✓ Port 587 is accessible")
            return True
        else:
            print("✗ Port 587 is blocked (firewall likely)")
            return False
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

test_port_access()