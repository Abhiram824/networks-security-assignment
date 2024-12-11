#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple
import json

MESSAGE_SIZE = 1024
# TODO feel free to use this helper or not
def receive_common_info() -> Tuple[int, int]:
    # TODO: Wait for a client message that sends a base number.
    # TODO: Return the tuple (base, prime modulus)
    pass

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_server(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    # TODO: Create a server socket. can be UDP or TCP.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((server_address, server_port))
    sock.listen(1)
    conn, addr = sock.accept()

    # TODO: Read client's proposal for base and modulus using receive_common_info
    data = conn.recv(MESSAGE_SIZE).decode()
    data = json.loads(data)
    base = data['base']
    prime_modulus = data['prime_modulus']
    # TODO: Generate your own secret key
    bob_secret_key = random.randint(1, 100)
    bob_pk = (base ** bob_secret_key) % prime_modulus
    # TODO: Exchange messages with the client
    bob_message = {}
    bob_message['public_key'] = bob_pk
    conn.send(json.dumps(bob_message).encode())
    
    alice_info = conn.recv(MESSAGE_SIZE).decode()
    alice_pk = json.loads(alice_info)["public_key"]

    # TODO: Compute the shared secret.
    shared_secret = (alice_pk ** bob_secret_key) % prime_modulus
    # TODO: Return the base number, prime modulus, the secret integer, and the shared secret
    return base, prime_modulus, bob_secret_key, shared_secret

def main(args):
    dh_exchange_server(args.address, args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the server will bind to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the server will listen on.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
