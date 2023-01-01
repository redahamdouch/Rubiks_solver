
import cv2 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

class Cube:

  def __init__(self,pos_f,pos_d,pos_r,pos_l,pos_u,pos_b):

    self.color_refs={}
    self.dic_faces ={'F':Face(pos_f,self),'D':Face(pos_d,self),'R':Face(pos_r,self),'L':Face(pos_l,self),'U':Face(pos_u,self),'B':Face(pos_b,self)}


  def set_color_ref(self,img,contour,color):
      
      x,y,w,h = cv2.boundingRect(contour) # offsets - with this you get 'mask'
      self.color_refs[color]=list(reversed(np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)))[1:]
  
  def color_to_calibrate(self):
      dic={0:"white",1:"red",2:"green",3:"orange",4:"blue",5:"yellow",6:"Done"}
      return dic[len(self.color_refs)]
  
  def validation(self):
    res = False
    liste = []
    dic={"yellow":"white","orange":"red","blue":"green", "white":"yellow","red":"orange","green":"blue"}
    if dic[self.dic_faces['F'].color_face] == self.dic_faces['B'].color_face:
      if dic[self.dic_faces['R'].color_face] == self.dic_faces['L'].color_face:
        if dic[self.dic_faces['U'].color_face] == self.dic_faces['D'].color_face:
          for  value in self.dic_faces.values():
            liste+=value.colors
            if liste.count("red") == 9 and liste.count("white") == 9 and liste.count("blue") == 9 and liste.count("yellow") == 9 and liste.count("orange") == 9 and liste.count("green") == 9 : 
              res = True
    
    return res


  def to_kociemba(self):
    dic_convert={}
    res=[]
    for key,value in self.dic_faces.items():
      dic_convert[value.color_face]=key
    for x in ["U","R","F","D","L","B"]:
      res+=[dic_convert[y] for y in self.dic_faces[x].colors]
    return res,dic_convert


  def draw_patron(self,frame):
    for key,value in self.dic_faces.items():
      if value.colors!=[]:
        frame=self.draw_face(value.position[0],value.position[1],20,frame,value.colors)
    return frame


  def draw_face(self,pt1,pt2,of,frame,color_of_cubes):
      dic_colors= {"blue" :[0,0,255],"green":[0,255,0],"orange":[237,127,38],"red":[255,0,0],"yellow":[255,255,0],"white":[255,255,255]}
      tab=[(of,of),(0,of),(-of,of),(of,0),(0,0),(-of,0),(of,-of),(0,-of),(-of,-of)]
      for i,x in enumerate(tab):
          cv2.rectangle(frame, (pt1[0]-x[0],pt1[1]-x[1]), (pt2[0]-x[0],pt2[1]-x[1]), tuple(list(reversed(dic_colors[color_of_cubes[i]]))), thickness=10)
      return frame   

  def face_to_reco (self):
    res='Done'
    for key,value in self.dic_faces.items():
      if value.colors ==[]:
        res= key
    return res 
    


      






class Face(Cube):

  colors=[]
  contours=[]
  img =[]
  position=[]
  color_face=''




  def __init__(self,position,Cube):

    self.position=position
    self.Cube=Cube
  
  
    




  def order_contours(self,contours):

    pt_centre = []
    for i in range(len(contours)):
        pt_centre.append(np.mean(contours[i], axis = 0))

    contours = np.array(contours)
    pt_centre = np.array(pt_centre)
    ind_y = pt_centre[:,1].argsort()

    #Peut etre le mettre avant la fonction, jsp
    #contours = np.array(contours)
    contours_sorted_y = contours[ind_y]
    centre_sorted_y = pt_centre[ind_y]


    pt_centre1 = centre_sorted_y[0:3]
    pt_centre2 = centre_sorted_y[3:6]
    pt_centre3 = centre_sorted_y[6:9]

    ligne1 = contours_sorted_y[0:3]
    ligne2 = contours_sorted_y[3:6]
    ligne3 = contours_sorted_y[6:9]

    ind_x1 = pt_centre1[:,0].argsort()
    ind_x2 = pt_centre2[:,0].argsort()
    ind_x3 = pt_centre3[:,0].argsort()

    ligne1 = ligne1[ind_x1].tolist()
    ligne2 = ligne2[ind_x2].tolist()
    ligne3 = ligne3[ind_x3].tolist()
    res = [np.array(x).astype(np.int32) for x in ligne1]
    for x in ligne2:
        res.append(np.array(x).astype(np.int32))
    for x in ligne3:
        res.append(np.array(x).astype(np.int32))
    self.contours=res
    return res



  def set_img_and_contours(self,img,contours):
    self.img =img
    self.contours=self.order_contours(contours)
    average=self.average_color(img,self.contours)
    self.distance_colors(average)
    self.color_face=self.colors[4]


  def average_color(self, img,contours):
    res=[]
    for c in contours:
      x,y,w,h = cv2.boundingRect(c)
      res.append(list(reversed(np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)))[1:])
    return res 



  def distance_colors(self, contours_colors):
    dic_colors=self.Cube.color_refs
    reco_colors=[]
    for contour in contours_colors:
        dist_min=np.inf
        for key,value in dic_colors.items():
            
            color_1 = convert_color(convert_color(sRGBColor(contour[0]/255,contour[1]/255, contour[2]/255), LabColor), LabColor);
            color_2 = convert_color(convert_color(sRGBColor(value[0]/255,value[1]/255,value[2]/255), LabColor), LabColor);
            delta_e = delta_e_cie2000(color_1, color_2)
    
            if delta_e<dist_min:
                dist_min=delta_e
                final_color=key
        reco_colors.append(final_color)
    self.colors=reco_colors


def longueur_square (points):
    tab_long = []
    res = True
    for i in range(len(points)):
        if i <3:
            dist = np.sqrt((points[i+1][0]-points[i][0])**2 + (points[i+1][1]-points[i][1])**2)
        else:
            dist = np.sqrt((points[-1][0]-points[0][0])**2 + (points[-1][1]-points[0][1])**2)
        if dist < 70 or dist > 100:
            res = False

    return res

def angle_cos(p0, p1, p2):
    import numpy as np

    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def detection(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_img = np.float32(gray_img)
    blurred = cv2.GaussianBlur(gray_img, (3, 3), 0)
    canny = cv2.Canny(frame, 20, 40)
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=2)
    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    squares=[]
    for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.04*cnt_len, True)
                    if len(cnt) == 4  and cv2.isContourConvex(cnt):
                        cnt = cnt.reshape(-1, 2)
                        max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                        if max_cos < 0.2 and cv2.contourArea(cnt)>5000 and  cv2.contourArea(cnt)<10000 :#and #longueur_square(cnt):
                            squares.append(cnt)

    cv2.drawContours(frame, squares, -1, (0,255,0), 3)

    return frame,squares

def draw_arrow(frame,orient):
    
    offset=200
    
    color = (0, 255, 0)
    thickness = 4
    if orient !="None":
        if orient =="Left" :
            start_point = (1000, 250)
            end_point = (start_point[0]-offset,start_point[1] )
        elif orient == "Up":
            start_point = (1000, 400)
            end_point=(start_point[0],start_point[1]-offset )
        elif orient == "Down":
            start_point = (1000, 250)
            end_point=(start_point[0],start_point[1]+offset )
        frame= cv2.arrowedLine(frame, start_point, end_point,color, thickness)
    return frame 
  
    