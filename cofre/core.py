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
from Crypto.Cipher import AES
import base64
from random import choice
import hashlib

import cofre.store

log = logging.getLogger(__name__)

class Error(Exception):
    pass

class Cofre:
    commands = ['put', 'get', 'dump']
    
    def __init__(self, config_file):            
        self.config = ConfigParser.ConfigParser()
        log.debug('parsing config file %s ' % config_file)
        self.config.read(config_file)    
        log.debug(self.config)
        log.info('using store: %s' % self.config.get('cofre','store'))
        log.info('using engine: %s' % self.config.get('cofre','engine'))
        
        self.store = cofre.store.SQLStore(self.config)
        
            
    def get(self, key):
        encrypted_password = self.store.get(key)
        return self.decrypt(encrypted_password, 'secret')
             
    def put(self, key, value):
        self.store.put(key,value)
        
    def parse(self, command, val):
        
        if command not in self.commands:
            raise Exception('invalid command: %s' % command)
            
        if command == 'put':
            if len(val) is 0:
                raise Error('what should we call this?')
                                
            password = self.generate_password()
            encrypted_password = self.encrypt(password,'secret')
            
            log.debug('encrypted password:%s' % encrypted_password)
                    
            self.put(val, encrypted_password )
            
            print('creating new entry for [%s] using password: %s' % (val, password))
            
        
        if command == 'get':
            if len(val) is 0:
                raise Error('please enter the name of what you are looking for.')
            
            p = self.get(val)
            
            print('password for key [%s] is: ' % (val,p) )
            
            
    def encrypt(self, value, secret):
        secret = hashlib.md5(secret).hexdigest()
        
        c = AES.new( secret, AES.MODE_ECB)
                        
        return c.encrypt(value)
     
    def decrypt(self, value, secret):
        log.info('decrypting %s' % value)
        secret = hashlib.md5(secret).hexdigest()

        # create a cipher object using the random secret
        c = AES.new(secret, AES.MODE_ECB)
                        
        return c.decrypt(value.encode('utf-8'))
         

    def generate_password(self, length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        """
        simple password generation logic, lifted from:
        http://code.djangoproject.com/browser/django/trunk/django/contrib/auth/models.py
        """        
        return ''.join([choice(allowed_chars) for i in range(length)])
        