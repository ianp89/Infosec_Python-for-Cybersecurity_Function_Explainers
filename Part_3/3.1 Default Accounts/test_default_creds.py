# These functions test systems for SSH and Tenet connections using default administrative accounts that come with many devices.
# Change these when you buy them!

import paramiko
import telnetlib
# paramiko and telnetlib are Python's libraries for SSH and Telnet interaction, respectively.
    
def SSHLogin(host,port,username,password):
    try: 
        ssh = paramiko.SSHClient()
        # SSHClient sets up the client side of the proposed SSH connection.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # The line above ignores the fact the user does not have a server key as would be the case with a pre-approved SSH connection.
        ssh.connect(host,port=port,username=username,password=password);
        # The connection values necessary to establish the connection will be passed in the function call.
        ssh_session = ssh.get_transport().open_session()
        # The line above actually passes the values sent to the function call and establishes a connection if valid.
        if ssh_session.active:
            print("Login successful on %s:%s with username %s and password %s" % (host,port,username,password))
            # Because the function could be called with a list of tuples, for instance, this readout will tell the user which sets succeeded.
    except:
            print("Login failed %s %s" % (username,password))
    ssh.close()
    # This closes the connection after test of connection viability (Don't leave open connections! They're discoverable!)
    
def TelnetLogin(host,port,username,password):
    user = bytes(username + "\n", "utf-8")
    password = bytes(password + "\n", "utf-8")
    # telnetlib requires input as byte-strings, whereas Python strings use multibyte strings (thanks stackoverflow). 
    # The bytes() function takes care of that with the encoding scheme specified.
    
    tn = telnetlib.Telnet(host, port)
    # This sets up the Telnet connection on host/port specified at function call.
    tn.read_until(bytes("login: ", "utf-8"))
    # telnetlib's "readuntil" function reads info on the wire until it comes across specified information.
    # Here, the function is looking for a logon prompt. The prompt may not match the script; in that case the script will fail. 
    # Same applies to "Password" below.
    tn.write(user)
    tn.read_until(bytes("Password: ", "utf-8"))
    tn.write(password + "\n")
    try: 
        result = tn.expect([bytes("Last login", "utf-8"]), timeout=2)
        # telnetlib's "expect" function is similar to read_until() but allows a list to be passed.
        # Many Telnet connections will verify a connection with a "Last login" time. 
        # If the function doesn't read one such time, it will continue after the specified timeout period.
        if (result[0] > 0):
        # expect() returns a tuple with results in the first position.
            print("Telnet login successful on %s:%s with username %s and password %s" % (host,port,username,password))
        tn.close()
        # Close your connections or risk being discovered!
    except EOFError:
        print("Login failed %s %s" % (username,password))

host = "127.0.0.1"
# The test case here is with one's local host/PC
with open("defaults.txt","r") as f:
# Python's text reading capabilities are used to open a file in this directory with common account/device defaults.
# Common defaults are available online with a simple Google search if using this script in a real-life scenario.
    for line in f:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        # This loop iterates through the user/password combos and splits each line into space-separated values for further manipulation.
        SSHLogin(host,port,username,password)
        TelnetLogin(host,port,username,password)
        # Both functions are called using the values from the document as just described.
