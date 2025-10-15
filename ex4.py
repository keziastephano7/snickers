#Lamport's Logical Clock

def lamport_clock():
    n = int(input("Enter number of processes: "))
    clocks = [0] * n
    while True:
        print("\n1. Internal Event\n2. Send Message\n3. Receive Message\n4. Exit")
        ch = int(input("Enter choice: "))
        if ch == 1:
            p = int(input("Enter process number: "))
            clocks[p] += 1
            print(f"Process {p} performed an event, Clock = {clocks}")
        elif ch == 2:
            s = int(input("Enter sender process: "))
            clocks[s] += 1
            print(f"Message sent from P{s} with timestamp {clocks[s]}")
        elif ch == 3:
            r = int(input("Enter receiver process: "))
            t = int(input("Enter received timestamp: "))
            clocks[r] = max(clocks[r], t) + 1
            print(f"Message received by P{r}, Clock = {clocks}")
        elif ch == 4:
            break
        else:
            print("Invalid choice!")

#Vector clock

def vector_clock():
    n = int(input("Enter number of processes: "))
    VC = [[0 for _ in range(n)] for _ in range(n)]
    while True:
        print("\n1. Internal Event\n2. Send Message\n3. Receive Message\n4. Exit")
        ch = int(input("Enter choice: "))
        if ch == 1:
            p = int(input("Enter process number: "))
            VC[p][p] += 1
            print(f"Internal event in P{p}, VC = {VC[p]}")
        elif ch == 2:
            s = int(input("Enter sender process: "))
            VC[s][s] += 1
            print(f"Message sent from P{s}, VC = {VC[s]}")
        elif ch == 3:
            r = int(input("Enter receiver process: "))
            sv = list(map(int, input("Enter sender vector (space-separated): ").split()))
            for i in range(n):
                VC[r][i] = max(VC[r][i], sv[i])
            VC[r][r] += 1
            print(f"Message received by P{r}, VC = {VC[r]}")
        elif ch == 4:
            break
        else:
            print("Invalid choice!")

print("\n1. Lamport Clock\n2. Vector Clock")
choice = int(input("Enter your choice: "))
if choice == 1:
    lamport_clock()
else:
    vector_clock()
