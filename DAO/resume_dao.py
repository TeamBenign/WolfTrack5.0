import sqlite3

class Resume:
        def __init__(self, id, username, filepath, position,likes):
            self.id = id
            self.username = username
            self.position = position
            self.filepath = filepath
            self.likes = likes
            
class ResumeDAO:
    def add_resume(self, value_set,db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        print(value_set)
        # Inserting rows into the 'resume' table
        cursor.execute("INSERT INTO resumes (username, fileName, position, likes) VALUES (?, ?, ?, ?)",
                        value_set)
        conn.commit()
        conn.close()
    
    
    def get_all_resumes(self, db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM resumes")
        rows = cursor.fetchall()  # Use fetchall() to get all rows
        conn.close()
        print('resumes ->>>', rows)
        resumes= [Resume(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return resumes
    
    def get_resumes_by_user_name(self, user_name, db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", tables)
        db_path = os.path.abspath(db)
        print(f"Connecting to database: {db_path}")

        cursor.execute("SELECT * FROM resumes WHERE username = ?", (user_name,))
        rows = cursor.fetchall()  # Use fetchall() to get all rows
        resumes= [Resume(row[0], row[1], row[2], row[3]) for row in rows]
        conn.close()
        print('rows ->>>', rows)
        return resumes