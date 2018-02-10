import indicoio, os, requests
from indicoio.custom import Collection

indicoio.config.api_key = '5c6a25f102276fa6acbf0a5ac79548a5'

collection = Collection("dogs")

<<<<<<< HEAD
=======
# Add Data
def train():
    for dir in os.listdir('Images'):
        pics, count = [], 0
        for file in os.listdir('Images/' + dir):
            print('Running:', dir, file)
            pics.append([os.path.abspath('Images/' + dir + '/' + file), dir])
            count += 1
            if count == 5:
                break
        collection.add_data(pics)
>>>>>>> 2909deece13ab51fdbeac40dec72b844842b7840

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

def predict( img ):
    #This function will take in an image and predict the breed using the API
    #print(*sorted(collection.predict(os.path.abspath('Images/Yorkshire_terrier/n02094433_4005.jpg')).items(), reverse=True,
    # key=lambda p: p[1]), sep='\n')

<<<<<<< HEAD
def predict(img):
    return sorted(collection.predict(img).items(), key=lambda s: s[1], reverse=True)[:5]
=======
def addToDb( img, breed):
    #This function will take in an image and the most likely breed to add to the database for future training
>>>>>>> 2909deece13ab51fdbeac40dec72b844842b7840
