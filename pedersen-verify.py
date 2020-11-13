import random
from math import ceil, gcd
from decimal import Decimal
from Crypto.Util import number

global g, h, p, q


# power in O(|y|)
def power(x, y, z):
    res = 1
    x = x % z
    if (x == 0):
        return 0
    while (y > 0):
        if ((y & 1) == 1):
            res = (res * x) % z
        y = y >> 1
        x = (x * x) % z
    return res


# get 'g' a generator
def getGenerators(n):
    order = 0
    for i in range(n):
        if (gcd(i, n) == 1):
            order += 1
    for i in range(n):
        if (gcd(i, n) == 1):
            temp = 1
            first = -1
            val = -2
            while(1):
                if (first == -1):
                    first = power(i, temp, n)
                else:
                    val = power(i, temp, n)

                if(val == first):
                    temp -= 1
                    if(temp == order):
                        return i
                    break
                temp += 1


# cal h
def getHval(g, n):
    res = g
    while(res == g):
        res = random.randrange(0, q)
    return res


# calc random coeficient
def coeff(k, secret):
    coeff = [secret]
    for i in range(k-1):
        coeff.append(random.getrandbits(128))
    return coeff


# calc y-coordinate
def calcY(x, coeffs, k):
    y = 0
    for i in range(k):
        y += x**i * coeffs[i]
    return y


# split secret between shareholders
def generateShares(coeffsS, coeffsT, shareno, k):
    # only 1 share genrated
    x = random.getrandbits(128)
    return calcY(x, coeffsS, k), calcY(x, coeffsT, k)


#  commitment scheme
def commitment(s, t):
    return power(g, s, q) * power(h, t, q)


# shared commitments
def sharedCommit(coeffsS, coeffsT, k):
    sharedCommit = []
    for i in range(k):
        sharedCommit.append(commitment(coeffsS[i], coeffsT[i]) % q)
    return sharedCommit


# verification
def verifySecret(s, t, sharedCommit, i):
    currCommit = commitment(s, t) % q
    combCommit = (sharedCommit[0] * (power(sharedCommit[1], i, q))) % q
    print(currCommit, combCommit)
    return currCommit == (combCommit)


# reconstruct secret
def reconstructSecret(shares, k):
    x0, y0 = 1, shares[0][0]
    x1, y1 = 2, shares[1][0]

    numerator = ((x1 * y0) - (x0 * y1)) % q
    denominator = (x1 - x0) % q
    gensecret = numerator // denominator
    return gensecret


if __name__ == "__main__":
    # calc p,q
    p= 2875240349 
    q = 136319
    # calc g
    g = getGenerators(q)
    # cal h
    h = getHval(g, q)
    print("p,q,g,h values:")
    print(p, q, g, h)
    print("\n")

    secret = random.getrandbits(128)
    print("The secret is: " + str(secret))
    print("Number of shareholders: 2")
    shareno = 2
    print("The value of k: 2")
    k = 2

    # coefficient of s and t
    coeffsS = coeff(k, secret)
    coeffsT = coeff(k, random.getrandbits(128))

    # generate shares
    s,t = generateShares(coeffsS, coeffsT, shareno, k)
    print("Shares are:")
    print(s,t)
    print("\n")

    # genrate public commitments
    sharedCommits = sharedCommit(coeffsS, coeffsT, k)
    print("public comitments:")
    print(sharedCommits)
    print("\n")

    # verify shares
    print("Verification for shares: ",verifySecret(s, t, sharedCommits, 1))
    print("\n")
