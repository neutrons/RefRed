class RunSequenceBreaker(object):
    final_list: list[int] | None = None
    str_final_list: list[str] | None = None

    def __init__(self, run_sequence: str | None = None):
        self.final_list = []
        self.str_final_list = []

        if run_sequence is None:
            return
        try:
            # remove white spaces
            _run_sequence = run_sequence.replace(" ", "")

            if _run_sequence == "":
                self.final_list = [-1]
                self.str_final_list = [""]
                return

            comma_separated = _run_sequence.split(",")

            for _element in comma_separated:
                hypen_separated = _element.split("-")
                nbr_element = len(hypen_separated)
                if nbr_element > 1:
                    _range = self.getRangeBetweenTwoNumbers(hypen_separated[0], hypen_separated[1])
                    for _r in _range:
                        self.final_list.append(_r)
                        self.str_final_list.append(str(_r))

                else:
                    self.final_list.append(int(hypen_separated[0]))
                    self.str_final_list.append(str(hypen_separated[0]))
        # TODO: specify exception (Glass)
        except:
            self.final_list = [-2]
            self.str_final_list = [""]

    def getRangeBetweenTwoNumbers(self, num1, num2):
        _num1 = int(num1)
        _num2 = int(num2)

        from_num = min([_num1, _num2])
        to_num = max([_num1, _num2])
        return list(range(from_num, to_num + 1))

    def getFinalList(self) -> list[int] | None:
        return self.final_list

    def getStringFinalList(self) -> list[str] | None:
        return self.str_final_list
