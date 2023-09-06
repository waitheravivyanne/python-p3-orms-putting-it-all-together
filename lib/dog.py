import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS dogs')
        CONN.commit()

    def save(self):
        if self.id is None:
         CURSOR.execute('''
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        ''', (self.name, self.breed))
         CONN.commit()
         self.id = CURSOR.lastrowid
        else:
            CURSOR.execute('UPDATE dogs SET name = ?, breed = ? WHERE id = ?', (self.name, self.breed, self.id))
            CONN.commit()
            return self

    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        new_dog.id = CURSOR.lastrowid
        return new_dog

    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        new_dog = cls(name, breed)
        new_dog.id = id
        return new_dog

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM dogs')
        rows = CURSOR.fetchall()
        dogs_list = [cls.new_from_db(row) for row in rows]
        return dogs_list

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, dog_id):
        CURSOR.execute('SELECT * FROM dogs WHERE id = ?', (dog_id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        CURSOR.execute('SELECT * FROM dogs WHERE name = ? AND breed = ?', (name, breed))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            CURSOR.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (name, breed))
            CONN.commit()
            new_dog_id = CURSOR.lastrowid
            return cls(name, breed, id=new_dog_id)

    def update(self):
        if self.id is None:
            raise ValueError("Can't update a dog that hasn't been saved yet")

        CURSOR.execute('UPDATE dogs SET name = ? WHERE id = ?', (self.name, self.id))
        CONN.commit()
