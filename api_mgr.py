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

def train(seg_num=0):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT i.imgpath, d.breed FROM imgMap i INNER JOIN dogbreeds d ON i.breed = d.id"
            cursor.execute(sql)
            data = segment_data(cursor.fetchall())
    finally:
        connection.close()
    for i, row in data[seg_num:]:
        successful = True
        try:
            for dog in row:
                print('Running:', dog['imgpath'], dog['breed'])
                collection.add_data([dog['imgpath'], dog['breed']])

            # Training
            collection.train()

            # Telling Collection to block until ready
            collection.wait()
        except Exception as e:
            print('Segment run failed:', i, '\n', e)
            successful = False
        finally:
            with open('log.txt', 'w') as log:
                log.write(str(i) + ': ' + str(successful))


def segment_data(data):
    img_dict, res = dict(), []
    for img in data:
        if img['breed'] in img_dict:
            img_dict[img['breed']].append(img)
        else:
            img_dict[img['breed']] = [img]
    while any(img_dict.values()):
        segment = []
        for k in img_dict:
            cut = 0
            while img_dict[k] and cut < 5:
                segment.append(img_dict[k].pop())
                cut += 1
        res.append(segment)
    return list(enumerate(res))


def predict(img):
    return sorted(collection.predict(img).items(), key=lambda s: s[1], reverse=True)[:5]


def init_db(img_dir):
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
            add_to_db(os.path.join(breed_dir_full, file), breed_dir)
    connection.close()


def add_to_db(img, breed):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO imgMap (breed, imgpath) VALUES ((SELECT id FROM dogbreeds WHERE breed='{breed}')," \
                  " '{path}')".format(breed=breed, path=img)
            cursor.execute(sql)
    finally:
        connection.commit()


def status_check():
    print(collection.info())
