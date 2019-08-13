import json
import maya
from assertpy import assert_that
from api_testing.core import Core
from api_testing.data import Data
from api_testing.api_journey import Api_Journey

def __data_stops():
    """set total stops order payload"""
    dict_1 = {"lat": 22.344674, "lng": 114.124651}
    dict_2 = {"lat": 22.375384, "lng": 114.18244}
    dict_3 = {"lat": 22.385669, "lng": 114.186962}
    total_stops = [dict_1, dict_2, dict_3]
    return total_stops

def __get_order(time=None):
    """get order for the first time and it can use time or not"""

    get_endpoint = Data().generate_endpoint('/v1/orders')
    if time is None:
        get_payloads = Data().payload_order(stops_dict=__data_stops())
    else:
        get_payloads = Data().payload_order_time(time=time, stops_dict=__data_stops())

    response = Api_Journey().orders(endpoint=get_endpoint, payloads=get_payloads)
    return response

def test_place_order_endpoint():
    """test place order endpoint without time
    detail checking :
    - check id is not empty
    - check status should 201
    - check total_distance should equal with total drivingDistancesInMeters
    """
    time = maya.now().add(minutes=1).iso8601()
    get_payloads = Data().payload_order_time(time=time, stops_dict=__data_stops())
    response_json = __get_order(time=time).json()
    calculate_balance = Core().calculate_currency(payload=get_payloads, response=response_json)
    total_distance = Core().calculate_distance(stops=get_payloads['stops'])
    response_status_code = __get_order().status_code
    response_calculate_balance = response_json['fare']['amount']

    assert_that(response_json['id']).is_not_none()
    assert_that(response_status_code).is_equal_to(201)
    assert_that(total_distance).is_equal_to(len(response_json['drivingDistancesInMeters']))
    assert_that(str(calculate_balance)).is_equal_to(response_calculate_balance)

def test_place_order_time_endpoint():
    """test place order endpoint with time
    detail checking :
    - check id is not empty
    - check status should 201
    - check total_distance should equal with total drivingDistancesInMeters
    """
    set_time = maya.now().add(minutes=1).iso8601()
    get_payloads = Data().payload_order_time(time=set_time, stops_dict=__data_stops())
    response_json = __get_order(time=set_time).json()
    response_status_code = __get_order().status_code
    total_distance = Core().calculate_distance(stops=get_payloads['stops'])

    assert_that(response_json['id']).is_not_none()
    assert_that(response_status_code).is_equal_to(201)
    assert_that(total_distance).is_equal_to(len(response_json['drivingDistancesInMeters']))

def test_fetch_order_detail_endpoint():
    """test fetch order detail endpoint
    detail checking :
    - compare id, driving_distance, amount, currency, stops_payload
    - checking response code should be 200
    - checking status should be ASSIGNING
    - checking id is not empty
    """
    get_order = __get_order()
    id = get_order.json()['id']
    driving_distance = get_order.json()['drivingDistancesInMeters']
    amount = get_order.json()['fare']['amount']
    currency = get_order.json()['fare']['currency']
    stops_payload = Data().payload_order(stops_dict=__data_stops())['stops']

    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}'.format(id))
    get_response = Api_Journey().fetch_data_endpoint(endpoint=get_endpoint)
    response_json = get_response.json()

    response_status_code = get_response.status_code
    response_id = response_json['id']
    response_stops = response_json['stops']
    response_driving_distance = response_json['drivingDistancesInMeters']
    response_amount = response_json['fare']['amount']
    response_currency = response_json['fare']['currency']
    response_status = response_json['status']
    response_created_time = response_json['createdTime']
    response_order_date_time = response_json['orderDateTime']

    assert_that(response_id).is_not_none()
    assert_that(response_status_code).is_equal_to(200)
    assert_that(id).is_equal_to(response_id)
    assert_that(driving_distance).is_equal_to(response_driving_distance)
    assert_that(amount).is_equal_to(response_amount)
    assert_that(currency).is_equal_to(response_currency)
    assert_that(stops_payload).is_equal_to(response_stops)
    assert_that(response_status).is_equal_to('ASSIGNING')

def test_assigning_cancel_endpoint():
    """test assigning and cancel endpoint
    detail checking :
    - compare id, date
    - checking response code should be 200
    - checking status should be CANCELLED
    - checking id is not empty
    """
    set_time = maya.now().add(minutes=1).iso8601()
    date = Core().get_date(input_full_date=set_time)
    id = __get_order(time=set_time).json()['id']

    get_endpoint_assign = Data().generate_endpoint('/v1/orders/{:d}'.format(id))
    get_response_assign = Api_Journey().fetch_data_endpoint(endpoint=get_endpoint_assign)

    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/cancel'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)

    response_status_code = get_response.status_code
    response_id = get_response.json()['id']
    response_status = get_response.json()['status']
    response_cancelled_time = get_response.json()['cancelledAt']
    response_date = Core().get_date(input_full_date=response_cancelled_time)

    assert_that(response_id).is_not_none()
    assert_that(response_status_code).is_equal_to(200)
    assert_that(id).is_equal_to(response_id)
    assert_that(response_status).is_equal_to('CANCELLED')
    assert_that(date).is_equal_to(response_date)


def test_fetch_order_detail_endpoint_not_exists():
    """test fetch order detail with failure id
    detail checking :
    - checking response code should be 404
    """
    id = 1000000
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}'.format(id))
    get_response = Api_Journey().fetch_data_endpoint(endpoint=get_endpoint)
    assert_that(get_response.status_code).is_equal_to(404)

def test_take_order_endpoint():
    """test take order endpoint
    detail checking :
    - compare id, date
    - checking response code should be 200
    - checking status should be ONGOING
    - checking id is not empty
    """
    set_time = maya.now().add(minutes=1).iso8601()
    date = Core().get_date(input_full_date=set_time)
    id = __get_order(time=set_time).json()['id']
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/take'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)

    response_status_code = get_response.status_code
    response_id = get_response.json()['id']
    response_status = get_response.json()['status']
    response_ongoing_time = get_response.json()['ongoingTime']
    response_date = Core().get_date(input_full_date=response_ongoing_time)

    assert_that(response_id).is_not_none()
    assert_that(response_status_code).is_equal_to(200)
    assert_that(id).is_equal_to(response_id)
    assert_that(response_status).is_equal_to('ONGOING')
    assert_that(date).is_equal_to(response_date)

def test_take_order_endpoint_not_exists():
    """test take order endpoint with failure id
    detail checking :
    - checking response code should be 404
    """
    id = 99999999999
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/take'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)
    assert_that(get_response.status_code).is_equal_to(404)

def test_take_order_endpoint_logic_violated():
    """test take order endpoint with logic violated
    detail checking :
    - checking response code should be 422
    - checking response message
    """
    id = 1
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/take'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)
    assert_that(get_response.status_code).is_equal_to(422)
    assert_that(get_response.json()['message']).is_equal_to('Order status is not ASSIGNING')

def test_complete_the_order_endpoint():
    """test complete the order endpoint
    detail checking :
    - compare id, date
    - checking response code should be 200
    - checking status should be ONGOING
    - checking id is not empty
    """
    set_time = maya.now().add(minutes=1).iso8601()
    date = Core().get_date(input_full_date=set_time)
    id = __get_order(time=set_time).json()['id']

    take_order_endpoint = Data().generate_endpoint('/v1/orders/{:d}/take'.format(id))
    take_order_response = Api_Journey().take_complete_cancel_endpoint(endpoint=take_order_endpoint)
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/complete'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)

    response_status_code = get_response.status_code
    response_id = get_response.json()['id']
    response_status = get_response.json()['status']
    response_completed_time = get_response.json()['completedAt']
    response_date = Core().get_date(input_full_date=response_completed_time)

    assert_that(response_id).is_not_none()
    assert_that(response_status_code).is_equal_to(200)
    assert_that(id).is_equal_to(response_id)
    assert_that(response_status).is_equal_to('COMPLETED')
    assert_that(date).is_equal_to(response_date)

def test_complete_the_order_endpoint_not_exists():
    """test complete the order endpoint with failure id
    detail checking :
    - checking response code should be 404
    """
    id = 99999999999
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/complete'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)
    assert_that(get_response.status_code).is_equal_to(404)

def test_complete_the_order_endpoint_logic_violated():
    """test complete the order endpoint with logic violated
    detail checking :
    - checking response code should be 422
    - checking response message
    """
    id = 1
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/complete'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)
    assert_that(get_response.status_code).is_equal_to(422)
    assert_that(get_response.json()['message']).is_equal_to('Order status is not ONGOING')

def test_cancel_the_order_endpoint():
    """test cancel the order endpoint
    detail checking :
    - compare id, date
    - checking response code should be 200
    - checking status should be CANCELLED
    - checking id is not empty
    """
    set_time = maya.now().add(minutes=1).iso8601()
    date = Core().get_date(input_full_date=set_time)
    id = __get_order(time=set_time).json()['id']

    take_order_endpoint = Data().generate_endpoint('/v1/orders/{:d}/take'.format(id))
    take_order_response = Api_Journey().take_complete_cancel_endpoint(endpoint=take_order_endpoint)
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/cancel'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)

    response_status_code = get_response.status_code
    response_id = get_response.json()['id']
    response_status = get_response.json()['status']
    response_cancelled_time = get_response.json()['cancelledAt']
    response_date = Core().get_date(input_full_date=response_cancelled_time)

    assert_that(response_id).is_not_none()
    assert_that(response_status_code).is_equal_to(200)
    assert_that(id).is_equal_to(response_id)
    assert_that(response_status).is_equal_to('CANCELLED')
    assert_that(date).is_equal_to(response_date)

def test_cancelled_the_order_endpoint_not_exists():
    """test cancel the order endpoint with failure id
    detail checking :
    - checking response code should be 404
    """
    id = 99999999999
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/cancel'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)
    assert_that(get_response.status_code).is_equal_to(404)

def test_cancelled_the_order_endpoint_logic_violated():
    """test cancel endpoint with logic violated
    detail checking :
    - checking response code should be 422
    - checking response message
    """
    id = 1
    get_endpoint = Data().generate_endpoint('/v1/orders/{:d}/cancel'.format(id))
    get_response = Api_Journey().take_complete_cancel_endpoint(endpoint=get_endpoint)
    assert_that(get_response.status_code).is_equal_to(422)
    assert_that(get_response.json()['message']).is_equal_to('Order status is COMPLETED already')
