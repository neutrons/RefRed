# standard imports
from typing import Any, Callable, Dict
from xml.dom.minidom import Document, Element

# third party imports
from pydantic import BaseModel

# RefRed imports
from RefRed.utilities import str2bool


class GlobalSettings(BaseModel):
    r"""Injects functionality to a global setting class

    This class is to be used as a base class for a specific global settings class.
    See `DeadTimeSettingsModel` for an example
    """

    def to_xml(self, indent: str = "") -> str:
        r"""Serialize the settings to XML format

        Parameters
        ----------
        indent: str
            Prefix to prepend each line of XML. Typically, a certain number of spaces
        """
        doc = Document()  # Create a new XML document

        def _to_xml(field: str) -> str:
            r"""Serialize one of the dead time settings to XML format"""
            element = doc.createElement(field)
            element_text = doc.createTextNode(str(getattr(self, field)))
            element.appendChild(element_text)
            return element.toxml()

        return "\n".join([indent + _to_xml(field) for field in self.dict()])

    def from_xml(self, node: Element):
        r"""Update the settings from the contents of an XML element

        If the XMl element is missing one (or more) setting, the setting(s) are not updated.
        """
        converters: Dict[str, Callable[[str], Any]] = {
            "apply_deadtime": str2bool,
            "paralyzable": str2bool,
            "dead_time": float,
            "tof_step": int,
        }
        for field, converter in converters.items():
            tmp: list = node.getElementsByTagName(field)
            if len(tmp):
                value = tmp[0].childNodes[0].nodeValue
                setattr(self, field, converter(value))
        return self

    def to_dict(self) -> Dict[str, Any]:
        r"""Return the settings as a dictionary"""
        return self.dict()
