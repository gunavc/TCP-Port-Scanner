import sys
import socket
import tkinter as tk
from tkinter import ttk
from threading import Thread

#*Creating a class to create all the functions and the UI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP Port Scanner")
        self.root.iconbitmap("icon.ico")
        self.root.geometry("500x500")

        #Displays the target ip address
        self.target_label = tk.Label(root, text="Target : ")
        self.target_label.pack(side=tk.TOP,padx=10,pady=10)

        #Input box to Enter the target
        self.target_entry = tk.StringVar()
        self.target_entry = tk.Entry(root, textvariable=self.target_entry)
        self.target_entry.pack(side=tk.TOP, padx=10, pady=10)
        self.target_entry.focus_set()

        #Button to scan for the ports
        self.scan_button = tk.Button(root, text="Scan", command=self.start_scan)
        self.scan_button.pack(side=tk.TOP, padx=10, pady=10)

        #Table to display
        self.result_table = ttk.Treeview(root, columns=("Port", "Status"), show="headings")
        self.result_table.heading("Port", text="Port")
        self.result_table.heading("Status", text="Status")
        self.result_table.pack(side=tk.TOP, padx=10, pady=10)

        #Progress Bar
        self.progress_bar = ttk.Progressbar(root, mode="indeterminate")

    def start_scan(self):
        #Getting the ip of the machine
        print(self.target_entry.get())
        self.target = socket.gethostbyname(self.target_entry.get())
        #self.target = socket.gethostbyname("www.google.com")
        print(self.target)
        #self.target = "10.30.201.186"
        #If invalid ip address
        if not self.target:
            tk.messagebox.showerror("Error obtaining the IP Address")
            return

        self.thread = Thread(target=self.scan_ports, args=(self.target,))
        self.thread.start()
        self.scan_button.config(state=tk.DISABLED)
        self.progress_bar.pack(side=tk.TOP, padx=10, pady=10)
        self.progress_bar.start()

    def scan_ports(self, target):
       #Searches for ports between 1 and 65534
        try: 
            for port in range(78,65535):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                
                result = s.connect_ex((target,port))
                if result ==0:
                    print("Port {} is open".format(port))
                    #Prints the ports in the gui table
                    self.result_table.insert("", tk.END, values=(port, "open"))
                s.close()

        #Handling exceptions
        #for keyboard interrupt   
        except KeyboardInterrupt:
            print("\n Exiting Program !!!!")
            sys.exit()
        #if hostname cannot be resolved
        except socket.gaierror:
                print("\n Hostname Could Not Be Resolved !!!!")
                sys.exit()
        #If there is a error with the socket
        except socket.error:
                print("\ Server not responding !!!!")
                sys.exit()

        self.scan_button.config(state=tk.NORMAL)
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

#Calling the class
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()