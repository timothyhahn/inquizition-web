## Debug Mode (Default: False)
debug = True

## Secret Key (Replace with your own secret key0
secret_key = 'secret'

from os.path import expanduser
home = expanduser("~")
database_path = 'sqlite:///' + home + '/test.db'
print database_path
