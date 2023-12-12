import os
import json
import datetime
import requests
import pandas as pd

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

def create_app(test_config=None):
    # flask --app flaskr run --debug
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
        cur.connection.commit()
        return (r[0] if r else None) if one else r

    def query_db_many(query, args=[], one=False):
        cur = db.get_db().cursor()
        cur.executemany(query, args)
        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.commit()
        return (r[0] if r else None) if one else r

    def close_db():
        db.get_db().close()

    # routes
    # return all oil prices.
    @app.route("/all_oil_price", methods=['GET', 'POST', 'PUT', 'DELETE'])
    def all_oil_price():
        if request.method == 'GET':
            query = "SELECT * FROM oil_price ORDER BY date ASC"
            result = query_db(query)
            close_db()
            if result is None:
                return jsonify({"message": "No data in database."}), 404
            return jsonify(result)

    def get_oil_price_from_eia():
        API_KEY = 'qwB5M8S2CmPSzvDeYN79s1vmSehRPMebQC08JBEd'
        url = f'https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={API_KEY}&frequency=daily&data[0]=value&facets[series][]=RWTC&start=1986-01-03&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
        response = requests.get(url)
        data = response.json()
        data_list = data['response']['data']
        # print(data_list)
        return data_list

    # return oil price by date.
    @app.route("/update_price", methods=['POST'])
    def update_price():
        from . import model
        # Get data from ETA
        data_list = get_oil_price_from_eia()
        check_query = "SELECT * FROM oil_price WHERE date = ? ORDER BY date ASC"
        check_result = query_db(check_query, (data_list[0]['period'],))
        print(check_result)
        if not check_result or not check_result[0]['oil_price']:
            print("Re-training started")
            # DRAFT:
            update_query1 = "INSERT OR IGNORE INTO oil_price (date, oil_price) VALUES(?, ?)"
            update_query2 = "UPDATE oil_price SET oil_price = ? WHERE date = ?"
            update_result1 = query_db_many(update_query1, [(x['period'], x['value']) for x in data_list[:7]])
            update_result2 = query_db_many(update_query2, [(x['value'], x['period']) for x in data_list[:7]])
            input_dataframe = pd.DataFrame([(x['period'], x['value']) for x in data_list], columns=['period', 'value'])
            forcast_result = model.predict_oil_price(input_dataframe)
            prediction_query1 = "INSERT OR IGNORE INTO oil_price (date, prediction) VALUES (?, ?)"
            prediction_query2 = "UPDATE oil_price SET prediction = ? WHERE date = ?"
            baseDate = datetime.datetime.strptime(data_list[0]['period'], '%Y-%m-%d')
            prediction_data = [((baseDate+datetime.timedelta(days=i+1)).strftime('%Y-%m-%d'),  list(forcast_result.values)[i]) for i in range(7)]
            prediction_query_result1 = query_db_many(prediction_query1, prediction_data)
            prediction_query_result2 = query_db_many(prediction_query2, [(x[1], x[0]) for x in prediction_data])
            
        
        # Compare with data in the database.
        # query = "SELECT * FROM oil_price"
        # result = query_db(query)
        # If the data is not in the database, insert it.
        # for data in data_list:
        #     if data not in result:
        #         query = "INSERT INTO oil_price (date, price) VALUES (?, ?)"
        #         db.get_db().execute(query, (data['date'], data['value']))
        #         db.get_db().commit()
        query = "SELECT * FROM oil_price ORDER BY date ASC"
        result = query_db(query)
        close_db()
        if result is None:
            return jsonify({"message": "No data in database."}), 404
        return jsonify(result)



    return app
