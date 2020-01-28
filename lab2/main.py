import argparse
import hashlib
from lab2.util import show_debug_messages
import lab2.signature


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_path', type=argparse.FileType('r'), required=True, help='Encoded file')
    parser.add_argument('-g', '--create', action='store_true', help='Create key and generate dg')
    parser.add_argument('-c', '--check', action='store_true', help='Check dg')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    el_gamal_system = lab2.signature.ElGamalSystem(128, args.file_path.name)
    public_key, private_key = el_gamal_system.generate_keys()
    signature = el_gamal_system.create_signature(private_key)
    if not el_gamal_system.is_invalid_signature(signature, public_key):
        print('DEBUG: Signature is invalid.')
    else:
        print('DEBUG: Signature is valid.')
    # if args.create:
    #     signature = el_gamal_system.create_signature(private_key)
    #     # el_gamal_system.
    #     pass
    # elif args.check:
    #     pass
