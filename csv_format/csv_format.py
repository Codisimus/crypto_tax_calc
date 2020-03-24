import csv


class CSVFormat:
    def __init__(self, columns, date_format):
        self.columns = columns
        self.date_format = date_format

    def load(self, path):
        objects = []
        with open(path, newline='') as file:
            for row in csv.DictReader(file):
                values = []
                for column in self.columns:
                    values.append(row[column])
                objects.append(self.from_string_array(values))
        return objects

    def write(self, objects, path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.columns)
            for obj in objects:
                writer.writerow(self.to_string_array(obj))

    def from_string_array(self, values):
        raise Exception()

    def to_string_array(self, obj):
        raise Exception()
