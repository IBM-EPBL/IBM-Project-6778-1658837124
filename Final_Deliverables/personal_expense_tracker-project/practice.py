import ibm_db,ibm_db_dbi

ibm_db_conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cgz83208;PWD=K56N6PSUzD5ZcQ3f",'','')


connection = ibm_db_dbi.Connection(ibm_db_conn)
cursor = connection.cursor()


# cursor.execute('''CREATE TABLE IF NOT EXISTS expense (
# 	id INTEGER NOT NULL, 
# 	user_id INTEGER NOT NULL, 
# 	title VARCHAR(50) NOT NULL, 
# 	category VARCHAR(50) NOT NULL, 
# 	amount FLOAT NOT NULL, 
# 	date DATE , 
# 	PRIMARY KEY (id)
# )''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS user (
# 	id INTEGER NOT NULL, 
# 	email VARCHAR(100) NOT NULL, 
# 	password VARCHAR(100), 
# 	name VARCHAR(1000), 
# 	PRIMARY KEY (id), 
# 	UNIQUE (email)
# )''')
# connection.commit()

# cursor.execute('''INSERT INTO user VALUES (0,'null@null',0,'null');''')
# cursor.execute('''INSERT INTO expense VALUES (0,0,'null','null',123,'1000-01-01')''')
# connection.commit()

cursor.execute('''DROP TABLE user;''')
cursor.execute('''DROP TABLE expense;''')
connection.commit()

print('deleted')
# sql = '''CREATE TABLE IF NOT EXISTS user (
# 	email VARCHAR(100) NOT NULL, 
# 	password VARCHAR(100), 
# 	name VARCHAR(1000),  
# 	UNIQUE (email)
# )'''
# # stmt = ibm_db.prepare(conn, sql)
# # ibm_db.execute(stmt)

# email="guna@gmail.com"
# # password=123
# name='guna'
# sql='''INSERT INTO user VALUES (?,?,?);'''
# stm = ibm_db.prepare(conn, sql)
# ibm_db.bind_param(stm,1,email)
# ibm_db.bind_param(stm,2,password)
# ibm_db.bind_param(stm,3,name)

# ibm_db.execute(stm)

# sql = "SELECT * FROM user WHERE name =?"
# stmt = ibm_db.prepare(conn, sql)
# ibm_db.bind_param(stmt,1,name)
# ibm_db.execute(stmt)
# account = ibm_db.fetch_row(stmt)
# print(account)
# account = ibm_db.fetch_assoc(stmt)
# print(account)
# sql='INSERT INTO expense("user_id","title","category","amount","date") VALUES (1,12,23, abc, 24/12/2002,);'

# #stmt = ibm_db.exec_immediate(conn, sql)
# sql='''DROP TABLE user;'''

# stmt = ibm_db.exec_immediate(conn, sql)
