'''
This file is code by the tired stage of the framework
The readout class is coded as new rules
'''

import numpy as np
import src

from src.core import Base, READOUT_TIME_WINDOW,MAX_OPERATION_TIME
from src.function import Coding

class Readout(Base):
    def __init__(self, id):
        self.id = id
        self.pre_reservoir_list = []
        self.read_number = 0
        self.pre_state = np.array([])


    def add_pre_reservoir(self, reservoir):
        self.pre_reservoir_list.append(reservoir)

    def initialization(self, coding_rule):
        neu_n =0
        for res in self.pre_reservoir_list:
            for neu in res.neuron_list:
                neu_n += 1
        self.coding = getattr(Coding(neu_n, READOUT_TIME_WINDOW), coding_rule)

    def add_read_neuron_s(self):
        self.read_number += 1

    def add_read_neuron_n(self, n_number):
        self.read_number += n_number

    def connect(self):
        pass

    def get_state(self,t):
        t_state = np.array([]).reshape(0,1)
        for res in self.pre_reservoir_list:
            for neu in res.neuron_list:
                t_state = np.concatenate((self.pre_reservoir_list,[[neu.fired_sequence[t]]]), axis= 0)
        return t_state

    def get_state_t(self):
        t = self.get_global_time()
        return self.get_state(t)

    def get_state_all(self):
        t = 0
        while t <= MAX_OPERATION_TIME :
            t_state = self.get_state(t)
            self.pre_reservoir_list = np.concatenate((self.pre_reservoir_list,t_state),axis=1)

    def output_t(self):
        t = self.get_global_time()
        state = self.coding(self.pre_reservoir_list[t:t+READOUT_TIME_WINDOW])
        return state