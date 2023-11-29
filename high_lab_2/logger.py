import os.path
import time


class LogWriter:
    """ синглтон класс логгера """
    # параметры логгера
    status_list = ["DEBUG", "INFO", "WANR", "ERROR", "CRITICAL"]
    log_file_name = "log.txt"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LogWriter, cls).__new__(cls)
            print("Класс логгера только один, при следующих вызовах new возвращаем ранее созданный экземпляр")
        print("Возвращаем ранее созданный экземпляр")
        return cls.instance

    def log(self, status, message):
        is_status_right = self.check_status(status)
        if not is_status_right:
            print("INCORRECT STATUS")
            exit(1)

        file = self.open_log_file()
        cur_time = time.asctime()
        log_string = "[{status}]{cur_time}: {message}\n".\
                     format(status=status, cur_time=cur_time, message=message)
        file.write(log_string)

    def open_log_file(self):
        file_exists = os.path.exists(self.log_file_name)

        # если файл уже есть, открываем файл на добавление
        if not file_exists:
            # если файла нет, создаем файл
            return open(self.log_file_name, "w")
        else:
            return open(self.log_file_name, "a")

    def check_status(self, status):
        if status in self.status_list:
            return True
        return False


if __name__ == "__main__":
    logger = LogWriter()
    logger.log("DEBUG", "бя")

    logger1 = LogWriter()
