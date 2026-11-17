"""Run persistent local Windows paper worker: python worker.py"""
import logging
from engine import run_worker
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
if __name__=='__main__': run_worker()
