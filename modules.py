import re
import socket
import asyncio
import pandas as pd
from datetime import datetime

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QThread, QMutex, QMutexLocker, pyqtSignal, QEventLoop

from namespaces import *


class ProcessingEngine:
    def __init__(self, app, linkedApp):
        self.app = app
        self.linkedApp = linkedApp

    def parsing_data(self):

        self.dataFile_path = self.linkedApp.lineEdit_filepath.text()
        if not self.dataFile_path:
            self.app.showWarning("Path is incorrect")
            return False
        QApplication.setOverrideCursor(Qt.WaitCursor)
        start_time = self.linkedApp.dateTimeEdit_from.dateTime().toPyDateTime()
        end_time = self.linkedApp.dateTimeEdit_to.dateTime().toPyDateTime()
        # print(start_time, end_time, sep='\n')

        # self.linkedApp.comboBox_pattern.currentText()
        with open(
            PATH_TO_PATTERNS + self.linkedApp.comboBox_pattern.currentText()
        ) as link:
            self.log_pattern = re.compile(link.read())

        logs = self.__parse_logs()
        df = self.__logs_to_dataframe(logs)
        self.filtered_logs = self.__filter_logs_by_time(df, start_time, end_time)
        QApplication.restoreOverrideCursor()
        return self.filtered_logs

    def items(self):
        return self.filtered_logs.columns.tolist()

    def __parse_logs(self):
        """with open(self.dataFile_path, 'r') as file:
            logs = []
            for line in file:
                match = self.log_pattern.match(line)
                if match:
                    logs.append(match.groupdict())
        return logs"""
        logs = []

        # dataFile_path - файл или папка?
        if os.path.isfile(self.dataFile_path):

            with open(self.dataFile_path, "r") as file:
                for line in file:
                    match = self.log_pattern.match(line)
                    if match:
                        logs.append(match.groupdict())

        elif os.path.isdir(self.dataFile_path):
            for filename in os.listdir(self.dataFile_path):
                file_path = os.path.join(self.dataFile_path, filename)

                # Убедимся, что это файл
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        for line in file:
                            match = self.log_pattern.match(line)
                            if match:
                                logs.append(match.groupdict())

        return logs

    def __logs_to_dataframe(self, logs):
        df = pd.DataFrame(logs)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%b %d %H:%M:%S %Y")
        return df

    def __filter_logs_by_time(self, df, start_time, end_time):
        mask = (df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)
        return df.loc[mask]

    def normalised_values2(self, val_list, label_list, n_percent=1):
        #
        # Расчет размера секций происходит (!) НЕЕ val * len(labels),
        #
        # А val * sqrt(len(labels))
        #

        ser = pd.Series(data=val_list, index=label_list)
        grouped = (
            ser.groupby(ser)
            .apply(lambda x: list(x.index))
            .rename_axis("repeats")
            .reset_index(name="labels")
        )
        print("repeats len:", len(grouped["repeats"].tolist()))
        # print([n * len(labels[i]) for i, n in enumerate(values)], labels, sep='\n')
        if False and len(grouped["repeats"].tolist()) > MAX_PIECES_IN_PIE:
            print("repeats:", grouped["repeats"].tolist()[0])
            rows_to_combine = grouped.iloc[
                0 : len(grouped["repeats"].tolist()) - MAX_PIECES_IN_PIE + 1
            ]
            print("iloc:", len(grouped["repeats"].tolist()) - MAX_PIECES_IN_PIE + 1)

            # Объединение всех списков в один
            combined_labels = [
                label for sublist in rows_to_combine["labels"] for label in sublist
            ]

            # Создание новой строки
            new_row = pd.DataFrame({"repeats": [1], "labels": [combined_labels]})

            # Удаление выбранных строк из исходного DataFrame
            grouped = grouped.drop(rows_to_combine.index)

            # Добавление новой строки в DataFrame
            grouped = pd.concat([new_row, grouped], ignore_index=True)

        if True:
            # Пороговый процент для repeats
            # n_percent = 1

            # Вычисление порогового значения repeats
            threshold = n_percent * grouped["repeats"].sum() / 100.0

            # Выбор строк, которые удовлетворяют условию
            rows_to_combine = grouped[grouped["repeats"] < threshold]

            # Объединение всех списков в один
            combined_labels = [
                label for sublist in rows_to_combine["labels"] for label in sublist
            ]

            # Создание новой строки
            new_row = pd.DataFrame({"repeats": [1], "labels": [combined_labels]})

            # Удаление выбранных строк из исходного DataFrame
            grouped = grouped.drop(rows_to_combine.index)

            # Добавление новой строки в DataFrame
            grouped = pd.concat([new_row, grouped], ignore_index=True)

        values, labels = grouped["repeats"].tolist(), grouped["labels"].tolist()
        print(grouped)
        print(values[0], len(labels[0]))
        return values, labels

    def normalised_values(self, val_list, label_list):
        self.normalised_values2(val_list, label_list)
        new_val_list = []
        new_label_list = []
        chenger_buf = {}
        summ_all_quantity = sum(val_list)
        threshold = summ_all_quantity / len(val_list)
        # print(summ_all_quantity, threshold, len(val_list))

        for i, n in enumerate(val_list):
            if (
                n / summ_all_quantity * len(val_list) > threshold * 2
            ):  # summ_all_quantity / n <= threshold * 2
                new_val_list.append(n)
                new_label_list.append(label_list[i])
            else:
                chenger_buf[n] = chenger_buf.get(n, 0) + 1
        other_val = sorted(chenger_buf.values(), reverse=True)
        new_val_list += [sum(other_val)]
        new_label_list += ["other"]  # * len(other_val)

        # print(val_list)
        # print(label_list)

        print(new_val_list)
        print(new_label_list)

        return new_val_list, new_label_list

    def make_labels(self, arr_arr_labels, arr_values=[], num_of_dis=2):
        new_arr_labels = []
        for i, label in enumerate(arr_arr_labels):
            limit_round = ", ".join(label[:num_of_dis])
            add_string = ""
            if len(label) > num_of_dis:
                add_string = f"... (len={len(label)})"
            if arr_values:
                new_arr_labels.append(f"[x{arr_values[i]}] {limit_round}{add_string}")
            else:
                new_arr_labels.append(f"{limit_round}{add_string}")
        return new_arr_labels

    def dataframe_to_model(self, df):
        from PyQt5.QtGui import QStandardItem, QStandardItemModel

        # Создание модели данных из DataFrame
        self.linkedApp.model = QStandardItemModel(df.shape[0], df.shape[1])
        self.linkedApp.model.setHorizontalHeaderLabels(df.columns)

        # Заполнение модели данными из DataFrame
        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                item = QStandardItem(str(df.iat[row, column]))
                self.linkedApp.model.setItem(row, column, item)
        return self.linkedApp.model

    def color_column(self, col, hex_color):
        from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor

        color = QColor(hex_color)
        brush = QBrush(color)

        for row in range(self.linkedApp.model.rowCount()):
            item = self.linkedApp.model.item(row, col)
            if item is not None:
                item.setBackground(brush)
            else:
                new_item = QStandardItem()
                new_item.setBackground(brush)
                self.linkedApp.model.setItem(row, col, new_item)


class ColorEngine:
    def __init__(self, app):
        self.app = app

    def adjust_brightness(hex_color, factor, d=4):
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

        def clamp(x):
            return max(0, min(x, 255))

        if factor % 2 == 0:
            # light
            rgb = tuple(clamp(c + factor * d) for c in rgb)
        else:
            # dark
            rgb = tuple(clamp(c - factor * d) for c in rgb)
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def float_to_rgb(float_color):
        r, g, b, a = float_color
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)


class GetDomainThread(QThread):
    finished = pyqtSignal(
        str, str
    )  # Сигнал, который будет испускаться после завершения обработки IP-адреса

    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address

    def run(self):
        try:
            domain = socket.gethostbyaddr(self.ip_address)[0]
        except (socket.herror, socket.gaierror):
            domain = self.ip_address
        self.finished.emit(self.ip_address, domain)  # Испускание сигнала с результатом


# DT: Data Type
class ProcessingDT:
    def __init__(self, column_name: str, data: list, number_exe_func=0):
        self.data = data
        self.column_name = column_name
        self.number_exe_func = number_exe_func

        # Available functions by key in the column name
        #
        # пускай 0 индекс будет применяться к данным в легенде
        self.available_func = {
            "ip": [self.__ip_to_domain],
            "trf": [lambda x: sum(x)],  # [lambda x: sum(sum(n for n in x))
            "timestamp": [self.__time_difference],
        }

    def get_len_available_func(self):
        for key, funcs in self.available_func.items():
            if self.column_name == key or self.column_name.split("_")[-1] == key:
                return len(funcs)
        return False

    def go(self, number_exe_func=-1):
        if number_exe_func >= 0:
            self.number_exe_func = number_exe_func

        for key, funcs in self.available_func.items():
            if self.column_name == key or self.column_name.split("_")[-1] == key:
                return funcs[self.number_exe_func](self.data)
        return False

    def go2D(self, depth=-1):
        arr2D = []
        for key, funcs in self.available_func.items():
            if self.column_name == key or self.column_name.split("_")[-1] == key:
                if depth < 0:
                    for line in self.data:
                        arr2D.append(funcs[self.number_exe_func](line))
                else:
                    # создаем слои из одинаковой глубины
                    arr2D = {}
                    for i_layer in range(depth):
                        # индекс - идекс в списке data
                        layer = {}
                        for i in range(len(self.data)):
                            if len(self.data[i]) > i_layer:
                                layer[i] = self.data[i][i_layer]
                        print("layer:", layer)
                        for i, dom in enumerate(
                            funcs[self.number_exe_func](layer.values())
                        ):
                            arr2D[list(layer.keys())[i]] = arr2D.get(
                                list(layer.keys())[i], []
                            ) + [dom]
                        print("arr2D:", arr2D)
                    # arr2D.append(funcs[self.number_exe_func](line if len(line) < depth else line[:depth]))
                return arr2D
        return False

    async def __get_domain_name(self, ip_address):
        loop = asyncio.get_event_loop()
        try:
            domain_name = await loop.run_in_executor(
                None, socket.gethostbyaddr, ip_address
            )
            return domain_name[0]  # Возвращаем только доменное имя
        except socket.herror:
            return ip_address  # Если доменное имя не найдено

    async def resolve_ips(self, ip_list):
        tasks = [self.__get_domain_name(ip) for ip in ip_list]
        return await asyncio.gather(*tasks)

    def __ip_to_domain2(self, ip_list):
        return asyncio.run(self.resolve_ips(ip_list))

    def __ip_to_domain(self, ip_address):
        self.event_loop = QEventLoop()
        self.num_end_fun = 0
        self.temp_dict = {}
        self.threads = []
        self.mutex = QMutex()
        self.len_ip_address = len(ip_address)

        for ip in ip_address:
            thread = GetDomainThread(ip)
            thread.finished.connect(self.__on_finished)
            thread.start()
            self.threads.append(thread)

        self.event_loop.exec_()

        # print(self.temp_dict, ip_address)
        return [self.temp_dict[ip] for ip in ip_address]

    def __on_finished(self, ip, domain):
        self.num_end_fun += 1
        with QMutexLocker(self.mutex):
            if self.num_end_fun == self.len_ip_address:
                self.event_loop.quit()
            self.temp_dict[ip] = domain

    def __time_difference(timestamps):
        min_time = min(timestamps)
        max_time = max(timestamps)

        difference = max_time - min_time

        # Преобразуем разницу в часы и минуты
        total_minutes = difference.total_seconds() // 60
        hours = total_minutes // 60
        minutes = total_minutes % 60

        return f"{int(hours):02}:{int(minutes):02}"


"""
def group_data(self, val_list, label_list, forcibly=False):

        def isSame(arr):
            a = arr[0]
            for i in arr:
                if i != a:
                    return False
            return True
        
        if len(val_list) <= 12 and not forcibly and not isSame(val_list):
            self.ui.checkBox.setEnabled(True)
            return val_list, [[n] for n in label_list]
        else:
            if not forcibly:
                self.ui.checkBox.setChecked(True)
                self.ui.checkBox.setEnabled(False)
            ser = pd.Series(data=val_list, index=label_list)
            calc_val = ser.value_counts()
            print('LINE: 154')
            print(calc_val.index.tolist())
            print(calc_val.values.tolist())

            new_labels = []
            for n in calc_val.index.tolist():
                new_labels.append([f'[{n}] '] + ser[ser ==  n].index.tolist())

            return calc_val.values.tolist(), new_labels

def make_labels(self, label_list, quantity_for_group_label = 2):
    new_labels = []
    for n in label_list:
        if len(n) == 1:
            new_labels.append(n[0])
        else:
            new_labels.append(', '.join([str(x) for i, x in enumerate(n) if i < quantity_for_group_label]) + '...')
    return new_labels



def normalised_values(self, val_list, label_list):
    new_val_list = []
    new_label_list = []
    chenger_buf = {}
    summ_all_quantity = sum(val_list)
    threshold = summ_all_quantity / len(val_list)
    #print(summ_all_quantity, threshold, len(val_list))

    for i, n in enumerate(val_list):
        if n / summ_all_quantity * len(val_list) > threshold * 2: # summ_all_quantity / n <= threshold * 2
            new_val_list.append(n)
            new_label_list.append(label_list[i])
        else:
            chenger_buf[n] = chenger_buf.get(n, 0) + 1
    other_val = sorted(chenger_buf.values(), reverse=True)
    new_val_list += [sum(other_val)]
    new_label_list += ['other'] # * len(other_val)


    #print(val_list)
    #print(label_list)

    print(new_val_list)
    print(new_label_list)

    return new_val_list, new_label_list


def processing(self):
    self.file_path = self.ui.line_filepath.text()
    if not self.file_path:
        self.showWarning('Please, select file')
        return

    start_time = self.ui.dateTime_from.dateTime().toPyDateTime()
    end_time = self.ui.dateTime_to.dateTime().toPyDateTime()
    print(start_time, end_time, sep='\n')

    self.log_pattern = re.compile(
    r'<(?P<priority>\d+)>'
    r'(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}) '
    r'(?P<hostname>\S+) '
    r'src="(?P<src_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<src_port>\d+)" '
    r'dst="(?P<dst_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<dst_port>\d+)" '
    r'msg="(?P<msg>[^"]+)" '
    r'note="(?P<note>[^"]+)" '
    r'user="(?P<user>[^"]+)" '
    r'devID="(?P<devID>\w+)" '
    r'cat="(?P<cat>[^"]+)" '
    r'sourceTranslatedAddress="(?P<source_translated_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" '
    r'sourceTranslatedPort=(?P<source_translated_port>\d+) '
    r'duration=(?P<duration>\d+) '
    r'sent=(?P<sent>\d+) '
    r'rcvd=(?P<rcvd>\d+) '
    r'dir="(?P<dir>[^"]+)" '
    r'protoID=(?P<protoID>\d+) '
    r'proto="(?P<proto>[^"]+)" '
    r'client_mac="(?P<client_mac>[^"]+)"'
    )

    logs = self.parse_logs(self.file_path)
    df = self.logs_to_dataframe(logs)
    

    #start_time = datetime(2024, 5, 18, 23, 0, 0)
    #end_time = datetime(2024, 5, 19, 0, 0, 0)
    self.filtered_logs = self.filter_logs_by_time(df, start_time, end_time)

    items = self.filtered_logs.columns.tolist()
    self.ui.comboBox_0.clear()
    self.ui.comboBox_0.addItems([DEFAULT_VAL_CB] + items)

    


def parse_logs(self, file_path):
    with open(file_path, 'r') as file:
        logs = []
        for line in file:
            match = self.log_pattern.match(line)
            if match:
                logs.append(match.groupdict())
    return logs

def logs_to_dataframe(self, logs):
    df = pd.DataFrame(logs)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%b %d %H:%M:%S %Y')
    return df

def filter_logs_by_time(self, df, start_time, end_time):
    mask = (df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)
    return df.loc[mask]"""
