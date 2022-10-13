"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from openadr_ven import initialize_openadr_client

open_adr_buying_price = 3
open_adr_selling_price = 3

def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    load_one = True
    load_two = True
    load_three = True
    power_reference = 0.0
    pv_mode = PVMode.ON

    # if msg.grid_status:
    #     if msg.bessSOC != 1 and open_adr_buying_price == open_adr_selling_price \
    #             and msg.current_load <8:
    #         if msg.bessSOC > 0.45:
    #             power_reference = -5.0
    #     elif msg.current_load > 8:
    #         power_reference = msg.current_load
    #
    # else:
    #     if msg.bessSOC == 1 and msg.solar_production > 0:
    #         if msg.solar_production < msg.current_load:
    #             power_reference = msg.current_load
    #             load_three = False
    #             pv_mode = PVMode.OFF
    #         else:
    #             power_reference = msg.current_load
    #     elif msg.bessSOC != 1:
    #         load_three = False
    #         pv_mode = PVMode.ON
    #
    #     elif open_adr_selling_price == open_adr_buying_price and msg.solar_production == 0:
    #         power_reference = msg.current_load

    # Dummy result is returned in every cycle here
    return ResultsMessage(data_msg=msg,
                          load_one=load_one,
                          load_two=load_two,
                          load_three=load_three,
                          power_reference=power_reference,
                          pv_mode=pv_mode)


# This coroutine will be called when there is an event to be handled.
async def openadr_handle_event(event):
    print("There is an event!")
    # print(event)
    first_signal = event['event_signals'][0]
    first_target = event['targets'][0]
    if first_signal['signal_name'] == 'ELECTRICITY_PRICE' and first_target['ven_id'] == 'uegos_ven_id_123':
        global open_adr_buying_price
        open_adr_buying_price = first_signal['intervals'][0]['signal_payload']

    # TODO: get open_adr_selling_price as well
    return 'optIn'


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    print("Solution initializing OpenADR Client (VEN)")
    initialize_openadr_client(None, openadr_handle_event)

    cntrl = Control()

    try:
        for data in cntrl.get_data_non_blocking():
            cntrl.push_results(worker(data))
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting solution")