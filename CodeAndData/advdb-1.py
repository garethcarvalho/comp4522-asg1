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
        return schema
    
    schema = {}
    for i in range(len(data[0])):
        schema[data[0][i]] = i
    return schema

def recovery_script(log: list[Log]) -> None:  #<--- Your CODE
    '''
    Restore the database to stable and sound condition, by processing the DB log.
    '''
    print("Calling your recovery script with DB_Log as an argument.")
    print("Recovery in process ...\n")

    schema = get_schema(data_base)
    last_log = log[len(log) - 1]
    last_log.status = False

    person_id = last_log.person_id
    attribute = last_log.attribute
    before_value = last_log.before_value
    after_value = last_log.after_value

    data_base[person_id][schema[attribute]] = before_value

    print(f'Attribute "{attribute}" where Unique_ID = "{person_id}" rolled back',
        f'from "{after_value}" to "{before_value}"\n')

def transaction_processing() -> None: #<-- Your CODE
    schema = get_schema(data_base)

    transaction = transactions.pop(0);
    person_id = int(transaction[0]);
    attribute = transaction[1];
    before_value = data_base[person_id][schema[attribute]]
    after_value = transaction[2];

    data_base[person_id][schema[attribute]] = after_value;
    log = Log(person_id, attribute, before_value, after_value, True)

    DB_Log.append(log)

    transactions.append(transaction)

    '''
    1. Process transaction in the transaction queue.
    2. Updates DB_Log accordingly
    3. This function does NOT commit the updates, just execute them
    ''' 

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

def write_data(file_name: str) -> None:
    with open(file_name, 'w') as data_file:
        for item in data_base:
            size = len(item)
            for i in range(size):
                data_file.write(str(item[i]))
                if i + 1 < size:
                    data_file.write(',')
            data_file.write('\n')
    
    log_path = file_name.split('.')[0] + '_Logs.csv'

    with open(log_path, 'w') as log_file:
        log_file.write(Log.get_log_schema())
        log_file.write('\n')
        for log in DB_Log:
            log_file.write(log.get_csv_format())
            log_file.write('\n')


def is_there_a_failure() -> bool:
    '''
    Simulates randomly a failure, returning True or False, accordingly
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
    global data_base
    data_base = read_file('CodeAndData/Employees_DB_ADV.csv')
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
                print(f'Transaction No. {index+1} has been commited! Changes are permanent.')
    if must_recover:
        # Call your recovery script
        recovery_script(DB_Log) ### Call the recovery function to restore DB to sound state
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
    
    # commit the data
    write_data('CodeAndData/new_database.csv')

    
main()