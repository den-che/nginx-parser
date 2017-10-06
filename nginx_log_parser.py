from db import db_session, Log
from sqlalchemy import func
from sqlalchemy import distinct
import os
import re
import sys 

code_500 = []
nginx_log_list = []
nginx_data_list = []


def load_log_file(filepath):
    if not os.path.exists(filepath):
        return None
    else:
        with open(filepath,'r') as log_file:
            for line in log_file:
                if line.strip():
                    nginx_log_list.append(line) 
        return nginx_log_list       


def log_parser_code_500(nginx_log):
    for line in nginx_log:
        if (line.find(" 500 ")!=-1):
            code_500.append(line)
    return code_500


def write_new_log(log_list):
    with open("log_code_500.txt",'w', encoding='utf-8') as log_500:
        for line in log_list:
            log_500.write(line)


def count_request(log_list):
    count_req = 0
    for line in log_list:
        if (line.find(" 200 ")!=-1 and (line.find("GET"))):
            count_req+=1
    return count_req


def nginx_parser(log_list):
    for line in log_list:
        nginx_data = {}
        item = line.split(" ")
        nginx_data["ip"] = item[0]
        nginx_data["method"] = item[5].strip("\"")
        nginx_data["code"] = item[8] 
        nginx_data_list.append(nginx_data)
    return nginx_data_list


def import_to_db(log_data_list):
    for dict_row in log_data_list:
        log = Log(dict_row.get('ip'),dict_row.get('method'),dict_row.get('code'))
        db_session.add(log)
    db_session.commit()   


def delete_records():
    try:
        deleted_rows = db_session.query(Log).delete()
        db_session.commit()    
    except:
        db_session.rollback()


def count_ip():
    distict_ip_num = db_session.query(func.count(distinct(Log.IP))).scalar()
    distict_code_num = db_session.query(func.count(distinct(Log.CODE))).scalar()
    distinct_method = db_session.query(func.count(distinct(Log.METHOD))).scalar()
    return distict_ip_num, distict_code_num, distinct_method  


if __name__ == "__main__":
    try:
        if sys.argv[1] == "full":
            nginx_log = load_log_file("nginx.log")
            log_code_500 = log_parser_code_500(nginx_log)
            print ("Request with code 500:\n{}".format(log_code_500))
            write_new_log(log_code_500)

            print("-"*100)
            log_data = nginx_parser(nginx_log)
            delete_records()
            print("All Records in Table deleted!")
            
            import_to_db(log_data)
            print("Log was upload")
        elif sys.argv[1] == "count":       
            num_ip, num_code, num_method = count_ip()
            print("IP: {}, CODE: {}, METHOD: {}".format(num_ip, num_code, num_method))
        else:
            print("Command is wrong. Input another value.")
    except(IndexError):
        print("Please type one of the command! count or full")    

