class ChangeDict(dict):
    """A subclass of dict which keeps track of whether it has been changed.
    """
    def __init__(self, *args, **kwargs):
        self.changed = False
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not (self.get(key) == value):
            self.changed = True
        super().__setitem__(key, value)

        
