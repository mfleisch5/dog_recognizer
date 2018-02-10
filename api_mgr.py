import indicoio, os, pymysql.cursors
from indicoio.custom import Collection

indicoio.config.api_key = 'API'

collection = Collection("dogs")
connection = pymysql.connect(host='localhost',
                             user='hbp',
                             password='hbp2018',
                             db='dogDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# Add Data

def train(img_dir):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT i.imgpath, d.breed FROM imgMap i INNER JOIN dogbreeds d"
            cursor.execute(sql)
            # result = cursor.fetchall()
            result = cursor.fetchmany(10)
            print(result)
    finally:
        connection.close()
    '''
      for dir in os.listdir(img_dir):
          breed = []
          dir = os.path.join(img_dir, dir)
          for file in os.listdir(dir):
              print('Running:', dir, file)
              breed.append([os.path.abspath(os.path.join(dir, file)), dir])
          collection.add_data(breed)
      '''
    # Training
    collection.train()

    # Telling Collection to block until ready
    collection.wait()


def predict(img):
    return sorted(collection.predict(img).items(), key=lambda s: s[1], reverse=True)[:5]


def initDb(img_dir):
    for breed_dir in os.listdir(img_dir):
        #breed_dir = os.path.join(img_dir, breed_dir)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO dogbreeds (breed) VALUES ('{b}')".format(b=breed_dir)
                cursor.execute(sql)
            connection.commit()
        finally:
            pass
    for breed_dir in os.listdir(img_dir):
        breed_dir_full = os.path.join(img_dir, breed_dir)
        for file in os.listdir(breed_dir):
            addToDb(os.path.join(breed_dir_full, file), breed_dir)
    connection.close()

def addToDb(img, breed):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO imgMap (breed, imgpath) VALUES ((SELECT id FROM dogbreeds WHERE breed={breed}), {path})".\
                format(breed=breed, path=img)
            cursor.execute(sql)
    finally:
        pass

initDb(os.path.realpath('Images'))