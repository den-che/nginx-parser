from db import db_session, Log
from sqlalchemy import func
from sqlalchemy import distinct
import os
import sys


def main_parser_nginx(file_path):
    code_500 = []
    count_method_code = 0   
    with open(file_path, 'r') as log_file:
        for line in log_file:
            if line.strip():
                code_500 += log_parser_code_500(line)
                nginx_parser(line)
                count_method_code = count_request(line,count_method_code)
        db_session.commit()
        print("Records number with CODE =200 and METHOD = GET: {}".format(count_method_code))

    write_new_log(code_500)   
    print("Log with CODE=500 was write in new file")    


def log_parser_code_500(line):
        code_500 = []
        item = line.split(" ")
        if item[8] == "500":
            code_500.append(line)
        return code_500


def write_new_log(log_list):
    with open("log_code_500.txt", 'w', encoding='utf-8') as log_500:
        for line in log_list:
            log_500.write(line)


def count_request(line, count_req=0):
    item = line.split(" ")
    method_post = item[5].strip("\"")
    if item[8] == "200" and method_post == "GET":
            count_req += 1
    return count_req


def nginx_parser(line):
    nginx_data = {}
    item = line.split(" ")
    nginx_data["ip"] = item[0]
    nginx_data["method"] = item[5].strip("\"")
    nginx_data["code"] = item[8] 
    import_to_db(nginx_data)  


def import_to_db(dict_row):
    log = Log(dict_row.get('ip'), dict_row.get('method'), dict_row.get('code'))
    db_session.add(log)
       


def delete_records():
    try:
        db_session.query(Log).delete()
        db_session.commit()
        return True    
    except:
        db_session.rollback()
        print("Records was not deleted. Commit was rolled ")
        return False

def count_column(column_name):
    db_count = db_session.query(func.count(distinct(column_name))).scalar()
    return db_count
    
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please type one of the command! count or upload")
        exit()

    if sys.argv[1] == "upload":
        file_path = "nginx.log"
        if not os.path.exists(file_path):
            print("File not found")
            exit()
        
        if delete_records() is True:
            print("All Records in Table deleted!")
                
        main_parser_nginx(file_path)             
        print("Log was upload")            
    elif sys.argv[1] == "count":
        print("IP: {}, CODE: {}, METHOD: {}".format(count_column(Log.IP), count_column(Log.CODE), count_column(Log.METHOD)))
    else:
        print("Command is wrong. Input another value.")
