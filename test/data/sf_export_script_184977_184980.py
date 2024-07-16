# Scaling factor calculation
# lr_reduction 2.0.23
# Script automatically generated on Mon Apr 22 17:01:11 2024

from lr_reduction.scaling_factors import LRScalingFactors
from lr_reduction.utils import mantid_algorithm_exec

mantid_algorithm_exec(
    LRScalingFactors.LRScalingFactors,
    DirectBeamRuns=[184978, 184979, 184980],
    IncidentMedium='air',
    Attenuators=[],
    TOFRange=[20880.0, 34170.0],
    TOFSteps=150,
    SignalPeakPixelRange=[136, 145, 136, 145, 136, 145],
    SignalBackgroundPixelRange=[133, 148, 133, 148, 133, 148],
    LowResolutionPixelRange=[0, 256, 0, 256, 0, 256],
    ScalingFactorFile='scaling_factors.cfg',
    UseDeadTimeCorrection=True,
    ParalyzableDeadTime=True,
    DeadTime=4.2,
    DeadTimeTOFStep=150,
)