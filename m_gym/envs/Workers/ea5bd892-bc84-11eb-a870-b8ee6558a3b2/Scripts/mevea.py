from time import sleep
#Executed at the loading of script
def initScript():

    GDict['Reset_Done'] = False
    #sleep(1)

    

#Executed every 10 ms
def callScript(deltaTime, simulationTime ):

    #print(GDict['Input_Reset'].getInputValue() == 1 and GDict['DataSource_Reset'].getDsValue() == 0, GDict['Input_Reset'].getInputValue(), GDict['DataSource_Reset'].getDsValue())
    #GDict['DataSource_Reset'].setDsValue(0)
    # If episode ended or call for reset received, restart simulation
    if GDict['Input_Reset'].getInputValue() == 1 and GDict['Reset_Done'] == False:
        GDict['Reset_Done'] = True
        GSolver.restartSimulation()
        #sleep(1)

    return 0