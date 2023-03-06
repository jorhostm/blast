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

 #   Read the pressure field
    i = 0
    frame = step.frames[i]
    field  = frame.fieldOutputs['P']
    P = read_bulk_data(field)
    labels_P = read_bulk_labels(field)
#   Read the normal field
    field  = frame.fieldOutputs['SDV_N']
    N = read_bulk_data(field)
    labels_N = read_bulk_labels(field)

    nframe = np.shape(step.frames)[0]
    nelt   = np.shape(P)[0]
    Pel = np.zeros([nframe,nelt])
    Nel = np.ones([nframe,nelt])
    time_field = np.zeros([nframe])

    labels_N_inv = np.zeros(nelt+1, dtype=np.int32)
    labels_N_inv[labels_N] = np.arange(0,len(labels_N))
    labels_P_inv = np.zeros(nelt+1, dtype=np.int32)
    labels_P_inv[labels_P] = np.arange(0,len(labels_P))

    indices = np.zeros(nelt, dtype=np.int32)
    indices[labels_P_inv[1:]] = labels_N_inv[1:]

    iter_frames = iter(step.frames)
    next(iter_frames)
    for i,frame in enumerate(iter_frames, start=1):
#       Read the pressure field 
        field  = frame.fieldOutputs['P']
        P = read_bulk_data(field)
#       Read the normal field
        field  = frame.fieldOutputs['SDV_N']
        N = read_bulk_data(field)
#       prepare arrays and store data
        Pel[i,:] = P[:,0]
        #Nel[i,labels_P_inv[1:]] = N[labels_N_inv[1:],0]
        Nel[i,:] = N[indices,0]
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
    np.savez_compressed(filename, P=Pel, N=Nel, PLAG=np.transpose([time_field,P_lag]), labels=labels_P)
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

post_plate(filename,pressure_curve)
exit()
####################################################################################
####################################################################################
# END OF SCRIPT
####################################################################################
####################################################################################