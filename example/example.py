with open('example.txt', 'r') as f:
    lines: list = f.readlines()
    print(lines[-1])