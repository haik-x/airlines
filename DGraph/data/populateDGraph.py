import pydgraph
import json

def set_schema(client):
    schema = """

    type Location {
        name
    }

    type Flight {
        airline
        fromLocation
        toLocation
        date
        passenger 
    }

    type Passenger {
        age
        gender
        reason
        stay
        transit
        connection
        waitTime
    }

    name: string @index(exact) .
    airline: string .
    fromLocation: uid .
    toLocation: uid @reverse . 
    date: string .
    age: int .
    gender: string .
    reason: string .
    stay: string .
    transit: string .
    connection: string @index(exact) .
    waitTime: int .
    passenger: [uid] @count @reverse . 
    """
    return client.alter(pydgraph.Operation(schema=schema))

def read_json(file_path):
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    return data_list

# ...

def create_data(client, data_list):
    txn = client.txn()

    try:
        for item in data_list:
            # Check if fromLocation exists
            from_location_uid = get_location_uid(txn, item['from'])

            if not from_location_uid:
                # Create fromLocation node
                mutation_from_location = {
                    'uid': f'_:{item["from"]}',
                    'dgraph.type': 'Location',
                    'name': item['from']
                }
                txn.mutate(set_obj=mutation_from_location)
                from_location_uid = f'_:{item["from"]}'
                from_location_uid = get_location_uid(txn, item['from'])

            # Check if toLocation exists
            to_location_uid = get_location_uid(txn, item['to'])

            if not to_location_uid:
                # Create toLocation node
                mutation_to_location = {
                    'uid': f'_:{item["to"]}',
                    'dgraph.type': 'Location',
                    'name': item['to']
                }
                txn.mutate(set_obj=mutation_to_location)
                to_location_uid = f'_:{item["to"]}'
                to_location_uid = get_location_uid(txn, item['to'])

            # Create the Flight node
            mutation_flight = {
                'uid': f'_:{item["airline"]}_{item["from"]}_{item["to"]}',
                'dgraph.type': 'Flight',
                'airline': item['airline'],
                'fromLocation': {'uid': from_location_uid},
                'toLocation': {'uid': to_location_uid},
                'date': f"{item['year']}-{item['month']}-{item['day']}",
                'passenger': [
                    {
                        'uid': f'_:{item["airline"]}_{item["from"]}_{item["to"]}_passenger',
                        'dgraph.type': 'Passenger',
                        'age': item['age'],
                        'gender': item['gender'],
                        'reason': item['reason'],
                        'stay': item['stay'],
                        'transit': item['transit'],
                        'connection': item['connection'],
                        'waitTime': item['wait']
                    }
                ]
            }

            # Mutate the Flight node
            response = txn.mutate(set_obj=mutation_flight)
            print(f"UIDs: {response.uids}")

        # Commit transaction after processing all items.
        commit_response = txn.commit()
        print(f"Commit Response: {commit_response}")

    finally:
        # Clean up.
        txn.discard()


def get_location_uid(txn, location_name):
    query = f"""query {{
        get_location(func: eq(name, "{location_name}")) {{
            uid
        }}
    }}"""

    res = txn.query(query)
    result = json.loads(res.json)
    
    if 'get_location' in result and result['get_location']:
        return result['get_location'][0]['uid']
    
    return None


def analyze_connection(client):
  query = """query analyze() {
            result(func: type(Location)) {
                name
                ~toLocation {
                    a as count(passenger @filter(eq(connection, true)))
                }
                total: sum(val(a))
                }
}"""

  res = client.txn(read_only=True).query(query)
  ppl = json.loads(res.json)

  locations_data = ppl.get('result', [])
  locations_all = analyze_all(client)

# Print results.
  for location_data, location_all in zip(locations_data, locations_all):
        if location_data.get('name', '') == location_all.get('name', ''):
            name = location_data.get('name', '')
            total_no_passengers = location_data.get('total', 0)
            total_no_passengers_all = location_all.get('total', 0)

        print(f"City: {name}, Total Passengers: {total_no_passengers}/{total_no_passengers_all}")

def analyze_all(client):
  query = """query analyze() {
            result(func: type(Location)) {
                name
                ~toLocation {
                    a as count(passenger)
                }
                total: sum(val(a))
                }
}"""

  res = client.txn(read_only=True).query(query)
  ppl = json.loads(res.json)

  locations_data = ppl.get('result', [])
  return locations_data



def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))