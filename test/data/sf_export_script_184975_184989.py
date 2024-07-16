# Scaling factor calculation
# lr_reduction 2.0.23
# Script automatically generated on Mon Apr 22 17:05:13 2024

from lr_reduction.scaling_factors import LRScalingFactors
from lr_reduction.utils import mantid_algorithm_exec

mantid_algorithm_exec(
    LRScalingFactors.LRScalingFactors,
    DirectBeamRuns=[184981, 184982, 184983, 184984, 184985, 184986, 184987, 184988, 184989],
    IncidentMedium='air',
    Attenuators=[],
    TOFRange=[9970.0, 23250.0],
    TOFSteps=150,
    SignalPeakPixelRange=[137, 145, 137, 145, 136, 145, 136, 145, 136, 145, 136, 145, 135, 147, 135, 147, 135, 147],
    SignalBackgroundPixelRange=[134, 148, 134, 148, 133, 148, 133, 148, 133, 148, 133, 148, 132, 150, 132, 150, 132, 150],
    LowResolutionPixelRange=[0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256],
    ScalingFactorFile='scaling_factors.cfg',
    UseDeadTimeCorrection=True,
    ParalyzableDeadTime=True,
    DeadTime=4.2,
    DeadTimeTOFStep=150,
)
