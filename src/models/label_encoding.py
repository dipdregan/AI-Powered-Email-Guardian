class LabelConverter:
    def __init__(self):
        self.ham = 0
        self.spam = 1

    def decode(self, label):
        if label == self.ham:
            return 'ham'
        elif label == self.spam:
            return 'spam'
        else:
            raise ValueError(f"Unknown label: {label}")
