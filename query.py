import sqlite3


def connect(query):
    connection = sqlite3.connect('animal.db')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    return result

def main():
    creat_age_upon_outcome = """
        CREATE TABLE IF NOT EXISTS age_upon_outcome
    (
       id INTEGER PRIMARY KEY AUTOINCREMENT
        , name VARCHAR(50)
    )
    """

    creat_animals_type = """
        CREATE TABLE IF NOT EXISTS animals_type
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        , name VARCHAR(50)
    )
        """

    creat_breeds = """
        CREATE TABLE IF NOT EXISTS breeds
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        , name VARCHAR(50)
    )
     """

    creat_colors = """
        CREATE TABLE IF NOT EXISTS colors 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        color VARCHAR(50) 
    )
     """

    creat_animals_colors = """
        CREATE TABLE IF NOT EXISTS animals_colors
    (
        animals_id INTEGER,
        colors_id INTEGER,
        FOREIGN KEY (animals_id) REFERENCES animals_final(id)
        FOREIGN KEY (colors_id) REFERENCES colors(id)
    )
     """

    creat_date_of_birth = """
        CREATE TABLE IF NOT EXISTS date_of_birth
    (
       id INTEGER PRIMARY KEY AUTOINCREMENT
        , name VARCHAR(50)
    )
     """

    creat_outcome = """
    CREATE TABLE IF NOT EXISTS outcome
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        , subtype VARCHAR(50)
        , 'type' VARCHAR(50)
        , 'month' INTEGER
        , 'year'  INTEGER
    )
     """


    creat_animals_final = """
    CREATE TABLE IF NOT EXISTS animals_final
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        , animal_id VARCHAR(50)
        , name VARCHAR(50)
        , age_upon_outcome_id INTEGER
        , type_id INTEGER
        , breed_id INTEGER
        , date_of_birth_id INTEGER
        , outcome_id INTEGER
        , FOREIGN KEY(age_upon_outcome_id) REFERENCES age_upon_outcome(id)
        , FOREIGN KEY(type_id) REFERENCES animals_type(id)
        , FOREIGN KEY(breed_id) REFERENCES breeds(id)
        , FOREIGN KEY(date_of_birth_id) REFERENCES date_of_birth(id)
        , FOREIGN KEY(outcome_id) REFERENCES outcome(id)
    )
    """


    insert_age_upon_outcome = """
        INSERT INTO age_upon_outcome (name) 
        SELECT DISTINCT
            animals.age_upon_outcome 
        FROM animals
    """

    insert_animals_type = """
        INSERT INTO animals_type (name) 
        SELECT DISTINCT
            animals.animal_type 
        FROM animals
    """

    insert_breeds = """
        INSERT INTO breeds (name) 
        SELECT DISTINCT
            animals.breed  
        FROM animals
    """

    insert_colors = """
        INSERT INTO colors (color)
        SELECT DISTINCT *
        FROM 
        (
            SELECT DISTINCT 
                color1 AS color
            FROM animals
            UNION ALL
            SELECT DISTINCT 
                color2 AS color
            FROM animals
        )
    """

    insert_animals_colors = """
        INSERT INTO animals_colors (animals_id, colors_id)
        SELECT DISTINCT 
            animals_final.id , colors.id 
        FROM animals 
        JOIN colors 
            ON colors.color = animals.color1 
        JOIN animals_final 
            ON animals_final.animal_id = animals.animal_id 
        UNION ALL 
        SELECT DISTINCT  
            animals_final.id , colors.id 
        FROM animals 
        JOIN colors ON colors.color = animals.color2
        JOIN animals_final 
            ON animals_final.animal_id = animals.animal_id
    """

    insert_date_of_birth = """
        INSERT INTO date_of_birth (name) 
        SELECT DISTINCT
            animals.date_of_birth  
        FROM animals
    """

    insert_outcome = """
        INSERT INTO outcome (subtype, "type", "month", "year")
        SELECT DISTINCT
            animals.outcome_subtype,
            animals.outcome_type,
            animals.outcome_month,
            animals.outcome_year 
        FROM animals
    """


    insert_animals_final = """
    INSERT INTO animals_final (animal_id, name, age_upon_outcome_id, type_id, breed_id, date_of_birth_id, outcome_id)
    SELECT 
        animals.animal_id, animals.name, age_upon_outcome.id, animals_type.id,  breeds.id, date_of_birth.id, outcome.id 
    FROM animals
    JOIN age_upon_outcome 
        ON age_upon_outcome.name = animals.age_upon_outcome
    JOIN animals_type 
        ON animals_type.name  = animals.animal_type
    JOIN breeds 
        ON breeds.name = animals.breed
    JOIN date_of_birth 
        ON date_of_birth.name = animals.date_of_birth 
    left JOIN outcome
        ON outcome.subtype  = animals.outcome_subtype
        AND outcome."type" = animals.outcome_type 
        AND outcome."month" = animals.outcome_month 
        AND outcome."year" = animals.outcome_year
    """

if __name__ == '__main__':
    main()

