import argparse
import hashlib
from lab3.util import show_debug_messages
from lab3.ecdsa import *


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_path', type=argparse.FileType('r'), required=True, help='Encoded file')
    parser.add_argument('--create', action='store_true', help='Create key and generate dg')
    parser.add_argument('--check', action='store_true', help='Check dg')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    lab3.ecdsa.CURVE = Curve(0, 7, CurvePoint(int("079be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798", 16),
                                   int("0483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8", 16), ),
                  int("0fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141", 16),
                  1, int("0fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f", 16))

    ecdsa = ECDSASystem(128, args.file_path.name)
    public_key, private_key = ecdsa.generate_keys()

    if args.create:
        signature = ecdsa.create_signature(private_key)
        ecdsa.save_sign_to_file(signature, public_key)
    elif args.check:
        signature, public_key = ecdsa.load_sign_from_file()
        if not ecdsa.is_invalid_signature(signature, public_key):
            print('DEBUG: Signature is invalid.')
        else:
            print('DEBUG: Signature is valid.')
