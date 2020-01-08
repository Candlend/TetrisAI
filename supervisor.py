import sys
import os
import csv

if __name__ == "__main__":
    train_time = 0
    with open('./settings/score.csv','w') as f:
        f_csv = csv.writer(f)
        while True:
            print('*' for _ in range(80))
            print("#%d th Trainning......." % train_time)
            res = os.system('python main.py')
            print("Trainning score result: %d" % res)
            f_csv.writerow([train_time, res])
            train_time += 1