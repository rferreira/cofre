#!/usr/bin/env python
# encoding: utf-8
"""
store.py

Created by Rafael Ferreira on 2010-10-18.
Copyright (c) 2010 Uva Software, LLC. All rights reserved.
"""

import os
import sqlite3
import logging
import time
import uuid

log = logging.getLogger(__name__)

class SQLStore:
    
    def __init__(self, config):
        self.path = config.get('cofre','store')
        self.c = sqlite3.connect(self.path)
        self.c.text_factory = str
        
        try:
            self.c.execute('create table store (id text primary key, key text, value text, timestamp float)')
        except sqlite3.OperationalError:
            pass
    

    def get(self,k):
        cursor = self.c.cursor()
        cursor.execute('select value from store where key=?', [k] )        

        for r in cursor:
            return r
            
        return None
    
    def put(self,k,v):        
        self.c.execute( 'insert into store values(?,?,?,?)', ( str(uuid.uuid4()), k, v, time.time() ))
        self.c.commit()
        
        