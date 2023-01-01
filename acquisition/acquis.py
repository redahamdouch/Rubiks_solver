import cv2 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from acquisition.util import *

def acquistion():
    dic_is_acquis= {"green":False,"orange":False,"red":False,"yellow":False,"white":False,"blue":False}
    is_calibrated  =False
    face_analysis=False
    verif=False
    face_to_calibrate=0
    aquises=[]
    order=["F","L","B","R","F","U","F","D","Done"]
    arrows=["None","Left","Left","Left","Left","Up","Down","Down","None"]
    cube = Cube(pos_f=[(1000,590),(1010,600)],pos_d=[(1000,660),(1010,670)],pos_r=[(1070,590),(1080,600)],pos_l=[(930,590),(940,600)],pos_u=[(1000,520),(1010,530)],pos_b=[(1140,590),(1150,600)])


    import cv2
    vid = cv2.VideoCapture(0)
    is_acquis=False
    while(True): 
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        frame=cube.draw_patron(frame)

            
        if face_analysis:
            
            if order[face_to_calibrate]!="Done":
                frame,squares=detection(frame)
                draw_arrow(frame,arrows[face_to_calibrate])
                if len(squares)==9 :


                    if order[face_to_calibrate]=='F' and cube.dic_faces[order[face_to_calibrate]].colors!=[]:

                        face=cube.dic_faces[order[face_to_calibrate]].colors
                        f_temp=Face([(0,0),(0,0)],cube)
                        f_temp.set_img_and_contours(frame,squares)
                        if face == f_temp.colors:
                            cv2.putText(frame, 'OK its the front face :)  !', (50, 50), font, 1, (0, 255, 0), 2, cv2.LINE_4)
                            cv2.imshow('frame',frame)
                            cv2.waitKey(2000)
                            face_to_calibrate+=1
                        else : 
                            cv2.putText(frame, "Error on the front face or orientation!", (50, 50), font, 1, (255,0, 0), 2, cv2.LINE_4)


                        
                        

                    else:
                        f_temp=Face([(0,0),(0,0)],cube)
                        f_temp.set_img_and_contours(frame,squares)
                        face_color=f_temp.color_face
                        if face_color in aquises:
                            cv2.putText(frame, 'Face already acquired!', (50, 50), font, 1, ( 255,0, 0), 2, cv2.LINE_4)
                        else:
                            cube.dic_faces[order[face_to_calibrate]].set_img_and_contours(frame,squares)
                            aquises.append(cube.dic_faces[order[face_to_calibrate]].color_face)
                            cv2.putText(frame, 'OK !', (50, 50), font, 1, (0, 255, 0), 2, cv2.LINE_4)
                            cv2.imshow('frame',frame)
                            cv2.waitKey(2000)
                            face_to_calibrate+=1



                else : 
                    cv2.putText(frame, 'Show face :'+order[face_to_calibrate], (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_4)

            else :
                cv2.putText(frame, 'DONE!', (50, 50), font, 1, (0, 255, 0), 2, cv2.LINE_4)
                face_analysis=False
                verif=True
                

        if not is_calibrated:
            color=cube.color_to_calibrate()


            if color !="Done":
                frame,squares=detection(frame)
            
                if len(squares)==9:
                    cv2.putText(frame, 'Ok ! :'+color, (50, 50), font, 1, (0, 255, 0), 2, cv2.LINE_4)
                    cv2.imshow('frame',frame)
                    middle_square_contour=cube.dic_faces["F"].order_contours(squares)[4]
                    cube.set_color_ref(frame,middle_square_contour,color)
                    cv2.waitKey(2000)
                else : 
                    cv2.putText(frame, 'Show middle face :'+color, (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_4)
            else :
                is_calibrated=True
                face_analysis=True
        
        if verif :
            if cube.validation():
                soluce,conversion=cube.to_kociemba()
                cv2.putText(frame, 'Acquisition completed ! :)  :'+color, (50, 50), font, 1, (0, 255,0 ), 2, cv2.LINE_4)
            else :
                cv2.putText(frame, 'Error in aquisition please retry:'+color, (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_4)
                verif = False
                face_to_calibrate=0
                aquises=[]
                face_analysis = True
                cv2.imshow('frame',frame)
                references =cube.color_refs

                cube = Cube(pos_f=[(1000,590),(1010,600)],pos_d=[(1000,660),(1010,670)],pos_r=[(1070,590),(1080,600)],pos_l=[(930,590),(940,600)],pos_u=[(1000,520),(1010,530)],pos_b=[(1140,590),(1150,600)])
                cube.color_refs=references
                cv2.waitKey(8000)


        cv2.imshow('frame',frame)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # After the loop release the cap object
    vid.release()

    cv2.destroyAllWindows()
    return soluce,conversion