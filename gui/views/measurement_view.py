# -*- coding: utf-8 -*-
"""
gui.views.measurement_view.py
October 10, 2019
@author: Francois Roy
"""
import os
import csv
from PyQt5 import uic
from PyQt5.QtCore import QModelIndex, QTimer
from utils import *
import logging
import threading


MEASUREMENTS_DIR = ROOT_DIR
VIEWS_DIR = ROOT_DIR.child('gui').child('views')


BASE_M, FORM_M = uic.loadUiType(VIEWS_DIR.child('measurement.ui'))


class MeasurementView(BASE_M, FORM_M):
    r"""The measurement controls"""
    def __init__(self, app):
        super(BASE_M, self).__init__()
        self.setupUi(self)
        self.extra = {'qthreadName': threading.current_thread().name}

        self._app = app
        self._model = None
        self._measurement = None

        self._labjacks = []
        self._motor_controllers = []
        self._mc_ports = []

        self._main_thread = threading.currentThread()
        self._threads = []

        self._dt = float("0.1")
        self.ui_time.addItems(["0.1", "0.5", "1.0", "2.0", "5.0"])
        self.ui_time.currentIndexChanged.connect(self.set_time_increment)

        self._timer = QTimer()
        self._timer.setInterval(1000 * self._dt)  # in ms
        self._timer.timeout.connect(self.update)

        self._display = self._app.display_widget.gv
        self._signal_selection = self._app.display_widget.sig_sel

        self._line_plot = pg.PlotCurveItem(pen='y')
        self._display.enableAutoRange()
        self._display.addItem(self._line_plot)
        self._display.setMouseEnabled(False)

        self._times = [0.0]
        self._data = None

        # set pump duty-cycle control
        self.ui_pump.valueChanged.connect(self.set_pump_duty_cycle)
        self.ui_fan.valueChanged.connect(self.set_fan_duty_cycle)

        self.ui_start.clicked.connect(self.start)
        self.ui_stop.clicked.connect(self.stop)

        self._signal_selection.currentIndexChanged.connect(self.update_display)
        self._signal = None

        self._csv_file = None
        self._csv_writer = None

        self.ui_stop.setEnabled(False)

    def set_time_increment(self):
        r""""""
        value = float(self.ui_time.currentText())
        logging.info("time interval set to: {}".format(value),
                     extra=self.extra)
        self._dt = value
        self._timer.setInterval(1000 * self._dt)  # in ms

    def display_finished_thread(self, thread_name):
        r"""Display the name of the finished threads."""
        if thread_name is not None:
            logging.info('Finishing thread {}'.format(thread_name),
                         extra=self.extra)

    def display_result(self, r):
        r""""""
        message = '\nThread target info:\n'
        # ll = OrderedDict(sorted(r.items(), key=lambda e: e[0]))
        for k, v in r.items(): # ll.items():
            message += '    {}: {}\n'.format(k, v)
        logging.info(message, extra=self.extra)

    @staticmethod
    def message(m, thread_name=threading.current_thread().name, level='info'):
        r"""Logging message"""
        extra = {'qthreadName': thread_name}
        if level == 'info':
            logging.info(m, extra=extra)
        elif level == 'warning':
            logging.warning(m, extra=extra)
        elif level == 'debug':
            logging.debug(m, extra=extra)
        else:
            logging.error(m, extra=extra)

    def progress(self, n):
        r"""Progress"""
        # TODO: implement the method.
        self._app.progressBar.show()
        self._app.progressBar.setValue(n)

    def set_model(self, model):
        r"""Sets model

        :param model: The model instance.
        """
        self._model = model
        self._measurement = self._model.measurement
        m_index = self._model.index(self._measurement.row(), 0, QModelIndex())
        self._model.insertRows(0, 1, parent=m_index,
                               type_info=MOTOR_CONTROLLER)
        mc = self._measurement.children()[0]
        mc_index = self._model.index(mc.row(), 0, m_index)
        # add pump and fan to motor controller
        self._model.insertRows(0, 1, parent=mc_index, type_info=FAN)
        f = mc.children()[0]
        f.children()[0].signal.field = self.fan_voltage
        f.children()[1].signal.field = self.fan_current
        self._model.insertRows(0, 1, parent=mc_index, type_info=PUMP)
        p = mc.children()[0]
        p.children()[0].signal.field = self.pump_voltage
        p.children()[1].signal.field = self.pump_current

        self._model.insertRows(0, 1, parent=m_index, type_info=LABJACK)
        lj = self._measurement.children()[0]
        lj_index = self._model.index(lj.row(), 0, m_index)
        # Add sensors
        names = ['T4', 'T3', 'T2', 'T1', 'p3', 'p2', 'p1', 'frate']
        channels = [7, 6, 5, 4, 3, 2, 1, 0]
        c_type = SINGLE_ENDED  # all single ended default
        gains = [0, 0, 0, 0, 0, 0, 0, 0]  # gains
        fields = [self.channel_7, self.channel_6, self.channel_5,
                  self.channel_4, self.channel_3, self.channel_2,
                  self.channel_1, self.channel_0]
        units = ['degC', 'degC', 'degC', 'degC', 'kPa', 'kPa', 'kPa', 'l/min']
        for i in range(8):
            self._model.insertRows(0, 1, parent=lj_index, type_info=SENSOR)
            s = lj.children()[0]
            s.set_data(0, "{}".format(names[i]))  # name
            s.set_data(1, "{}".format(channels[i]))  # channel
            # s.set_data(2, "{}".format(c_type))  # channel type
            # s.set_data(3, "{}".format(int(gains[i])))  # channel gains
            s.signal.field = fields[i]
            s.signal.units = units[i]

        measurement = m_index.internalPointer()
        children = measurement.children()

        ljs = []
        mc = []
        for child in children:
            if child.type_info == LABJACK:
                ljs.append(child)
            elif child.type_info == MOTOR_CONTROLLER:
                mc.append(child)
        self._labjacks = ljs
        self._motor_controllers = mc

    def set_fan_duty_cycle(self):
        r""""""
        value = int(self.ui_fan.value())
        logging.debug("Fan duty cycle {}".format(str(value)),
                      extra=self.extra)
        if self._motor_controllers[0] is not None:
            self._motor_controllers[0].duty_cycles[1] = \
                int((min(value, 100) * 127) / 100)

    def set_pump_duty_cycle(self):
        r""""""
        value = int(self.ui_pump.value())
        logging.debug("Pump duty clycle {}".format(str(value)),
                      extra=self.extra)
        if self._motor_controllers[0] is not None:
            self._motor_controllers[0].duty_cycles[0] = \
                int((min(value, 100) * 127) / 100)

    def set_selection(self, current):
        """
        :param current:
        :type current: QModelIndex
        """
        pass

    def set_threads(self):
        r"""Set threads in launching order."""
        # pump thread should start after the loop has started
        for device in self._model.measurement.children():
            if device.type_info == MOTOR_CONTROLLER:
                thread = Worker(device.update_duty_cycles)
                thread.setName('MotorControllerThread')
                thread.signals.message.connect(self.message)
                thread.signals.finished.connect(self.display_finished_thread)
                self._threads.append(thread)
            if device.type_info == LABJACK:
                # reading must start after processing
                thread = Worker(device.read_stream_data)
                thread.setName('StreamReaderThread-{}'.format(device.name))
                thread.signals.message.connect(self.message)
                thread.signals.finished.connect(self.display_finished_thread)
                thread.signals.result.connect(self.display_result)
                self._threads.append(thread)

    def start(self):
        r"""Start the acquisition loop"""
        # self._app.console.widget().clear()  # clear log window
        # reset threads
        self._threads = []
        self.set_threads()
        self.ui_pump.setValue(0)
        self.ui_fan.setValue(0)
        self._motor_controllers[0].set_device(port="COM7")
        self._labjacks[0].activate()
        logging.info('Starting acquisition', extra=self.extra)

        self.set_data()  # initialize both data frame and plot selection
        self._signal = self._signal_selection.currentText()

        self._times = [0.0]
        self._timer.start()  # start timer
        for thread in self._threads:  # start remaining threads
            thread.start()
        self.start_rec()

        self.ui_start.setEnabled(False)
        self.ui_time.setEnabled(False)
        self.ui_stop.setEnabled(True)

    def set_data(self):
        r""""""
        labels = OrderedDict()
        labels["time (s)"] = [0.]
        signal_names = set_signal_names(self._measurement)
        for val in signal_names:
            labels[val] = [0.]  # dummy value
        self._data = labels  # pd.DataFrame.from_dict(labels)

        self._signal_selection.clear()
        for _ in signal_names:
            self._signal_selection.addItem(_.replace('_', ' '))

    def stop(self):
        r""""""
        logging.info('Stopping acquisition', extra=self.extra)
        self.ui_pump.setValue(0)
        self.ui_fan.setValue(0)
        self.stop_rec()
        self._timer.stop()  # stop timer
        for mc in self._motor_controllers:
            mc.stop()
        for lj in self._labjacks:
            logging.info('Stopping device: {}'.format(lj.device.deviceName),
                         extra=self.extra)
            lj.stop()

        for thread in threading.enumerate():  # join threads if alive
            if thread is self._main_thread:
                continue
            thread.join()
            logging.debug('Joining {}'.format(thread.getName()),
                          extra=self.extra)
        self.ui_start.setEnabled(True)
        self.ui_time.setEnabled(True)
        self.ui_stop.setEnabled(False)

    def start_rec(self):
        r"""Start recording data in a csv file. The data is stored in
        ``MEASUREMENT_DIR`` under the name `data.csv`. This file is overridden
        every time the `start acquisition` button is clicked.

        """
        if not os.path.exists(MEASUREMENTS_DIR):
            os.makedirs(MEASUREMENTS_DIR)
        self._csv_file = open(MEASUREMENTS_DIR.child('data.csv'), 'wb')
        self._csv_writer = csv.DictWriter(
            self._csv_file, fieldnames=list(self._data.keys()))
        self._csv_writer.writeheader()

    def stop_rec(self):
        r"""Close the csv file if open."""
        if self._csv_file is not None:
            if not self._csv_file.closed:
                self._csv_file.close()

    def update(self):
        r"""Update every time increment."""
        mc = self._motor_controllers[0]
        lj = self._labjacks[0]
        r = None

        lj._finished = False
        errors = 0
        missed = 0
        # Read from Queue until there is no data.
        try:
            # get([block[, timeout]])¶
            # Remove and return an item from the queue. If optional
            # args block is true and timeout is None (the default),
            # block if necessary until an item is available. If timeout
            # is a positive number, it blocks at most timeout seconds
            # and raises the Empty exception if no item was available
            # within that time. Otherwise (block is false), return an
            # item if one is immediately available, else raise the
            # Empty exception (timeout is ignored in that case).
            # Pull results out of the Queue in a blocking manner.
            result = lj.raw_data.get(False)  # (True, 0.0001)
            if result["errors"] != 0:
                errors += result["errors"]
                missed += result["missed"]
                logging.warning(
                    "Total Errors: {}, Total Missed: "
                    "{}".format(errors, missed),
                    extra=self.extra)
            # Convert the raw bytes (result['result']) to voltage data.
            r = lj.device.processStreamData(result['result'])
            lj.raw_data.task_done()
            lj.raw_data_ready.clear()
        except lj.raw_data.Empty:
            if lj._finished:
                logging.info("Done reading from the Queue.", extra=self.extra)
            else:
                logging.error("Queue is empty. Stopping...", extra=self.extra)
                lj._finished = True
        except Exception as e:
            logging.error("{}: {}".format(e), extra=self.extra)
            lj._finished = True

        with lj.raw_data.mutex:
            lj.raw_data.queue.clear()
        current_time = self._times[-1] + self._dt
        self._times.append(current_time)
        self._data["time (s)"] = self._times

        for s in lj.sensors():
            name = '{} {} ({})'.format(s.parent().name,
                                       s.name,
                                       s.signal.units)
            if r is not None:
                # Get the average, make sure the length of the list
                # is a float for float division.
                voltage = (
                    (sum(r[AIN.upper() + str(s.channel)]) /
                     float(len(r[AIN.upper() + str(s.channel)])))
                )
                # convert to physical quantity
                v = Q_(np.asarray([voltage]), 'V')
                if s.name == 'p1':
                    quantity = convert_pressure_px119(
                        v, r_shunt=Q_(470.0, 'ohm'),
                        value_range=Q_(np.array([0, 30]), 'psi'), zero=Q_(1.375, 'kPa')
                    ).magnitude[0]
                elif s.name == 'p2':
                    quantity = convert_pressure_px119(
                        v, r_shunt=Q_(470.0, 'ohm'),
                        value_range=Q_(np.array([0, 30]), 'psi'), zero=Q_(1.7, 'kPa')
                    ).magnitude[0]
                elif s.name == 'p3':
                    quantity = convert_pressure_px119(
                        v, r_shunt=Q_(470.0, 'ohm'),
                        value_range=Q_(np.array([0, 30]), 'psi'), zero=Q_(1.85, 'kPa')
                    ).magnitude[0]
                elif s.name == 'T1':
                    # logging.debug("T sensor voltage {}".format(v[0]), extra=self.extra)
                    quantity = convert_temperature_rtd(
                        v, v_in=Q_(2.5, 'V'),
                        r1=Q_(100., 'ohm'), filename='pt100.txt', zero=Q_(0.29, 'degC')
                    ).magnitude[0]
                elif s.name == 'T2':
                    # logging.debug("T sensor voltage {}".format(v[0]), extra=self.extra)
                    quantity = convert_temperature_rtd(
                        v, v_in=Q_(2.5, 'V'),
                        r1=Q_(100., 'ohm'), filename='pt100.txt', zero=Q_(-0.05, 'degC')
                    ).magnitude[0]
                elif s.name == 'T3':
                    # logging.debug("T sensor voltage {}".format(v[0]), extra=self.extra)
                    quantity = convert_temperature_rtd(
                        v, v_in=Q_(2.5, 'V'),
                        r1=Q_(100., 'ohm'), filename='pt100.txt'
                    ).magnitude[0]
                elif s.name == 'T4':
                    # logging.debug("T sensor voltage {}".format(v[0]), extra=self.extra)
                    quantity = convert_temperature_rtd(
                        v, v_in=Q_(2.5, 'V'),
                        r1=Q_(100., 'ohm'), filename='pt100.txt'
                    ).magnitude[0]
                elif s.name == 'frate':  # flow rate
                    # logging.debug("magmeter voltage {}".format(v[0]), extra=self.extra)
                    quantity = convert_flow_rate_magmeter(
                        v, r_shunt=Q_(465.2, 'ohm'),
                        value_range=Q_(np.array([0, 80]), 'l/min')
                    ).magnitude[0]
                    if quantity < 0.0:
                        quantity = 0.0
                else:
                    quantity = voltage
            s.signal.field.setText('{:3.1f}'.format(quantity))
            self._data[name].append(quantity)

        for i, m in enumerate(mc.children()):
            if m is not None:
                mc.r_lock.acquire()
                for s in m.sensors():
                    value = s.read()
                    name = '{} {} ({})'.format(s.parent().name,
                                               s.name,
                                               s.signal.units)
                    s.signal.field.setText('{:3.2f}'.format(value))
                    self._data[name].append(value)
                mc.r_lock.release()
        d = {}
        for k, v in self._data.items():
            d[k] = '{:3.10f}'.format(v[-1])
        self._csv_writer.writerow(d)
        self._line_plot.setData(self._times, self._data[self._signal])

    def update_display(self):
        r""""""
        # self._display.clear()
        self._signal = self._signal_selection.currentText()
        logging.debug("signal {}".format(self._signal), extra=self.extra)
