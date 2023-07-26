import psycopg2

def CreatTable():
    with conn.cursor() as cur:
        cur.execute("""
        			DROP TABLE Client_Phone;
        			DROP TABLE Client;
        			""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Client(
    	        client_id SERIAL PRIMARY KEY,
    	        firstname VARCHAR(30) NOT NULL,
    	        lastname VARCHAR(30) NOT NULL,
    	        email VARCHAR(30) UNIQUE 
    	    );
                """)
        cur.execute("""
     	    CREATE TABLE IF NOT EXISTS Client_Phone(
                client_id INTEGER REFERENCES Client(client_id),
    	        phone CHAR(11) UNIQUE
            );""")

def AddClient(firstname, lastname, email):
    with conn.cursor() as cur:
        cur.execute("""
     	    INSERT INTO Client(firstname, lastname, email)
     	    VALUES(%s, %s , %s);
     	    """, (firstname, lastname, email))

def AddPhone(phone, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Client_Phone(client_id, phone)
            VALUES(%s, %s);
            """, (client_id, phone))

def Change_Client(client_id, firstname = None, lastname = None, email = None):
    with conn.cursor() as cur:
        if firstname != None:
            cur.execute("""
                UPDATE Client
                SET firstname=%s
                WHERE client_id=%s;
                """, (firstname, client_id))
        if lastname != None:
            cur.execute("""
                UPDATE Client
                SET lastname=%s
                WHERE client_id=%s;
                """, (lastname, client_id))
        if email != None:
            cur.execute("""
                UPDATE Client
                SET email=%s
                WHERE client_id=%s;
                """, (email, client_id))

def Delete_Phone(phone, client_id):
    with conn.cursor() as cur:
        cur.execute("""
		    DELETE FROM Client_Phone
		    WHERE client_id=%s AND phone=%s;
		    """, (client_id, phone))

def Delete_Client(client_id):
    with conn.cursor() as cur:
        cur.execute("""
        	DELETE FROM Client_Phone
        	WHERE client_id=%s;
        	""", (client_id))
        cur.execute("""
    		DELETE FROM Client
    		WHERE client_id=%s;
    		""", (client_id))

def Find_Client (firstname=None, lastname=None, email=None, phone=None):
    with conn.cursor() as cur:
	    cur.execute("""
		    SELECT firstname, lastname, email, phone
		    FROM Client c
		    LEFT JOIN Client_Phone cp ON c.client_id = cp.client_id
		    WHERE   (firstname=%s OR %("firstname")s IS NULL) AND
		            (lastname=%s OR %("lastname")s IS NULL) AND
		            (email=%s OR %("email")s IS NULL) AND
		            (phone=%s OR %("phone")s IS NULL)
		    """,{"firstname":firstname, "lastname":lastname, "email":email, "phone":phone})

with psycopg2.connect(database="Project1", user="postgres", password="Belik67306") as conn:
    CreatTable()
    AddClient("Oleg", "Bush", "uhfuiehf@gmail.com")
    AddPhone("364574", 1)
    Change_Client("Oleg", "Push", "dshfihfdl@yandex.ru")
    Delete_Phone("364574", 1)
    Find_Client("Oleg", "Gush","dhgffhsddghf@gmail.com", "364574")
    Delete_Client(1)

cur.close()
conn.close()