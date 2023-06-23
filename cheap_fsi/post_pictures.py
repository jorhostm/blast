from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=350.707153320312,height=198.241241455078)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

def post_pictures_bck(odbfile):
    o1 = session.openOdb(name=odbfile+'.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, legend=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(DEFORMED, ))
    session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(visibleEdges=FREE)
    session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(renderShellThickness=OFF)
    session.viewports['Viewport: 1'].enableMultipleColors()
    session.viewports['Viewport: 1'].setColor(initialColor='#BDBDBD')
    cmap = session.viewports['Viewport: 1'].colorMappings['Part instance']
    cmap.updateOverrides(overrides={'PLATESHELL-1':(True, '#999999', 'Default','#999999')})
    #session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    #session.View(name='User-2', nearPlane=733.91, farPlane=1012.1, width=430.66, height=284.3, projection=PERSPECTIVE, cameraPosition=(-294.31, -47.634,828.51), cameraUpVector=(0.082124, 0.95979, -0.26844), cameraTarget=(-7.455, 0.81538, 5.221), viewOffsetX=0, viewOffsetY=0, autoFit=OFF)
    session.View(name='User-2', nearPlane=442.64, farPlane=1327.9, width=164.76, height=180.74, projection=PERSPECTIVE, cameraPosition=(-414.21, 18.165,832.32), cameraUpVector=( 0.16006, 0.93524, -0.31576), cameraTarget=(-3.0425, -1.2913, 48.56), viewOffsetX=0, viewOffsetY=0, autoFit=OFF)
    session.viewports['Viewport: 1'].view.setValues(session.views['User-2'])
    session.viewports['Viewport: 1'].enableMultipleColors()
    session.viewports['Viewport: 1'].setColor(initialColor='#BDBDBD')
    cmap=session.viewports['Viewport: 1'].colorMappings['Part instance']
    #session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    session.viewports['Viewport: 1'].disableMultipleColors()
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(DEFORMED, ))
    session.printOptions.setValues(reduceColors=False)
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
    session.printToFile(fileName=odbfile+'_15', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
    session.viewports[session.currentViewportName].odbDisplay.setFrame(step='Load',frame=10)
    session.printToFile(fileName=odbfile+'_10', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
    session.viewports[session.currentViewportName].odbDisplay.setFrame(step='Load',frame=7)
    session.printToFile(fileName=odbfile+'_7', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
    session.viewports[session.currentViewportName].odbDisplay.setFrame(step='Load',frame=5)
    session.printToFile(fileName=odbfile+'_5', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

#    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=20 )
#    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
#    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_UNDEF, ))
#---
#    session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=OFF, maxValue=1, minAutoCompute=OFF, minValue=0)
#---
#    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='SDV_D', outputPosition=INTEGRATION_POINT, )
#    session.printToFile(fileName=odbfile+'_D', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

#    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='SDV_OMEGA', outputPosition=INTEGRATION_POINT, )
#    session.printToFile(fileName=odbfile+'_OMEGA', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

#    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legend=ON)
#    session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=ON, minAutoCompute=ON)
#    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='SDV_P', outputPosition=INTEGRATION_POINT, )
#    session.printToFile(fileName=odbfile+'_P', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

    session.odbs[odbfile+'.odb'].close()

def post_pictures(odbfile):
    o1 = session.openOdb(name=odbfile+'.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, legend=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(DEFORMED, ))
    session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(visibleEdges=FREE)
    session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(renderShellThickness=ON)
    session.viewports['Viewport: 1'].enableMultipleColors()
    session.viewports['Viewport: 1'].setColor(initialColor='#BDBDBD')
    cmap = session.viewports['Viewport: 1'].colorMappings['Part instance']
    cmap.updateOverrides(overrides={'PLATESHELL-1':(True, '#999999', 'Default','#999999')})
    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    #session.View(name='User-2', nearPlane=733.91, farPlane=1012.1, width=430.66, height=284.3, projection=PERSPECTIVE, cameraPosition=(-294.31, -47.634,828.51), cameraUpVector=(0.082124, 0.95979, -0.26844), cameraTarget=(-7.455, 0.81538, 5.221), viewOffsetX=0, viewOffsetY=0, autoFit=OFF)
    session.View(name='User-2', nearPlane=442.64, farPlane=1327.9, width=164.76, height=180.74, projection=PERSPECTIVE, cameraPosition=(-414.21, 18.165,832.32), cameraUpVector=( 0.16006, 0.93524, -0.31576), cameraTarget=(-3.0425, -1.2913, 48.56), viewOffsetX=0, viewOffsetY=0, autoFit=OFF)
    session.viewports['Viewport: 1'].view.setValues(session.views['User-2'])
    session.viewports['Viewport: 1'].enableMultipleColors()
    session.viewports['Viewport: 1'].setColor(initialColor='#BDBDBD')
    cmap=session.viewports['Viewport: 1'].colorMappings['Part instance']
    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    session.viewports['Viewport: 1'].disableMultipleColors()
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(DEFORMED, ))
    session.printOptions.setValues(reduceColors=False)
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=20 )
#    session.printToFile(fileName=odbfile+'_20', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
#    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=15 )
#    session.printToFile(fileName=odbfile+'_15', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
#    session.viewports[session.currentViewportName].odbDisplay.setFrame(step='Load',frame=10)
#    session.printToFile(fileName=odbfile+'_10', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
#    session.viewports[session.currentViewportName].odbDisplay.setFrame(step='Load',frame=7)
#    session.printToFile(fileName=odbfile+'_7', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
#    session.viewports[session.currentViewportName].odbDisplay.setFrame(step='Load',frame=5)
#    session.printToFile(fileName=odbfile+'_5', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))



    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_UNDEF, ))
    frames = [5,7,10,15]
    for i in frames:
        session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=i )
#---
#        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=OFF, maxValue=1, minAutoCompute=OFF, minValue=0)
#        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=OFF, maxValue=1.51, minAutoCompute=OFF, minValue=1.0)
#---
#        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='STH', outputPosition=INTEGRATION_POINT, )
#        session.printToFile(fileName=odbfile+'_STH'+'_'+str(i), format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=OFF, maxValue=1, minAutoCompute=OFF, minValue=0)
        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='SDV_DAMAGE', outputPosition=INTEGRATION_POINT, )
        session.printToFile(fileName=odbfile+'_D'+'_'+str(i), format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='SDV_OMEGA', outputPosition=INTEGRATION_POINT, )
        session.printToFile(fileName=odbfile+'_OMEGA'+'_'+str(i), format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

#        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=OFF, maxValue=0.6667, minAutoCompute=OFF, minValue=-0.6667)
#        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='TRIAX', outputPosition=INTEGRATION_POINT, )
#        session.printToFile(fileName=odbfile+'_TRIAX'+'_'+str(i), format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

#    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='SDV_OMEGA', outputPosition=INTEGRATION_POINT, )
#    session.printToFile(fileName=odbfile+'_OMEGA', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

#    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legend=ON)
#    session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=ON, minAutoCompute=ON)
#    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='SDV_P', outputPosition=INTEGRATION_POINT, )
#    session.printToFile(fileName=odbfile+'_P', format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))

    session.odbs[odbfile+'.odb'].close()

#post_pictures('./blast_virtual_good/model_blast_1_6016_T4')
#post_pictures('./blast_virtual_good/model_blast_1_6016_T6')
#post_pictures('./blast_virtual_good/model_blast_1_6016_T7')

#post_pictures('model_mesh_2_T7')
#post_pictures('model_mesh_1_T7')
#post_pictures_bck('1-HV_3p0_T7_15')
post_pictures_bck('4-HV_1p5_FSI_10')
post_pictures_bck('4-HV_1p5_FSI_15')
post_pictures_bck('4-45_1p5_FSI_10')
post_pictures_bck('4-45_1p5_FSI_15')

#post_pictures_bck('./blast_virtual_good/model_blast_2_6016_T4')
#post_pictures('model_blast_2_6016_T7')

#post_pictures_bck('./Input_files/BLAST/model_T6_min')
#post_pictures_bck('./Input_files/BLAST/model_T6_max')

#post_pictures_bck('./Input_files/BLAST/model_T4_min')
#post_pictures_bck('./Input_files/BLAST/model_T4_max')

#post_pictures_bck('./Input_files/BLAST/model_T7_min')
#post_pictures_bck('./Input_files/BLAST/model_T7_max')

#post_pictures_bck('./blast_namo_last/model_blast_1_6016_T6')
#post_pictures_bck('./blast_namo_last/model_blast_1_6016_T7')
#post_pictures_bck('./blast_namo_last/model_blast_2_6016_T6')
#post_pictures_bck('./blast_namo_last/model_blast_3_6016_T6')
#post_pictures_bck('./blast_namo_last/model_blast_4_6016_T6')
#post_pictures_bck('./blast_namo_last/model_blast_5_6016_T6')
