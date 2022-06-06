from flask import Flask, jsonify
import sqlite3


def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASII'] = False
    app.config['DEBAG'] = True


    def dp_connect(query):
        connection = sqlite3.connect('animal.db')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result

    @app.route('/<itemid>/')
    def animals_id(itemid):
        query = f"""
                    SELECT 
                        animals_final.animal_id  
                        , animals_final.name  
                        , age_upon_outcome.name
                        , animals_type.name
                        , breeds.name
                        , colors.color 
                        , date_of_birth.name 
                        , outcome.subtype
                        , outcome."type" 
                        , outcome."month" 
                        , outcome."year" 
                    FROM animals_final
                    LEFT JOIN age_upon_outcome ON animals_final.age_upon_outcome_id  = age_upon_outcome.id
                    LEFT JOIN animals_type ON animals_final.type_id  = animals_type.id
                    LEFT JOIN breeds ON animals_final.breed_id  = breeds.id
                    LEFT JOIN animals_colors  ON animals_colors.animals_id  = animals_final.id
                    LEFT JOIN colors ON animals_colors.colors_id = colors.id
                    LEFT JOIN date_of_birth ON animals_final.date_of_birth_id  = date_of_birth.id
                    LEFT JOIN outcome
                        ON outcome.id = animals_final.outcome_id
                    WHERE animals_final.id = {itemid}
                """
        response = dp_connect(query)[0]
        response_json = {
            'animal_id': response[0],
            'name': response[1],
            'age_upon_outcome': response[2],
            'animals_type': response[3],
            'breeds': response[4],
            'animals_colors': response[5],
            'date_of_birth': response[6],
            'outcome_subtype': response[7],
            'outcome_type': response[8],
            'outcome_month': response[9],
            'outcome_year': response[10]
            }
        return jsonify(response_json)


    app.run(debug=True)

if __name__ == '__main__':
    main()


