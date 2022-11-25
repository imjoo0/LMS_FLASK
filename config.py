#db
db = {
    'user' : 'root',
    'password' : 'wndud234',
    'host' : 'localhost',
    'port' : 3306,
    'database' : 'test'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"