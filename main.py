import paramiko
from colorama import init, Fore, Style

def configure_bridge(hostname, username, password, bridge_name, interface_list):
    # Membuat objek SSHClient
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Melakukan koneksi SSH ke perangkat MikroTik
        ssh_client.connect(hostname, username=username, password=password)

        # Membuka channel SSH
        ssh_channel = ssh_client.invoke_shell()

        # Mengirim perintah untuk masuk ke mode konfigurasi
        ssh_channel.send("configure\r")

        # Menunggu respons dari perangkat
        while not ssh_channel.recv_ready():
            pass

        # Membaca respons dari perangkat
        output = ssh_channel.recv(1024).decode()

        # Mengirim perintah untuk membuat bridge
        ssh_channel.send(f"/interface bridge add name={bridge_name}\r")

        # Menunggu respons dari perangkat
        while not ssh_channel.recv_ready():
            pass

        # Membaca respons dari perangkat
        output = ssh_channel.recv(1024).decode()

        # Mengirim perintah untuk menambahkan interface ke bridge
        for interface in interface_list:
            ssh_channel.send(f"/interface bridge port add bridge={bridge_name} interface={interface}\r")

            # Menunggu respons dari perangkat
            while not ssh_channel.recv_ready():
                pass

            # Membaca respons dari perangkat
            output = ssh_channel.recv(1024).decode()

        # Mengirim perintah untuk keluar dari mode konfigurasi
        ssh_channel.send("exit\r")

        # Menutup koneksi SSH
        ssh_client.close()

        print(Fore.GREEN + "Konfigurasi bridge berhasil!" + Style.RESET_ALL)
    except paramiko.AuthenticationException:
        print(Fore.RED + "Gagal melakukan autentikasi. Periksa kembali username dan password." + Style.RESET_ALL)
    except paramiko.SSHException:
        print(Fore.RED + "Gagal melakukan koneksi SSH." + Style.RESET_ALL)
    except paramiko.socket.error as e:
        print(Fore.RED + f"Terjadi kesalahan: {e}" + Style.RESET_ALL)

def print_banner():
    banner = r'''
    
░░███╗░░░░███╗░░
░████║░░░████║░░
██╔██║░░██╔██║░░
╚═╝██║░░╚═╝██║░░
███████╗███████╗
╚══════╝╚══════╝

████████╗██╗░░██╗░░░░░██╗  ░░███╗░░
╚══██╔══╝██║░██╔╝░░░░░██║  ░████║░░
░░░██║░░░█████═╝░░░░░░██║  ██╔██║░░
░░░██║░░░██╔═██╗░██╗░░██║  ╚═╝██║░░
░░░██║░░░██║░╚██╗╚█████╔╝  ███████╗
░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░  ╚══════╝
                                
    '''
    print(Fore.YELLOW + banner + Style.RESET_ALL)

# Memanggil fungsi untuk menampilkan banner
print_banner()

# Memasukkan informasi perangkat dan konfigurasi bridge
hostname = "alamat_ip_mikrotik"
username = "username"
password = "password"
bridge_name = "bridge1"
interface_list = ["ether1", "ether2", "ether3"]

# Memanggil fungsi untuk mengkonfigurasi bridge
configure_bridge(hostname, username, password, bridge_name, interface_list)
      
