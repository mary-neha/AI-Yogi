import cv2
import streamlit as st
import numpy as np
import math,pickle
from PIL import Image
import mediapipe as mp
import pyttsx3

def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def main_content():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    load_model=pickle.load(open('resources/YogaModel.pkl','rb'))
 
    def getAngle(a, b, c):
        ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        return round(ang + 360 if ang < 0 else ang)
 
    def feature_list(poseLandmarks,posename):
        return [getAngle(poseLandmarks[16],poseLandmarks[14],poseLandmarks[12]),
        getAngle(poseLandmarks[14],poseLandmarks[12],poseLandmarks[24]),
        getAngle(poseLandmarks[13],poseLandmarks[11],poseLandmarks[23]),
        getAngle(poseLandmarks[15],poseLandmarks[13],poseLandmarks[11]),
        getAngle(poseLandmarks[12],poseLandmarks[24],poseLandmarks[26]),
        getAngle(poseLandmarks[11],poseLandmarks[23],poseLandmarks[25]),
        getAngle(poseLandmarks[24],poseLandmarks[26],poseLandmarks[28]),
        getAngle(poseLandmarks[23],poseLandmarks[25],poseLandmarks[27]),
        getAngle(poseLandmarks[26],poseLandmarks[28],poseLandmarks[32]),
        getAngle(poseLandmarks[25],poseLandmarks[27],poseLandmarks[31]),
        getAngle(poseLandmarks[0],poseLandmarks[12],poseLandmarks[11]),
        getAngle(poseLandmarks[0],poseLandmarks[11],poseLandmarks[12]),
        posename]   

    app_mode=st.sidebar.selectbox('Select The Pose',['Tree','Mountain','Warrior2'])

    if app_mode=='Tree': 
        col1, col2, col3 = st.columns([2,1,5])
        with col1:
            with st.container():
                st.markdown("<h3 style='color: #8B4513'>VRIKSHASANA:</h3>", unsafe_allow_html=True)
                st.write("Try Tutorial")
                st.video('https://www.youtube.com/embed/PZ1zAvcKzrg') 
                st.markdown("<ul style='color:#87CEEB'>"
                            "<li>Improves balance and concentration.</li>"
                            "<li>Stretches the groins, inner thighs, chest, and shoulders.</li>"
                            "</ul>", unsafe_allow_html=True)            
                #image = Image.open('resources/tree.jpg')
                #st.image(image, caption='Tree Pose')
                message = st.empty()
                #st.markdown("<p style='font-size:16px; color:green; font-family: Arial, sans-serif;'><em>Before you start, listen to the instructions:</em></p>", unsafe_allow_html=True)
        # Speak out the instruction
                speak("Assume the tree pose.Before you start, listen to the instructions Stand on one leg with your arms raised above your head. Hold your position steady.")
                
                #image = Image.open('resources/tree.jpg')
                #st.image(image, caption='Tree Pose')
                message = st.empty()
        with col3:
            st.write("Webcam Live Feed")
            button=st.empty()
            start=button.button('Start')
            if start:
                stop=button.button('Stop')
                visible_message = st.empty()
                FRAME_WINDOW = st.image([])
                accuracytxtbox = st.empty()
                cap = cv2.VideoCapture(0)
            
            
                with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                    while cap.isOpened():
                        ret, frame = cap.read()
                        h,w,c=frame.shape 
                        # Recolor image to RGB
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False
                    
                        # Make detection
                        results = pose.process(image)
                        
                        # Recolor back to BGR
                        image.flags.writeable = True
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        
                        # Render detections
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                                )               
                        
                        FRAME_WINDOW.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                        poseLandmarks=[]
                        if results.pose_landmarks:
                            for lm in results.pose_landmarks.landmark:            
                                poseLandmarks.append((int(lm.x*w),int(lm.y*h)))
                        if len(poseLandmarks)==0:
                            visible_message.text("Body Not Visible")
                            accuracytxtbox.text('')
                            continue
                        else:
                            visible_message.text("")
                            
                            d=feature_list(poseLandmarks,1)
                            rt_accuracy=int(round(load_model.predict(np.array(d).reshape(1, -1))[0],0))
                            if rt_accuracy<100:
                                accuracytxtbox.text(f"Accuracy:{rt_accuracy}")
                            else:
                                accuracytxtbox.text(f"Accuracy:{100}")
                            if rt_accuracy<75:
                                message.markdown('<p style="font-size: 48px; color: red"> Not so good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>75 and rt_accuracy<85:
                                message.markdown('<p style="font-size: 48px; color: green"> Good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>85 and rt_accuracy<95:
                                message.markdown('<p style="font-size: 48px; color: #7FFFD4"> Very good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>95 and rt_accuracy<100:
                                message.markdown('<p style="font-size: 48px; color: #20B2AA"> Near to perfection </p>', unsafe_allow_html=True)
                            elif rt_accuracy>=100:
                                message.markdown('<p style="font-size: 48px; color: #87CEEB"> You reached your goal perfection </p>', unsafe_allow_html=True)
                            
                        
                        if stop:
                            cap.release()
                            cv2.destroyAllWindows()
                    else:
                        st.write('Your Camera is Not Detected !')

    elif app_mode=='Mountain':  
        col1, col2, col3 = st.columns([2, 1, 5])
        with col1:
            with st.container():
                st.markdown("<h3 style='color: #8B4513'>TADASANA:</h3>", unsafe_allow_html=True)
                st.write("Try Tutorial")
                st.video('https://www.youtube.com/embed/E1xym-F_B84') # Example video link
               # st.markdown("<h3 style='color:#00AEEF'>Advantages:</h3>", unsafe_allow_html=True)
                st.markdown("<ul style='color:#87CEEB'>"
                            "<li>Improves posture and balance.</li>"
                            "<li>Reduces flat feet.</li>"
                            "</ul>", unsafe_allow_html=True)
               # image = Image.open('resources/mountain.jpg')
               # st.image(image, caption='Mountain Pose', use_column_width=True)
                message = st.empty()
                st.markdown("<p style='font-size:16px; color:green; font-family: Arial, sans-serif;'><em>Before you start, listen to the instructions:</em></p>", unsafe_allow_html=True)

        # Speak out the instruction
                speak("Assume the mountain pose  Before you start, listen to the instructions Stand straight with your feet together, and arms by your sides. Focus on your breathing and keep your spine straight.")
                st.write("Mountain Pose")
               # image = Image.open('resources/mountain.jpg')
               # st.image(image, caption='Mountain Pose', use_column_width=True)
                message = st.empty()
        with col3:
            st.write("Webcam Live Feed")
            button=st.empty()
            start=button.button('Start')
            if start:
                stop=button.button('Stop')
                visible_message = st.empty()
                FRAME_WINDOW = st.image([])
                accuracytxtbox = st.empty()
                cap = cv2.VideoCapture(0)
                with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                    while cap.isOpened():
                        ret, frame = cap.read()
                        h,w,c=frame.shape 
                        # Recolor image to RGB
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False
                    
                        # Make detection
                        results = pose.process(image)
                        
                        # Recolor back to BGR
                        image.flags.writeable = True
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        
                        # Render detections
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                                )               
                        
                        FRAME_WINDOW.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                        poseLandmarks=[]
                        if results.pose_landmarks:
                            for lm in results.pose_landmarks.landmark:            
                                poseLandmarks.append((int(lm.x*w),int(lm.y*h)))
                        if len(poseLandmarks)==0:
                            visible_message.text("Body Not Visible")
                            accuracytxtbox.text('')
                            continue
                        else:
                            visible_message.text("")
                            
                            d=feature_list(poseLandmarks,2)
                            rt_accuracy=int(round(load_model.predict(np.array(d).reshape(1, -1))[0],0))
                            if rt_accuracy<100:
                                accuracytxtbox.text(f"Accuracy:{rt_accuracy}")
                            else:
                                accuracytxtbox.text(f"Accuracy:{100}")
                            if rt_accuracy<75:
                                message.markdown('<p style="font-size: 48px; color: red"> Not so good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>75 and rt_accuracy<85:
                                message.markdown('<p style="font-size: 48px; color: green"> Good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>85 and rt_accuracy<95:
                                message.markdown('<p style="font-size: 48px; color: #7FFFD4"> Very good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>95 and rt_accuracy<100:
                                message.markdown('<p style="font-size: 48px; color: #20B2AA"> Near to perfection </p>', unsafe_allow_html=True)
                            elif rt_accuracy>=100:
                                message.markdown('<p style="font-size: 48px; color: #87CEEB"> You reached your goal perfection </p>', unsafe_allow_html=True)
                            
                        
                        if stop:
                            cap.release()
                            cv2.destroyAllWindows()
                    else:
                        st.write('Your Camera is Not Detected !')
         
    elif app_mode=='Warrior2':
        col1, col2, col3 = st.columns([2,1,5])
        with col1:
            with st.container():
                st.markdown("<h3 style='color: #8B4513'>VEERABHADRASANAM:</h3>", unsafe_allow_html=True)
                st.write("Try Tutorial")
                st.video('https://www.youtube.com/embed/Mn6RSIRCV3w') # Example video link
                #st.markdown("<h3 style='color:#00AEEF'>Advantages:</h3>", unsafe_allow_html=True)
                st.markdown("<ul style='color:#87CEEB'>"
                            "<li>Opens the hips, chest, and shoulders.</li>"
                            "<li>Improves focus and stability and relieves backaches</li>"
                            "</ul>", unsafe_allow_html=True)
                #image = Image.open('resources/warrior2.jpg')
                #st.image(image, caption='Warrior2 Pose', use_column_width=True)
                message = st.empty()
                st.markdown("<p style='font-size:16px; color:green; font-family: Arial, sans-serif font-style:italic;'><em>Before you start, listen to the instructions:</em></p>", unsafe_allow_html=True)
                
        # Speak out the instruction
                speak("Assume the warrior  pose Before you start, listen to the instructions Stand with your legs wide apart, raise your arms parallel to the floor, and keep your gaze forward over your front hand.")
               # image = Image.open('resources/warrior2.jpg')
               # st.image(image, caption='Warrior2 Pose', use_column_width=True)
                message = st.empty()
        with col3:
            st.write("Webcam Live Feed")
            # run = st.checkbox('Start Video')
            button=st.empty()
            start=button.button('Start')
            if start:
                stop=button.button('Stop')
                visible_message = st.empty()
                FRAME_WINDOW = st.image([])
                accuracytxtbox = st.empty()
                cap = cv2.VideoCapture(0)
                with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                    while cap.isOpened():
                        ret, frame = cap.read()
                        h,w,c=frame.shape 
                        # Recolor image to RGB
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False
                    
                        # Make detection
                        results = pose.process(image)
                        
                        # Recolor back to BGR
                        image.flags.writeable = True
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        
                        # Render detections
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                                )               
                        
                        FRAME_WINDOW.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                        poseLandmarks=[]
                        if results.pose_landmarks:
                            for lm in results.pose_landmarks.landmark:            
                                poseLandmarks.append((int(lm.x*w),int(lm.y*h)))
                        if len(poseLandmarks)==0:
                            visible_message.text("Body Not Visible")
                            accuracytxtbox.text('')
                            continue
                        else:
                            visible_message.text("")
                            
                            d=feature_list(poseLandmarks,3)
                            rt_accuracy=int(round(load_model.predict(np.array(d).reshape(1, -1))[0],0))
                            if rt_accuracy<100:
                                accuracytxtbox.text(f"Accuracy:{rt_accuracy}")
                            else:
                                accuracytxtbox.text(f"Accuracy:{100}")
                            if rt_accuracy<75:
                                message.markdown('<p style="font-size: 48px; color: red"> Not so good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>75 and rt_accuracy<85:
                                message.markdown('<p style="font-size: 48px; color: green"> Good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>85 and rt_accuracy<95:
                                message.markdown('<p style="font-size: 48px; color: #7FFFD4"> Very good </p>', unsafe_allow_html=True)
                            elif rt_accuracy>95 and rt_accuracy<100:
                                message.markdown('<p style="font-size: 48px; color: #20B2AA"> Near to perfection </p>', unsafe_allow_html=True)
                            elif rt_accuracy>=100:
                                message.markdown('<p style="font-size: 48px; color: #87CEEB"> You reached your goal perfection </p>', unsafe_allow_html=True)
                            
                        
                        if stop:
                            cap.release()
                            cv2.destroyAllWindows()
                    else:
                        st.write('Your Camera is Not Detected !')
