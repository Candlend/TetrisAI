import sys
import os
import csv

if __name__ == "__main__":
    target_train_times = -1
    target_train_rounds = 5
    train_round = 0
    total_times = 0
    with open('./settings/score.csv','w') as f:
        f_csv = csv.writer(f)
        while (((total_times < target_train_times) or (target_train_times == -1))
                and ((train_round < target_train_rounds) or (target_train_rounds == -1))):
            print('*' for _ in range(80))
            print("#%d th Training......." % train_round)
            if target_train_times != -1:
                res = os.system('python main.py %d' % (target_train_times - total_times))
            else:
                res = os.system('python main.py')

            print("Trained seconds: %d" % res)
            total_times += res
            train_round += 1