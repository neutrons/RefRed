class ListSettings(object):
    def __init__(self):

        self.q_min = 0.005
        self.d_q0 = 0.0
        self.dq_over_q = 0.028
        self.tof_bin = 40  # micros
        self.q_bin = 0.01  # logarithmic binning
        self.angle_offset = 0.0
        self.angle_offset_error = 0.001

    def to_dict(self):
        """
        Return dictionary with default values
        """
        return dict(q_min = self.q_min,
                    d_q0 = self.d_q0,
                    dq_over_q = self.dq_over_q,
                    tof_bin = self.tof_bin,
                    angle_offset = self.angle_offset,
                    angle_offset_error = self.angle_offset_error
                    )

    def __eq__(self, other) -> bool:
        if isinstance(other, dict):
            for attrname in [
                "q_min",
                "d_q0",
                "dq_over_q",
                "tof_bin",
                "q_bin",
                "angle_offset",
                "angle_offset_error",
            ]:
                if getattr(self, attrname) != other[attrname]:
                    return False

            return True

        # don't know how to compare so must be different
        return False
