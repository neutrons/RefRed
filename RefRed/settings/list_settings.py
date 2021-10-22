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

    def __eq__(self, other) -> bool:
        if isinstance(other, dict):
            if self.q_min != other["q_min"]:
                return False
            if self.d_q0 != other["d_q0"]:
                return False
            if self.dq_over_q != other["dq_over_q"]:
                return False
            if self.tof_bin != other["tof_bin"]:
                return False
            if self.q_bin != other["q_bin"]:
                return False
            if self.clocking_pixel != other["clocking_pixel"]:
                return False
            if self.angle_offset != other["angle_offset"]:
                return False
            if self.angle_offset_error != other["angle_offset_error"]:
                return False

            return True
        # don't know how to compare so must be different
        return False
