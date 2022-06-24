## Project_Course_2022
### Authors:
Jacopo Caucig -
Lorenzo Lellini - 
Hakim El Achak

# Measurement Framework for Room Impulse Response Dataset and Acoustic Source Calibration

A compact tool, fully developed in Python, for the acquisition of Room Impulse Responses and the creation of high quality Dataset. It also performs Acoustic Source Localization based on RIR acoustical informations.

In nowadays audio applications (i.e. virtual reality, auralization, sound field reconstruction, beamforming), the relevance of measuring the room impulse response with an adequate signal-to-noise ratio becomes more and more evident. These needs moved us to implement a versatile and automatic framework which can fulfill this task and not only. 

On the other hand, a large number of microphone array techniques, such as source localization, noise reduction, source separation or acoustic wavefield
analysis and synthesis, assume that the position of each sensor (microphone) is perfectly known. Many of the previous mentioned applications are very sensitive to the microphone positions, and therefore a very accurate positioning is required. In such cases, manual measurement of positions is difficult to perform, and self-calibration methods are required, using acoustic information to estimate the array geometry.


## USER INTERFACE

<p align="center">
<img src="./Images/main.png" width="550" height="500">
</p>


That is how it looks the GUI at the starting point and it is mainly divided into 2 sections: 'SYSTEM SETTINGS' and 'CALIBRATION'.

### 1) SYSTEM SETTINGS

This section is dedicated to the declaration of specific parameters and technical aspects needed for the RIRs's acquisition. 

In particular, in the first part (point 1,2,3) it asks you to choose the proper audio devices where the needed inputs/ouputs channels are connected.
A routing matrix (fig. below) allows you to choose from the selectable channels the right number of inputs and outputs that you are going to use. 



<p align="center">
<img src="./Images/matrix.jpg" >
</p>

In this specific example the number of the max_num available of input/output was 30. 


In the second part instead (point 4,5), you can choose two relevant parameters as sampling frequency and the proper sound speed in relation to the temperature. 

System latency may differ from device to device so a simple method for the estimation of the used device's latency was implemented; this is crucial for the RIRs to be correct. 
After pressing the button (point 6) a secondary window will appear in which, as it can be seen in the figure below, all the needed passages are specified. 


<p align="center">
<img src="./Images/latency.png" width="450" height="400">
</p>



The numerical order was put on purpose through all the GUI in order to facilitate the user to follow all the steps in a right manner.


### 2) CALIBRATION

At this point, after naming the measurment folder (1), some parameters such as 'room dimensions'(2) and 'known source positions'(3a,3b) are needed by the calibration algorithm in order to be correctly functional. 
The known positions of the inital sound sources can be entered manually or by uploading a proper json file (later specified). 
As this proccess is symmetric, in both cases it is requeired to specify the tipology of source (microphone or loudspeaker) of which the calibration is desired.

Now, since the apllication has all the preliminary data, by pressing the corresponding button (4) the actual acoustic source calibration will start. 

At this point it is necessary to wait for the acquisition by all of the selected microphones together with the RIR creation and sound source localization. Based on the number of inputs/outputs chosen, obviously the computational cost changes.


At the end of the measure, you will obtain a proper Dataset organized in this way:
- a .json file in which are reported the measurement conditions and room properties and the estimated device positions;
- a folder for each known source in which there are:
     - a .wav file of the RIR of each microphone, of the actual recordings and of the input test signal
     - a .npy file containing the storage Matrix of the RIRs


Point 5 and 6 show respectively the 3D plot of the sources position estiamtion and the RIRs's waveforms acquired. 
Point 7 prints the coordinates esatimed positions. 



## IMPLEMENTATION


The Framework is implemented in Python to allow the use of multiples convenient libraries such as 'Sounddevice' for the device detection, channel selection and sound reproduction and recording, 'PyRoomAcoustics' for the simulations, 'Tkinter' for the creation of the GUI and other common libraries such as 'Numpy' and 'Scipy' for the elaboration of data. 

The code for the measuring and the acquisition or the RIR is based on 'pyrirtool' [1], an algorithm that recall the ESS method and its modifications proposed by Angelo Farina [2].

The whole code is divided in modules that can be ran separately or together through the Main which opens the GUI. The two most important modules of the framework are 'Sine SweepRIRmeasure' which creates and plays the test signal through the desired channels, computes and saves the RIRs, and the 'Calibration' module which uses the known device positions to estimate unknown device positions.


***Required packages***: a the .txt file is included in the project folder which can be used to install in the environment the complete list of the packages needed by the algorithm to be correctly functional. 





### REFERENCES

- [1] maj4e - "pyrirtool"- https://github.com/maj4e/pyrirtool.
- [2] A. Farina – "Advancements in impulse response measurements by sine sweeps", 122nd AES Convention, May 2007.
