## Cofre is a simple tool for managing passwords

# What makes cofre serendipitous:
* You don't need another password (it uses your SSH keys)
* You can store anything in it, username/password combinations, ssn, etc...
* Pretty much everything is encrypted using RSA keys

## Cofre Primer:

### first we get it installed:

	$ sudo pip install cofre
	
#### then we initialize it's database:

	$ cofre --init
	initializing config: /home/rafael/.cofre/cofre.cfg
	
### now we can start storing secrets:

	$ cofre put mysite.com raf@ophion.org:mypassword
	created a new record for [mysite.com] with creds: [raf@ophion.org:mypassword]

cofre can also auto generate a password for you:

	$ cofre put mybank raf@ophion.org:
	created a new record for [mybank] with creds: [raf@ophion.org:3QZ8YKaU6x]

*note that all we had to do was end the credentials with a ':'*

### looking something up is also simple:

	$ cofre get bank
	results:
	+----------+--------+---------------------------+
	|    id    |  name  |           creds           |
	+----------+--------+---------------------------+
	| b634a168 | mybank | raf@ophion.org:3QZ8YKaU6x |
	+----------+--------+---------------------------+

cofre performs fuzzy searches so it will returns the record(s) that closest match what you types

### viewing all entries in the database:

	$ cofre list
	results:
	+----------+------------+---------------------------+
	|    id    |    name    |           creds           |
	+----------+------------+---------------------------+
	| f53521f3 | mysite.com | raf@ophion.org:mypassword |
	| b634a168 | mybank     | raf@ophion.org:3QZ8YKaU6x |
	+----------+------------+---------------------------+

### deleting a record from the database:

	$ cofre del mybank
	record deleted.

### export & import:

cofre exports its database as unencrypted json:
	
	$ cofre export
	{
	    "records": [
	        {
	            "id": "f53521f3-cf5e-4cd3-a881-4309e34fbb6e", 
	            "creds": "raf@ophion.org:mypassword", 
	            "name": "mysite.com"
	        }
	    ], 
	    "cofre": "export", 
	    "version": "0.2.2", 
	    "generated": "Wed Nov 17 21:46:34 2010"
	}

and can import json back:

	cofre import /tmp/export.txt 
	importing entries from /tmp/export.txt
	1 records successfully imported.
			
### Troubleshooting:

####  Issues with m2crypto

M2Crypto is a library used for the RSA encryption and it prob will not install cleanly via pip (crap, I know). I suggest either using your platform package manager or downloading it directly from http://chandlerproject.org/bin/view/Projects/MeTooCrypto


#### SSH Keys 

Make sure you have a RSA SSH key (ssh-keygen is your friend). The actual location of the SSH key file can be changed by editing your cofre.cfg file


	