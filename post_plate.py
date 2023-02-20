from odbAccess import *
import odbAmplitude
import sys
import numpy as np
#
def read_bulk_data(field):
    """ Read data from the bulkDataBlocks of the FieldOutput object """
    return np.concatenate([block.data for block in field.bulkDataBlocks])

def read_bulk_labels(field):
    """ Read data from the bulkDataBlocks of the FieldOutput object """
    return np.concatenate([block.elementLabels for block in field.bulkDataBlocks])
#
def read_bulk_node_labels(field):
    """ Read node labels from the bulkDataBlocks of the FieldOutput object
    """
    return np.concatenate([block.nodeLabels
                           for block in field.bulkDataBlocks])
#
def post_plate(filename,pressure_curve):
    #-------------------------------------------------------------------------------
    # Open odb file
    #-------------------------------------------------------------------------------
    odb  = openOdb(path=filename+'.odb')
    #-------------------------------------------------------------------------------
    # Load the step
    #-------------------------------------------------------------------------------
    stepname = 'Load'
    step = odb.steps[stepname]
    #-------------------------------------------------------------------------------
    # Get overall pressure curve
    #-------------------------------------------------------------------------------
    time_curve  = [tple[0] for tple in odb.amplitudes[pressure_curve].data]
    press_curve = [tple[1] for tple in odb.amplitudes[pressure_curve].data]
    #-------------------------------------------------------------------------------
    # Extract local pressure and normal for the element
    #-------------------------------------------------------------------------------
    for i,frame in enumerate(step.frames):
#       Read the pressure field 
        field  = frame.fieldOutputs['P']
        P = read_bulk_data(field)
        labels_P = read_bulk_labels(field)
#       Read the normal field
        field  = frame.fieldOutputs['SDV_N']
        N = read_bulk_data(field)
        labels = read_bulk_labels(field)
#       prepare arrays and store data
        if i == 0:
           nframe = np.shape(step.frames)[0]
           nelt   = np.shape(P)[0]
           Pel = np.zeros([nframe,nelt])
           Nel = np.zeros([nframe,nelt])
           time_field = np.zeros([nframe])
           Nel[i,:] = np.ones([nelt])
        else:
           Pel[i,:] = P[:,0]
           for j in range(0,len(P)):
               Nel[i,j] = N[np.where(labels == labels_P[j])[0][0],0]
#       Get the time of field
        time_field[i] = frame.frameValue
#   Interpolate overall pressure
    P_lag = np.interp(time_field,time_curve,press_curve)
    #-------------------------------------------------------------------------------
    # export data
    #-------------------------------------------------------------------------------
    #np.savetxt(filename+'_P.csv',Pel,delimiter=',')
    #np.savetxt(filename+'_N.csv',Nel,delimiter=',')
    #np.savetxt(filename+'_PLAG.csv',np.transpose([time_field,P_lag]),delimiter=',')
    np.savez_compressed(filename, P=Pel, N=Nel, PLAG=np.transpose([time_field,P_lag]), labels=labels, NN=N)
    #-------------------------------------------------------------------------------
    # Close odb file
    #-------------------------------------------------------------------------------
    odb.close()
    return
####################################################################################
####################################################################################
# START OF SCRIPT
####################################################################################
####################################################################################
filename = sys.argv[1]
pressure_curve = 'DRIVER15BAR'
if len(sys.argv) > 2:
    pressure_curve = sys.argv[2]

print("Processing file: ", filename, ". Pressure curve: ", pressure_curve)
post_plate(filename,pressure_curve)
exit()
####################################################################################
####################################################################################
# END OF SCRIPT
####################################################################################
####################################################################################