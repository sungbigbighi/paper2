from PIL import Image
import numpy as np
import random 
import cv2
import numpy
import math

def PSNR(img11, img22):
    mse = np.mean((img11 - img22)** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

## -------------------------------------


EC=0

img = Image.open("lena.bmp")
img_np= np.array(img)
imgMSB = img.copy()
imgLSB = img.copy()


# n=2 n=3 n=4
def zeroPadding(pixel_in_binary):
    pixel_in_binary = pixel_in_binary[2:]
    
    length_of_binary=len(pixel_in_binary)

    if length_of_binary !=8:
        zero_to_be_padded = 8-length_of_binary
        padded_binary= zero_to_be_padded*"0" + pixel_in_binary
    else:
        padded_binary = pixel_in_binary

    return padded_binary


def zeroPadding_4_digit(pixel_in_binary):
    pixel_in_binary = pixel_in_binary[2:]
    
    length_of_binary=len(pixel_in_binary)

    if length_of_binary <4:
        zero_to_be_padded = 4-length_of_binary
        padded_binary= zero_to_be_padded*"0" + pixel_in_binary
    else:
        padded_binary = pixel_in_binary

    return padded_binary

def zeroPadding_5_digit(pixel_in_binary):
    pixel_in_binary = pixel_in_binary[2:]
    
    length_of_binary=len(pixel_in_binary)

    if length_of_binary <5:
        zero_to_be_padded = 5-length_of_binary
        padded_binary= zero_to_be_padded*"0" + pixel_in_binary
    else:
        padded_binary = pixel_in_binary

    return padded_binary

for i in range(0,512,1):
    for j in range(0,512,1):
        
        #取LSB
        pixel = img.getpixel((i,j))
        padded_pixel = zeroPadding(str(bin(pixel)))


        MSB = padded_pixel[0:4]
        LSB = padded_pixel[4:] ##n=3

        MSB_to_dec = int(MSB,2)
        LSB_to_dec = int(LSB,2)

        imgLSB.putpixel((i,j),LSB_to_dec)
        imgMSB.putpixel((i,j),MSB_to_dec)


# for i in range(512):
#     for j in range(512):
#         print(imgLSB.getpixel((i,j)))

imgLSB.save("LSB_image.bmp")
imgMSB.save("MSB_image.bmp")

imgLSB_np = np.array(imgLSB)
imgMSB_np = np.array(imgMSB)



pred_img_LSB = imgLSB.copy()
pred_img_LSB_np=np.array(pred_img_LSB)


pred_img_MSB = imgMSB.copy()
pred_img_MSB_np=np.array(pred_img_MSB)

stego_img_MSB = imgMSB.copy()
stego_img_LSB =imgLSB.copy()

stego_merged_image =img.copy()

# ## LSB image Prediction
for i in range(0,512,1):
    for j in range(0,512,1):        
        if(i==0 and j==0):#左上右下角落/2
            pred_img_LSB_np[i,j]=int((imgLSB_np[i+1,j]+imgLSB_np[i,j+1])/2)
        elif(i==511 and j==511):
            pred_img_LSB_np[i,j]=int((imgLSB_np[i-1,j]+imgLSB_np[i,j-1])/2)
        elif(i%2==0 and i<511 and j==0):#左黑白
            pred_img_LSB_np[i,0]=int((imgLSB_np[i-1,0]+imgLSB_np[i+1,0]+imgLSB_np[i,1])/3)
        elif(i%2==1 and i<511 and j==511):#右黑白
            pred_img_LSB_np[i,511]=int((imgLSB_np[i-1,511]+imgLSB_np[i+1,511]+imgLSB_np[i,510])/3)
        elif(i==0 and j%2==0 and j<511):#上黑白
            pred_img_LSB_np[0,j]=int((imgLSB_np[0,j-1]+imgLSB_np[0,j+1]+imgLSB_np[1,j])/3)
        elif(i==511 and j%2==1 and j<511):#下黑白
            pred_img_LSB_np[511,j]=int((imgLSB_np[511,j-1]+imgLSB_np[511,j+1]+imgLSB_np[510,j])/3)
        elif(i%2==1 and j%2==1 and 0<i<511 and 0<j<511):
            neighbor=[(imgLSB_np[i-1,j]),(imgLSB_np[i,j-1]),(imgLSB_np[i+1,j]),(imgLSB_np[i,j+1])]#鄰近四個邊
            pred_img_LSB_np[i,j]=int((int((neighbor[0])+(int(neighbor[1]))+(int(neighbor[2])+(int(neighbor[3]))))/4))#取小排序
        elif(i%2==0 and j%2==0 and 0<i<511 and 0<j<511):
            neighbor=[(imgLSB_np[i-1,j]),(imgLSB_np[i,j-1]),(imgLSB_np[i+1,j]),(imgLSB_np[i,j+1])]#鄰近四個邊
            pred_img_LSB_np[i,j]=int((int((neighbor[0])+(int(neighbor[1]))+(int(neighbor[2])+(int(neighbor[3]))))/4))#取小排序


pred_img_LSB = Image.fromarray(pred_img_LSB_np)
pred_img_LSB.save("pred_LSB.bmp")

# MSB image Prediction (黑旗)
for i in range(0,512,1):
    for j in range(0,512,1):        
        if(i==0 and j==0):#左上右下角落/2
            pred_img_MSB_np[i,j]=int((imgMSB_np[i+1,j]+imgMSB_np[i,j+1])/2)
        elif(i==511 and j==511):
            pred_img_MSB_np[i,j]=int((imgMSB_np[i-1,j]+imgMSB_np[i,j-1])/2)
        elif(i%2==0 and i<511 and j==0):#左黑白
            pred_img_MSB_np[i,0]=int((imgMSB_np[i-1,0]+imgMSB_np[i+1,0]+imgMSB_np[i,1])/3)
        elif(i%2==1 and i<511 and j==511):#右黑白
            pred_img_MSB_np[i,511]=int((imgMSB_np[i-1,511]+imgMSB_np[i+1,511]+imgMSB_np[i,510])/3)
        elif(i==0 and j%2==0 and j<511):#上黑白
            pred_img_MSB_np[0,j]=int((imgMSB_np[0,j-1]+imgMSB_np[0,j+1]+imgMSB_np[1,j])/3)
        elif(i==511 and j%2==1 and j<511):#下黑白
            pred_img_MSB_np[511,j]=int((imgMSB_np[511,j-1]+imgMSB_np[511,j+1]+imgMSB_np[510,j])/3)
        elif(i%2==1 and j%2==1 and 0<i<511 and 0<j<511):
            neighbor=[(imgMSB_np[i-1,j]),(imgMSB_np[i,j-1]),(imgMSB_np[i+1,j]),(imgMSB_np[i,j+1])]#鄰近四個邊
            pred_img_MSB_np[i,j]=int((int((neighbor[0])+(int(neighbor[1]))+(int(neighbor[2])+(int(neighbor[3]))))/4))#取小排序
        elif(i%2==0 and j%2==0 and 0<i<511 and 0<j<511):
            neighbor=[(imgMSB_np[i-1,j]),(imgMSB_np[i,j-1]),(imgMSB_np[i+1,j]),(imgMSB_np[i,j+1])]#鄰近四個邊
            pred_img_MSB_np[i,j]=int((int((neighbor[0])+(int(neighbor[1]))+(int(neighbor[2])+(int(neighbor[3]))))/4))#取小排序



pred_img_MSB = Image.fromarray(pred_img_MSB_np)
pred_img_MSB.save("pred_MSB.bmp")

## ---------------------------------
## 遍歷黑棋位置 - MSB

for y in range(512):
    for x in range(512):
        if y % 2 == 0 and x % 2 ==0:
            if x!=0 and y!=0 and x!=511 and y!=511:
                ##Center pixels

                up_pixel = imgMSB.getpixel((x,y-1))
                down_pixel = imgMSB.getpixel((x,y+1))
                left_pixel = imgMSB.getpixel((x-1,y))
                right_pixel = imgMSB.getpixel((x+1,y))
                Pred=math.floor((up_pixel+down_pixel+left_pixel+right_pixel)/4)
                

                pred_img_MSB.putpixel((x,y),Pred)
        elif y % 2 == 1 and x % 2 ==1:
            if x!=0 and y!=0 and x!=511 and y!=511:
                ##Center pixels

                up_pixel = imgMSB.getpixel((x,y-1))
                down_pixel = imgMSB.getpixel((x,y+1))
                left_pixel = imgMSB.getpixel((x-1,y))
                right_pixel = imgMSB.getpixel((x+1,y))
                Pred=math.floor((up_pixel+down_pixel+left_pixel+right_pixel)/4)
                

                pred_img_MSB.putpixel((x,y),Pred)



pred_img_MSB.save("testpred_msb_.bmp")
## ---------------MSB Embedding 黑旗

# Pred_image_process
for y in range(512):
    for x in range(512):
        if y % 2 == 0 and x % 2 ==0:
            if x!=0 and y!=0 and x!=511 and y!=511:
                original_pixel = imgMSB.getpixel((x,y))
                pred_pixel = pred_img_MSB.getpixel((x,y))
                pred_error = original_pixel - pred_pixel

                if pred_error == 0 and original_pixel!=0: #embed
                    k=random.randint(0,1)
                    stego_pixel = original_pixel - k
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                    EC+=1
                elif pred_error < 0 and original_pixel!=0:
                    stego_pixel = original_pixel - 1
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                    
                elif pred_error > 0 and original_pixel!=0:
                    stego_pixel = original_pixel
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                

                

        elif y % 2 == 1 and x % 2 ==1:
            if x!=0 and y!=0 and x!=511 and y!=511:
                original_pixel = imgMSB.getpixel((x,y))
                pred_pixel = pred_img_MSB.getpixel((x,y))

                pred_error = original_pixel - pred_pixel

                if pred_error == 0 and original_pixel!=0: #embed
                    k=random.randint(0,1)
                    stego_pixel = original_pixel - k
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                    EC+=1
                    
                elif pred_error < 0 and original_pixel!=0:
                    stego_pixel = original_pixel - 1
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                    
                elif pred_error > 0 and original_pixel!=0:
                    stego_pixel = original_pixel
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                

stego_img_MSB.save("MSB_Stego.bmp")
## ------------------------------------------------------------------------
print("黑旗MSB，EC=",EC)

## 遍歷黑旗 LSB
for y in range(512):
    for x in range(512):
        if y % 2 == 0 and x % 2 ==0:
            if x!=0 and y!=0 and x!=511 and y!=511:
                ##Center pixels

                up_pixel = imgLSB.getpixel((x,y-1))
                down_pixel = imgLSB.getpixel((x,y+1))
                left_pixel = imgLSB.getpixel((x-1,y))
                right_pixel = imgLSB.getpixel((x+1,y))
                Pred=math.floor((up_pixel+down_pixel+left_pixel+right_pixel)/4)
                

                pred_img_LSB.putpixel((x,y),Pred)
        elif y % 2 == 1 and x % 2 ==1:
            if x!=0 and y!=0 and x!=511 and y!=511:
                ##Center pixels

                up_pixel = imgLSB.getpixel((x,y-1))
                down_pixel = imgLSB.getpixel((x,y+1))
                left_pixel = imgLSB.getpixel((x-1,y))
                right_pixel = imgLSB.getpixel((x+1,y))
                Pred=math.floor((up_pixel+down_pixel+left_pixel+right_pixel)/4)
                
                pred_img_LSB.putpixel((x,y),Pred)

pred_img_LSB.save("testpred_lsb_.bmp")

#-------------------------------------------------------------
#LSB embedding 黑旗

for y in range(512):
    for x in range(512):
        if y % 2 == 0 and x % 2 ==0:
            if x!=0 and y!=0 and x!=511 and y!=511:
                original_pixel = imgLSB.getpixel((x,y))
                pred_pixel = pred_img_LSB.getpixel((x,y))
                pred_error = original_pixel - pred_pixel

                if pred_error == 0 and original_pixel!=15: #embed
                    k=random.randint(0,1)
                    stego_pixel = original_pixel + k
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                    EC+=1
                elif pred_error > 0 and original_pixel!=15:
                    stego_pixel = original_pixel + 1
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                    
                elif pred_error < 0 and original_pixel!=15:
                    stego_pixel = original_pixel
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                

        elif y % 2 == 1 and x % 2 ==1:
            if x!=0 and y!=0 and x!=511 and y!=511:
                original_pixel = imgLSB.getpixel((x,y))
                pred_pixel = pred_img_LSB.getpixel((x,y))

                pred_error = original_pixel - pred_pixel

                if pred_error == 0 and original_pixel!=15: #embed
                    k=random.randint(0,1)
                    stego_pixel = original_pixel + k
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                    EC+=1
                    
                elif pred_error > 0 and original_pixel!=15:
                    stego_pixel = original_pixel + 1
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                    
                elif pred_error < 0 and original_pixel!=15:
                    stego_pixel = original_pixel
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                

stego_img_LSB.save("LSB_Stego.bmp")
print("黑旗LSB，EC=",EC)
#-----------------------------------------MSB白旗--------------
#MSB白旗

for y in range(512):
    for x in range(512):
        if y % 2 == 0 and x % 2 ==1:
            if x!=0 and y!=0 and x!=511 and y!=511:
                ##Center pixels

                up_pixel = stego_img_MSB.getpixel((x,y-1))
                down_pixel = stego_img_MSB.getpixel((x,y+1))
                left_pixel = stego_img_MSB.getpixel((x-1,y))
                right_pixel = stego_img_MSB.getpixel((x+1,y))
                Pred=math.floor((up_pixel+down_pixel+left_pixel+right_pixel)/4)
                

                pred_img_MSB.putpixel((x,y),Pred)
        elif y % 2 == 1 and x % 2 ==0:
            if x!=0 and y!=0 and x!=511 and y!=511:
                ##Center pixels

                up_pixel = stego_img_MSB.getpixel((x,y-1))
                down_pixel = stego_img_MSB.getpixel((x,y+1))
                left_pixel = stego_img_MSB.getpixel((x-1,y))
                right_pixel = stego_img_MSB.getpixel((x+1,y))
                Pred=math.floor((up_pixel+down_pixel+left_pixel+right_pixel)/4)
                

                pred_img_MSB.putpixel((x,y),Pred)

pred_img_MSB.save("testpred_msb_white.bmp")

#---------------MSB白旗 embedding
# Pred_image_process
for y in range(512):
    for x in range(512):
        if y % 2 == 0 and x % 2 ==1:
            if x!=0 and y!=0 and x!=511 and y!=511:
                original_pixel = stego_img_MSB.getpixel((x,y))
                pred_pixel = pred_img_MSB.getpixel((x,y))
                pred_error = original_pixel - pred_pixel

                if pred_error == 1 and original_pixel!=15: #embed
                    k=random.randint(0,1)
                    stego_pixel = original_pixel + k
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                    EC+=1
                elif pred_error > 1 and original_pixel!=15:
                    stego_pixel = original_pixel + 1
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                    
                elif pred_error <1 and original_pixel!=15:
                    stego_pixel = original_pixel
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                

        elif y % 2 == 1 and x % 2 ==0:
            if x!=0 and y!=0 and x!=511 and y!=511:
                original_pixel = stego_img_MSB.getpixel((x,y))
                pred_pixel = pred_img_MSB.getpixel((x,y))

                pred_error = original_pixel - pred_pixel

                if pred_error == 1 and original_pixel!=15: #embed
                    k=random.randint(0,1)
                    stego_pixel = original_pixel + k
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                    EC+=1
                    
                elif pred_error > 1 and original_pixel!=15:
                    stego_pixel = original_pixel + 1
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                    
                elif pred_error < 1 and original_pixel!=15:
                    stego_pixel = original_pixel
                    stego_img_MSB.putpixel((x,y),stego_pixel)
                

stego_img_MSB.save("MSB_Stego_white.bmp")
## ------------------------------------------------------------------------
print("白旗MSB，EC=",EC)

## LSB 白旗----------------------------------------------------------------
for y in range(512):
    for x in range(512):
        if y % 2 == 0 and x % 2 ==1:
            if x!=0 and y!=0 and x!=511 and y!=511:
                ##Center pixels

                up_pixel = stego_img_LSB.getpixel((x,y-1))
                down_pixel = stego_img_LSB.getpixel((x,y+1))
                left_pixel = stego_img_LSB.getpixel((x-1,y))
                right_pixel = stego_img_LSB.getpixel((x+1,y))
                Pred=math.floor(up_pixel+down_pixel+left_pixel+right_pixel)
                

                pred_img_LSB.putpixel((x,y),Pred)
        elif y % 2 == 1 and x % 2 ==0:
            if x!=0 and y!=0 and x!=511 and y!=511:
                ##Center pixels

                up_pixel = stego_img_LSB.getpixel((x,y-1))
                down_pixel = stego_img_LSB.getpixel((x,y+1))
                left_pixel = stego_img_LSB.getpixel((x-1,y))
                right_pixel = stego_img_LSB.getpixel((x+1,y))
                Pred=math.floor(up_pixel+down_pixel+left_pixel+right_pixel)
                
                pred_img_LSB.putpixel((x,y),Pred)

pred_img_LSB.save("testpred_lsb_white.bmp")

#-------------------------------LSB embedding 白旗------------------------

#LSB embedding 黑旗

for y in range(512):
    for x in range(512):
        if y % 2 == 0 and x % 2 ==1:
            if x!=0 and y!=0 and x!=511 and y!=511:
                original_pixel = stego_img_LSB.getpixel((x,y))
                pred_pixel = pred_img_LSB.getpixel((x,y))
                pred_error = original_pixel - pred_pixel

                if pred_error == 0 and original_pixel!=0: #embed
                    k=random.randint(0,1)
                    stego_pixel = original_pixel - k
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                    EC+=1
                elif pred_error < 0 and original_pixel!=0:
                    stego_pixel = original_pixel -1
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                    
                elif pred_error > 0 and original_pixel!=0:
                    stego_pixel = original_pixel
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                

        elif y % 2 == 1 and x % 2 ==0:
            if x!=0 and y!=0 and x!=511 and y!=511:
                original_pixel = stego_img_LSB.getpixel((x,y))
                pred_pixel = pred_img_LSB.getpixel((x,y))

                pred_error = original_pixel - pred_pixel

                if pred_error == 0 and original_pixel!=0: #embed
                    k=random.randint(0,1)
                    stego_pixel = original_pixel - k
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                    EC+=1
                    
                elif pred_error < 0 and original_pixel!=0:
                    stego_pixel = original_pixel - 1
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                    
                elif pred_error > 0 and original_pixel!=0:
                    stego_pixel = original_pixel
                    stego_img_LSB.putpixel((x,y),stego_pixel)
                

stego_img_LSB.save("LSB_Stego_white.bmp")

#-------------------合併---------------------------

for y in range(512):
    for x in range(512):
        if x!=0 and y!=0 and x!=511 and y!=511:
            LSB_part=stego_img_LSB.getpixel((x,y))
            MSB_part=stego_img_MSB.getpixel((x,y))

            bin_LSB=bin(LSB_part)
            bin_MSB=bin(MSB_part)

            padded_LSB = zeroPadding_4_digit(bin_LSB)
            padded_MSB = zeroPadding_4_digit(bin_MSB)

  
            
            merged_pixel_in_binary = padded_MSB+padded_LSB
            # print(merged_pixel_in_binary)

            merged_pixel_in_decimal= int(merged_pixel_in_binary,2)
            # print(merged_pixel_in_decimal)

            stego_merged_image.putpixel((x,y),merged_pixel_in_decimal)


stego_merged_image.save("final_stego.bmp")

img11_array = np.array(img11)
stego_merged_image_array = np.array(stego_merged_image)
print("白旗LSB，EC=",EC)
print("The PSNR between image1 and image2 is: %.3f" % PSNR(img_np,stego_merged_image_array))



