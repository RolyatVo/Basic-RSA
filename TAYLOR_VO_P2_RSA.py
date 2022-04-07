"""
Author: Taylor Vo
Langauge: Python 3
Date: April 5, 2022
Class: CS427
Project2: RSA

"""
import random


def get_args():
    """
    get standard input and return a dictionary containing values:
    sign: (mode, message)
    verify: (mode, mod, message, signature)
    :return: dictionary given a stdin
    """
    arg = input().split(" ")
    arg_map = {}
    if arg[0] == "sign":
        arg_map['mode'] = arg[0]
        arg_map['message'] = arg[1].strip("\"")

    elif arg[0] == "verify":
        arg_map['mode'] = arg[0]
        arg_map['mod'] = int(arg[1], 16)
        arg_map['message'] = arg[2].strip("\"")
        arg_map['signature'] = int(arg[3], 16)
    else:
        print("ERROR unknown command")
        exit(1)

    return arg_map


def mod_exp(x, e, m):
    """
    This function uses fast modular exponentiation
    :param x: base
    :param e: exponent
    :param m: modular
    :return:
    """
    g = 1
    while e > 0:
        # if exp is even divide by 2 since x^64 = (x^32)^2 mod n
        if e % 2 == 0:
            x = (x * x) % m
            e = e // 2
        else:
            # if exp is odd, this is same as x^65 = x*((x^32)^2) mod n
            g = (x * g) % m
            e -= 1
    return g


def is_prime(n, k=100):
    # run rabin_miller multiple times so we are sure we didn't get a funny prime
    i = 0
    while i < k:
        if rabin_miller_test(n) == False:
            return False
        i += 1
    return True


def rabin_miller_test(n):
    """
        Taken from Wikipedia's website and slides from class:
        https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    """
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


def inverse(a, m):
    """
        Taken from Wikipedia's website
        inverse
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """
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


def elf_hash(s: str):
    """
        Taken from Wikipedia's website:
        https://en.wikipedia.org/wiki/PJW_hash_function
    """
    h, high = 0, 0
    for i in range(len(s)):
        h = (h << 4) + ord(s[i])
        high = h & 0xF0000000
        if high != 0:
            h ^= high >> 24
        h &= (~high & 0xFFFFFFFF)
    return h


def main(debug=False):
    args = get_args()
    if args.get('mode') == "sign":
        p, q = random_prime(), random_prime()
        n = p * q
        # we know the totient of p or q since they are primes, from slides in class.
        t = (p - 1) * (q - 1)

        # e is a set value
        e = 65537

        n_str = hex(n)[2:]
        if debug:
            print(f"p: {hex(p)[2:]}, q: {hex(q)[2:]}, n: {n_str}, t: {hex(t)[2:]}")
            print(f"Recieved messge: {args.get('message')}")

        d = inverse(e, t)
        h = elf_hash(args.get('message'))
        if debug:
            print(f"Hashed message: {hex(h)[2:]}")
            print(f"Signing with private key: {hex(d)[2:]}")

            signed = mod_exp(h, d, n)
            signed_str = hex(signed)[2:]
            print(f"Signed hash: {signed_str}")

            uninvert = (mod_exp(signed, e, n))
            print(f"uninverted message: {hex(uninvert)[2:]}")

            print(f"complete output for verification:\n{n_str} \"{args.get('message')}\" {signed_str}")
    else:
        h = elf_hash(args.get('message'))
        if h == mod_exp(args.get('signature'), 65537, args.get('mod')):
            print("message verified!!")
        else:
            print("!!! message is forged !!!")

    return


if __name__ == '__main__':
    main(debug=True)
