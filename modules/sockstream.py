'''
This file is part of Hyphan.
Hyphan is free software: you can redistribute it and/or modify
it under the terms of the GNU Afferno General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Hyphan is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Afferno General Public License for more details.

You should have received a copy of the GNU Afferno General Public
License along with Hyphan.  If not, see
https://www.gnu.org/licenses/agpl-3.0.html>.
----
Mod for HyphanBot monitoring services with sockets.
'''

import _thread as thread
import select
import socket
import logging

helptext = """
SockStream allows you to connect to Hyphan via a socket to monitor messages it may receive, and send administerative commands to control Hyphan.
"""

class SockStream(object):
    """docstring for SockStream"""
    def __init__(self, port, bot, welcome_msg="Connected to SockStream!"):
        self.sock = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = port
        self.bot = bot
        #self.latest_update = bot.getUpdates()[-1:]
        self.update_ready = False
        self.welcome_msg = welcome_msg
        self.logger = logging.getLogger(__name__)

    def listen(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.logger.info("SockStream listening on "+self.host+":"+str(self.port))
        while True:
            conn, addr = self.sock.accept()
            thread.start_new_thread(self.connection, (conn,))
        self.sock.close()

    def get_latest_update(self, bot, update):
        self.logger.info("Sock got update!")
        self.latest_update = update
        self.update_ready = True

    def stream_updates(self, conn):
        while True:
            try:
                read_ready, write_ready, in_error = \
                    select.select([conn], [conn], [], 5)

                if write_ready:
                    # Send message log to monitor/logging service
                    if self.update_ready:
                        self.update_ready = False
                        conn.send(("[%s] %s (@%s): %s" % (str(self.latest_update.message.chat_id),
                                                    self.latest_update.message.from_user.first_name,
                                                    self.latest_update.message.from_user.username,
                                                    self.latest_update.message.text)).encode("utf-8")+b'\n')
            except:
                break

    def connection(self, conn):
        self.logger.info("Connection from "+self.host+":"+str(self.port))
        conn.send(self.welcome_msg.encode("utf-8")+b'\n')
        thread.start_new_thread(self.stream_updates, (conn,))
        while True:
            try:
                read_ready, write_ready, in_error = \
                    select.select([conn], [conn], [], 5)

                if read_ready:
                    data = conn.recv(1024).decode("utf-8").strip()
                    #self.logger.info("SockStream recieved: "+data)
                    self.parseData(data, conn)
                    if data == "help":
                        conn.send(helptext.encode("utf-8"))
                        self.logger.info("Sock sent help.")
                    elif data == "quit":
                        conn.send(b'Quitting...\n')
                        self.logger.info("Sock sent quit message.")
                        break
                    else:
                        conn.send(data.encode("utf-8")+b'\n')
            except:
                break
        conn.close()
        self.logger.info("Disconnection at "+self.host+":"+str(self.port))

    def parseData(self, data, conn):
        if data is "help":
            conn.send(helptext.encode("utf-8"))
        elif data is "quit":
            conn.send(b'Not yet implemented\n')


class Dispatch(object):
    """docstring for Dispatch"""
    def __init__(self, api, updater):
        self.api = api
        self.updater = updater
        self.start_server()

    def start_server(self):
        # Need to start the server as a new thread to keep Hyphan running...
        thread.start_new_thread(self.start_sockstream, ())
        self.api.set_help("sockstream", helptext)

    def start_sockstream(self):
        port = self.api.get_config("port", 9000)
        welcome_msg = self.api.get_config("welcomemsg", "Welcome to HyphanBot!")
        sockstream = SockStream(int(port), self.updater.bot, welcome_msg)
        self.updater.dispatcher.addTelegramMessageHandler(sockstream.get_latest_update)
        sockstream.listen()
