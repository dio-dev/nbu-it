import asyncio
import datetime
from dbTools import get_nbu_objects, create_location, update_location
from GoogleFinder import Google_finder
from time import sleep
weekdays = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')


async def update_bd():

    objects = get_nbu_objects()
    google_service = Google_finder()
    for item in objects:
        try:
            adress = google_service.get_address_by_location(item.gps_latitude, item.gps_longitude)
            update_location(item.adress_id, adress["region"],  adress["city"], adress["street_name"], adress["street_number"],
                            adress["index"])
        except:
            print("error")

async def start_checker():
    counter = 0
    await update_bd()
    while True:
        counter += 1

        if counter == 1440:
            await update_bd()
            counter = 0

        await asyncio.sleep(60)


