from __init__ import CURSOR, CONN


class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Department instances """
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()
    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Department instances """
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
            """Save the department instance to the database."""
            if self.id is None:
                sql= """INSERT INTO departments(name, location)VALUES(?, ?)"""
                CURSOR.execute(sql,(self.name, self.location))
                self.id = CURSOR.lastrowid
            else:
                sql ="""
                    UPDATE departments
                    SET name = ?, location = ?
                    WHERE id = ?
                     """
                CURSOR.execute(sql, (self.name, self.location, self.id))
                CONN.commit()

    def update(self):
         if self.id is None:
              raise ValueError("Cannot update ..")
         sql ="""
             UPDATE departments
             SET name = ?, location = ?
             WHERE id = ?
          """
         CURSOR.execute(sql,(self.name, self.location, self.id))
         CONN.commit()
    def delete(self):
        """Delete the Department instance from the database."""
        if self.id is None:
            raise ValueError("Cannot delete a department that hasn't been saved yet.")

        sql = """
            DELETE FROM departments
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
    @classmethod
    def create(cls, name, location):
         """create and save new department instance to the database."""
         department = cls(name, location)
         #save to the db which will assign an id
         department.save()
         return department
Department.create_table()
department = Department.create("Payroll", "Building A, 5th Floor")
print(department)

@classmethod
def find(cls, id):
        """Find a Department instance by its ID."""
        sql = """
            SELECT id, name, location
            FROM departments
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls(*row)
        else:
            return None