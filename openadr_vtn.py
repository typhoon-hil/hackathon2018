import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRServer, enable_default_logging
from openleadr.objects import Target, Interval
from functools import partial
from hackathon.utils.link import FrameworkLink
from hackathon.utils.utils import *
from threading import Thread

"""
class SIGNAL_TYPE(metaclass=Enum):
    DELTA = "delta"
    LEVEL = "level"
    MULTIPLIER = "multiplier"
    PRICE = "price"
    PRICE_MULTIPLIER = "priceMultiplier"
    PRICE_RELATIVE = "priceRelative"
    SETPOINT = "setpoint"
    X_LOAD_CONTROL_CAPACITY = "x-loadControlCapacity"
    X_LOAD_CONTROL_LEVEL_OFFSET = "x-loadControlLevelOffset"
    X_LOAD_CONTROL_PERCENT_OFFSET = "x-loadControlPercentOffset"
    X_LOAD_CONTROL_SETPOINT = "x-loadControlSetpoint"


class SIGNAL_NAME(metaclass=Enum):
    SIMPLE = "SIMPLE"
    simple = "simple"
    ELECTRICITY_PRICE = "ELECTRICITY_PRICE"
    ENERGY_PRICE = "ENERGY_PRICE"
    DEMAND_CHARGE = "DEMAND_CHARGE"
    BID_PRICE = "BID_PRICE"
    BID_LOAD = "BID_LOAD"
    BID_ENERGY = "BID_ENERGY"
    CHARGE_STATE = "CHARGE_STATE"
    LOAD_DISPATCH = "LOAD_DISPATCH"
    LOAD_CONTROL = "LOAD_CONTROL"

"""

enable_default_logging()

# Create the server object
server = OpenADRServer(vtn_id='example_vtn', requested_poll_freq=timedelta(seconds=1))
stop_msgs = False

async def on_create_party_registration(registration_info):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    print("UEGOS VTN on_create_party_registration")
    if registration_info['ven_name'] == 'uegos_ven_1':
        ven_id = 'uegos_ven_id_123'
        registration_id = 'reg_id_123'
        return ven_id, registration_id
    else:
        return False

async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    """
    Inspect a report offering from the VEN and return a callback and sampling interval for receiving the reports.
    """
    print("UEGOS VTN on_register_report")
    callback = partial(on_update_report, ven_id=ven_id, resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval

async def on_update_report(data, ven_id, resource_id, measurement):
    """
    Callback that receives report data from the VEN and handles it.
    """
    global server
    for time, value in data:
        print(f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")
        if value > 15:
            print("UEGOS VTN firing event!!!!!!!")
            # event will be sent soon
            server.add_event(ven_id='uegos_ven_id_123',
                signal_name='LOAD_CONTROL',
                signal_type='level',
                intervals=[{'dtstart': datetime.now(timezone.utc),
                    'duration': timedelta(minutes=1),
                    'signal_payload': 1}],
                callback=event_response_callback)

async def event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    print(f"VEN {ven_id} responded to Event {event_id} with: {opt_type}")

# This function is waiting for msg from framework
def framework_messenger(arg, stop):
    print("\nInitialize framework messenger")

    # communication link with the framework
    link = FrameworkLink()

    for data in link.get_data_vtn():
        print("framework send his regards")
        print(data.buying_price)
        print(stop())
        # push event
        server.add_event(ven_id='uegos_ven_id_123',
            signal_name='ELECTRICITY_PRICE',
            signal_type='price',
            intervals=[{'dtstart': datetime.now(timezone.utc),
                'duration': timedelta(minutes=1),
                'signal_payload': data.buying_price}],
            callback=event_response_callback)

def run(args) -> None:

    global server, stop_msgs
    
    # Start thread which receives messages from framework
    thread = Thread(target = framework_messenger, args = (10, lambda: stop_msgs))
    thread.daemon=True # terminate thread when main process ends
    thread.start()

    # Add the handler for client (VEN) registrations
    server.add_handler('on_create_party_registration', on_create_party_registration)

    # Add the handler for report registrations from the VEN
    server.add_handler('on_register_report', on_register_report)

    # Add a prepared event for a VEN that will be picked up when it polls for new messages.
    """server.add_event(ven_id='uegos_ven_id_123',
                     signal_name='simple',
                     signal_type='level',
                     intervals=[{'dtstart': datetime.now(timezone.utc),
                                 'duration': timedelta(minutes=1),
                                 'signal_payload': 1}],
                     callback=event_response_callback)"""

    try:
        # Run the server on the asyncio event loop
        loop = asyncio.get_event_loop()
        loop.create_task(server.run())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()

    print("Exitting OpenADR VTN Server...\n")
