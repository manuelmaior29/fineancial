class StandardTransaction:
    def __init__(self, transaction_type, category, label, date, cleaned_desc, notes, amount, currency):
        self.transaction_type = transaction_type
        self.date = date
        self.category = category
        self.amount = amount
        self.currency = currency
        self.cleaned_desc = cleaned_desc
        self.label = label
        self.notes = notes

    def to_dict(self):
        return vars(self) 
