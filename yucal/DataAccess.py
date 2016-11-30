import sqlite3

db = sqlite3.connect("C:/Users/ilana/yuData.db")
curse = db.cursor();

dbFile = db.execute("SELECT * FROM events");
results = dbFile.fetchall();

print(results);

print("DB read complete");

db.close();

