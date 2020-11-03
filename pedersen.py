import random
from math import ceil, gcd
from decimal import Decimal
from Crypto.Util import number

global randsize, g, h, p, q
randsize = 10**5


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


# pwer in O(|y|)
def power(x, y):
    if(y == 0):
        return 1
    temp = power(x, int(y / 2))

    if (y % 2 == 0):
        return temp * temp
    else:
        if(y > 0):
            return x * temp * temp
        else:
            return (temp * temp) / x


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
                if(first == -1):
                    first = power(i, temp) % n
                else:
                    val = power(i, temp) % n

                if(val == first):
                    temp -= 1
                    if(temp == order):
                        return i
                    break
                temp += 1


# cal h
def getHval(g, n):
    res = 0
    for i in range(2, n):
        if (gcd(i, n) == 1 and i != g):
            res = i
    return res


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
def generateShares(coeffsS, coeffsT, shareno, k):
    shares = []
    for x in range(1, shareno+1):
        shares.append([calcY(x, coeffsS, k), calcY(x, coeffsT, k)])

    return shares


#  commitment scheme
def commitment(s, t):
    return power(g, s) * power(h, t)


# shared commitments
def sharedCommit(coeffsS, coeffsT, k):
    sharedCommit = []
    for i in range(len(coeffsS)):
        sharedCommit.append(commitment(coeffsS[i], coeffsT[i]) % p)
    return sharedCommit


# verification
def verifySecret(s, t, sharedCommit, i):
    currCommit = commitment(s, t) % p
    combCommit = 1
    for j in range(len(sharedCommit)):
        if j == 0:
            combCommit *= sharedCommit[j]
        else:
            combCommit *= pow(sharedCommit[j], i)
            i *= i
    return currCommit == (combCommit % p)


# reconstruct secret
def reconstructSecret(shares, k):
    gensecret = 0
    prod = Decimal(1)

    for i in range(1, k+1):
        xi, yi = i, shares[i-1][0]
        prod = Decimal(1)
        for j in range(1, k+1):
            xj = j
            if i != j:
                prod *= Decimal(Decimal(xj)/(xj-xi))
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

    # calc p,q
    p, q = getPrimes(16)
    # calc g
    g = getGenerators(q)
    # cal h
    h = getHval(g, q)
    print("p,q,g,h values:")
    print(p, q, g, h)
    print("\n")
    # coefficient of s and t
    coeffsS = coeff(k, secret)
    coeffsT = coeff(k, random.randrange(0, randsize))

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
        print("Verification for " + str(i+1) + "th shareholder: ",
              verifySecret(shares[i][0], shares[i][1], sharedCommits, i+1))
    print("\n")

    # reconstruct secret using k shares
    # kshares = random.sample(shares, k)
    gensecret = reconstructSecret(shares, k)
    print("Generated secret is: ", gensecret)
