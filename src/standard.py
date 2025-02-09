class StandardTransaction:
    def __init__(self, transaction_type, category, label, date, cleaned_desc, notes, amount, currency):
        self.transaction_type = transaction_type
        self.category = category
        self.label = label
        self.date = date
        self.cleaned_desc = cleaned_desc
        self.notes = notes
        self.amount = amount
        self.currency = currency

    def to_dict(self):
        return vars(self) 
