import random
from math import ceil
from decimal import Decimal
from Crypto.Util import number

global randsize, p
p = number.getPrime(1024)


# calc random coeficient
def coeff(k, secret):
    coeff = [secret]
    for i in range(k-1):
        coeff.append(random.randrange(0, p-1))
    return coeff


# calc y-coordinate
def calcY(x, coeffs, k):
    y = 0
    for i in range(k):
        y += x**i * coeffs[i]
    return y


# split secret between shareholders
def generateShares(secret, shareno, k):
    shares = []
    coeffs = coeff(k, secret)
    for x in range(1, shareno+1):
        shares.append([x, calcY(x, coeffs, k) % p])
    return shares


# reconstruct secret
def reconstructSecret(shares):
    x0, y0 = shares[0][0], shares[0][1]
    x1, y1 = shares[1][0], shares[1][1]

    numerator = ((x1 * y0) - (x0 * y1)) % p
    denominator = (x1 - x0) % p
    gensecret = numerator // denominator
    return gensecret


if __name__ == "__main__":
    # value of p
    print("Value of p is: " + str(p))
    print("\n")

    secret = random.randrange(1, p-1)
    print("The secret is: " + str(secret))
    print("Number of shareholders: 2")
    shareno = 2
    print("The value of k: 2")
    k = 2

    # generate shares
    shares = generateShares(secret, shareno, k)
    print("Shares are:")
    print(shares)
    print("\n")

    # reconstruct secret using k shares
    kshares = random.sample(shares, k)
    gensecret = reconstructSecret(kshares)
    print("diff: ", str(gensecret-secret))
    print("Generated secret from 2 shares is: ", gensecret)
