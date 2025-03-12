from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from namespaces import *
from modules import *
from user_experience import *
import math
import os


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()

    def save_plot(self, filename):
        self.figure.savefig(filename)


class CustomTab(QWidget):
    def __init__(self, app, linkedApp, title_val="", parent=None):
        super().__init__(parent)
        # self.type = type
        # titles = ['Open File', 'Summary ({})', 'Statistic ({})']
        self.title_val = title_val  # titles[type].format(title)
        self.app = app
        self.linkedApp = linkedApp
        self.initUI()

    def initUI(self):
        raise NotImplementedError(
            "Subclasses should implement this method!"
        )  # self.optionsTabs[self.type](self)


class HelloTab(CustomTab):
    title = "Welcome"

    def initUI(self):
        self.tab = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(self.tab)

        gridLayout = QtWidgets.QGridLayout(self.tab)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setText("Hello")
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(70)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.ee = ExperienceEngine(self.app, self)
        self.ee.set_background()

        self.setLayout(gridLayout)

    # Он уже есть в MyApp, так что хз
    def resizeEvent(self, event):
        self.ee.set_background()
        super().resizeEvent(event)


class HomeTab(CustomTab):
    title = "Home"

    def initUI(self):
        if self.title_val:
            self.title += f" ({self.title_val})"
        self.tab = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(self.tab)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        gridLayout.addItem(spacerItem2, 5, 5, 1, 1)
        self.dateTimeEdit_to = QtWidgets.QDateTimeEdit(self.tab)
        self.dateTimeEdit_to.setCalendarPopup(True)
        gridLayout.addWidget(self.dateTimeEdit_to, 5, 2, 1, 3)
        self.pushButton_open = QtWidgets.QPushButton(self.tab)
        self.pushButton_open.setText("Open")
        gridLayout.addWidget(self.pushButton_open, 2, 6, 1, 1)
        label = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        label.setText("From")
        gridLayout.addWidget(label, 4, 1, 1, 1)
        self.dateTimeEdit_from = QtWidgets.QDateTimeEdit(self.tab)
        self.dateTimeEdit_from.setCalendarPopup(True)
        gridLayout.addWidget(self.dateTimeEdit_from, 5, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        gridLayout.addItem(spacerItem3, 2, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        gridLayout.addItem(spacerItem4, 2, 7, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        gridLayout.addItem(spacerItem5, 9, 2, 1, 1)
        label_2 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        label_2.setFont(font)
        label_2.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        label_2.setText("To")
        gridLayout.addWidget(label_2, 4, 3, 1, 1)
        """self.pushButton_analyze = QtWidgets.QPushButton(self.tab)
        self.pushButton_analyze.setText('Analyze')
        gridLayout.addWidget(self.pushButton_analyze, 6, 1, 1, 6)"""
        self.pushButton_raw = QtWidgets.QPushButton(self.tab)
        self.pushButton_raw.setText("View RAW")
        gridLayout.addWidget(self.pushButton_raw, 6, 6, 1, 1)
        self.pushButton_analyze = QtWidgets.QPushButton(self.tab)
        self.pushButton_analyze.setText("Analyze")
        gridLayout.addWidget(self.pushButton_analyze, 8, 1, 1, 6)
        self.comboBox_pattern = QtWidgets.QComboBox(self.tab)
        self.comboBox_pattern.setMinimumSize(QtCore.QSize(95, 0))
        gridLayout.addWidget(self.comboBox_pattern, 5, 6, 1, 1)
        label_3 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        label_3.setFont(font)
        label_3.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        label_3.setText("Pattern")
        gridLayout.addWidget(label_3, 4, 6, 1, 1)
        self.lineEdit_filepath = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_filepath.setMinimumSize(QtCore.QSize(360, 0))
        gridLayout.addWidget(self.lineEdit_filepath, 2, 1, 1, 5)
        """self.lineEdit_filepath = QtWidgets.QComboBox(self.tab)
        self.lineEdit_filepath.setEditable(True)
        self.lineEdit_filepath.setMinimumSize(QtCore.QSize(360, 0))"""
        gridLayout.addWidget(self.lineEdit_filepath, 2, 1, 1, 5)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        gridLayout.addItem(spacerItem6, 3, 1, 1, 1)

        self.setLayout(gridLayout)

        self.pushButton_open.clicked.connect(self.choice_type_open)
        self.comboBox_pattern.addItems(PATTERN_OPTIONS)
        self.pushButton_analyze.clicked.connect(self.analyze)
        self.pushButton_raw.clicked.connect(self.open_raw)

        def filter_existing_paths(file_paths):
            existing_paths = [path for path in file_paths if os.path.exists(path)]
            return existing_paths

        if self.app.ds.settings.get("files_path"):

            existing_file_paths = filter_existing_paths(
                self.app.ds.settings.get("files_path")
            )
            self.app.ds.settings["files_path"] = existing_file_paths

            completer = QCompleter(existing_file_paths)
            completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.lineEdit_filepath.setCompleter(completer)

        if self.app.ds.settings.get("date_from") and self.app.ds.settings.get(
            "date_to"
        ):
            self.dateTimeEdit_from.setDateTime(
                QDateTime.fromString(self.app.ds.settings["date_from"], Qt.ISODate)
            )
            self.dateTimeEdit_to.setDateTime(
                QDateTime.fromString(self.app.ds.settings["date_to"], Qt.ISODate)
            )

    def analyze(self):
        self.app.ds.settings["date_from"] = self.dateTimeEdit_from.dateTime().toString(
            Qt.ISODate
        )
        self.app.ds.settings["date_to"] = self.dateTimeEdit_to.dateTime().toString(
            Qt.ISODate
        )
        if self.lineEdit_filepath.text() not in self.app.ds.settings.get(
            "files_path", []
        ):
            # This `carayoba` put file path in the storage
            self.app.ds.settings.update(
                {
                    "files_path": self.app.ds.settings.get("files_path", [])
                    + [self.lineEdit_filepath.text()]
                }
            )

        self.app.create_tab(
            self.app,
            self,
            SummaryTab,
            title=os.path.basename(self.lineEdit_filepath.text()),
            title2line=f"{self.dateTimeEdit_from.dateTime().toPyDateTime()} — {self.dateTimeEdit_to.dateTime().toPyDateTime()}",
        )

    def open_raw(self):
        if self.app.showDialog("It can take some time..."):
            self.app.create_tab(
                self.app,
                self,
                RawTab,
                title=os.path.basename(self.lineEdit_filepath.text()),
            )

    def choice_type_open(self):
        if self.app.showDialog(
            "What would you like",
            title="Choice",
            button_text=("File", "Folder"),
            set_icon_flag=False,
        ):
            self.openFileDialog()
        else:
            self.openDirectoryDialog()

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "Python Files (*.log);;All Files (*)",
            options=options,
        )
        if fileName:
            print(fileName)
            self.lineEdit_filepath.setText(fileName)

    def openDirectoryDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", "", options=options
        )
        if directory:
            print(directory)
            self.lineEdit_filepath.setText(directory)


class SummaryTab(CustomTab):
    title = "Summary"

    def initUI(self):
        if self.title_val:
            self.title += f" ({self.title_val})"
        self.tab = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(self.tab)
        self.widget = QtWidgets.QWidget(self.tab)
        gridLayout.addWidget(self.widget, 0, 0, 1, 4)
        self.comboBox_0 = QtWidgets.QComboBox(self.tab)
        gridLayout.addWidget(self.comboBox_0, 1, 0, 1, 1)

        self.comboBox_1 = QtWidgets.QComboBox(self.tab)
        self.comboBox_1.setEditable(True)
        gridLayout.addWidget(self.comboBox_1, 1, 1, 1, 2)
        self.setLayout(gridLayout)

        self.comboBox_2 = QtWidgets.QComboBox(self.tab)
        gridLayout.addWidget(self.comboBox_2, 1, 3, 1, 1)

        self.canvas = MplCanvas(self, width=8, height=4, dpi=100)
        self.canvas.axes.axis("off")
        self.canvas.axes.set_frame_on(False)
        layout = QtWidgets.QVBoxLayout(self.widget)
        layout.addWidget(self.canvas)
        self.widget.setLayout(layout)

        self.comboBox_0.currentIndexChanged.connect(self.selected_step1)
        self.comboBox_1.currentIndexChanged.connect(self.selected_step2)
        self.comboBox_2.currentIndexChanged.connect(self.selected_step3)

        self.canvas.mpl_connect("button_press_event", self.onclick)

        self.pe = ProcessingEngine(self.app, self.linkedApp)
        # self.pe.parsing_data()
        # На случай отсутвия пути
        if self.pe.parsing_data() is False:
            return
        # print(self.pe.filtered_logs.head())

        self.comboBox_0.clear()
        self.comboBox_0.addItems([DEFAULT_VAL_CB] + self.pe.items())
        # print(self.pe.filtered_logs)

    def selected_step1(self, index):
        if self.comboBox_0.currentText() == DEFAULT_VAL_CB:
            return
        self.selColumn = self.pe.filtered_logs[
            self.comboBox_0.currentText()
        ].value_counts()
        # print(self.selColumn)
        self.draw_plot2(
            *self.pe.normalised_values2(
                self.selColumn.values.tolist(), self.selColumn.index.tolist()
            ),
            self.comboBox_0.currentText(),
        )

        self.model = QStringListModel()
        self.model.setStringList(self.selColumn.index.tolist())

        self.comboBox_1.clear()
        self.completer = QtWidgets.QCompleter(self.model, self)
        self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.comboBox_1.setCompleter(self.completer)
        self.comboBox_1.addItems(self.selColumn.index.tolist())
        self.comboBox_1.setCurrentIndex(-1)
        self.comboBox_1.lineEdit().setPlaceholderText(DEFAULT_VAL_OR_WRITE_CB)

    def selected_step2(self, index):
        # print(f'"{self.comboBox_1.currentText()}"')
        if self.comboBox_1.currentText() == "":
            self.comboBox_2.clear()
            return
        elif self.comboBox_1.currentText() not in self.selColumn.index.tolist():
            return

        self.comboBox_2.clear()
        self.comboBox_2.addItems([DEFAULT_VAL_CB] + self.pe.items())

    def selected_step3(self, index):
        if (
            self.comboBox_2.currentText() == DEFAULT_VAL_CB
            or not self.comboBox_2.currentText()
        ):
            return
        elif self.comboBox_1.currentText() not in self.selColumn.index.tolist():
            return

        # df только с нужными значениями в выбранной колонке
        df = self.pe.filtered_logs[
            self.pe.filtered_logs[self.comboBox_0.currentText()]
            == self.comboBox_1.currentText()
        ]
        # Series с подсчитаными значениями по колличесву повторений
        self.dataForBar = df[self.comboBox_2.currentText()].value_counts()
        self.app.create_tab(
            self.app,
            self,
            StatisticTab,
            title=f"{self.comboBox_0.currentText()} — {self.comboBox_1.currentText()} — {self.comboBox_2.currentText()}",
        )

    # no use
    def draw_plot(self, val, label, noteForLabel=[]):
        if noteForLabel:
            label = [f"{n} ({noteForLabel[i]})" for i, n in enumerate(label)]
        self.canvas.axes.cla()
        self.canvas.axes.pie(
            val,
            labels=label,
            wedgeprops=dict(width=0.4),
            labeldistance=5,
            colors=COLOR_PALETTE_20[: len(val)],
        )  # explode=nDist,
        self.canvas.axes.legend(
            loc="upper left", bbox_to_anchor=(-0.5, 1), fontsize=LEGEND_FONT_SIZE
        )
        self.canvas.draw()

    def draw_plot2(self, val, label, coloumn_name="", noteForLabel=[]):
        if noteForLabel:
            label = [f"{n} ({noteForLabel[i]})" for i, n in enumerate(label)]

        self.canvas.figure.clf()
        # Эта жаба `figure.clf()` удаляет все нахер,
        # поэтому приходится создавать новый субплот..
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.axes.cla()

        #
        # Расчет размера секций происходит (!)НЕЕ val * len(labels),
        #
        # А val * sqrt(len(labels))
        #

        def calculate_percentages(numbers):
            if not numbers:  # Проверка на случай пустого списка
                return []

            total = sum(numbers)  # Находим общую сумму всех чисел в списке
            if total == 0:  # Проверка, чтобы избежать деления на ноль
                return [0] * len(numbers)

            percentages = [
                num * 100 / total for num in numbers
            ]  # Вычисляем процент для каждого числа
            return percentages

        # Вторая диаграмма (для легенды)
        modify_color = []
        modify_val = []
        dir_labels = []

        for i, el in enumerate(label):

            if val[i] / len(label[i]) < 1 / DIVIDER_FOR_COLOR_DELIMITER:
                modify_val.append(val[i] * math.ceil(math.sqrt(len(el))))
                modify_color.append(COLOR_PALETTE_20[i])
                dir_labels.append(el)
            else:
                for j, tag in enumerate(el):
                    modify_val.append(val[i])
                    modify_color.append(
                        ColorEngine.adjust_brightness(
                            COLOR_PALETTE_20[i % len(COLOR_PALETTE_20)], j % 2
                        )
                    )
                    dir_labels.append(el)
        print("Len: ", len(modify_val))

        label_text = []
        for l in dir_labels:
            label_text.append(" ".join(l))

        figure2 = Figure()
        ax2 = figure2.add_subplot(111)
        self.wedges2, texts2 = ax2.pie(
            val, labels=label, colors=COLOR_PALETTE_20[: len(val)]
        )
        # ax2.axis('equal')

        _wedgeprops = {"edgecolor": "none", "width": 0.4}

        _props = {
            "boxstyle": "round,pad=0.5",
            "facecolor": TEXT_IN_PLOTTEXT,
            "edgecolor": ColorEngine.adjust_brightness(TEXT_IN_PLOTTEXT, 11),
            "alpha": 0.4,
        }

        self.wedges1, _ = self.canvas.axes.pie(
            modify_val,
            labels=label_text,
            labeldistance=5,
            colors=modify_color,
            wedgeprops=_wedgeprops,
        )  # explode=nDist,
        PDT = ProcessingDT(coloumn_name, label)
        avail_func_len = PDT.get_len_available_func()
        alternative_label = PDT.go2D(depth=2)

        text_string = ""
        if avail_func_len is not False:
            for i in range(1, avail_func_len):
                text_string += PDT.go(i)
                text_string += "\n"
        # text_string = ProcessingDT(coloumn_name, [n[0] for n in label]).go()
        # print(text_string)
        if alternative_label is not False:
            label = alternative_label.values()

        self.canvas.figure.text(
            0.95,
            0.95,
            "lkjlkj",
            ha="right",
            va="top",
            bbox=_props,
            fontsize=LEGEND_FONT_SIZE,
        )
        self.canvas.figure.legend(
            self.wedges2,
            self.pe.make_labels(label, val),
            loc="upper left",
            fontsize=LEGEND_FONT_SIZE,
        )  # bbox_to_anchor=(-0.7, 1),
        self.canvas.draw()
        # self.canvas.

    def onclick(self, event):
        # Проверяем, кликнут ли в пределах осей
        if event.inaxes == self.canvas.axes:
            # Проверяем, кликнут ли на сегмент
            for wedge in self.wedges1:
                if wedge.contains_point([event.x, event.y]):
                    label = wedge.get_label().split(" ")
                    self.segment_color = ColorEngine.float_to_rgb(wedge.get_facecolor())
                    print(self.segment_color)
                    print("Clicked on segment:", len(label), type(label))
                    if len(label) > 1:
                        self.df_for_table = self.pe.filtered_logs[
                            self.pe.filtered_logs[self.comboBox_0.currentText()].isin(
                                label
                            )
                        ]
                    else:
                        self.df_for_table = self.pe.filtered_logs[
                            self.pe.filtered_logs[self.comboBox_0.currentText()]
                            == label[0]
                        ]
                    dialog = TableDialog(self.app, self, "Information Table")
                    dialog.exec_()
                    break


class InfoDialog(QDialog):
    def __init__(self, app, linkedApp, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.linkedApp = linkedApp
        self.app = app
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.initUI()

    def resizeEvent(self, event):
        self.app.ds.settings["x_dt"] = event.size().width()
        self.app.ds.settings["y_dt"] = event.size().height()
        super().resizeEvent(event)

    def initUI(self):
        raise NotImplementedError("Subclasses should implement this method!")


class TableDialog(InfoDialog):
    def initUI(self):
        # Dialog = QtWidgets.QDialog()
        self.setWindowTitle(self.title)
        self.resize(self.app.ds.settings["x_dt"], self.app.ds.settings["y_dt"])
        gridLayout = QtWidgets.QGridLayout(self)
        self.tableView = QtWidgets.QTableView(self)
        # self.tableView.setStyleSheet(f"background-color: {self.linkedApp.segment_color};")
        gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        self.setLayout(gridLayout)

        self.model = ProcessingEngine(self.app, self).dataframe_to_model(
            self.linkedApp.df_for_table
        )
        ProcessingEngine(self.app, self).color_column(
            self.linkedApp.df_for_table.columns.get_loc(
                self.linkedApp.comboBox_0.currentText()
            ),
            self.linkedApp.segment_color,
        )
        self.tableView.setModel(self.model)


class RawTab(CustomTab):
    title = "RAW"

    def initUI(self):
        if self.title_val:
            self.title += f" ({self.title_val})"
        self.tab = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(self.tab)
        self.tableView = QtWidgets.QTableView(self.tab)
        gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        self.setLayout(gridLayout)

        self.pe = ProcessingEngine(self.app, self.linkedApp)
        df = self.pe.parsing_data()
        # if not df:
        #    return

        # Создание модели данных из DataFrame
        self.model = self.pe.dataframe_to_model(df)
        self.tableView.setModel(self.model)


class StatisticTab(CustomTab):
    title = "Statistic"

    def initUI(self):
        if self.title_val:
            self.title += f" ({self.title_val})"
        self.tab = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(self.tab)
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setText("GroupBy")
        gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.tab)
        gridLayout.addWidget(self.widget, 1, 0, 1, 1)
        self.setLayout(gridLayout)

        self.canvas = MplCanvas(self, width=8, height=4, dpi=100)
        layout = QtWidgets.QVBoxLayout(self.widget)
        layout.addWidget(self.canvas)
        self.widget.setLayout(layout)

        self.checkBox.stateChanged.connect(self.processing)

        self.processing()

    def processing(self):
        # print(self.linkedApp.dataForBar)
        # bar_values, bar_labels = self.group_data(self.linkedApp.dataForBar.values.tolist(), [str(n) for n in self.linkedApp.dataForBar.index.tolist()], self.checkBox.isChecked())
        bar_values, bar_labels = ProcessingEngine(self.app, self).normalised_values2(
            self.linkedApp.dataForBar.values.tolist(),
            [str(n) for n in self.linkedApp.dataForBar.index.tolist()],
        )
        bar_labels = ProcessingEngine(self.app, self).make_labels(
            bar_labels, bar_values
        )
        # bar_labels = self.make_labels2(bar_values, bar_labels, 3)
        self.draw_plot(bar_values, bar_labels)

    # На выходе список со списками лейблов на случай,
    # если несколько разных лейблов имеют одно и тоже значение
    #
    # А `make_labels` делает итоговый вариант
    # При страбатывании `quantity_for_group_label` нужно помнить,
    # что список начинается с `[<num>]`,
    # поэтому поумолчанию будет выведен 1 элемент с `...`
    def group_data(self, val_list, label_list, forcibly=False):

        def isSame(arr):
            a = arr[0]
            for i in arr:
                if i != a:
                    return False
            return True

        if (
            len(val_list) <= MAX_COLUMNS_STATISTIC
            and not forcibly
            and not isSame(val_list)
        ):
            self.checkBox.setEnabled(True)
            return val_list, [[n] for n in label_list]
        else:
            if not forcibly:
                self.checkBox.setChecked(True)
                self.checkBox.setEnabled(False)
            ser = pd.Series(data=val_list, index=label_list)
            calc_val = ser.value_counts()
            print("LINE: 250")
            # print(calc_val.index.tolist())
            # print(calc_val.values.tolist())
            print(calc_val)

            new_labels = []
            for n in calc_val.index.tolist():
                new_labels.append([f"[{n}] "] + ser[ser == n].index.tolist())
            # print(new_labels)
            return calc_val.values.tolist(), new_labels

    def make_labels2(self, value_list, label_list, quantity_for_group_label=2):
        print("make:", value_list[0], label_list[0])
        new_label_list = []
        for i, label in enumerate(label_list):
            if len(label) > quantity_for_group_label:
                new_label_list.append(
                    f'[{value_list[i]}x] {" ,".join(label_list[:quantity_for_group_label])}... (len={len(label)})'
                )
            else:
                new_label_list.append(
                    f'[{value_list[i]}x] {" ,".join(label_list[:quantity_for_group_label])}'
                )
        return new_label_list

    def make_labels(self, label_list, quantity_for_group_label=2):
        new_labels = []
        for n in label_list:
            if len(n) == 1:
                new_labels.append(n[0])
            else:
                new_labels.append(
                    ", ".join(
                        [
                            str(x)
                            for i, x in enumerate(n)
                            if i < quantity_for_group_label
                        ]
                    )
                    + ("..." if len(n) > quantity_for_group_label else "")
                )
        return new_labels

    def draw_plot(self, val, label, noteForLabel=[]):
        if noteForLabel:
            label = [f"{n} ({noteForLabel[i]})" for i, n in enumerate(label)]
        self.canvas.axes.cla()
        self.canvas.axes.barh(
            label,
            val,
            label=[str(item) for item in label],
            height=0.2,
            color=COLOR_PALETTE_20[: len(label)],
        )
        self.canvas.axes.legend(
            fontsize=LEGEND_FONT_SIZE, loc="lower right", reverse=True
        )
        self.canvas.axes.spines["top"].set_visible(False)
        self.canvas.axes.spines["right"].set_visible(False)
        self.canvas.axes.spines["left"].set_visible(False)
        self.canvas.axes.spines["bottom"].set_visible(False)
        self.canvas.axes.yaxis.set_ticks([])
        # self.canvas.axes.yaxis.set_tick_params(pad=10)
        self.canvas.draw()


class ClosableTabBar(QTabBar):
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            index = self.tabAt(event.pos())
            if index != -1:
                self.parent().removeTab(index)
        super().mousePressEvent(event)


if __name__ == "__main__":
    print("Ты дебил")
