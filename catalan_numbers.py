import json
import os

def load_catalan_numbers_until(n):
    #load already computed Catalan numbers
    if (os.path.exists('catalan_numbers.txt')):
        with open('catalan_numbers.txt') as json_file:
            c = json.load(json_file)
    else:
        c = [1]

    if len(c) >= n+1:
        return c
    else:
        for i in range(len(c), n+1):
            c.insert(i, __compute_catalan_number(i, c))

    with open('catalan_numbers.txt', 'w') as outfile:
        json.dump(c, outfile)

    return c

def __compute_catalan_number(n, c):
    if len(c) >= n+1:
        return c[n]
    else:
        s = 0
        for i in range(0,n):
            s += __compute_catalan_number(i, c) * __compute_catalan_number(n-1-i, c)
        return s

def catalan_number(n):
    c = load_catalan_numbers_until(n)
    if len(c) >= n+1:
        return c[n]
    else:
        return null

if __name__ == "__main__":
    n = int(input("Compute Catalan numbers until:"))
    c = load_catalan_numbers_until(n)
    print(c[n])