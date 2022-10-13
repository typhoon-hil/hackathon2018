import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRClient, OpenADRServer, enable_default_logging
from openleadr.objects import Target, Interval
from functools import partial

from datetime import timedelta
from threading import Thread

stop_openadr = False

async def openadr_main(collect_report_value, openadr_handle_event):
    print("creating client")
    client = OpenADRClient(ven_name="uegos_ven_1",
                           vtn_url="http://localhost:8080/OpenADR2/Simple/2.0b",
                           allow_jitter=False)
    client.add_handler('on_event', openadr_handle_event)

    # Add the report capability to the client
    #client.add_report(callback=collect_report_value, resource_id='windtourbine001', measurement='voltage', sampling_rate=timedelta(seconds=14))

    print("running openADR client")
    await client.run()

def initialize_openadr(arg, collect_report_value, openadr_handle_event):
    print("initialize open adr")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(openadr_main(collect_report_value, openadr_handle_event))
    loop.run_forever()

def initialize_openadr_client(collect_report_value, openadr_handle_event):
    # start openadr client
    print("Initializing OpenADR client")
    # create thread
    thread = Thread(target = initialize_openadr, args = (10, lambda: collect_report_value, openadr_handle_event))
    thread.daemon = True # terminate thread when main process ends
    thread.start()


