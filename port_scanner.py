import socket
from common_ports import *
from tabulate import tabulate
tabulate.PRESERVE_WHITESPACE = True
def get_open_ports(target, port_range, verbose = False):
    
    if target.upper() == target.lower():
        try:
            socket.inet_aton(target)
            # legal
        except:
            # Not legal
            return "Error: Invalid IP address"

    open_ports = []
    for port in range(port_range[0],port_range[1]+1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        ip = ""
        name = ""
        x = ""
        if(target.upper() == target.lower()):
            ip = target
            try:
                name = socket.getfqdn(ip)
                if name == ip:
                    x = f"Open ports for {ip}"
                else:
                    x = f"Open ports for {name} ({ip})"# \nPORT     SERVICE"
                
            except:
                return "Error: Invalid IP address"

        else:
            try:
                ip = socket.gethostbyname(target)
                x = f"Open ports for {target} ({ip})"#\nPORT     SERVICE"
            except:
                return "Error: Invalid hostname"
            name = target

        if(s.connect_ex((ip,port))):
            s.close()
            continue  
        else:
            s.close()
            open_ports.append(port)            


        s.close()
    if(verbose == False):
        return (open_ports)
    else:
        table = []
        for p in open_ports:
            a = []
            a.append(str(p)+" ")
            a.append(ports_and_services[p])
            table.append(a)
            #f"\n{p}       {ports_and_services[p]}" 
        bot = tabulate(table,["PORT ","SERVICE"],tablefmt="plain",colalign=("left",))
        x = x + "\n" + bot
        return x
