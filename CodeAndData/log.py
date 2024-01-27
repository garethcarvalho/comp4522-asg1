import time

class Log:
    
    def __init__(self, person_id: int, attribute: str, before_value: str | int, after_value: str | int, status: bool):
        self.person_id = person_id
        self.attribute = attribute
        self.before_value =  before_value
        self.after_value = after_value
        self.status = status
        self.timestamp = time.time()
        # self.transaction_id = get_transaction_id()

    def __str__(self):
        string = f'[ ({self.timestamp}) | Path: "Employees/{self.person_id}" | {self.attribute}: "{self.before_value}" -> "{self.after_value}" | Status: {self.status} ]'
        return string