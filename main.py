from processes import *
from multiprocessing import Process
import csv, time


def data_in_class():
    with open('crimes.csv', 'r') as file:
        reader = csv.reader(file)
        list_of_crimes = list(reader)

    return Processes(list_of_crimes[1:len(list_of_crimes)])


def main():
    crimes = data_in_class()
    crimes.part()
    t = time.time()
    pro1 = Process(target=crimes.process1())
    pro1.start()
    pro1.join()
    print('Время выполнения первого процесса:', str(time.time() - t)[:5])

    t = time.time()
    pro2 = Process(target=crimes.process2())
    pro2.start()
    pro2.join()
    print('Время выполнения второго процесса:', str(time.time() - t)[:5])

    t = time.time()
    pro3 = Process(target=crimes.process3())
    pro3.start()
    pro3.join()
    print('Время выполнения третьего процесса:', str(time.time() - t)[:5])

if __name__ == '__main__':
    main()