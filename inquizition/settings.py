## Debug Mode (Default: False)
debug = False

## Secret Key (Replace with your own secret key) 
secret_key = 'secret' # Doesn't matter too much right now.

#from os.path import expanduser
#home = expanduser("~")
#database_path = 'sqlite:///' + home + '/inquizition.db'
import os

if 'DATABASE_URL' in os.environ:
	database_path = os.environ['DATABASE_URL']
else:
	database_path = 'postgresql://postgres@localhost/inquizition'
