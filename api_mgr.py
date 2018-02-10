import indicoio, os, requests, pymysql.cursors
from indicoio.custom import Collection

indicoio.config.api_key = 'API'

collection = Collection("dogs")


# Add Data

def train(img_dir):
    for dir in os.listdir(img_dir):
        breed = []
        dir = os.path.join(img_dir, dir)
        for file in os.listdir(dir):
            print('Running:', dir, file)
            breed.append([os.path.abspath(os.path.join(dir, file)), dir])
        collection.add_data(breed)

    # Training
    collection.train()

    # Telling Collection to block until ready
    collection.wait()


def predict(img):
    return sorted(collection.predict(img).items(), key=lambda s: s[1], reverse=True)[:5]


def initDb():
    connection = pymysql.connect(host='localhost',
                                 user='user',
                                 password='passwd',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    for dir in os.listdir(img_dir):
        dir = os.path.join(img_dir, dir)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO 'breeds' ('breed') VALUES ({b})".format(b=dir)
                cursor.execute(sql, ())
        finally:
            pass
        for file in os.listdir(dir):
            pass


def addToDb(img, breed):
    pass