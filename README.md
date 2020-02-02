## Welcome to Visualizing Stereo Pairs!
This originated as a final solo project for the CSC420 Computer Vision course at the University of Toronto, and further extended as a personal project.

The first part of this project deals with creating anaglyph composites OR creating a grayscale displarity map (similar to a depth map) from a stereo image pair.
The second part of this project deals with automatically generating a model using displacement mapping on a mesh. This includes a Maya UI component that allows the user to select their desired colour texture and displacement map, and controls to handle the strength of displacment of the mesh, as well as camera zoom.

Enjoy!

## Usage - Generating Anaglyph and Disparity Images
- All of the code can be run using `main.py`
- Browse for available images in `/image_pairs.` You can add your own left and right images by specifying `MyImage_left.jpg` and `MyImage_right.jpg`
- The first argument for running main.py is the image name prefix, followed by a number.
- The number can be only `1` or `2`, where `1` indicates running the Anaglyph generation code, and `2` runs the Disparity Map Generation. 
- Example: `python main.py veronica 1` will run Anaglyph code for the `veronica_left` and `veronica_right` image pair.
- Example: `python main.py foot 2` will run Stereo Disparity code for the `foot_left` and `foot_right` image pair. There are more prompts following this initial command, that ask to run the Middlebury evaluation vs. StereoBM computation, and the Gaussian kernel size. 
- Example for your own images: If image pair is `MyImage_left.jpg` and `MyImage_right.jpg`, then the command will be `python main.py MyImage 1` for Anaglyph Generation or `python main.py MyImage 2` for Stereo Disparity generation. 

## Usage - Maya Scripting and UI
- The two main scripts are `create_stereoUI.py` and `create_stereo_model.mel`. 
- `create_stereoUI.py` generates a UI that allows the user to make the apparatus from scratch, which includes making a plane, attaching an external material (`popout_material.mb`) setting up a camera attached to a circle that orbits around the plane mesh. Users can also upload their own disparity/displacement maps and colour textures!

- ***IMPORTANT! If you choose to run these scripts, move these two scripts to the Maya `/scripts` directory of your computer. In `create_stereoUI.py`, change the following mel.eval line to include the directory of your `create_stereo_model.mel` script!***

```python
def runMEL():
    print("Running Stereo Generation Script")
    # Replace this line with the absolute path of wherever you put the create_stereo_model.mel script!!!!!
    mel.eval('source "/Users/royashams/Documents/maya/projects/default/scripts/create_stereo_model.mel";')
```

## Directory Structure
- All image pairs are in /image_pairs. This includes the original left and right images for "veronica", "fountain", "foot", and "nike"
- Outputted anaglyph images are in /Anaglyphs
- Drawn matches for Technique 1 (Anaglyphs) are listed in /Matched
- Plain rectified image pairs are in /Rectified
- /MiddleburyDisparity contains original noisy disparity map from the Middlebury 3 Evaluation
- /StereoBM_Disparity contains original noisy disparity map from SteroBM OpenCV function
- All images with a Gaussian blur are under /Blurred

## Important Notes
- Before running the Middlebury Evaluation, make sure that `imagemagick` is installed. 
- The Gaussian kernel size in option 2 must be an odd number. Larger numbers work better for noisier images. 
- The code (main.py) automatically generates all outputted images in this assignment. The 3D models were manually created using Blender.
