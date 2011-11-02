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

import cofre.core
from cofre.errors import *

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
    
    def list(self):
        cursor = self.c.cursor()
        results = []
        cursor.execute('SELECT id,key,value FROM store ')        

        for r in cursor:
            record = cofre.core.Record(r[0])
            record.name = r[1]
            record.creds = r[2]
            
            results.append(record)
            
        return results

    def get(self,k):
        cursor = self.c.cursor()
        results = []
        cursor.execute('SELECT id,key,value FROM store WHERE key GLOB ?', [ '*' + k + '*'] )        

        for r in cursor:
            record = cofre.core.Record(r[0])
            record.name = r[1]
            record.creds = r[2]
            
            results.append(record)
            
        return results
    
    def put(self,k,v, identifier=None):
        
        if identifier is None:
            identifier = str(uuid.uuid4())
            
        
        cursor = self.c.cursor()
        cursor.execute("""select * from store where key == ? """, [k])

        if len(cursor.fetchall()) > 0:
            raise DuplicateRecord('record with name %s already exist' % k)
              
        self.c.execute( 'insert into store values(?,?,?,?)', (identifier, k, v, time.time() ))
        self.c.commit()
        
    def delete(self,name): 
        results = self.get(name)
        if len(results) > 1:
             raise Error('more than 1 record matches search pattern, not sure which one to delete')

        if len(results) == 0:
             raise Error('could not find any records that match your search pattern')
        
        self.c.execute("""DELETE FROM store WHERE key == ? """, [name])
        self.c.commit()
        
        