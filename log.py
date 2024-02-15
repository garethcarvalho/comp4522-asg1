import time

class Log:
    log_count: int = 0

    def __init__(self, person_id: int, attribute: str, before_value: str | int, after_value: str | int, status: bool) -> None:
        self.transaction_id = Log.get_next_transaction_id()
        self.person_id = person_id
        self.attribute = attribute
        self.before_value =  before_value
        self.after_value = after_value
        self.status = status

    def __str__(self) -> str:
        string = f'[ ({self.transaction_id}) | Path: "Employees/{self.person_id}" | {self.attribute}: "{self.before_value}" -> "{self.after_value}" | Completed: {self.status} ]'
        return string
    
    def get_csv_format(self) -> str:
        return f'{self.transaction_id},{self.person_id},{self.attribute},{self.before_value},{self.after_value},{self.status}'
    
    @staticmethod
    def get_next_transaction_id(timestamp: float = -1.0) -> str:
        if timestamp == -1.0:
            timestamp = time.time()
        timestamp = int(timestamp)

        transaction_id = str(timestamp) + str(Log.log_count)
        Log.log_count += 1

        return transaction_id
    
    @staticmethod
    def get_log_schema() -> str:
        return "transaction_id,person_id,attribute,before_value,after_value,completed"
