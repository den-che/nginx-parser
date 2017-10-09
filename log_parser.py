from db import db_session, Log
from sqlalchemy import func
from sqlalchemy import distinct
import os
import sys


def load_log_file(file_path):
    nginx_log_list = []   
    with open(file_path, 'r') as log_file:
        for line in log_file:
        #Can't avoid \n if we don't have construction if
            if line.strip():
                nginx_log_list.append(line)
    return nginx_log_list


def log_parser_code_500(nginx_log):
    code_500 = []
    print(nginx_log) 
    for line in nginx_log:
        item = line.split(" ")
        if item[8] == "500":
            code_500.append(line)
    return code_500


def write_new_log(log_list):
    with open("log_code_500.txt", 'w', encoding='utf-8') as log_500:
        for line in log_list:
            log_500.write(line)


def count_request(log_list):
    count_req = 0
    for line in log_list:
        item = line.split(" ")
        if item[8] == "200" and item[5] == "GET":
            count_req += 1
    return count_req


def nginx_parser(log_list):
    # TODO try to use this iteration once in file
    for line in log_list:
        nginx_data = {}
        item = line.split(" ")
        nginx_data["ip"] = item[0]
        nginx_data["method"] = item[5].strip("\"")
        nginx_data["code"] = item[8] 
        import_to_db(nginx_data)  


def import_to_db(dict_row):
    log = Log(dict_row.get('ip'), dict_row.get('method'), dict_row.get('code'))
    db_session.add(log)
    db_session.commit()   


def delete_records():
    try:
        db_session.query(Log).delete()
        db_session.commit()    
    except:
        db_session.rollback()
        # TODO add error
        # Add Error description
        print("Records was not deleted. Commit was rolled ")
        

def count_column(column_name):
    db_count = db_session.query(func.count(distinct(column_name))).scalar()
    return db_count
    
    
def count_ip():
    # TODO try to use db_session.query(***).scalar() just once
    distinct_ip_num = count_column(Log.IP)
    distinct_code_num = count_column(Log.CODE)
    distinct_method = count_column(Log.METHOD)
    return distinct_ip_num, distinct_code_num, distinct_method  


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please type one of the command! count or fill")
        exit()

    if sys.argv[1] == "fill":
        file_path = "nginx.log"
        # TODO if file not exists
        if not os.path.exists(file_path):
            print("File not found")
        else:
            if file_path.endswith(".txt"):
                nginx_log = load_log_file(file_path)
                log_code_500 = log_parser_code_500(nginx_log)
                print("Request with code 500:\n{}".format(log_code_500))
                write_new_log(log_code_500)
        
                print("-" * 100)
                # TODO if file have wrong format
                delete_records()
                print("All Records in Table deleted!")
                log_data = nginx_parser(nginx_log) 
                print("Log was upload")            
    elif sys.argv[1] == "count":
        num_ip, num_code, num_method = count_ip()
        print("IP: {}, CODE: {}, METHOD: {}".format(num_ip, num_code, num_method))
    else:
        print("Command is wrong. Input another value.")
