'''
Created on 2009-12-24

@author: Administrator
'''
import socket
import time

M = 99999999
length_of_berth = 90#bits
penalty_of_arrival_before = 1.0
penalty_of_arrival_after = 1.0
penalty_of_delay_beyond_due = 2.0
penalty_of_not_at_favorite_position = 1.0
total_time = 72
extra_time = 10
max_crane = 2
speed_row = 4#15
speed_column =2# 5
num_of_period = 4
num_of_yc =30
basic_date = "10/12/20"
begin_date = 20

block_list=["A1","B1","C1","D1",
            "A2","B2","C2","D2",
            "A3","B3","C3","D3",
            "A4","B4","C4","D4",
            "A5","B5","C5","D5",
            "A6","B6","C6","D6",
            "A7","B7","C7","D7",
            "A8","B8","C8","D8",
            "A9","B9","C9","D9"]

yc_list = ["YC1","YC2","YC3","YC4","YC5","YC6","YC7","YC8","YC9","YC10",
           "YC11","YC12","YC13","YC14","YC15","YC16","YC17","YC18","YC19","YC20",
           "YC21","YC22","YC23","YC24","YC25","YC26","YC27","YC28","YC29","YC30",
           "YC31","YC32","YC33","YC34","YC35","YC36","YC37","YC38","YC39","YC40"]
port = {'tos_server':8000,
        'MDI_test':8999}

child_id = {'operator':901,
            'yc_plan':902,
            'berth_plan':903,
            'pre-marshalling_plan':904}

job_queue=[]

def request_handler(server, _job_queue):
    state='OK'
    #print 'state at first', state
    while True:
        while _job_queue:
            if state=='OK':
                time.sleep(0.1)
                state=''
                print 'state after state==', state
                job=_job_queue.pop(0)
                state=job()
                print 'state after state=job()', state
                time.sleep(0.1)
            else:
                time.sleep(0.2)
        time.sleep(0.2)
        try:
            request, client_address = server.get_request()
            request.setblocking(True)
        except socket.error:
            continue
        if server.verify_request(request, client_address):
            try:
                server.process_request(request, client_address)
            except:
                server.handle_error(request, client_address)
                server.close_request(request)
                




