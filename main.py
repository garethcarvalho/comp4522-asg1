# Adv DB Winter 2024 - 1
import random
import os
from log import Log

data_base = []  # Global binding for the Database contents
'''
transactions = [['id1',' attribute1', 'value1'], ['id2',' attribute2', 'value2'],
                ['id3', 'attribute3', 'value3']]
'''
transactions = [['1', 'Department', 'Music'], ['5', 'Civil_status', 'Divorced'],
                ['15', 'Salary', '200000']]
DB_Log: list[Log] = [] # <-- You WILL populate this as you go

schema = None

def get_schema(data: list) -> dict:
    '''
    Returns a dictionary representing the schema of the provided data.
    It expects the first row of the data to be the schema.
    '''
    global schema
    if schema != None:
        # If the schema already exists, return the schema
        return schema
    # Otherwise, generate the schema from the first row
    # of the data.
    schema = {}
    for i in range(len(data[0])):
        schema[data[0][i]] = i
    return schema

def recovery_script(log: list[Log]) -> None:  #<--- Your CODE
    '''
    Restore the database to stable and sound condition, by processing the DB log.
    '''
    print("Calling your recovery script with DB_Log as an argument.")
    print("Recovery in process...\n")

    schema = get_schema(data_base) # Grab the shema of the data.
    last_log = log[len(log) - 1] # Grab the most recent log.
    last_log.status = False

    person_id = last_log.person_id
    attribute = last_log.attribute
    before_value = last_log.before_value
    after_value = last_log.after_value

    data_base[person_id][schema[attribute]] = before_value # Roll the new value back to the old value.

    print(f'Attribute "{attribute}" where Unique_ID = "{person_id}" rolled back',
        f'from "{after_value}" to "{before_value}"\n')

def transaction_processing() -> None: #<-- Your CODE
    '''
    Processes the next transaction in the `transactions` list. The data is mutated
    in main memory, but is not committed to secondary memory yet.
    '''
    schema = get_schema(data_base) # Grab the schema of the data

    transaction = transactions.pop(0);
    person_id = int(transaction[0]);
    attribute = transaction[1];
    before_value = data_base[person_id][schema[attribute]]
    after_value = transaction[2];

    data_base[person_id][schema[attribute]] = after_value; # Mutate according to the transaction.
    log = Log(person_id, attribute, before_value, after_value, True) # Create the new log.

    DB_Log.append(log) # Append the new log to the end of the list.

    transactions.append(transaction) # Append the transaction back in the queue.
    # This is just to avoid the program from throwing an error if it gets through
    # the transactions without any failures.

def read_file(file_name: str) -> list:
    '''
    Read the contents of a CSV file line-by-line and return a list of lists
    '''
    data = []
    #
    # one line at-a-time reading file
    #
    with open(file_name, 'r') as reader:
    # Read and print the entire file line by line
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            line = line.strip().split(',')
            data.append(line)
             # get the next line
            line = reader.readline()

    size = len(data)
    print('The data entries BEFORE updates are presented below:')
    for item in data:
        print(item)
    print(f"\nThere are {size} records in the database, including one header.\n")
    return data

def commit_data(file_name: str) -> None:
    '''
    Writes the contents of `data_base` to a .csv file 
    with the given `file_name`.
    '''
    with open(file_name, 'w') as data_file:
        # Write to a file with the given file name
        item_count = len(data_base)
        for i in range(item_count):
            item = data_base[i]
            size = len(item)
            for j in range(size):
                # Write each item, attribute by attribute,
                # Formatted like a .csv file
                data_file.write(str(item[j]))
                if j + 1 < size:
                    data_file.write(',')

            if i + 1 < item_count:
                data_file.write('\n')

def write_logs(database_file_name: str) -> None:
    '''
    Writes the contents of `DB_Log` to a .csv file
    with the `database_file_name` with "_Logs" appended
    to the end of it.
    '''
    # Append "_Logs.csv" to the file name
    log_path = database_file_name.split('.')[0] + '_Logs.csv'

    with open(log_path, 'w') as log_file:
        # Write to the file with static function that returns
        # a formatted .csv string for reach log.
        log_file.write(Log.get_log_schema())
        log_file.write('\n')
        for log in DB_Log:
            log_file.write(log.get_csv_format())
            log_file.write('\n')
    

def is_there_a_failure() -> bool:
    '''
    Simulates randomly a failure, returning `True` or `False`, accordingly
    '''
    value = random.randint(0,1)
    if value == 1:
        result = True
    else:
        result = False
    return result

def main() -> None:
    number_of_transactions = len(transactions)
    must_recover = False

    # This is the name of the new database file, so as the original data
    # does not get overwritten for the purposes of the assignment.
    database_file_name = 'new_database.csv'

    global data_base # I pull the data_base in here globally because otherwise it just create a new local variable.
    data_base = read_file('Employees_DB_ADV.csv')

    failure = is_there_a_failure()
    failing_transaction_index = None

    while not failure:
        # Process transaction
        for index in range(number_of_transactions):
            print(f"\nProcessing transaction No. {index+1}.")
            transaction_processing()   #<--- Your CODE (Call function transaction_processing)
            print("UPDATES have not been committed yet...\n")
            failure = is_there_a_failure()
            if failure:
                must_recover = True
                failing_transaction_index = index + 1
                print(f'There was a failure whilst processing transaction No. {failing_transaction_index}.')
                break
            else:
                commit_data(database_file_name) # Commit data to secondary memory.
                write_logs(database_file_name) # Write the logs to a file.
                print(f'Transaction No. {index+1} has been commited! Changes are permanent.')
    if must_recover:
        # Call your recovery script
        recovery_script(DB_Log) ### Call the recovery function to restore DB to sound state.
        write_logs(database_file_name) # Update the logs to reflect the rollback.
    else:
        # All transactiones ended up well
        print("All transaction ended up well.")
        print("Updates to the database were committed!\n")

    print('The data entries AFTER updates -and RECOVERY, if necessary- are presented below:')
    for item in data_base:
        print(item)

    print('\nLogs:\n')
    for log in DB_Log:
        print(log)

    
main()