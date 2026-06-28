from pydantic import BaseModel
from typing import Type, Any, Optional

class Dict2Class(object):
    
    def __init__(self, my_dict):
        
        for key in my_dict:
            setattr(self, key, my_dict[key])




class Dict2PydanticClass(object):
    
    def __init__(self, my_dict: dict, target_class: Optional[Type[BaseModel]] = None):
        """
        Convert a dictionary to a class instance, with Pydantic support.
        
        Args:
            my_dict: Dictionary containing the data
            target_class: Optional Pydantic BaseModel class to use as template.
                         If provided, validates and parses using Pydantic.
        """
        if target_class and issubclass(target_class, BaseModel):
            # Use Pydantic's validation and parsing
            self._instance = target_class(**my_dict)
            
            # Copy all attributes to self
            for key, value in self._instance.__dict__.items():
                setattr(self, key, value)
        else:
            # Original behavior
            for key in my_dict:
                setattr(self, key, my_dict[key])
    
    def get_pydantic_instance(self):
        """Return the underlying Pydantic instance if available."""
        return getattr(self, '_instance', None)