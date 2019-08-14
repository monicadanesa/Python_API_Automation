import maya
import math
import datetime

class Core:
    """Class related with all calculations"""
    def __init__(self):
        pass

    def calculate_distance(self, stops):
        if len(stops) == 2:
            distance = 1
        elif len(stops) >= 2:
            distance = len(stops) - 1

        return distance

    def round_half_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n*multiplier + 0.5) / multiplier

    def get_date(self, input_full_date):
        date = maya.parse(input_full_date).datetime()
        return date.date()

    def get_time(self, input_full_date):
        time = maya.parse(input_full_date).datetime()
        return time.time()

    def calculate_currency(self, payload=None, response=None):
        time_payload = payload['orderAt']
        now_time = self.get_time(time_payload)
        distance_in_meters = response['drivingDistancesInMeters']
        amount = response['fare']['amount']

        start = datetime.time(22, 00)
        end = datetime.time(5, 00)

        if now_time >= start or now_time <= end:
            total_balance_2_km = 30
            each_200_meter_costs = 8
        else:
            total_balance_2_km = 20
            each_200_meter_costs = 5

        total_distance_in_meters = sum(distance_in_meters)

        if total_distance_in_meters <= 2000:
            total_balance = total_balance_2_km
        elif total_distance_in_meters > 2000:
            calculate_distance_less_2_km = int((total_distance_in_meters - 2000) / 200)
            total_balance_less_2_km = calculate_distance_less_2_km * each_200_meter_costs
            prorate_calculation = (total_distance_in_meters - 2000) - (calculate_distance_less_2_km * 200)
            total_prorate_balance = ((prorate_calculation / 200) * each_200_meter_costs)
            total_balance = total_balance_2_km + total_balance_less_2_km + total_prorate_balance
            total_balance = self.round_half_up(total_balance, 2)

        return total_balance
