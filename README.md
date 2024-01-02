# os3m Target Testing

## Overview

This repository documents the comprehensive testing process for different targets using the os3m mouse. The purpose of these tests was to identify characteristic curves for various targets and to optimize sensor readings. This document serves as a lab report detailing firmware modifications, test setups, results, and analysis.

## Firmware Modifications for Raw Data Capture

To facilitate the capture of raw LDC data, modifications were made to the firmware. The changes are specific to the `sendGamepadReport` function within the `main` function of the firmware code.

### Modified Code Snippet

```cpp
// Send the difference in LDC readings as HID gamepad inputs
sendGamepadReport((uint16_t)ldc1_ch1_dif, (uint16_t)ldc1_ch0_dif, 0, 0, 0, 0);
```

This alteration sends the differential LDC readings as inputs to the HID gamepad, with the first two channels populated and the remaining channels zeroed out.

## Experimental Setup

The experimental setup included a custom-designed measurement rig to hold the targets at specific distances from the sensor array. Data capture was automated using a platformio project on an Arduino Nano to read distances from digital calipers and a series of Python scripts to log data and generate visualizations.

### Hardware Components

- os3m sensor array with firmware modifications
- Measurement rig with adjustable target holder (hot glue)
- Digital calipers interfaced with an Arduino Nano

### Test Targets

A variety of targets were tested, including commonly found objects such as coins and specifically designed optimum targets based on hypothesized performance characteristics.

![Targets 1](images/test_targets.jpg)
![Targets 2](images/test_targets_2.jpg)

## Test Sequence

Tests were conducted by zeroing the calipers first with the target as close to the sensing element as it could go. In the case of large targets like a quarter this was just above the surface of the PCB because of collisions. 

Then the test target was pulled 40 mm away from the PCB, and the os3m was zeroed. 

The target was then slowly moved towards and way from the LDC sensing element.

Tests were conducted with the target centered over a single coil, and then between the coils L1 and L2. 

## Results and Analysis

Each test produced a set of raw data files, which were processed to generate interactive visualizations and summary statistics. The tests aimed to establish a relationship between the size, shape, and composition of the targets and the LDC sensor readings.

This testing also aimed to find the characteristic curves of the LDC readings vs distance. 

### Data Visualization

The test results were visualized using Plotly graphs, which illustrate the relationship between the target distance and LDC sensor output. Two sensor configurations were tested: single and dual LDC setups.

![Target: Dime, Dual LDC Graph](images/dime_dual_LDC_Graph.png)
![Size vs LDC Single Sensor](images/size_vs_LDC_Single.png)
![Size vs LDC Dual Summed](images/size_vs_LDC_Dual_Summed.png)

Graphs of this data were generated using `plotly` and can be found in: `data_capture/test_runs_to_keep`

You will probably have to download and open the HTML files locally for their interactive elements to work. 

### Test Setup Images

The following images showcase the measurement rigs and the array of test targets:

![Caliper Parser Breadboard](images/caliper_parser_breadboard.jpg)
Used to prototype the circuit for reading data from the calipers.

![Measurement Rig Front](images/front_distance_rig.jpg)
![Measurement Rig Back](images/back_distance_rig.jpg)

## Repository Structure

- `caliper_reader`: Contains the platformio project and test scripts for the Arduino Nano used in data acquisition from the digital calipers.
- `data_capture`: Includes the Python scripts for data logging and analysis, as well as the raw CSV data files and generated HTML files with interactive graphs.
- `hypothesized_optimum_target`: Features the design files for the proposed optimum target based on testing insights.

## Conclusion

The testing process has successfully characterized the response of the os3m system to various targets, providing valuable data to inform the design of an optimized target. Future work will involve refining the target design and validating its performance in further tests.

For next steps I have designed and ordered what I hypothesize to be the optimum target shape. 

![Send Cut Send Optimum Target Quote](hypothesized_optimum_target/send_cut_send_target_quote.png)

This design should allow the mouse to not be dependent on US currency for the target shape, and optimize the target response to be at a good sensing strength. 

More testing is necessary to tune in response once a target is selected, but with this data collection a function to linearize the response of the LDC sensor could be made. This would greatly increase the control accuracy of the system. 

## Licensing

The resources in this repository are provided under the terms outlined in the [LICENSE](LICENSE) file.
