import random
from math import ceil, gcd
from decimal import Decimal
from Crypto.Util import number

global g, h, p, q


# check if no. is prime
def isPrime(n):
    if (n <= 1):
        return False
    if (n <= 3):
        return True
    if (n % 2 == 0 or n % 3 == 0):
        return False
    i = 5
    while(i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i = i + 6

    return True


# prime nos generator
def getPrimes(n):
    k = number.getPrime(n)  # n-bit random prime no
    s = k-1
    while((k-1) % s != 0 or not isPrime(s)):
        s -= 1
    return k, s


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
    for i in range(n-1, 1, -1):
        if (gcd(i, n) == 1):
            return i
    # order = 0
    # for i in range(n):
    #     if (gcd(i, n) == 1):
    #         order += 1
    # for i in range(n):
    #     if (gcd(i, n) == 1):
    #         temp = 1
    #         first = -1
    #         val = -2
    #         while(1):
    #             if (first == -1):
    #                 first = power(i, temp, n)
    #             else:
    #                 val = power(i, temp, n)

    #             if(val == first):
    #                 temp -= 1
    #                 if(temp == order):
    #                     return i
    #                 break
    #             temp += 1


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
        coeff.append(random.randrange(0, q))
    return coeff


# calc y-coordinate
def calcY(x, coeffs, k):
    y = 0
    for i in range(k):
        y += x**i * coeffs[i]
    return y


# split secret between shareholders
def generateShares(coeffsS, coeffsT, shareno, k):
    shares = []
    for x in range(1, shareno+1):
        shares.append([calcY(x, coeffsS, k), calcY(x, coeffsT, k)])

    return shares


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
    # combCommit = 1
    # for j in range(1, len(sharedCommit)):
    #     if j == 0:
    #         combCommit *= sharedCommit[j]
    #     else:
    #         combCommit = combCommit * power(sharedCommit[j], power(i, j))
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
    # p, q = getPrimes(16)
    p = -1
    q = number.getPrime(1024)
    # calc g
    g = getGenerators(q)
    # cal h
    h = getHval(g, q)
    print("p,q,g,h values:")
    print(p, q, g, h)
    print("\n")

    secret = random.randrange(1, q)
    print("The secret is: " + str(secret))
    print("Number of shareholders: 2")
    shareno = 2
    print("The value of k: 2")
    k = 2

    # coefficient of s and t
    coeffsS = coeff(k, secret)
    coeffsT = coeff(k, random.randrange(0, q))

    # generate shares
    shares = generateShares(coeffsS, coeffsT, shareno, k)
    print("Shares are:")
    for share in shares:
        print(share)
    print("\n")

    # genrate public commitments
    sharedCommits = sharedCommit(coeffsS, coeffsT, k)
    print("public comitments:")
    print(sharedCommits)
    print("\n")

    # verify shares
    for i in range(shareno):
        print("Verification for shareholder no. " + str(i+1) + ": ",
              verifySecret(shares[i][0], shares[i][1], sharedCommits, i+1))
    print("\n")

    # reconstruct secret using k shares
    # kshares = random.sample(shares, k)
    gensecret = reconstructSecret(shares, k)
    print("Generated secret from 2 shares is: ", gensecret)
