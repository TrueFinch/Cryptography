import argparse
import hashlib
from lab2.util import show_debug_messages

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_path', type=argparse.FileType('r'), required=True, help='Encoded file')
    parser.add_argument('-g', '--create', action='store_true', help='Create key and generate dg')
    parser.add_argument('-c', '--check', action='store_true', help='Check dg')

    return parser.parse_args()


def get_file_hash(path):
    if show_debug_messages:
        print('DEBUG: Start hashing file.')
    file_hash = hashlib.sha256()
    with open(path, 'r') as file_in:
        file_hash.update(file_in.read().encode('utf-8'))
    result = int(file_hash.hexdigest(), 16)
    if show_debug_messages:
        print('DEBUG: Finish hashing file.')
    return result


if __name__ == '__main__':
    args = parse_args()
    chunk_size = 128
    hash_value = get_file_hash(args.file_path.name)
