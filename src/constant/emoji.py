import re

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # Emoticons
                           u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
                           u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                           u"\U0001F700-\U0001F77F"  # Alchemical Symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U0001F251"  # Enclosed Characters
                           u"\U0001F600-\U0001F636"  # Emoticons & Smileys
                           u"\U0001F681-\U0001F6C5"  # Transport & Map Symbols
                           u"\U0001F300-\U0001F567"  # Other Symbols
                           u"\U0001F004-\U0001F0CF"  # Mahjong Tiles
                           u"\U0001F170-\U0001F251"  # Enclosed Alphanumeric Supplement
                           u"\U0001F1E6-\U0001F1FF"  # Regional Indicator Symbols
                           u"\U0001F910-\U0001F918"  # Face Hand Symbols
                           u"\U0001F919-\U0001F91E"  # Zodiac Signs
                           u"\U0001F920-\U0001F927"  # Hand Symbols
                           u"\U0001F930-\U0001F939"  # Food Symbols
                           u"\U0001F940-\U0001F945"  # Animal Symbols
                           u"\U0001F950-\U0001F96B"  # Other Symbols
                           u"\U0001F980-\U0001F991"  # Plant Symbols
                           u"\U0001F992-\U0001F9AA"  # Object Symbols
                           "]+", flags=re.UNICODE)
