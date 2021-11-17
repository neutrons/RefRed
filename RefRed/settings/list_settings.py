class ListSettings(object):
    def __init__(self):

        self.q_min = 0.005
        self.d_q0 = 0.0004
        self.dq_over_q = 0.005
        self.tof_bin = 40  # micros
        self.q_bin = 0.01  # logarithmic binning
        self.angle_offset = 0.016
        self.angle_offset_error = 0.001

    def __eq__(self, other) -> bool:
        if isinstance(other, dict):
            for attrname in [
                "q_min",
                "d_q0",
                "dq_over_q",
                "tof_bin",
                "q_bin",
                "clocking_pixel",
                "angle_offset",
                "angle_offset_error",
            ]:
                if getattr(self, attrname) != other[attrname]:
                    return False

            return True

        # don't know how to compare so must be different
        return False
