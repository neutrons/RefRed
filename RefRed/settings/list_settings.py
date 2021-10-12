class ListSettings(object):
    def __init__(self):

        self.q_min = 0.005
        self.d_q0 = 0.0004
        self.dq_over_q = 0.005
        self.tof_bin = 40  # micros
        self.q_bin = 0.01  # logarithmic binning
        self.clocking_pixel = [121, 197]
        self.angle_offset = 0.016
        self.angle_offset_error = 0.001
