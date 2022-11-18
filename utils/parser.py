import datetime
import asyncio
import aiohttp
import asyncpg

from bs4 import BeautifulSoup
from pathlib import Path

from utils.GetEnviromentVariable import get_environment_variables


URL = "https://auto.ria.com/uk/toplivo/"
regions = [('vinnica', 'Вінницька'),
           ('zhitomir', 'Житомирська'),
           ('ternopol', 'Тернопільська'),
           ('khmelnickij', 'Хмельницька'),
           ('lvov', 'Львівська'),
           ('chernigov', 'Чернігівська'),
           ('kharkov', 'Харківська'),
           ('sumy', 'Сумська'),
           ('rovno', 'Рівненська'),
           ('kiev', 'Київська'),
           ('dnepr-dnepropetrovsk', 'Дніпровська'),
           ('odessa', 'Одеська'),
           ('doneckaya-obl', 'Донецька'),
           ('zaporozhe', 'Запорізька'),
           ('ivano-frankovsk', 'Івано-Франківська'),
           ('kropivnickij-kirovograd', 'Кропивницька'),
           ('luganskaya-obl', 'Луганська'),
           ('luczk', 'Волинська'),
           ('nikolaev', 'Миколаївська'),
           ('poltava', 'Полтавська'),
           ('uzhgorod', 'Закарпатська'),
           ('kherson', 'Херсонська'),
           ('cherkassy', 'Черкаська'),
           ('chernovczy', 'Чернівецька')
           ]
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'accept': '*/*'
}


async def db_connect():
    """
        String for getting all data from database:
        select fuel_pricetable.price, ff.name, fr.name, f.name
        from fuel_pricetable
        join fuel_fuel ff on ff.id = fuel_pricetable.id_fuel_id
        join fuel_region fr on fr.id = fuel_pricetable.id_region_id
        join fuel_fueloperator f on f.id = fuel_pricetable.id_fuel_operator_id
    :return: cursor
    """
    base_dir = str(Path(__file__).resolve().parent.parent)
    env = get_environment_variables(base_dir)
    return await asyncpg.connect(user=env('POSTGRES_USER'),
                                 password=env('POSTGRES_PASSWORD'),
                                 database=env('POSTGRES_DB'),
                                 host=env('DB_HOST'),
                                 port=env('DB_PORT')
                                 )


async def get_html(url: str, query_list: list) -> list:
    html_list = []
    for query in query_list:
        url += f'{query[0]}/#refuel'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=HEADERS) as resp:
                    if resp.status == 200:
                        html_list.append({query[1]: await resp.text()})
        except:
            continue
    return html_list


async def page_parse(html_list: list) -> list:
    result_list = []
    fuel_price = dict()
    for region in html_list:
        for key, value in region.items():
            soup = BeautifulSoup(value, 'html.parser')
            tables = [
                [
                    [td.get_text(strip=True) for td in tr.find_all('td')]
                    for tr in table.find_all('tr')
                ]
                for table in soup.find_all('table')
            ]
            for el in tables[0][1:]:
                fuel_price[el[0]] = {
                    'A95plus': el[1],
                    'A95': el[2],
                    'A92': el[3],
                    'Diesel': el[4],
                    'Gas': el[5]
                }
            result_list.append({key: fuel_price})
    return result_list


async def write_to_db(data_list: list):
    sql_string = "insert into fuel_pricetable(date, price, id_fuel_id, id_fuel_operator_id, id_region_id) values"
    now_data = datetime.date.today()
    sql_values_list = []
    conn = await db_connect()
    regions_name_list = dict(await conn.fetch('select name, id from fuel_region'))
    fuel_name_list = dict(await conn.fetch('select name, id from fuel_fuel'))
    fuel_operator_name_list = dict(await conn.fetch('select name, id from fuel_fueloperator'))

    # Parse a list of data
    for itm in data_list:
        for region, value in itm.items():
            if region not in regions_name_list:
                print(f'{region} not in database')
                continue
            for fuel_operator, fuel in value.items():
                if fuel_operator not in fuel_operator_name_list:
                    print(f'{fuel_operator} from {region} not in database')
                    continue
                for name, price in fuel.items():
                    if price == '-':
                        continue
                    if name not in fuel_name_list:
                        print(f'{name} not in database')
                        continue
                    sql_insert_one = f"""
                    ('{now_data}', {price},
                    (select id from fuel_fuel where name='{name}'),
                    (select id from fuel_fueloperator where name='{fuel_operator}'),
                    (select id from fuel_region where name='{region}'))"""
                    sql_values_list.append(sql_insert_one)
    sql_string += ', '.join(sql_values_list) + ';'
    await conn.execute(sql_string)
    await conn.close()


async def main():
    all_html_pages = await get_html(URL, regions)
    fuel_data = await page_parse(all_html_pages)
    await write_to_db(fuel_data)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
