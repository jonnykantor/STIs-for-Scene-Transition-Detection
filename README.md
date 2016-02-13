Author: Jonathan Kantor  
For: CMPT 365 (Multimedia) - Simon Fraser University  
Date: Nov 27, 2014  

## Spatiotemporal Image Creation for Scene Transition Detection in Video
---
Language used: Python version 2.7 (available in CSIL)

#####Libraries used:
*	NumPy 1.9.1 64 bit for Windows (http://sourceforge.net/projects/numpy/files/NumPy/)
*	OpenCV 2.4.9 64 bit for Windows (http://opencv.org/downloads.html)
*	Tkinter
*	Math
*	tkMessageBox
*	tkFileDialog
*	PILlow 2.6.1 64 bit for Windows (https://pypi.python.org/pypi/Pillow/2.6.1)

As a brief forward, I attempted to put together a working standalone executable for this using py2exe (http://www.py2exe.org/) however, probably due to my inexperience with setup scripts, or something with respect to my specific system, while the executable works and displays the GUI properly, some key functions of OpenCV (mainly capturing video from files) doesn’t appear to work properly (that is, the video-capture will not start). However the source files, whether run from the IDLE IDE or the console, work flawlessly provided all the necessary libraries (listed above, with URLs where necessary) are installed.
Now then, on to the documentation;

#####General function:  
When started, the application should provide a simple GUI implementing the Tkinter module’s buttons/labels in a small window – The top button reads “Choose Video”, the middle button reads “STI via Histogram Intersection” (part 2 of the assignment), and the bottom button reads “STI via copying pixels” (part 1 of the assignment). A text label below this reads “Choose rows or columns for computation” followed by two radio buttons, one of which reads “Rows”, and the other “Columns”; the default activation for the buttons is Rows. See figure 1 below.
Naturally both parts one and two of the assignment require a video to proceed, so clicking on either STI button before having chosen a video will result in the error message in figure 2, below, but will not end the program – merely prompting the user to actually go ahead and select a video.
Upon clicking the “Choose Video” button, a File read dialog box will open, from which the user can browse to, and select a video – the default file choices are *.mp4, *.mpg, and *.avi – although there is also a *.* choice, and the user can technically select whatever file they like – though non-video files will result in a (non-fatal) error. See the file dialog box below in figure 3.

![Figure 1, the starting GUI before any actions have been taken on it](https://raw.githubusercontent.com/jonnykantor/Images-and-Screengrabs/master/STI_Project_screenshots/Screen_1_Gui_Layout.png)  
######<sub>Figure 1, the starting GUI before any actions have been taken on it  </sub>

![Figure 2, warning the user that should they fail to select a video, they will be trapped forever](https://raw.githubusercontent.com/jonnykantor/Images-and-Screengrabs/master/STI_Project_screenshots/Screen_2_NoVideo_Error.png)  
######<sub>Figure 2, warning the user that should they fail to select a video, they will be trapped forever</sub>

![Figure 3, a prime example of a read only File dialog box in its natural habitat](https://raw.githubusercontent.com/jonnykantor/Images-and-Screengrabs/master/STI_Project_screenshots/Screen_3_OFD.png)  
######<sub>Figure 3, a prime example of a read only File dialog box in its natural habitat</sub>  

At any point prior to choosing one of the two STI functions (once a video file has been selected) the user can change the radio button from rows to columns or vice-versa. Once a video file is selected, the user may choose either STI button, or neither and simply exit the program, but that’s no fun, so on to what those do. Choosing an STI button will fire that function off, and the user will not be able to interact with the GUI at all until the function is complete.

#####Part 1: STI through copying pixels

After loading the video file, two new windows will open: In one, the video (resized to 32x32) will play at a standard rate of about 30fps, while in the other, the central columns/rows (depending on user choice) will begin to accrue gradually in a new image (the STI). Once the video has finished playing both windows will close, and a transposed copy of the finished composite image from the second window will display in the original GUI underneath a Label saying “STI”, which is itself underneath where the radio buttons are located. See figure’s 4, 5 below. As to how this all works, the function takes each frame, and places the pixels of each row/column into a 3 dimensional array (time x column/row x pixel), and then creates a new frame at the same time from the 3 dimensional array at that time. At the end of the run the array is transposed (turned sideways) so that rows/columns -> columns making ‘time’ the x axis.  

![Figure 4: The three windows (and the python shell in the background) half way through processing a short video](https://raw.githubusercontent.com/jonnykantor/Images-and-Screengrabs/master/STI_Project_screenshots/Screen_4_Pixel_in_progress.png)  
######<sub>Figure 4: The three windows (and the python shell in the background) half way through processing a short video</sub>  

![Figure 5, the final product of part 1, a row-based STI!](https://raw.githubusercontent.com/jonnykantor/Images-and-Screengrabs/master/STI_Project_screenshots/Screen_5_Pixel_finished.png)  
######<sub>Figure 5, the final product of part 1, a row-based STI!</sub>  

It seems fairly straightforward to see a general area of scene transition, although there is obviously a lot of noise (the above image has a quick left->right wipe happening about half-way through the (roughly) 4-second video, but even though colors are quite different between the two, the exact point of change is difficult to see.

#####Part 2: STI through histogram intersection

If the user were to choose the second button, “STI vi Histogram Intersection” they would not be treated by any new windows, but a new text-label that simply says “Computing, please wait…” where “STI” is in figure 5. This is largely because the function openVid is, like the comparePixel function, working frame by frame through the video. – however, in order to create a full histogram, we need to process every column/row of the image over time, not just one column, and as such we cannot display even one full histogram until the entire video has been processed. So what the user sees is a ‘loading’ message, followed by two STI’s being presented where the one STI in figure 5 is: A sample frame showing the shift to chromaticity taken from either the center row/column in a similar manner to part 1, where all the pixel values have been changed to {r, g, b} = ({r, g, b}/(r+g+b))*255 (with care taken to correctly type the various operations so we don’t just end up with a whole bunch of needless zeroes), unless r+g+b = 0 in which case {r, g, b} is just set to {0}. See figure 6 below for an example on the same video taken by rows.
The histogram intersection STI does not look especially more intuitive here, in fact it looks worse! However, this seems to be a result of the video being very small, of poor quality, and the cut being very fast; also, color noise across the video seems to have resulted in a difficult to detect transition, especially in the right half of the image. Using a clearer video with less sudden movement and a slower transition might work.

![Figure 6, a histogram intersection STI with an example chromaticity converted image above it](https://raw.githubusercontent.com/jonnykantor/Images-and-Screengrabs/master/STI_Project_screenshots/Screen_6_HIST_finished.png)  
######<sub>Figure 6, a histogram intersection STI with an example chromaticity converted image above it</sub>  
