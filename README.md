# Nmap output parser

Parse nmap .xml output as shown. Can take either `nmap` command or .xml file as input.

## Usage

`python3 parse_nmap.py -T4 -Pn --open -A -p- 10.10.253.13`

`python3 parse_nmap.py nmap_results/10.10.180.23_2025-03-20_15.04.xml `

Command must end with the IP address. I am too lazy to fix this yet. Probably won't either tbh. 

---

![image](https://github.com/user-attachments/assets/80925eff-1148-4768-a486-198b7e102148)

