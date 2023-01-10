# quicksNXS LRScalingFactors scaling factor calculation script
# Script  automatically generated on 27_10_2021

import mantid
import mantid.simpleapi as api

api.LRScalingFactors(DirectBeamRuns=[184981, 184982, 184983, 184984, 184985, 184986, 184987, 184988, 184989], IncidentMedium="air", TOFSteps=200, TOFRange=[9970.0, 23250.0], SignalPeakPixelRange=[137, 145, 137, 145, 136, 145, 136, 145, 136, 145, 136, 145, 135, 147, 135, 147, 135, 147], SignalBackgroundPixelRange=[134, 148, 134, 148, 133, 148, 133, 148, 133, 148, 133, 148, 132, 150, 132, 150, 132, 150], LowResolutionPixelRange=[0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256], ScalingFactorFile="scaling_factors.cfg")