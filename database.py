import json
import datetime

class Database():
    def __init__(self) -> None:
        self.path_data = 'database/data.json'
        self.path_positions = 'database/positions.json'

    def __read_data(self):
        with open(self.path_data, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def __write_data(self, data):
        with open(self.path_data, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def __read_positions(self):
        with open(self.path_positions, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    def __read_deals(self):
        pass

    def __write_deals(self, data):
        pass

    def registration(self, user_id: int, user_name: str):
        data = self.__read_data()

        if str(user_id) not in str(data):
            registration_date = datetime.datetime.now().strftime("%m/%d/%Y|%H:%M:%S")
            data.append({'user_id': user_id, 'user_name': user_name, 
                         'start_summ': 1000, 'profit': 0, 
                         'registration_date': registration_date, 'count_deals': 0 })
            self.__write_data(data)
        else:
            return

    def get_user(self, user_id: int):
        data = self.__read_data()
        for x in data:
            if x['user_id'] == user_id:
                return x

    def get_balance(self, user_id: int):
        data = self.__read_data()
        for x in data:
            if x['user_id'] == user_id:
                return x['start_summ'] + x['profit']
            
    def get_position(self, user_id: int):
        data = self.__read_data()
        for x in data:
            if x['user_id'] == user_id:
                return x['positions']
            