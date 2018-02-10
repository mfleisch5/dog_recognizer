import indicoio
from indicoio.custom import Collection
indicoio.config.api_key = '5c6a25f102276fa6acbf0a5ac79548a5'

collection = Collection("dogs")

# Add Data
collection.add_data([["text1", "label1"], ["text2", "label2"], ...])

# Training
collection.train()

# Telling Collection to block until ready
collection.wait()

# Done! Start analyzing text
collection.predict("indico is so easy to use!")