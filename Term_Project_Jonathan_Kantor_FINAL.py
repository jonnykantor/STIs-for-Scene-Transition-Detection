import numpy as np
import cv2
import math
from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename 
from PIL import Image, ImageTk


#GLOBALS        
root = Tk()
file_name = ['']
v = IntVar()
v.set(0) #initially set to rows
l_t = Label(root, text=None)
l = Label(root, image=None)
l2 = Label(root, image=None)
#END GLOBALS

def chromaticityConversion(in_Arr): #alters an input array's rgb values to chromaticity values - No error checking on this end    

    a = in_Arr #This just assigns a new pointer to the same array, changes to one affect both!
    #a = np.copy(in_Arr) #This creates a copy of the original array, time consuming - don't use unless you need both displayed
    for j in range(len(a)):
        for i in range(len(a[0])):
            r, g, b = a[j][i][0], a[j][i][1], a[j][i][2]
            if(r==0)&(g==0)&(b==0):
                a[j][i][0], a[j][i][1], a[j][i][2] = 0, 0, 0
            else:
                a[j][i][0] = int(round((((a[j][i][0]+0.0)/((r+0)+g+b))*255)))
                a[j][i][1] = int(round((((a[j][i][1]+0.0)/((r+0)+g+b))*255)))
                a[j][i][2] = int(round((((a[j][i][2]+0.0)/((r+0)+g+b))*255)))
    return a
#END chromaticityConversion()

#Written to ease makeHist - returns a pair of flattened nested arrays on the r/g channels for an input column of RGB pixel arrays
def flattenRGArray(in_Arr):
    new_Arr = [[], []]
    for x in range(len(in_Arr)):
        new_Arr[0].append(in_Arr[x][0]) #red channel
        new_Arr[1].append(in_Arr[x][1]) #green channel
    
    new_Arr2 = np.asarray(new_Arr, dtype=np.uint8) #list-to-array
    return new_Arr2
#END flattenRGBArray()

#return a 2D histogram on r/g for an input column array
def makeHist(img_Arr):  
    col = img_Arr 
    forHist = flattenRGArray(col)
    
    bins = int(1 + math.log(len(col), 2)) # number of bins
    c_range = [0, 256, 0, 256] # range for each bin

    hist = cv2.calcHist(forHist, [0, 1], None, [bins, bins], c_range) #make histogram
    
    return hist
#END makeHist()

#input img array, output list of histograms by column
def histList(img_Arr):
    L = []
    D = []
    run = len(img_Arr)
    for i in range(run):
        L.append(makeHist(img_Arr[i]))
    
    return L
#END histList()

#returns a list of histogram intersections for hist i, i+1, where 0<=i<len(list)
def histDifList(hist_list):
    L = []
    run = len(hist_list)
    
    for i in range(run-1): #can't compare the len(L) and len(L+1) list
        L.append(cv2.compareHist(hist_list[i], hist_list[i+1], 2))
    
    return L
#END histDifList()

#THIS FUNCTION HANDLES PART 1 OF THE ASSIGNMENT
def pixelCopy(opc, play, fn):
    isValid = True
    count = 0   
    cap = cv2.VideoCapture(fn[0]) #fn[0] = 'input_file_path'

    if not cap.isOpened():
        print("can't open the file")
        
    if opc == 0:
        row_array_matrix = []
    if opc == 1:
        column_array_matrix = []
        
    #FOR EACH FRAME
    while(True):
        try:
            ret, frame = cap.read()
            if not ret:
                break
        except:
            print("Frame failed to load")
            isValid = False
        
        #resize the image frame by frame to 32x32
        frame = cv2.resize(frame, (32, 32))

        #start filling matrix with central row/column based on input
        if opc == 0: #if Row
            row_array = [frame[16, y] for y in range(32)]
            row_array_matrix.append(row_array)
        elif opc == 1: #if column
            column_array = [frame[y, 16] for y in range(32)]
            column_array_matrix.append(column_array)

        if play == 1:
            
            ###ATTEMPT AT REAL-TIME DISPLAY FRAME BY FRAME###
            if opc == 0:
                frame_row = np.asarray(row_array_matrix, dtype=np.uint8)
                if isValid == True:
                    try:
                        count = count + 1
                        cv2.namedWindow('frame_row', 1)
                        cv2.imshow('frame_row', frame_row)
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                    except:
                        print("STI frame failed to display")
            elif opc == 1:
                frame_column = np.asarray(column_array_matrix, dtype=np.uint8)
                if isValid == True:
                    try:
                        count = count + 1
                        cv2.namedWindow('frame_column', 1)
                        cv2.imshow('frame_column', frame_column)
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                    except:
                        print("STI frame failed to display")
            
            
            ###DISPLAY VIDEO HERE, NOT NECESSARY FOR FILLING MATRIX, MAY WANT TO IMPLEMENT ANYWAY###
            
            if isValid == True: #DISPLAY FRAME
                try:
                    cv2.namedWindow('frame', 1)
                    #cv2.moveWindow('frame', 1000, 400)  #roughly center of screen, not ideal
                    cv2.imshow('frame',frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                except:
                    print("Frame failed to display")
                
    #ATTEMPT AT USING TKIMG
    img = []
    if opc == 0:
        img = Image.fromarray(np.transpose(frame_row, (1, 0, 2)), "RGB")
    elif opc == 1:
        img = Image.fromarray(np.transpose(frame_column, (1, 0, 2)), "RGB")
    
    img2 = ImageTk.PhotoImage(img)
    l_t.configure(text="STI:")
    l.configure(image=img2)
    l2.configure(image=None)
    l.image = img2
    l2.image = None
    l_t.pack()
    l.pack()
    root.update()
    
    #END ATTEMPT AT USING TKIMG
    
    if play == 1:
        cv2.destroyAllWindows()
        
#END pixelCopy
            
#THIS FUNCTION HANDLES THE BULK OF PART 2 OF THE ASSIGNMENT
def openVid(opc, fn):
    l_t.configure(text="Please wait, computing...")
    l_t.pack()
    root.update()
    
    isValid = True
    count = 0   

    cap = cv2.VideoCapture(fn[0]) #fn[0] = 'input_file_path'
    
    if not cap.isOpened():
        print("can't open the file")

    #FOR EACH FRAME
    while(True):
        try:
            ret, frame = cap.read()
            if not ret:
                break
        except:
            print("Frame failed to load")
            isValid = False
        
        #resize the image frame by frame to 32x32
        frame = cv2.resize(frame, (32, 32))

        #setup 4D matrix storing each column of each frame over time
        if count == 0:
            A = [chromaticityConversion([frame[i]]) for i in range(32)]
            count = count + 1
        else:
            for i in range(32):
                A[i].append(frame[i])
    
    #Chromaticity conversion for the rest of the matrix here, major time-sink but what can you do
    #columns to be processed equals (# of frames)*(# of columns) and each column has 32 pixels to
    #be altered in this case. O(n*m)
    
    for i in range(len(A)):
        A[i] = chromaticityConversion(A[i])
        
    columnMat = np.transpose(A, (2, 1, 0, 3)) #create new matrix from row dominant to column dominant
    
    #This block covers making and presenting the transposed chromaticityConverted image made up of
    #the same row/column position over time - given part 1 of the assignment, this is only necessary
    #for 1 image showing the central column/row of the frame
    
    if opc == 0: #ROW
        
        chrom_Mat_Row = np.asarray(A[len(A)/2], dtype=np.uint8) 
        img1 = Image.fromarray(chrom_Mat_Row.transpose(1, 0, 2))
        
    
    elif opc == 1: #COLUMN
        
        chrom_Mat_Column = np.asarray(columnMat[len(columnMat)/2], dtype=np.uint8) 
        img1 = Image.fromarray(chrom_Mat_Column.transpose(1, 0, 2))
        
    

    #Make Histograms for original image, using all columns/rows over time to return
    #a time*(column or row) image, so each histogram will be a 1*time flattened list
    #using histogram intersection
    
    if opc == 0:    #ROW
        final_hist_list = []
        for i in range(len(A)): #range is 32 in this case
            chrom_Mat_Row = np.asarray(A[i], dtype=np.uint8) #SPECIFIC CASE TODO: GENERALIZE
            L = histList(chrom_Mat_Row)
            L2 = histDifList(L)
            final_hist_list.append(L2)
        #cv2.imshow('image', np.asarray(final_hist_list, dtype=np.uint8))
        final_hist_list = np.dot(final_hist_list, (1.0/32))
        final_hist_list = np.dot(final_hist_list, 255)
        img2 = Image.fromarray(np.asarray(final_hist_list, dtype=np.uint8), "L")
        
            
    elif opc == 1:  #COLUMN
        final_hist_list = []
        for i in range(len(A)): #range is 32 in this case
            chrom_Mat_Column = np.asarray(columnMat[0], dtype=np.uint8) #SPECIFIC CASE TODO: GENERALIZE
            L = histList(chrom_Mat_Column)
            L2 = histDifList(L)
            final_hist_list.append(L2)
        final_hist_list = np.dot(final_hist_list, (1.0/32))
        final_hist_list = np.dot(final_hist_list, 255)
        img2 = Image.fromarray(np.asarray(final_hist_list, dtype=np.uint8), "L")

    #ATTEMPT AT USING TKIMG

    
    img3 = ImageTk.PhotoImage(img1)
    img4 = ImageTk.PhotoImage(img2)
    l_t.configure(text="STI, Chromaticity on top:")
    l.configure(image=img3)
    l2.configure(image=img4)
    l.image = img3
    l2.image = img4
    l_t.pack()
    l.pack()
    l2.pack()
    root.update()
    
    #END ATTEMPT AT USING TKIMG
#END openVid()

def callback():
    name= askopenfilename(filetypes=(("Video files", "*.mp4;*.mpg;*.avi"),("All files", "*.*")))
    file_name[0] = name
#END callback()
    
def parse_next(fn, cmd):
    if (fn == []) or (fn[0] == ''):
        showinfo("Warning", "You must select a video using the 'Choose Video' button before choosing a function")
        
    else:
        if cmd == 1: #pixel copying
            pixelCopy(v.get(), 1, fn)
        elif cmd == 2: #histogram intersection
            openVid(v.get(), fn) 
#END parse_next()    

def main():

    root.title("CMPT 365 STI widget by Jonny Kantor")
    compute_choice = [("Rows", 0), ("Columns", 1)]
    
    
    Button(text="Choose Video", width = 60, command=lambda : callback()).pack()
    Button(text="STI via Histogram Intersection", width = 60, command=lambda : parse_next(file_name, 2)).pack()
    Button(text="STI via copying pixels", width = 60, command=lambda : parse_next(file_name, 1)).pack()
    Label(root, text="""Choose rows or columns for computation:""", justify = LEFT, padx = 20).pack()
    for txt, val in compute_choice:
        Radiobutton(root, text=txt, padx = 20, variable=v, value=val).pack()  
    root.mainloop()    
    
if __name__ == '__main__':
  main()
