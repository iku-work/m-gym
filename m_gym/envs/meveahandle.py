import subprocess
from time import sleep
import numpy as np
from shutil import rmtree
import m_gym.envs.MeveaIO as io
from os import kill
from signal import CTRL_BREAK_EVENT

class MeveaHandle:

    def __init__(self, worker_number, analog_inputs,digital_inputs,analog_outputs,digital_outputs):

        self.worker_number = worker_number
        
        self.analog_inputs = analog_inputs
        self.digital_inputs = digital_inputs

        self.analog_outputs = analog_outputs
        self.digital_outputs = digital_outputs

    def set_inputs(self, values_array):
        
        inputs_count_total = 0
        inputs_digital_count = 0

        for analog_input in range(len(self.analog_inputs)):
            io.set_analog_input(int(self.analog_inputs[inputs_count_total]), self.worker_number, values_array[inputs_count_total])
            inputs_count_total += 1
            
        for digital_input in range(len(self.digital_inputs)):
            io.set_digital_input(digital_input, self.worker_number, round(values_array[inputs_count_total]))
            inputs_count_total += 1


    def get_outputs(self):
        
        analog =  [io.get_analog_output(int(analog_output_number),self.worker_number) for analog_output_number in self.analog_outputs]
        digital = [io.get_digital_output(int(digital_output_number),self.worker_number) for digital_output_number in self.digital_outputs]

        joined_outputs_list = analog + digital

        return np.array(joined_outputs_list, dtype=np.float32)
    
    def set_single_digital_input(self,  block, channel, value):
        io.set_digital_input(block, channel, value)

    def get_single_digital_output(self, block, channel):
        return io.get_digital_output(block, channel)

    def set_single_analog_input(self,  block, channel, value):
        io.set_analog_input(block, channel, value)

    def get_single_analog_output(self, block, channel):
        return io.get_analog_output(block, channel)

    def start_process(self, path_to_file, render):
        

        if render == True:
            # Run cmd command
            command = 'MeveaSolver.exe /mvs  {}'.format(path_to_file)
        else:
            command = 'MeveaSolver.exe /headless /mvs  {}'.format(path_to_file)

        self.process = subprocess.Popen(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def terminate(self):

        kill(self.process.pid, CTRL_BREAK_EVENT)
        sleep(2)
    
    def delete_folder(self, folder):
        #if self.copied:
        try:
            rmtree(folder)
        except OSError as e:
            print("Error: %s : %s" % (folder, e.strerror))
