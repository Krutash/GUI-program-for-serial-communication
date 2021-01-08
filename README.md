****************************************************************
Author : Utkarsh Kumar
****************************************************************
HOW TO RUN THE APPLICATION:
1. Run Chromstation-1.0.0.py from your IDLE.
2. The First thing you'll see is dashboard with buttons on left and a graph on right.
3. The graph shows the previously collected data in online mode.
4. The four buttons on left are Online Mode, Review Mode, Overlay Mode and Calibration Mode(from top to bottom).
5. This project was developed in Inovative Sensor Section; SIS Division; Electronics and Instrumentation Group, IGCAR-Kalpakkam.
6. The further Details of respective operative modes is given below:
***********************************************************************
ONLINE MODE:
1. The online mode is for data acquisiton from the Chromatogram.
2. It has been programmed to recognize certain signals from the hardware that indicate the start of chromatogram.
3. For changes in signal recognition please look into input_new_device.py.
4. For more comprehensive explaination on how to use the software please visit :
********************************************************
REVIEW MODE
1. To load a graph in Review mode, refer to the samples provided in Sample data.
2. If you drag under the peak using mouse, you'll get the computed area of the peak in Area box.
3. There are options to naviagate directly to calibration page for further linear analysis.
***************************************************************
CALIBRATION MODE
1. You'll see a tablulated layout in this page
2. Click on the Analyte button to set name for the analyte.
3. Put analyte concentraion and corresponding area of peak under Analyte and Area column respectively.
4. Now after putting known concentraions, click on units to put the units of the concentration.
5. Click on Calibrate to generate linearly regressed curve and to visualize the curve click on plot.
6. For further details on calibration parameteres click on details.
7. Now if u insert an area to an unknown concentration and press enter, on the corresponding column you'll get the calculated concentration.
*********************************************************
OVERLAY MODE
1. In overlay mode there is option to overlay 5 graphs at a time.
2. The graphs are overlayed on an absolute scale for relative overlay, preprocess the data.
