#!/usr/Python3

import requests, json, argparse, datetime, time, http
from rich.progress import track

class Experiment():

    def __init__(self):
        self._api_host = "webapi"
        self._api_port = "3000"
        self._db_host = "mongo"
        self._db_port = "27017"
        self._content_type_header = "application/json; charset=utf-8"
        self._authorization_mechanism = "SCRAM-SHA-1"
        self._authorization_token = ""
        self._batch_ids = []
        self._batch_results = []

    def set_api_url(self, host, port):
        assert isinstance(host, str) and isinstance(port, str)
        self._api_host = host
        self._api_port = port

    def set_db_url(self, host, port):
        assert isinstance(host, str) and isinstance(port, str)
        self._db_host = host
        self._db_port = port

    def _get_api_url(self):
        return "{}:{}".format(
            self._api_host,
            self._api_port
        )

    def _get_db_url(self):
        return "{}:{}".format(
            self._db_host,
            self._db_port
        )

    def _get_standard_header(self):
        return {
            "Content-Type": self._content_type_header
        }

    def _get_authorization_header(self):
        return {
            "Content-Type": self._content_type_header,
            "Authorization": "Bearer {}".format(self._authorization_token)
        }

    def _get_registration_data(self, username, email, password):
        assert isinstance(username, str) and isinstance(email, str) and isinstance(password, str)
        return {
            "username": username,
            "email": email,
            "password": password
        }

    def _get_experiment_data(self, db_name, collection_name, raw_schema_format):
        assert isinstance(db_name, str) and isinstance(collection_name, str) and isinstance(raw_schema_format, bool)
        return {
            "authentication": {
                "authMechanism": self._authorization_mechanism
            },
            "port": self._db_port,
            "address": self._db_host,
            "databaseName": db_name,
            "collectionName": collection_name,
            "rawSchemaFormat": raw_schema_format
        }

    def _get_login_data(self, email, password):
        return {
            "email": email,
            "password": password
        }

    def _get_datetime(self, result, date_field):
        assert isinstance(result, object) and isinstance(date_field, str)
        return datetime.datetime.strptime(result[date_field], '%Y-%m-%dT%H:%M:%S.%fZ')

    def _calculate_datetime_deltas(self, result):
        start_date = self._get_datetime(result, 'startDate')
        extraction_date = self._get_datetime(result, 'extractionDate')
        ordered_aggregation_date = self._get_datetime(result, 'orderedAggregationDate')
        unordered_aggregation_date = self._get_datetime(result, 'unorderedAggregationDate')
        union_date = self._get_datetime(result, 'unionDate')
        end_date = self._get_datetime(result, 'endDate')
        assert isinstance(start_date, datetime.datetime) \
            and isinstance(extraction_date, datetime.datetime) \
            and isinstance(end_date, datetime.datetime)
        union_time_delta = union_date - start_date
        total_time_delta = end_date - start_date
        extraction_time_to_total_time_ratio = union_time_delta / total_time_delta
        return {
            union_time_delta: union_time_delta,
            total_time_delta: total_time_delta,
            extraction_time_to_total_time_ratio: extraction_time_to_total_time_ratio
        }

    def register(self, username, email, password):
        assert isinstance(username, str) \
            and isinstance(email, str) \
            and isinstance(password, str)
        requests.post(
            "http://{}/api/register".format(self._get_api_url()),
            headers = self._get_standard_header(),
            json = self._get_registration_data(username, email, password)
        )

    def login(self, email, password):
        assert isinstance(email, str) and isinstance(password, str)
        response = requests.post(
            "http://{}/api/login".format(self._get_api_url()),
            headers = self._get_standard_header(),
            json = self._get_login_data(email, password)
        )
        self._authorization_token = response.json()['token']

    def run(self, db_name, collection_name, raw_schema_format=False):
        assert isinstance(db_name, str) \
            and isinstance(collection_name, str) \
            and isinstance(raw_schema_format, bool)
        data = self._get_experiment_data(db_name, collection_name, raw_schema_format)
        response = requests.post(
            "http://{}/api/batch/rawschema/steps/all".format(self._get_api_url()),
            headers = self._get_authorization_header(),
            json = self._get_experiment_data(db_name, collection_name, raw_schema_format)
        )
        self._batch_ids.append(response.json()['batchId'])
        print("Status:", response.json()['status'])

    def load_results(self):
        for batch in self._load_all_batches():
            self._load_result(batch['_id'])

    def _load_result(self, batch_id):
        assert isinstance(batch_id, str)
        response = requests.get(
            "http://{}/api/batch/{}".format(self._get_api_url(), batch_id),
            headers = self._get_authorization_header()
        )
        self._batch_results.append(response.json())

    def _create_latex_tabular(self):
        begin = '\\begin{tabular}{ccccccc} \n'
        toprule = '\\toprule \n'
        header = '\\textbf{Collection} & \\textbf{N_JSON} & \\textbf{RS} & \\textbf{ROrd} & \\textbf{TB} & \\textbf{TT}  & \\textbf{TB/TT} \\\\ \n'
        midrule = '\\midrule \n'
        rows = ''
        for result in self._batch_results:
            union_time_delta, total_time_delta, union_time_to_total_time_ratio = self._calculate_datetime_deltas(result)
            rows += '{} & {} & {} & {} & {} & {} & {} \\\\ \n'.format(
                result['collectionName'],
                result['collectionCount'],
                result['uniqueUnorderedCount'],
                result['uniqueOrderedCount'],
                union_time_delta.total_seconds(),
                total_time_delta.total_seconds(),
                union_time_to_total_time_ratio
            )
        bottomrule = '\\bottomrule \n'
        end = '\\end{tabular} \n'
        return begin + toprule + header + midrule + rows + bottomrule + end

    def save_latex_tabular(self, output="./table.tex"):
        tabular = self._create_latex_tabular()
        with open(output, 'w') as file:
            file.write(tabular)

    def _load_all_batches(self):
        response = requests.get(
            "http://{}/api/batches".format(self._get_api_url()),
            headers = self._get_authorization_header(),
        )
        return response.json()    

    def delete_batches(self):
        for batch in self._load_all_batches():
            requests.delete(
                "http://{}/api/batch/{}".format(self._get_api_url(), batch['_id']),
                headers = self._get_authorization_header(),
            )
            print("Deleted:", batch['_id'])
    
    def check_batch_status(self):
        ready = False
        while not ready:
            count_undone = 0
            for batch in self._load_all_batches():
                requests.get(
                    "http://{}/api/batches".format(self._get_api_url()),
                    headers = self._get_authorization_header(),
                )
                if batch['status'] != "DONE":
                    count_undone += 1
            if count_undone == 0:
                ready = True
                return
            time.sleep(15)


def main(args):
    try:
        experiment = Experiment()
        experiment.set_api_url(args.api_host, args.api_port)
        experiment.set_db_url(args.db_host, args.db_port)
        if args.register:
            experiment.register(args.username, args.email, args.password)
        experiment.login(args.email, args.password)
        if args.delete_batches:
            experiment.delete_batches()
            return
        for collection in track(args.collections, description="Processing..."):
            print("Start experiment on database", args.database, "and collection", collection, "!")
            try:
                experiment.run(args.database, collection)
            except requests.exceptions.RequestException as e:
                print("Exception occurred:", e)
                experiment.check_batch_status()
            except Exception as e:
                print("Status: FAILED (", e, ")")
            finally:
                print("Finished experiment!")
        experiment.load_results()
        experiment.save_latex_tabular(args.output)
        print("Loaded experiment results!")
    except requests.exceptions.ConnectionError as ce:
        print("Connection failed:", ce)
    except Exception as e:
        print("Error occurred:", e)



def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_host', default='webapi', type=str)
    parser.add_argument('--api_port', default='3000', type=str)
    parser.add_argument('--db_host', default='mongo', type=str)
    parser.add_argument('--db_port', default='27017', type=str)
    parser.add_argument('-d', '--database', required=True)
    parser.add_argument('-c', '--collections', required=True, type=str, nargs='+')
    parser.add_argument('-r', '--register', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('-u', '--username', default='test', type=str)
    parser.add_argument('-e', '--email', default='test@test.de', type=str)
    parser.add_argument('-p', '--password', default='test123456', type=str)
    parser.add_argument('-o', '--output', default='./table.tex', type=str)
    parser.add_argument('--delete_batches', default=False, action=argparse.BooleanOptionalAction)
    return parser.parse_args()

if __name__ == '__main__':
    main(setup())

