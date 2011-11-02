#!/usr/bin/env python
# encoding: utf-8
"""
core.py

Created by Rafael Ferreira on 2010-10-18.
Copyright (c) 2010 Uva Software, LLC. All rights reserved.
"""
import ConfigParser
import sys
import logging
import os, os.path
from random import choice
from datetime import datetime
import hashlib
import json
import subprocess
import prettytable

from cofre import __version__ as version
import cofre.store
import cofre.simplesecure as ss
from cofre.errors import *

log = logging.getLogger(__name__)


class Record:
    def __init__(self, n=None):
        self.id = n
        
    def to_dict(self):
        return {
            'id'    : self.id,
            'name'  : self.name,
            'creds'  : self.creds,
        }
    
    @staticmethod
    def from_dict(d):
        record = Record(d['id'])
        record.name = d['name'].strip()
        record.creds = d['creds'].strip()

        return record
        
    def decrypt(self):        
        self.creds = ss.decrypt(self.creds)        
    
    def encrypt(self):
        self.creds = ss.encrypt(self.creds)

class Cofre:
        
    commands = {
        'put':'creates a new record, example: put mybank.com user:12323kd',
        'get':'retries records using fuzzy logic, example: get mybank',
        'list':'lists all managed credentials',
        'del':'deletes a record, example: del mybank.com',
        'export':'json exports the password database',
        'import':'loads a json export, example: import file.txt',        
    }
    
    def __init__(self, settings):
        log.debug(settings)        
        self.config = ConfigParser.ConfigParser()
        log.debug('parsing config file %s ' % settings['config'])
        self.config.read(settings['config'])    
        log.debug(self.config)
        log.info('using store: %s' % self.config.get('cofre','store'))
        log.info('using engine: %s' % self.config.get('cofre','engine'))
        log.info('using key: %s' % self.config.get('cofre','key'))
        self.store = cofre.store.SQLStore(self.config)      
        self.settings = settings  

    def list(self):
        results = self.store.list()
        for r in results:
            r.decrypt()            
        return results
        
    def delete(self, name):
        log.debug('deleting record %s '  % name)
        return self.store.delete(name)
            
    def get(self, key):
        results = self.store.get(key)
        
        for r in results:
            r.decrypt()
        
        return results
             
    def put(self, record):
        record.encrypt()
        self.store.put(record.name, record.creds, identifier=record.id)

    def pprint(self, results):
        x = prettytable.PrettyTable([
            'id', 'name', 'creds'
            ])
       
        x.sortby = 'name'
        x.set_field_align('name', 'l')
        x.set_field_align('creds', 'l')

                
        for r in results:               
            x.add_row( [ r.id[:8], r.name, r.creds ] )

        print('results:')    
        print(x)             


        # are we running in quick mode? if so copy the single result to the clipboard
        if self.settings.get('quick', False) is True:
            if len(results) == 1:
                username, password = results[0].creds.split(':')
                log.debug('copying password to clip')
                cmd = 'echo %s | %s' % (password, self.config.get('cofre','clipboard'))                
                subprocess.call(cmd, shell=True)
                print('password is ready to be pasted.')
                




    def generate_password(self, length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        """
        simple password generation logic, lifted from:
        http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/models.py
        """        
        return choice('1234567890') + ''.join([choice(allowed_chars) for i in range(length-1)])

    
    def parse(self, args):
        """
        parsers and runs the correct command
        """
        
        command = args[0]
        
        if command not in self.commands.keys():
            raise Error('invalid command: %s' % command)
            
        log.debug('loading private key')
        ss.load(self.config.get('cofre','key'))
        log.debug('done')    
            
        if command == 'put':
            if len(args) == 1:
                raise Error('what should we call this?')
                
            elif len(args) == 2:
                raise Error('what should we store?')

            record = Record()
            record.name = args[1]    
            
            if len(args) == 3:      
                if args[2][-1] == ':':
                      record.creds = args[2] + self.generate_password()
                                
                else:      
                    record.creds = args[2]
                                   
            self.put(record)
            record.decrypt()
            
            print('created a new record for [%s] with creds: [%s]' % (record.name, record.creds))
            
        
        elif command == 'get':
            if len(args) is 1:
                raise Error('please enter the name of what you are looking for.')
            
            results  = self.get(args[1])
            
            if len(results) == 0:
                print('oops, we could not find anything that matches')
                sys.exit(1)
                
            self.pprint(results)
                        
        
        elif command == 'del':   
            if len(args) is 1:
                raise Error('please enter the name of the record to be deleted.')                         
                
            self.delete(args[1])
            
            print('record deleted.')
            
        elif command == 'list':
            self.pprint(self.list())
            
        elif command == 'export':
            r = self.list()
            exp = { 
                'cofre' : 'export',
                'version'  : version,
                'generated'     : datetime.now().ctime()
            }
            exp['records'] = [ record.to_dict() for record in r ]
            print json.dumps( exp, indent=4)
            
        elif command == 'import':
            if len(args) is 1:
                raise Error('usage: cofre import FILENAME - looks like you forgot the file name')
                
            print('importing entries from %s' % args[1])
            
            d = json.load(open(args[1]))
            c = 0
                        
            for entry in d['records']:
                try:
                    record = Record.from_dict(entry)                    
                    log.debug('saving new record with id %s' % record.id)
                    self.put(record)
                    c += 1
                except Exception, ex:
                    print('error importing record - it will be skipped' )
                    log.exception(ex)   
            
            print('%d records successfully imported.' % c)
                             
        sys.exit(0)    
    
    
        