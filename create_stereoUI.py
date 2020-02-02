import maya.cmds as mc
import maya.mel as mel
import os
cwd = os.getcwd()

disparity_bw = ""
colour_path = ""
disparity_height = 0.0

winName = 'myWindow'
winWidth = 500 

# Run the script for stereo image generation, this builds a plane with a camera attached to a semicircle
# Attaches plane with displacement material
def runMEL():
    print("Running Stereo Generation Script")
    # Replace this line with the absolute path of wherever you put the create_stereo_model.mel script!!!!!
    mel.eval('source "/Users/royashams/Documents/maya/projects/default/scripts/create_stereo_model.mel";')

# Change the text field after choosing image paths
def changeTextFld(which_image, pathname):
    if which_image == "disparity":
        mc.textField("disparity_field", edit=True, tx=pathname)
    if which_image == "colour":
        mc.textField("colour_field", edit=True, tx=pathname)

# Opens a file browser, and attaches the chosen image to the plane material
def chooseFile(which_image):
   filename = mc.fileDialog2(fileMode=1, caption="Import Image")
   if which_image == "disparity":
       disparity_bw = filename[0]
       disparity_string = 'string $disparity_bw = "' + disparity_bw + '";'
       mel.eval(disparity_string)
       mel.eval('setAttr "popout_material:file1.ftn" -type "string" $disparity_bw;')
       changeTextFld('disparity', filename[0])
       
   if which_image == "colour":
       colour_texture = filename[0]
       colour_string = 'string $colour_texture = "' + colour_texture + '";'
       mel.eval(colour_string)
       mel.eval('setAttr "popout_material:file2.ftn" -type "string" $colour_texture;')

       # Now resize the plane according to this new colour image
       ftn_width = mc.getAttr("popout_material:file2.outSizeX") / 100.0
       ftn_height = mc.getAttr("popout_material:file2.outSizeY") / 100.0
       mc.select("pPlane1")
       mc.setAttr("pPlane1.scaleX", ftn_width)
       mc.setAttr("pPlane1.scaleY", ftn_height)
       
       changeTextFld('colour', filename[0])
      
  
 

def buildUI():
  if mc.window(winName, exists=True):
      mc.deleteUI(winName)
  mc.window(winName, width=winWidth, title='Build a Stereo Visualization')
  mainCL = mc.columnLayout() 

  tmpWidth = [winWidth*0.3, winWidth*0.5, winWidth*0.2]
  mc.rowColumnLayout(nr = 5)

  mc.button('Generate Mesh and Camera Setup', width=winWidth, command="runMEL()")
  mc.rowColumnLayout(nr = 4)

  # Make browser texts
  mc.text( label='Disparity Image Path' )
  mc.text( label='Colour Image Path' )
  mc.text( label='' )
  mc.text( label='' )

  # Make text fields
  disp_field = mc.textField("disparity_field", tx="")
  col_field = mc.textField("colour_field", tx="")
  
  # Make sliders 
  slider = mc.floatSliderGrp(label='Displacement Height', field=True, minValue=0.0, maxValue=1.0, value=0)
  circle_slider = mc.floatSliderGrp(label='Camera Zoom Out', field=True, minValue=0.0, maxValue=20.0, value=9)

  # Change the displacement height using slider input
  def changeDispHeight(*_):
    displacement_height = mc.floatSliderGrp(slider, q=True, v=True)
    print("aaa")
    print(displacement_height)
    mc.setAttr("pPlaneShape1.aiDispHeight", displacement_height)

  # Change the zoom of the camera
  def changeCircleDim(*_):
      circle_scale = mc.floatSliderGrp(circle_slider, q=True, v=True)
      print("aaa")
      print(circle_scale)
      mc.setAttr("nurbsCircle1.scaleX", circle_scale)
      mc.setAttr("nurbsCircle1.scaleZ", circle_scale)
  
  # File browser buttons
  mc.button( label='Browse File', command="chooseFile('disparity')" )
  mc.button( label='Browse File', command="chooseFile('colour')" )
  
  # Update using slider values
  b = mc.button('Update Height')
  mc.button(b, e=True, c=changeDispHeight)
  circle_b = mc.button('Update Zoom')    
  mc.button(circle_b, e=True, c=changeCircleDim)

  mc.showWindow(winName)
  mc.window(winName, e=True, width=winWidth, height=1)
  return
buildUI()
