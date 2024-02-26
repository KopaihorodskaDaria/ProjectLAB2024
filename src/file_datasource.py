from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


# функція, що читає дані із файлу та додає до списку
# використовується у методі read()
def finding_data(filename, data_list, data_class):
    with open(filename, 'r') as file:
        data_read = reader(file)
        next(data_read)
        for row in data_read:
            data = data_class(*map(float, row))
            data_list.append(data)


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_data = []
        self.gps_data = []
        self.index_acc = 0
        self.index_gps = 0

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""

        #  перевірка чи є дані
        if not self.accelerometer_data:
            finding_data(self.accelerometer_filename, self.accelerometer_data, Accelerometer)
        if not self.gps_data:
            finding_data(self.gps_filename, self.gps_data, Gps)

        #  отримуємо дані та оновлюємо індекси
        accelerometer = self.accelerometer_data[self.index_acc]
        gps = self.gps_data[self.index_gps]
        self.index_acc = (self.index_acc + 1) % len(self.accelerometer_data)
        self.index_gps = (self.index_gps + 1) % len(self.gps_data)

        return AggregatedData( # повертаємо об'єкт AggregatedData із даними
            accelerometer,
            gps,
            datetime.now(),
            config.USER_ID,
        )

    def startReading(self):
        """Метод повинен викликатись перед початком читання даних"""

        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')

    def stopReading(self):
        """Метод повинен викликатись для закінчення читання даних"""

        # якщо файл відкритий, то закриваємо його
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()

