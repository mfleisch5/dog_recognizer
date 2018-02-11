import indicoio, os, pymysql.cursors, base64
from indicoio.custom import Collection

indicoio.config.api_key = base64.b64decode(b'NWM2YTI1ZjEwMjI3NmZhNmFjYmYwYTVhYzc5NTQ4YTU=')

collection = Collection("dogs")
connection = pymysql.connect(host='localhost',
                             user='hbp',
                             password='hbp2018',
                             db='dogDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# Add Data

def train():
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT i.imgpath, d.breed FROM imgMap i INNER JOIN dogbreeds d ON i.breed = d.id"
            cursor.execute(sql)
            result = cursor.fetchall()
            #print(result)
    finally:
        connection.close()
    for row in result:
        print('Running:', row['imgpath'], row['breed'])
        collection.add_data([row['imgpath'], row['breed']])

    # Training
    collection.train()

    # Telling Collection to block until ready
    collection.wait()

def predict(img):
    return sorted(collection.predict(img).items(), key=lambda s: s[1], reverse=True)[:5]


def initDb(img_dir):
    for breed_dir in os.listdir(img_dir):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO dogbreeds (breed) VALUES ('{b}')".format(b=breed_dir)
                #print(sql)
                cursor.execute(sql)
            connection.commit()
        finally:
            pass
    for breed_dir in os.listdir(img_dir):
        breed_dir_full = os.path.join(img_dir, breed_dir)
        for file in os.listdir(breed_dir_full):
            addToDb(os.path.join(breed_dir_full, file), breed_dir)
    connection.close()


def addToDb(img, breed):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO imgMap (breed, imgpath) VALUES ((SELECT id FROM dogbreeds WHERE breed='{breed}')," \
                  " '{path}')".format(breed=breed, path=img)
            #print(sql)
            cursor.execute(sql)
    finally:
        connection.commit()
