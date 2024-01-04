
def update_data_user(data):
    first_name, last_name = data.get('name').split()
    data['first_name'] = first_name
    data['last_name'] = last_name
    data['telegram_id'] = int(data.get('telegram_id'))
    del data['name']
    return data