"""Network client/server for transmitting json data.
"""

__author__ = "Robert Jennings rcj@linux.vnet.ibm.com"
__copyright__ = "Copyright (c) 2008 IBM Corporation"
__license__ = "Common Public License v1.0"

import socket
import types
import logging
import json

from powerpcAMS.amsdata import gather_all_data, gather_system_data

CMD_GET_ALL_DATA = 0
CMD_GET_SYS_DATA = 1
CMD_MAX = 1
DATA_METHODS = (gather_all_data, gather_system_data)

# Update CMDVERS each time a new method is added to DATA_METHODS.
# The update should increment the digits to the right of the decimal point.
# The digits to the left of the decimal point should be increased when
# backwards compatibility is broken.
CMDVERS = 1.0000000

def send_json_message(socket, message):
    json_message = json.dumps(message)
    socket.send("%d\n" % len(json_message))
    socket.sendall(json_message)

def receive_json_message(socket):
    len_str = ''
    while True:
        c = socket.recv(1)
        if c == '\n': break
        len_str += c
    mesg_len = int(len_str)
    return json.loads(socket.recv(mesg_len))

def send_data_loop(port):
    """Send json data to any client that connects to a given network port.

    Keyword arguments:
    port -- network port number to use for this server
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('', port))
    except socket.error, msg:
        (errno, errstr) = msg.args
        logging.error("Network error: (%d) " % errno + errstr)
        return 1

    conn = None

    try:
        while (1):
            sock.listen(1)
            (conn, addr) = sock.accept()
            logging.debug("Client connected from " + repr(addr))

            result = "success"
            data = None
            client_data = None
            # Read request from client
            # By accepting a request from the client, including the
            # request data version we can change what the server will
            # send in the future.
            try:
                client_data = receive_json_message(conn)
            except:
                logging.debug("Unable to parse client request.")
                logging.info("Bad client request, ignoring.")
                result = "error"
                data = "bad client request"

            # Currently the server only expects a dictionary from the client
            # with the following values to send AMS data:
            # {"command":0, "version":1.0}
            if (result is not "error" and
                 ("version" not in client_data or
                  client_data["version"] > CMDVERS or
                  int(client_data["version"]) != int(CMDVERS))):
                logging.debug("Unsupported client request version, ignoring.")
                result = "error"
                data = "Unsupported version, server is %f" % CMDVERS

            if (result is not "error" and
                 ("command" not in client_data or
                  client_data["command"] < 0 or
                  client_data["command"] > CMD_MAX)):
                logging.debug("Unsupported request from client, ignoring.")
                result = "error"
                data = "Unsupported request"

            if result is not "error":
                data_method = DATA_METHODS[client_data["command"]]

                # Gather system data and send json objects to the client
                data = data_method()
                if data is None:
                    result = "error"
                    data = "Unspecified data gathering error, check server log."
                logging.debug("Sending %d data objects to client.", len(data))

            response = {"result": result, "data": data}

            send_json_message(conn, response)
            # Clean up
            conn.close()
            conn = None

    # Catch a keyboard interrupt by cleaning up the socket
    except KeyboardInterrupt:
        if conn:
            conn.close()
        sock.close()
        logging.info("Server exiting due to keyboard interrupt.")
        return 0

    # Catch a network error and clean up, return 1 to indicate an error
    except socket.error, msg:
        if conn:
            conn.close()
        sock.close()
        (errno, errstr) = msg.args
        logging.error("Network error: (%d) " % errno + errstr)
        return 1

    # Give the user something slightly helpful for any other error
    except:
        if conn:
            conn.close()
        sock.close()
        logging.error("Unknown error while sending data.")
        raise


# Client
def net_get_data(host="localhost", port=50000, cmd=CMD_GET_ALL_DATA):
    """Get json data from a simple network server.

    Keywork arguments:
    host -- server host name (default localhost)
    port -- server port number (default 50000)

    Returns:
    List of objects received from the server
    """
    data = {}

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.connect((host, port))
    except socket.error, msg:
        (errno, errstr) = msg.args
        logging.error("Network error: (%d) " % errno + errstr)
        return {
            "result": "error",
            "data": "Client: Is the server still running?",
        }

    # By sending a request to the server, including a version for the data
    # request, we can change the data sent by the server in the future.
    if type(cmd) is types.IntType and cmd >= 0 and cmd <= CMD_MAX:
        client_request = {"command": cmd, "version": CMDVERS}
        logging.debug("Sending request for %s (ver:%f)",
                      client_request["command"],
                      client_request["version"])
    else:
        logging.error("BUG: Unknown command request for network client.")
        print type(cmd)
        print repr(cmd)
        return {
            "result": "error",
            "data": "Client: Bad request.",
        }

    send_json_message(sock, client_request)

    # Get server response
    try:
        data = receive_json_message(sock)
    except EOFError:
        pass
    sock.close()

    if type(data) is not types.DictType or "result" not in data:
        data = {
            "result": "error",
            "data": "Unknown server error",
        }

    logging.debug("Data returned to client: " + repr(data))

    return data
