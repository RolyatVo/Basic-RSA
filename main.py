"""
Author: Taylor Vo
Langauge: Python 3
Date: April 5, 2022
Class: CS427
Project2: RSA

"""
import random


def get_args():
    arg = input().split(" ")
    arg.pop(0)
    arg_map = {}
    if arg[0] == "sign":
        arg_map['mode'] = arg[0]
        arg_map['message'] = arg[1].strip("\"")

    elif arg[0] == "verify":
        arg_map['mode'] = arg[0]
        arg_map['mod'] = arg[1]
        arg_map['message'] = arg[2].strip("\"")
        arg_map['signature'] = arg[3]
    else:
        print("ERROR unknown command")
        exit(1)

    return arg_map


def mod_exp(x, e, m):
    g = 1
    while e > 0:
        # if exp is even divide by 2 since x^64 = x^32 mod n
        if e % 2 == 0:
            x = (x * x) % m
            e = e // 2
        else:
            # if exp is odd
            g = (x * g) % m
            e -= 1
    return g


def is_prime(n, k=100):
    i = 0
    while i < k:
        if rabin_miller_test(n) == False:
            return False
        i += 1
    return True


"""
    Taken from Wikipedia's website and slides from class: 
    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
"""
def rabin_miller_test(n):
    if n % 2 == 0 or n <= 1:
        return False
    d = n - 1
    while d % 2 == 0:
        d = d // 2
    a = random.randint(3, n - 2)

    x = mod_exp(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = mod_exp(a, d, n)
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def random_prime():
    r = random.randint(0x8000, 0xFFFF)
    while not is_prime(r):
        r = random.randint(0x8000, 0xFFFF)
    return r


"""
    Taken from Wikipedia's website
    inverse
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
"""
def inverse(a, m):
    t, newt = 0, 1
    r, newr = m, a

    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr

    if r > 1:
        print("NOT POSSIBLE")

    if t < 0:
        t = t + m
    return t


"""
    Taken from wikipedia's website: 
    https://en.wikipedia.org/wiki/PJW_hash_function
"""
def elf_hash(s: str):
    h, high = 0, 0
    for i in range(len(s)):
        h = (h << 4) + ord(s[i])
        high = h & 0xF0000000
        if high != 0:
            h ^= high >> 24
        h &= ~high
    return h


def main(debug=False):
    args = get_args()
    if args.get('mode') == "sign":
        p, q = random_prime(), random_prime()
        # p, q = int(0x9da5), int(0xb28b)
        n = p * q
        t = (p - 1) * (q - 1)
        e = 65537

        if debug:
            print(f"p: {hex(p)[2:]}, q: {hex(q)[2:]}, n: {hex(n)[2:]} blen: {n.bit_length()}, t: {hex(t)[2:]}")
        d = inverse(e, t)
        if debug:
            print(f"Recieved messge: {args.get('message')}")

        h = elf_hash(args.get('message'))
        if debug:
            print(f"Hashed message: {hex(h)[2:]}")
            print(f"Signing with private key: {hex(d)[2:]}")
            signed = mod_exp(h, d, n)
            print(f"Signed hash: {hex(signed)[2:]}")
            uninvert = (mod_exp(signed, e, n))
            print(f"uninverted message: {hex(uninvert)[2:]}")
            print(f"complete output for verification:\n{hex(n)[2:]} \"{args.get('message')}\" {hex(signed)[2:]}")
    else:
        print(args)
        h = elf_hash(args.get('message'))
        if h == mod_exp(int(args.get('signature'), 16),  65537, int(args.get('mod'), 16)):
            print("message verified!!")
        else:
            print("!!! message is forged !!!")

    return


if __name__ == '__main__':
    main(debug=True)
