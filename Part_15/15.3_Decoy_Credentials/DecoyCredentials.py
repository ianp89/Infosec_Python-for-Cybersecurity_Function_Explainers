# This script creates a dummy SSH server to capture suspicious login attempts, and logs them out to avoid noticing they were detected.

import asyncio, asyncssh, crypt, sys, time, random
# Python's asyncio and asyncssh are utilized here to implement as SSH server super efficiently.

def handle_client(process):
    process.exit(0)

class MySSHServer(asyncssh.SSHServer):
# This class of SSH server would allow authentication with no other actions possible, and terminates in a hopefully unsuspicious way.
    
    def connection_made(self, conn):
        self._conn = conn
        # The connection is stored locally.

    def password_auth_supported(self):
        return True
        # Allows username, password collection to catch decoy account attempts, and password attacks in process.

    def validate_password(self, username, password):
        print('Login attempt from %s with username %s and password %s' %
                (self._conn.get_extra_info('peername')[0],username,password))
                # Captures IP address, user, password, of attempted login.
        time.sleep(random.randint(0,5))
        raise asyncssh.DisconnectError(10,"Connection lost") 
        # Sleeps for a random interval until disconnecting the user so the attacker thinks there is just a problem rather than a decoy.

async def start_server():
    await asyncssh.create_server(MySSHServer, '', 8022,
                                 server_host_keys=['ssh_host_key'],
                                 process_factory=handle_client)
    # Starts a server instance (MySSHServer defined above, listening on all interfaces at port 8022, with specified key and request handler).

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))
loop.run_forever()
# This block of code starts the SSH server and runs it assuming no errors arise.
