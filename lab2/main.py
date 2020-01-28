import argparse
import hashlib
from lab2.util import show_debug_messages
import lab2.signature


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_path', type=argparse.FileType('r'), required=True, help='Encoded file')
    parser.add_argument('--create', action='store_true', help='Create key and generate dg')
    parser.add_argument('--check', action='store_true', help='Check dg')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    el_gamal_system = lab2.signature.ElGamalSystem(128, args.file_path.name)
    public_key, private_key = el_gamal_system.generate_keys()

    if args.create:
        signature = el_gamal_system.create_signature(private_key)
        el_gamal_system.save_sign_to_file(signature, public_key)
    elif args.check:
        signature, public_key = el_gamal_system.load_sign_from_file()
        if not el_gamal_system.is_invalid_signature(signature, public_key):
            print('DEBUG: Signature is invalid.')
        else:
            print('DEBUG: Signature is valid.')
