def fizz_buzz(n, m):
    if not(1 <= n < m <= 10000):
        raise ValueError('Input numbers do not satisfy the condition 1 <= n < m <= 10000.')

    for i in range(n, m+1):
        if i % 3 == 0 and i % 5 == 0:
            print('FizzBuzz')
        elif i % 3 == 0:
            print('Fizz')
        elif i % 5 == 0:
            print('Buzz')
        else:
            print(i)

n = int(input())
m = int(input())

fizz_buzz(n,m)