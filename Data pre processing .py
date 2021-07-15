#!/usr/bin/env python
# coding: utf-8

# In[ ]:


mypath="Desktop/mammo data/manifest-1616439774456/CMMD"


# In[ ]:


import os as os
from os import listdir
from os import walk


# In[ ]:


file_list=[]
for root, dirs, files in os.walk(mypath,topdown=False):
    for file in files:
        if file.endswith('.dcm'):
            file_list.append(os.path.join(root, file))


# In[ ]:


file_list


# In[ ]:


parent="Desktop" # making a new directory
k=os.path.join(parent,"Dicom_mammo")
os.mkdir(k)
os.mkdir(Desktop/mammo_final_JPEG)


# In[ ]:


import shutil
import re # for regex 
for name in file_list:
    first_part = re.search(r"D[0-9]?-[0-9]+",name).group() # extract initial part of intended filename
    second_part= name[-7:] # extract the second part of intended file name
    new_name=first_part+"_"+second_part # synthesise new name
    shutil.copy(src=name,dst="Desktop/Dicom_mammo") # Copying the .dcm files to the new folder
    os.rename(src="Desktop/Dicom_mammo"+ "/" + second_part, # renaming the files to avoid duplication
             dst="Desktop/Dicom_mammo/"+ new_name)
    


# In[ ]:


import pydicom as dicom
import os
import cv2
import PIL # optional
# make it True if you want in PNG format
PNG = False
# Specify the .dcm folder path
folder_path = "Desktop/Dicom_mammo"
# Specify the output jpg/png folder path
jpg_folder_path = "Desktop/mammo_final_JPEG"

images_path = os.listdir(folder_path)
for n, image in enumerate(images_path):
    if image==".ipynb_checkpoints":
        continue
    ds = dicom.dcmread(os.path.join(folder_path, image))
    pixel_array_numpy = ds.pixel_array
    if PNG == False:
     image = image.replace('.dcm', '.jpg')
    else:
     image = image.replace('.dcm', '.png')
    cv2.imwrite(os.path.join(jpg_folder_path, image), pixel_array_numpy)
    if n % 50 == 0:
        print('{} image converted'.format(n))


# In[ ]:


os.listdir("Desktop/mammo_final_JPEG")


# In[ ]:


import pandas as pd


# In[ ]:


JPEG_file=pd.DataFrame({"Filename":[i for i in os.listdir("Desktop/mammo_final_JPEG")]})


# In[ ]:


JPEG_file.index +=1


# In[ ]:


JPEG_file['Patient_Id']=[i[:7] for i in os.listdir("Desktop/mammo_final_JPEG")]


# In[ ]:


JPEG_file.index


# In[ ]:


JPEG_file.to_csv(path_or_buf="Desktop/mammo data/Filenames.csv")


# In[ ]:


original_data=pd.read_csv("Desktop/mammo data/CMMD_clinicaldata_revision.csv")


# In[ ]:


original_data=pd.DataFrame(original_data)


# In[ ]:


original_data.rename(columns={'ID1':'Patient_Id'},inplace=True)


# In[ ]:


original_data.columns


# In[ ]:


original_data.columns[0]


# In[ ]:


original_data.to_csv("Desktop/mammo data/original_data.csv")


# In[ ]:


JPEG_file.columns


# In[ ]:


import numpy as np
JPEG_file['Exam_laterality']= np.where(JPEG_file['Filename'].str[-5:].isin (["3.jpg","4.jpg"]),"Bilateral","Unilateral")


# In[ ]:


Bi=JPEG_file.loc[JPEG_file["Exam_laterality"]=="Bilateral"]


# In[ ]:


Bi_IDs= Bi['Patient_Id'].unique().tolist()


# In[ ]:


len(Bi_IDs)


# In[ ]:


JPEG_file['Exam_laterality']= np.where(JPEG_file['Patient_Id'].isin (Bi_IDs),"Bilateral","Unilateral")


# In[ ]:


Bi=JPEG_file.loc[JPEG_file["Exam_laterality"]=="Bilateral"]


# In[ ]:


Uni=JPEG_file.loc[JPEG_file["Exam_laterality"]!="Bilateral"]


# In[ ]:


Uni=pd.merge(Uni,original_data,how="left")


# In[ ]:


Bi


# In[ ]:


Bi['LeftRight']=np.where(Bi['Filename'].str[-5:].isin(["3.jpg","4.jpg"]),"R","L")


# In[ ]:


Bi=pd.merge(Bi,original_data,"left")


# In[ ]:


Bi


# In[ ]:


Uni


# In[ ]:


final_JPEG_data=pd.concat([Uni,Bi],axis=0)


# In[ ]:


final_JPEG_data.to_csv("python_final.csv")


# In[ ]:


# Flipping the images of the right breast
Flip_index= final_JPEG_data.loc[final_JPEG_data["LeftRight"]=="R"]


# In[ ]:


Flip_index.index


# In[ ]:


del(flip_filepaths) # Function to construct file paths to right side images
flip_filepaths=set()
def flip_images_paths (Folder):
 for Filename in Flip_index['Filename']:
    path = os.path.join("mammo_final_JPEG/JPEG_data",Folder,Filename)
    if os.path.isfile(path):
        flip_filepaths.add(path)


# In[ ]:


flip_filepaths


# In[ ]:


flip_images_paths("JPEG_first_part")


# In[ ]:


len(flip_filepaths)


# In[ ]:


flip_images_paths("JPEG_2nd_part")


# In[ ]:


len(flip_filepaths)


# In[ ]:


os.mkdir("flipped images")# make a directory for flipped images


# In[ ]:


flip_filepaths


# In[ ]:


import PIL
from PIL import Image
dest_paths_flipimages= [os.path.join("flipped images",i[-15:]) for i in flip_filepaths]


# In[ ]:


dest_paths_flipimages


# In[401]:


def flip_images (image_path,dest_path):  # defining a function for flipping all right side breast MGs to ensure uniformity 
    for n,path in enumerate (image_path):
        ori_image=Image.open(path)
        mirror_flip=ori_image.transpose(Image.FLIP_LEFT_RIGHT)
        mirror_flip.save(dest_path[n])
        if n % 50 == 0:
         print('{} images flipped'.format(n))
    


# In[402]:


flip_images(flip_filepaths,dest_paths_flipimages)


# In[405]:


ext_image_files=os.listdir("/Volumes/ShashSSD/mammo_final_JPEG/JPEG complete")
ext_image_files= [i for i in ext_image_files if not i.startswith(".")]
ext_image_paths=set(os.path.join("/Volumes/ShashSSD/mammo_final_JPEG/JPEG complete",i) for i in ext_image_files)


# In[443]:


im=Image.open("JPG_test/D1-0003_1-1.jpg")
width,height=im.size
width,height


# In[450]:


# create another directory in External volume
os.mkdir("/Volumes/ShashSSD/mammo_final_JPEG/cropped_images")


# In[451]:


path_save= [os.path.join("/Volumes/ShashSSD/mammo_final_JPEG/cropped_images",i[-15:]) for i in ext_image_paths]


# In[467]:


def crop_images(ext_image_paths,path_save):
    for n,path in enumerate(ext_image_paths):
        im= Image.open(path)
        im2= im.crop((0,0,1532,2294))
        im2.save(path_save[n])
        if n % 50 == 0:
            print(f"{n} pictures cropped")
    


# In[468]:


crop_images(ext_image_paths,path_save)


# In[452]:


dimensions=(1,2,3,4)
dimensions[1]


# In[ ]:




