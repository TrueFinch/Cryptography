import argparse
from lab1 import randprime_functions, rsa
import time
from lab1.util import show_debug_messages


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-td', '--td', action='store_true', help='The Trivial division primality test function')
    parser.add_argument('-ss', '--ss', action='store_true', help='The Solovay–Strassen primality test function')
    parser.add_argument('-mr', '--mr', action='store_true', help='The Miller–Rabin primality test function')
    parser.add_argument('-lib', '--lib', action='store_true', help='Use library sumpy to generate prime number')
    parser.add_argument('-f', '--file_path', type=argparse.FileType('r'), required=True,
                        help='Path to file with text to encode')
    parser.add_argument('-k', '--key_length', type=int, default=1024,
                        help='The encryption key max length. Please use degrees of number two. Minimum usefull is 64.')
    parser.add_argument('-c', '--chunk_size', type=int, default=128, help='The size of the chunk of the text.')
    parser.add_argument('-b', '--bigbyteorder', action='store_true', help='Big endian byteorder while encoding data.')
    parser.add_argument('-l', '--littlebyteorder', action='store_true',
                        help='Little endian byteorder while encoding data.')

    return parser.parse_args()


def get_randprime_function(a_args):
    if a_args.td:
        return ['td', randprime_functions.td_randprime]
    if a_args.ss:
        return ['ss', randprime_functions.ss_randprime]
    if a_args.mr:
        return ['mr', randprime_functions.mr_randprime]
    return ['lib', randprime_functions.lib_randprime]


def encode(a_args, coder, randprime_function):
    if show_debug_messages:
        print('DEBUG: Start of encoding data.')
    with open(a_args.file_path.name, 'rb') as file_in, \
            open("{}_encoded_{}".format(randprime_function, a_args.file_path.name), 'w') as file_en:
        for chunk in iter(lambda: file_in.read(a_args.chunk_size), b''):
            encoded_chunk = coder.encode_bytes(chunk)
            file_en.write(str(encoded_chunk) + '\n')
        file_in.close()
        file_en.close()
    if show_debug_messages:
        print('DEBUG: Finish of encoding data.')
    return


def decode(a_args, coder, randprime_function):
    if show_debug_messages:
        print('DEBUG: Start of decoding data.')
    with open("{}_encoded_{}".format(randprime_function, a_args.file_path.name), 'r') as file_en, \
            open("{}_decoded_{}".format(randprime_function, a_args.file_path.name), 'wb') as file_de:
        lines = file_en.readlines()
        common = len(lines)
        checkpoints = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.1]
        checkpoint = 0
        for i, chunk in enumerate(lines):
            decoded_chunk = coder.decode_bytes(int(chunk))
            file_de.write(decoded_chunk)
            if i / common > checkpoints[checkpoint] and show_debug_messages:
                print('DEBUG: {:05.2f}% decoding complete.'.format(i / common * 100))
                checkpoint += 1
        file_en.close()
        file_de.close()
    if show_debug_messages:
        print('DEBUG: Finish of decoding data.')
    return


def get_byteorder(a_args):
    if a_args.bigbyteorder and a_args.littlebyteorder:
        return 'error'
    if a_args.littlebyteorder:
        return 'little'
    return 'big'


if __name__ == '__main__':
    args = parse_args()

    randprime_function_name, randprime_generation_function = get_randprime_function(args)

    if show_debug_messages:
        print("DEBUG: Using {} test function.".format(randprime_function_name))
        print("DEBUG: Using key with max length {}.".format(args.key_length))
        print("DEBUG: File {} is going to encode.".format(args.file_path.name))

    byteorder = get_byteorder(args)
    if byteorder == 'error':
        print('Arguments error! Use only -b or only -l! Not both!')
        exit(0)

    start_time = time.time()
    rsa_coder = rsa.Rsa(randprime_generation_function, args.key_length, args.chunk_size, byteorder)
    finish_time = time.time()
    rsa_time = finish_time - start_time
    if show_debug_messages:
        print("DEBUG: RSA key generated in {} seconds".format(rsa_time))

    start_time = time.time()
    encode(args, rsa_coder, randprime_function_name)
    finish_time = time.time()
    encode_time = finish_time - start_time
    if show_debug_messages:
        print("DEBUG: File encoded in {} seconds".format(encode_time))

    start_time = time.time()
    decode(args, rsa_coder, randprime_function_name)
    finish_time = time.time()
    decode_time = finish_time - start_time
    if show_debug_messages:
        print("DEBUG: File decoded in {} seconds".format(decode_time))

    info_string = """Max key length: {}\nChunk size: {}\nByte order: {}\nKey generated in {} seconds\nEncode in {} seconds\nDecode in {} seconds\nPublic key: {}\nPrivate key: {}\nModule is {}""".format(
        rsa_coder.max_key_length, args.chunk_size,
        byteorder, rsa_time, encode_time,
        decode_time, rsa_coder.e, rsa_coder.d,
        rsa_coder.n)

    if show_debug_messages:
        print("DEBUG: {}".format(info_string))
    with open("{}_info_{}".format(randprime_function_name, args.file_path.name), 'w') as file_info:
        file_info.write(info_string)
    file_info.close()
