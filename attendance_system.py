
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.constants import ACTIVE, DISABLED
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
import face_recognition as fr

from datetime import datetime

class AttendanceSystem:
    def __init__(self, title):
        print("Initializing " + title)
        self.base_directory = ""
        self.title = title
        self.attendance_marked = []

    def run(self):
        self.root = tk.Tk()
        self.root.title = self.title

        self._browse_button = tk.Button(self.root, text="Browse Image Dir", command=self._select_folder)
        self._browse_button.grid(row=0, column=0)

        self.root.mainloop()

    def _select_folder(self):
        
        current_directory = filedialog.askdirectory()

        self.base_directory = current_directory
        print("Current Directory: ", current_directory)
        directory_files = os.listdir(current_directory)

        if len(directory_files) == 0:
            raise FileExistsError("Empty directory selected !!!")

        images = [image_file for image_file in directory_files if 'jpg' in image_file]

        self._image_files = [os.path.join(current_directory, image_file) for image_file in images]
        self._classes = [image_file.split(".")[0] for image_file in images]

        print(f'Classes: {self._classes}, Image Files: {self._image_files}')

        self._attendance_folder_path = os.path.join(self.base_directory, "attendance")

        try:
            os.mkdir(self._attendance_folder_path)
        except FileExistsError:
            print("Attendance Folder already exists")

        current_date = str(datetime.now().date())
        self._attendance_file_name = os.path.join(self._attendance_folder_path, current_date + ".csv")

        with open(self._attendance_file_name, "w") as attendance_file:
            attendance_file.write('"Time","Name"\n')
        
        self._browse_button["state"] = DISABLED
        self._encode_images()

    def _encode_images(self):
        self._encodings_list = []

        for img in self._image_files:
            img = cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fr.face_encodings(img)[0]
            self._encodings_list.append(encode)

        print("Encoding complete")
        print("Intializing Webcam !!!")
        self._display_webcam()

    
    def _display_webcam(self):
        width, height = 800, 600
        cap = cv2.VideoCapture(0)
        
        # self.root.geometry("800x600")

        self._lmain = tk.Label(self.root)
        self._lmain.grid(row=1, column=0)
        
        def show_frame():
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # cv2image = cv2.resize(cv2image, (800, 600))
            imgS = cv2.resize(cv2image, (0, 0), None, 0.25, 0.25)
            # imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faces_in_frame = fr.face_locations(imgS)
            encode_in_frame = fr.face_encodings(imgS, faces_in_frame)

            for encode_face, face_location in zip(encode_in_frame, faces_in_frame):
                matches = fr.compare_faces(self._encodings_list, encode_face)
                face_distance = fr.face_distance(self._encodings_list, encode_face)

                best_match_index = np.argmin(face_distance)

                if matches[best_match_index]:
                    name = self._classes[best_match_index].upper()
                    if name not in self.attendance_marked:
                        self.attendance_marked.append(name)
                        ts = str(datetime.now())
                        cv2.imwrite(f'{name}_{ts}', imgS)
                        with open(self._attendance_file_name, "a") as attendance_file:
                            attendance_file.write(f'"{ts}", "{name}"\n')


                    y1, x2, y2, x1 = face_location
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(cv2image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(cv2image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(cv2image, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self._lmain.imgtk = imgtk
            self._lmain.configure(image=imgtk)
            self._lmain.after(10, show_frame)

        show_frame()




if __name__ == "__main__":
    print("Hello")
    AttendanceSystem("RWS Attendance System").run()
    