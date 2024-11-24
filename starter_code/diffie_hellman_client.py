#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple
import socket
import json

MESSAGE_SIZE = 1024
# TODO feel free to use this helper or not
def send_common_info(sock: socket.socket, server_address: str, server_port: int) -> Tuple[int, int]:
    # TODO: Connect to the server and propose a base number and prime
    # TODO: You can generate these randomly, or just use a fixed set
    # TODO: Return the tuple (base, prime modulus)
    BASE = 19
    PRIME_MODULUS = 797
    sock.connect((server_address, server_port))
    data = {}
    data['base'] = BASE
    data['prime_modulus'] = PRIME_MODULUS
    sock.sendall(json.dumps(data).encode())
    return BASE, PRIME_MODULUS
    pass

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_client(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    # TODO: Create a socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # TODO: Send the proposed base and modulus number to the server using send_common_info
    base, prime_modulus = send_common_info(sock, server_address, server_port)
    # TODO: Come up with a random secret key
    alice_secret_key = random.randint(1, 100)
    # TODO: Calculate the message the client sends using the secret integer.
    alice_pk = (base ** alice_secret_key) % prime_modulus
    alice_message = {}
    alice_message['public_key'] = alice_pk
    # TODO: Exhange messages with the server
    sock.sendall(json.dumps(alice_message).encode())
    bob_info = sock.recv(MESSAGE_SIZE).decode()
    bob_info = json.loads(bob_info)
    # TODO: Calculate the secret using your own secret key and server message
    shared_secret = (bob_info['public_key'] ** alice_secret_key) % prime_modulus
    # TODO: Return the base number, the modulus, the private key, and the shared secret

    return base, prime_modulus, alice_secret_key, shared_secret


def main(args):
    if args.seed:
        random.seed(args.seed)
    
    dh_exchange_client(args.address, args.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the client will connect to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the client will connect to.",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="Random seed to make the exchange deterministic.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
