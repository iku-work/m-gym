import xml.etree.ElementTree as ET
from os import getcwd, path, makedirs, listdir
from shutil import copytree, copy
from errno import ENOTDIR
from pathlib import Path
from uuid import uuid1
import m_gym
import random

class CreateSimulation():

  def __init__(self, config):

    self.config = config
    self.model_name = config['model_name']
    self.model_file_location = config['model_file_location']
    self.excluded = config['excluded']
    self.service_inputs = config['service_inputs']
    self.render = config['render']


    # Get useful data from the config.json file
    #self.current_dir = path.dirname(path.abspath(__file__))
    self.current_dir =path.dirname(path.abspath(m_gym.envs.createsim.__file__))

    # Find simulation model folder
    self.model_folder = self.current_dir + '\\' + self.model_file_location

    # Find simulation model xml file
    self.xml_file_path =  self.model_folder + '\\{}.xml'.format(self.model_name)

    # Find simulation model mvs file
    self.model_file_path = self.model_folder + '\\{}.mvs'.format(self.model_name)



    # Open file
    try:
      self.xmldoc = ET.parse(self.xml_file_path)
    except Exception as e:
      raise IOError(e)
      #print('Error opening xml file!')

    self.inputs, self.outputs = self.read_xml()
    self.action_len = self.calc_len(self.inputs)
    self.observation_len = self.calc_len(self.outputs)
    
    self.current_id = uuid1()
    self.workers_dir = ""
    if config.get("workers_directory"):
      #print(config.get("workers_directory"))
      self.workers_dir = '{}\\{}'.format(self.model_folder, self.config['workers_directory']) 
      #print("works")
    else:
      self.workers_dir = '{}\\{}\\{}'.format(self.model_folder,'..','Workers') 


    self.new_folder = '{}\\{}'.format(self.workers_dir,self.current_id) 

    print(self.new_folder)

    if not path.exists(self.workers_dir):
      makedirs(self.workers_dir)

    try:
      copytree(self.model_folder, self.new_folder)

    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == ENOTDIR:
            copy(self.model_folder, self.new_folder)
        else:
            print('Directory not copied. Error: %s' % e)


    self.worker_number = random.randint(0,15)
    self.new_xml_file_path = self.new_folder + '\\{}.xml'.format(self.model_name)
    print(self.new_xml_file_path)
    self.new_xml_file = ET.parse(self.new_xml_file_path)
    self.analog_inputs_blocks, self.digital_inputs_blocks = self.set_inputs(self.new_xml_file_path, self.new_xml_file, self.inputs, self.worker_number)

    

    self.analog_outputs_blocks, self.digital_outputs_blocks = self.set_outputs(self.new_xml_file_path, self.new_xml_file, self.outputs, self.worker_number)
    self.set_name(self.new_xml_file_path, self.new_xml_file, self.worker_number)
    self.model_file_path = self.new_folder + '\\{}.mvs'.format(self.model_name)
    self.change_sim_name(self.model_file_path, self.current_id)


  # Function for removing spaces and change to lowercase of the instances
  def normalize_value(self, value):
    cleaned_item = value.replace(" ", "")
    cleaned_lower = cleaned_item.lower()
    return cleaned_lower

  def read_xml(self):
    

    def get_attributes(root, element):
    
      analog_names = []
      analog_blocks = []
      digital_names = []
      digital_blocks = []
      
      if element == 'Inputs':
        attrib_name = 'InType'
        attrib_io_name = 'JoyNro'
      elif element == 'Outputs':
        attrib_name = 'OutputType'
        attrib_io_name = 'ChannelBlock'
      else:
        print('No such element!')

      for model_io in root.find(element):
        if model_io.tag not in self.excluded:
          if model_io.attrib[attrib_name] == "Analog":
            analog_names.append(model_io.tag)
            analog_blocks.append(model_io.attrib[attrib_io_name])
          elif model_io.attrib[attrib_name] == "Digital":
            digital_names.append(model_io.tag)
            digital_blocks.append(model_io.attrib[attrib_io_name])
          else:
            print("ERROR: Bad input type of {} input. Check {}.xml".format(model_io.tag, self.model_name))
            raise BadType 

      return [analog_names, analog_blocks, digital_names, digital_blocks]

    # change values of I/O blocks and channels after copying template folder

    #Get root of the xml file
    root = self.xmldoc.getroot()
    
    inputs = get_attributes(root, 'Inputs')
    outputs = get_attributes(root, 'Outputs')

    return inputs, outputs

  def change_sim_name(self, mvs_path, worker_number):
    mvs_doc = ET.parse(mvs_path)
    root = mvs_doc.getroot()

    environment = root.find('Environment')
    sim_name = environment.attrib['simulationName']
    environment.set('simulationName', sim_name + str(worker_number))
    mvs_doc.write(mvs_path)



  def set_inputs(self, xml_path, xml_doc, inputs_list, worker_number):
    
    root = xml_doc.getroot()
    
    inputs_element = root.find('Inputs')
    
    print(inputs_element.text)

    analog_inputs_names = inputs_list[0]
    analog_inputs_len = len(analog_inputs_names)
    digital_inputs_names = inputs_list[2]
    digital_inputs_len = len(digital_inputs_names)
    analog_inputs_blocks = inputs_list[1]
    digital_inputs_blocks = inputs_list[3]

    service_inputs = self.config['service_inputs']

    for analog_input_index in range(analog_inputs_len):
      analog_input = inputs_element.find(analog_inputs_names[analog_input_index])
      analog_input.set("JoyCh", str(worker_number))


    for digital_input_index in range(digital_inputs_len):
      digital_input = inputs_element.find(digital_inputs_names[digital_input_index])
      digital_input.set("JoyCh", str(worker_number))


    print("Service inputs: ", service_inputs)
    for service_input_name in service_inputs:
      service_input = inputs_element.find(service_input_name)
      service_input.set("JoyCh", str(worker_number))

    xml_doc.write(xml_path)

    return analog_inputs_blocks, digital_inputs_blocks

  def set_service_io(self):

    service_outputs = self.config['service_outputs']


  def set_outputs(self, xml_path, xml_doc, outputs_list, worker_number):
    
    root = xml_doc.getroot()
    outputs_element = root.find('Outputs')
    analog_outputs_names = outputs_list[0]
    analog_outputs_len = len(analog_outputs_names)
    digital_outputs_names = outputs_list[2]
    digital_outputs_len = len(digital_outputs_names)

    analog_outputs_blocks = outputs_list[1]
    digital_outputs_blocks = outputs_list[3]

    for analog_output_index in range(analog_outputs_len):
      analog_output = outputs_element.find(analog_outputs_names[analog_output_index])
      analog_output.set("ChannelIndex", str(worker_number))

    for digital_output_index in range(digital_outputs_len):
      digital_output = outputs_element.find(digital_outputs_names[digital_output_index])
      digital_output.set("ChannelIndex", str(worker_number))


    xml_doc.write(xml_path)
    return analog_outputs_blocks, digital_outputs_blocks

  def set_name(self,xml_path, xml_doc, worker_number):
    
    root  = xml_doc.getroot()
    model_element = root.find('Model')
    model_element.set('Name', model_element.attrib['Name'] + str(worker_number))
    xml_doc.write(xml_path)
  
  def calc_len(self, values_list):
    return len(values_list[0]) + len(values_list[2])


  def check_dir(self, mvs_folder):

      if not Path.exists(Path(mvs_folder)):
          print('Error: Directory {} not found'.format(mvs_folder))
          return False
      else:
          return True

class BadType(Exception):  
  pass





