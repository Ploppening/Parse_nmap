# Nmap output parser

Parse nmap .xml output as shown.

## Usage

`python3 parse_nmap.py -T4 -Pn --open -A -p- 10.10.253.13`

`python3 parse_nmap.py nmap_results/10.10.180.23_2025-03-20_15.04.xml `


![image](https://github.com/user-attachments/assets/80925eff-1148-4768-a486-198b7e102148)


`❯ parse_nmap nmap_results/10.10.181.92_2025-03-24_10.40.xml 

[+] Results for 10.10.181.92_2025-03-24_10.40 running Linux 4.15

      PORT | STATE | SERVICE     | VERSION

Port    21 |  OPEN | ftp         | vsftpd 2.0.8 or later
  └── ftp-anon: Anonymous FTP login allowed (FTP code 230)
drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts [NSE: writeable]
  └── ftp-syst: 
  STAT: 
FTP server status:
     Connected to ::ffff:10.13.61.96
     Logged in as ftp
     TYPE: ASCII
     No session bandwidth limit
     Session timeout in seconds is 300
     Control connection is plain text
     Data connections will be plain text
     At session startup, client count was 5
     vsFTPd 3.0.3 - secure, fast, stable
End of status

Port    22 |  OPEN | ssh         | OpenSSH 7.6p1 Ubuntu 4ubuntu0.3
  └── ssh-hostkey: 
  2048 8b:ca:21:62:1c:2b:23:fa:6b:c6:1f:a8:13:fe:1c:68 (RSA)
  256 95:89:a4:12:e2:e6:ab:90:5d:45:19:ff:41:5f:74:ce (ECDSA)
  256 e1:2a:96:a4:ea:8f:68:8f:cc:74:b8:f0:28:72:70:cd (ED25519)

Port   139 |  OPEN | netbios-ssn | Samba smbd 3.X - 4.X

Port   445 |  OPEN | netbios-ssn | Samba smbd 4.7.6-Ubuntu

[+] Host script results

  └── smb-os-discovery: 
  OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
  Computer name: anonymous
  NetBIOS computer name: ANONYMOUS\x00
  Domain name: \x00
  FQDN: anonymous
  System time: 2025-03-23T21:42:24+00:00


  └── smb2-security-mode: 
  3:1:1: 
    Message signing enabled but not required

  └── smb2-time: 
  date: 2025-03-23T21:42:24
  start_date: N/A

  └── smb-security-mode: 
  account_used: guest
  authentication_level: user
  challenge_response: supported
  message_signing: disabled (dangerous, but default)

  └── nbstat: NetBIOS name: ANONYMOUS, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

[+] Original Nmap Output: nmap_results/10.10.181.92_2025-03-24_10.40.nmap`

