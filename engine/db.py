import sqlite3
con= sqlite3.connect("Peak.db")
cursor= con.cursor()
query="CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)
#query="INSERT INTO sys_command VALUES(null,'whatsapp','C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
#cursor.execute(query)
#con.commit()
query="CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100),url VARCHAR(1000))"
cursor.execute(query)
query="INSERT INTO web_command VALUES(null,'whatsapp','https://web.whatsapp.com/')"
cursor.execute(query)
con.commit()