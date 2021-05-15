import requests
import pandas as pd
import sqlite3
import sqlalchemy

DATABASE_LOCATION = "sqlite:///verkeersBorden.db"
TOWN_CODE = 'GM1680'
URL = 'https://data.ndw.nu/api/rest/static-road-data/traffic-signs/v1/current-state?'

base_url = URL + 'town-code={}'.format(TOWN_CODE)
print(base_url)


def get_data(url):
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    df.rename(columns={'location.wgs84.latitude': 'latitude', 'location.wgs84.longitude': 'longitude', 'location.rd.x': 'x', 'location.rd.y': 'y', 'location.placement': 'placement', 'location.side': 'side', 'location.road.name': 'road_name', 'location.road.type': 'road_type', 'location.road.number': 'number',
              'location.road.wvk_id': 'wvk_id', 'location.county.name': 'name', 'location.county.code': 'code', 'location.county.townname': 'townname', 'details.image': 'image', 'details.first_seen': 'first_seen', 'details.last_seen': 'last_seen', 'details.removed': 'removed'}, inplace=True)
    return df


def get_image(img_url):
    response = requests.get(img_url)
    name_prep = img_url.rsplit('.')[-2]
    name = name_prep.split('/')[-1]
    file = open("ndw_verkeersborden\images\{}.png".format(name), "wb")
    file.write(response.content)
    file.close()


if __name__ == "__main__":
    print("this is the start of the script")
    vkb_df = get_data(base_url)
    del vkb_df['text_signs']
    print(vkb_df.head())

    # engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    # connection = sqlite3.connect("verkeersBorden.db")
    # cursor = connection.cursor()

#     sqlquery = """
#     CREATE TABLE IF NOT EXISTS Borden (
#     id                    VARCHAR (200) PRIMARY KEY
#                                         UNIQUE,
#     type                  VARCHAR (200),
#     schema_version        VARCHAR (200),
#     validated             VARCHAR (200),
#     validated_on          VARCHAR (200),
#     user_id               VARCHAR (200),
#     organisation_id       VARCHAR (200),
#     rvv_code              VARCHAR (200),
#     text_signs            VARCHAR (200),
#     publication_timestamp VARCHAR (200),
#     latitude              VARCHAR (200),
#     longitude             VARCHAR (200),
#     x                     VARCHAR (200),
#     y                     VARCHAR (200),
#     placement             VARCHAR (200),
#     side                  VARCHAR (200),
#     road_name             VARCHAR (200),
#     road_type             VARCHAR (200),
#     number                VARCHAR (200),
#     wvk_id                VARCHAR (200),
#     name                  VARCHAR (200),
#     code                  VARCHAR (200),
#     townname              VARCHAR (200),
#     image                 VARCHAR (200),
#     first_seen            VARCHAR (200),
#     last_seen             VARCHAR (200),
#     removed               VARCHAR (200)
# );
#     """
    # new_id = df_sql['id'][0]

    # sqlquery2 = "INSERT INTO Borden(id) VALUES({})".format(new_id)
    # # print(sqlquery2)
    # cursor.execute(sqlquery2)
    # connection.commit()
    # df_sql.to_sql("Borden2", connection,
    # # if_exists='append', index=False)
    # try:
    #     vkb_df.to_sql("Borden", connection,
    #                   if_exists='append', index=False)
    # except:
    #     print("Does not work")
