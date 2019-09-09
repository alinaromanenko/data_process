from concurrent.futures import ThreadPoolExecutor
from threading import Thread, RLock, Condition
from queue import Queue


class Processes:
    def __init__(self, lst, size = 7):
        self.data = lst
        self.stats = []
        self.info = []
        self.crimes_count = []
        self.q = Queue(7)
        self._mute = RLock()
        self._empty = Condition(self._mute)
        self._full = Condition(self._mute)
        self._size = size
        self._queue = []

    def part(self):
        """Общая часть работы для всей программы"""
        for crime in self.data:
            try:
                if crime[9] == 'San Francisco':
                    if crime[1] != 'Passing Call':
                        self.info.append(crime[1])
            except:
                pass

        self.stats = set(self.info)

    def process1(self):
        """Первый последовательный процесс"""
        for crime in self.stats:
            self.crimes_count.append((crime, self.info.count(crime)))

        self.crimes_count.sort(key=lambda i: i[1])
        for i in range(1, 6):
            print(self.crimes_count[len(self.crimes_count) - i][0],
                  str(int(self.crimes_count[len(self.crimes_count) - i][1]) / len(self.data) * 100)[:3] + '%')
        self.crimes_count = []

    def work(self):  # crime
        """Запуск очереди"""
        while True:
            crime = self.q.get()
            self.crimes_count.append((crime, self.info.count(crime)))
            if crime is None:
                break

    def process2(self):
        """Многопоточный процесс с очередью"""
        with ThreadPoolExecutor(max_workers=5) as pool:
            # [pool.submit(self.work, crime) for crime in self.stats]

            th1 = Thread(target=self.work)
            th2 = Thread(target=self.work)
            th1.start()
            th2.start()
            for crime in self.stats:
                self.q.put(crime)
            self.q.put(None)
            self.q.put(None)
            th2.join()
            th1.join()

            self.crimes_count.sort(key=lambda i: i[1])
            for i in range(1, 6):
                print(self.crimes_count[len(self.crimes_count) - i][0],
                      str(int(self.crimes_count[len(self.crimes_count) - i][1]) / len(self.data) * 100)[:3] + '%')
            self.crimes_count = []

    def put(self):
       with self._full:
            while len(self._queue) >= self._size:
                self._full.wait()
            for crime in self.stats:
                self._queue.append(crime)
            self._empty.notify()

    def get(self):
        with self._empty:
            while len(self._queue) == 0:
                self._empty.wait()
            crime = self._queue.pop(0)
            self.crimes_count.append((crime, self.info.count(crime)))
            self._full.notify()

    def process3(self):
        """Многопоточный процесс с блокировкой"""
        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.submit(self.put())

            print(len(self.crimes_count))
            self.crimes_count = []
