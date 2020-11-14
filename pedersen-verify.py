import random
import time
from math import ceil, gcd
from decimal import Decimal

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
def generateShares(coeffsS, coeffsT, k, x):
    # only 1 share genrated
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
    # print(currCommit, combCommit)
    return currCommit == (combCommit)


if __name__ == "__main__":
    # calc p,q
    # p = 2875240349
    q = 160083459653027294572947538361142474693461858573551936926737179537830262185487287460372060800072797326040636201799277740168218919629285080416550852599849507880591377952261893937217490455277823851473372222317985032827403671415987326023409645117312652552473362242135660471225018078630032279914142026248951857619
    # calc g
    g = 160083459653027294572947538361142474693461858573551936926737179537830262185487287460372060800072797326040636201799277740168218919629285080416550852599849507880591377952261893937217490455277823851473372222317985032827403671415987326023409645117312652552473362242135660471225018078630032279914142026248951857618
    # cal h
    h = 4622164940323503878229125126763790441392467089381226534935353758227759798512707452963303817720328816545610697278405374421700833749651545466085820017114632564777590112132367806793222358332078082265829895090981485054499626286890474905993040926284567236051366034621783191089838512453483923770949371557572226013

    codeStart = time.time()
    secret = random.getrandbits(128)
    print("The secret is: " + str(secret))
    # print("Number of shareholders: 2")
    # shareno = 2
    print("The value of k: 2")
    k = 2

    # coefficient of s and t
    coeffsS = coeff(k, secret)
    coeffsT = coeff(k, random.getrandbits(128))

    # generate shares
    x = random.getrandbits(128)
    s, t = generateShares(coeffsS, coeffsT, k, x)
    print("Shares are:")
    print(s, t)
    print("\n")

    # genrate public commitments
    sharedCommits = sharedCommit(coeffsS, coeffsT, k)
    print("public comitments:")
    print(sharedCommits)
    print("\n")

    # verify shares
    print("Verification for shares: ", verifySecret(s, t, sharedCommits, x))
    print("\n")
    codeEnd = time.time()

    print("Execution time of code is: " + str(codeEnd - codeStart))
