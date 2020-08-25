# COLMAP_reverse-process
After getting the COLMAP 3D point clouds, reversing the whole COLMAP process getting the 2D point-cloud images

The quat2rotm.py file contains steps 8 and 9, which the results plot easyplot1 to easyplot 108: the results of 
108 images from 3d to 2d
The txt texts can be deleted since these are all been used in the functions.
Notice that there exists 3 points3Dchange for different objects. What we use here is points3Dchange.txt,
which has a large number of points and can therefore cost more calculation. The other two are not as ideal 
as this one given but all these data are provided.
Also, the original images that COLMap takes are contained in the folder named 'original images'. There are 
two files called 'blunder.out' and 'bounder.out.list' in it, with the fused file, we can open and edit the 
dense 3D points cloud in Meshlab if we want to pick the essential object by our own. Also, we can have the 
3D point colors modeled in application named 'blender'. The result after using 'blender' is provided named
'tablewithcube'. Notice that the cube is simply added through 'blender' just for fun. The real cube is added
in the txt files and then tested.
