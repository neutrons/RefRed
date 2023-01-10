# quicksNXS LRScalingFactors scaling factor calculation script
# Script  automatically generated on 03_11_2021

import mantid.simpleapi as api

api.LRScalingFactors(
    DirectBeamRuns=[184978, 184979, 184980],
    IncidentMedium="air",
    TOFSteps=200,
    TOFRange=[20880.0, 34170.0],
    SignalPeakPixelRange=[136, 145, 136, 145, 136, 145],
    SignalBackgroundPixelRange=[133, 148, 133, 148, 133, 148],
    LowResolutionPixelRange=[0, 256, 0, 256, 0, 256],
    ScalingFactorFile="/tmp/UUGKIwuJfA.cfg",
)
