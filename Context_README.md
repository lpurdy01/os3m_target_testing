# os3m_target_testing
This repo contains resources used in testing targets and finding characteristic curves.

# Firmware Changes to Capture Raw LDC Data.

To capture raw LDC data the `sendGamepadReport` command in the `main` function needs to be changed to:

```cpp
sendGamepadReport((uint16_t)ldc1_ch1_dif, (uint16_t)ldc1_ch0_dif, 0, 0, 0, 0);
```

# Images
![Target: Dime, Dual LDC Graph](images/dime_dual_LDC_Graph.png)
![Caliper Parser Breadboard](images/caliper_parser_breadboard.jpg)
![Measurement Rig Front](images/front_distance_rig.jpg)
![Measurement Rig Back](images/back_distance_rig.jpg)
![Targets 1](images/test_targets.jpg)
![Targets 2](images/test_targets_2.jpg)
![Size vs LCD Single Sensor](images/size_vs_LDC_Single.png)
![Size vs LDC Dual Summed](images/size_vs_LDC_Dual_Summed.png)
![Send Cut Send Optimum Target Quote](hypothesized_optimum_target/send_cut_send_target_quote.png)