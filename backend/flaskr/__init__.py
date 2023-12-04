import os
import json

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # def query_db(query, args=(), one=False):
    #     cur = db().cursor()
    #     cur.execute(query, args)
    #     r = [dict((cur.description[i][0], value) \
    #               for i, value in enumerate(row)) for row in cur.fetchall()]
    #     cur.connection.close()
    #     return (r[0] if r else None) if one else r
    #
    # my_query = query_db("select * from majorroadstiger limit %s", (3,))
    #
    # json_output = json.dumps(my_query)

    # crontab every Thursday:
    # get_from_website()
    # sql.known.insert(new_data)
    # train()
    # predict()
    # sql.future.remove(new_data)
    # sql.future.insert(future_data)

    # print(json_output)

    def query_db(query, args=(), one=False):
        cur = db.get_db().cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return (r[0] if r else None) if one else r

    # routes
    # return all oil prices.
    @app.route("/all_oil_price", methods=['GET', 'POST', 'PUT', 'DELETE'])
    def all_oil_price():
        # if request.method == 'GET':
        #     query = "SELECT * FROM oil_price"
        #     result = query_db(query)
        #     if result is None:
        #         return "No data in database."
        #     response = json.dumps(result)
        #     response.headers.add('Access-Control-Allow-Origin', '*')
        #     return response
        if request.method == 'GET':
            query = "SELECT * FROM oil_price"
            result = query_db(query)
            if result is None:
                return jsonify({"message": "No data in database."}), 404
            return jsonify(result)


    # oil price of the specific date.
    @app.route("/oil_price", methods=['GET', 'POST', 'PUT', 'DELETE'])
    def oil_price():
        if request.method == 'GET':
            # return oil price of specific date
            date = request.args.get('date')
            query = "SELECT * FROM oil_price WHERE date = %s"
            result = query_db(query, (date,))
            if result is None:
                return "No data in database."
            result_json_output = json.dumps(result)
            return result_json_output

        elif request.method == 'POST':
            # insert new data into database
            if request.is_json:
                content = request.get_json()
                new_data = (content['date'], content['oil_price'])
                query = "INSERT INTO oil_price VALUES (%s, %s)".format(content['date'], content['oil_price'])
                query_db(query, new_data)
                return "Insert successfully."
            else:
                return "Request is not JSON."

        elif request.method == 'PUT':
            # update data in database
            if request.is_json:
                content = request.get_json()
                new_data = (content['oil_price'], content['date'])
                query = "UPDATE oil_price SET oil_price = %s WHERE date = %s"
                query_db(query, new_data)
                return "Update successfully."
            else:
                return "Request is not JSON."

        elif request.method == 'DELETE':
            # delete data in database
            if request.is_json:
                content = request.get_json()
                date = content['date']
                query = "DELETE FROM oil_price WHERE date = %s"
                query_db(query, (date,))
                return "Delete successfully."
            else:
                return "Request is not JSON."


    return app