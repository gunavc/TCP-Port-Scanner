import sys
import socket
import tkinter as tk
#from datetime import datetime

#Getting the ip 
target = socket.gethostbyname(socket.gethostname())
try:
    root = tk.Tk()
    root.title("Number of Open Ports")
    root.geometry("500x500")

    display_label = tk.Text(root)
    display_label.pack()

    #Searches for ports between 1 and 65534
    for port in range(1,65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
         
        result = s.connect_ex((target,port))
        if result ==0:
            print("Port {} is open".format(port))
            #Prints the ports in the gui window
            display_label.insert(tk.END,f"Port {port} is open\n")
        # else:
        #     print("Port {} is closed".format(port))
        s.close()

    root.mainloop()
    
#Handling exceptions
# for keyboard interrupt   
except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
#if hostname cannot be resolved
except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
# If there is a error with the socket
except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()
