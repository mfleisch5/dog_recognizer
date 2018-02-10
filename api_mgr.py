import indicoio, os, base64
from indicoio.custom import Collection
indicoio.config.api_key = '5c6a25f102276fa6acbf0a5ac79548a5'

collection = Collection("dogs")

# Add Data
""""
for dir in os.listdir('Images'):
    pics, count = [], 0
    for file in os.listdir('Images/' + dir):
        print('Running:', dir, file)
        pics.append([os.path.abspath('Images/' + dir + '/' + file), dir])
        count += 1
        if count == 5:
            break
    collection.add_data(pics)



# Training
collection.train()

# Telling Collection to block until ready
collection.wait()
"""


print(*sorted(collection.predict(os.path.abspath('Images/Yorkshire_terrier/n02094433_4005.jpg')).items(), reverse=True,
              key=lambda p: p[1]), sep='\n')
