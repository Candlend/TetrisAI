import matplotlib.pyplot as plt
import sys
import numpy as np

def equation(a1, a2, a3, a4, x):
    return (a1 * x + a2 * x ** 2 + a3 * x ** 3+ a4 * x ** 4)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        t = 0
        # print(sys.argv)
        with open(sys.argv[1],"r") as f:
            while True:
                args = f.readline()
                if not args:
                    break
                print("Equation %d:...." % t)
                args = args.strip().split(' ')
                print(args)
                args = [float(_) for _ in  args]
                x = np.arange(args[0], args[1], abs(args[1] - args[0]) / float(sys.argv[2]))
                y = [equation(args[2], args[3], args[4], args[5], _) for _ in x]
                y = np.array(y)
                print('Vector generated...')
                plt.plot(x, y, color='red')
                print('ploted...')
                plt.savefig('%d.png' % t)
                plt.clf()
                t += 1