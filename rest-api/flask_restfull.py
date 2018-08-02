from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import zabbix_cloud

app = Flask(__name__)
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


parser = reqparse.RequestParser()
parser.add_argument('task')


class History(Resource):
    def get(self, k, item_id):
        return zabbix_cloud.get_history_by_itemid(k, item_id)


class Discovery(Resource):
    def get(self, item_id):
        return zabbix_cloud.get_metrics_by_uuid(item_id)


api.add_resource(Discovery, '/discovery/<item_id>')
api.add_resource(History, '/history/<k>/<item_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
