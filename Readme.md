# Attendance Project

This attendance project is based on face recognition. The front end is done in Tkinter. The python file is provided to understand the code. 

## Build the application

To distribute the application, we need to create an exe out of it. It can be done by using pyinstaller.

```
# Install pyinstaller

pip install pyinstaller

# Build the application
pyinstaller attendance_system.spec

```

## Start the application

### Using exe

Double click on the exe.  
A window will open.  
Click on the Browse Button and navigate to the folder that contains the attendance images.  
After selecting, keep the application running.  
Anyone who comes in front of the webcam will be recorded and recognized  
The recognized information will be stored in the same images folder by name attendance.  

### Using python

This application was developed on Python 3.9.7. Please use this version or any later version. 

Make sure, you have Tkinter in the system as well.  
https://www.activestate.com/resources/quick-reads/how-to-install-tkinter-in-windows/

First install the necessary packages

    pip install -r requirements.txt

Run the code 

    python attendance_system.py

An application window would open.  
Please follow the steps in the previous section to use it.  