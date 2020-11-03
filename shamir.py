import random
from math import ceil
from decimal import Decimal

global randsize
randsize = 10**5
_PRIME = 2 ** 127 - 1


# calc random coeficient
def coeff(k, secret):
    coeff = [secret]
    for i in range(k-1):
        coeff.append(random.randrange(0, randsize))
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
        shares.append([x, calcY(x, coeffs, k) % _PRIME])
    return shares


# reconstruct secret
def reconstructSecret(shares):
    gensecret = 0
    prod = Decimal(1)

    for i in range(len(shares)):
        xi, yi = shares[i][0], shares[i][1]
        prod = Decimal(1)
        for j in range(len(shares)):
            xj = shares[j][0]
            if i != j:
                prod *= Decimal(Decimal(xj)/(xj-xi)) % _PRIME
        prod *= yi
        gensecret += prod
    return int(round(Decimal(gensecret), 0))


if __name__ == "__main__":
    print("Enter the secret:")
    secret = int(input())
    print("Enter number of shareholders:")
    shareno = int(input())
    print("Enter the value of k:")
    k = int(input())

    # generate shares
    shares = generateShares(secret, shareno, k)
    print("Shares are:")
    print(shares)
    print("\n")

    # reconstruct secret using k shares
    kshares = random.sample(shares, k)
    gensecret = reconstructSecret(kshares)
    print("Generated secret is: ", gensecret)
