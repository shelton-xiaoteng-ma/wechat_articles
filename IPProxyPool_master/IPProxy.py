# coding:utf-8
from multiprocessing import Value, Queue, Process
import sys
sys.path.append("..")
from IPProxyPool_master.api.apiServer import start_api_server
from IPProxyPool_master.db.DataStore import store_data

from IPProxyPool_master.validator.Validator import validator, getMyIP
from IPProxyPool_master.spider.ProxyCrawl import startProxyCrawl

from IPProxyPool_master.config import TASK_QUEUE_SIZE

if __name__ == "__main__":
    myip = getMyIP()
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue(maxsize=TASK_QUEUE_SIZE)
    q2 = Queue()
    p0 = Process(target=start_api_server)
    p1 = Process(target=startProxyCrawl, args=(q1, DB_PROXY_NUM,myip))
    p2 = Process(target=validator, args=(q1, q2, myip))
    p3 = Process(target=store_data, args=(q2, DB_PROXY_NUM))
    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p0.join()
    p1.join()
    p2.join()
    p3.join()
