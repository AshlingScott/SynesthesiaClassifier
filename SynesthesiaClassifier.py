import sqlite3
import re

# Connect to the database
DATA = "C:\\Users\\Administrator\\Desktop\\books\\books.db"
conn = sqlite3.connect(DATA)
cursor = conn.cursor()

"""# Create the table
sql = CREATE TABLE synesthesia (
            book_index INTEGER, 
            vision INTEGER, 
            sound INTEGER, 
            smell INTEGER, 
            taste INTEGER, 
            touch INTEGER, 
            vision_sound INTEGER, 
            vision_smell INTEGER, 
            vision_taste INTEGER,
            vision_touch INTEGER, 
            sound_smell INTEGER, 
            sound_taste INTEGER, 
            sound_touch INTEGER, 
            smell_taste INTEGER, 
            smell_touch INTEGER, 
            taste_touch INTEGER
        );

# Commit the changes
conn.commit()"""


# The total counts of synesthetic events, to export to the database
totals = []

vision_words = [
    "see", "look", "watch", "observe", "notice", "gaze", "view", "behold", "perceive",
    "discern", "spot", "spy", "scan", "examine", "inspect", "peer", "stare",
    "glance", "glimpse", "eyeball", "ogle", "discriminate", "peek", "visualize",
    "envision", "picture", "imagine",
    "conjure", "image", "landscape", "scenery", "vista", "panorama", "scene",
    "perspective", "sightseeing", "show", "display", "appearance", "visionary",
    "eyewitness", "observer", "spectator", "beholder", "bright", "light", "dark",
    "colorful", "vivid", "dull", "shiny", "glowing", "brilliant", "radiant", "luminous",
    "gleaming", "sparkling", "glistening", "muted", "shadowy", "murky", "hazy", "clear",
    "blurry", "fuzzy", "sharp", "foggy", "misty", "smoky", "transparent", "translucent",
    "opaque", "sunlit", "moonlit", "dim", "dazzling", "glare", "glimmer", "glint", "beam",
    "glow", "twinkle", "sparkle", "shimmer", "flash", "reflection", "silhouette", "contrast",
    "hue", "shade", "tint", "chromatic", "monochromatic", "multicolored",
    "polychromatic", "rainbow", "vibrant", "pale", "pastel", "neon", "eyeful", "observant",
    "eyeglasses", "glasses", "telescope", "binoculars", "periscope", "ocular", "spectacles",
    "spyglass", "contact", "lens", "eyepiece", "goggle", "regard", "descry", "discover",
    "recognize", "wink", "blink", "squint", "leer", "gleam", "gleeful",
    "keen", "perceptive", "discern", "scrutinize", "hawk-eyed", "eagle-eyed",
    "pert", "coy", "arch", "sly", "furtive", "covert", "peeping", "peering", "astute",
    "discerning", "penetration", "gaze", "stare", "glower", "frown", "scowl",
    "glowering", "frowning", "leering", "scowling", "blink", "squint",
    "droop", "flutter", "widen", "narrow", "squint", "gaze", "glance",
    "peering", "peep", "pry", "glimpse", "descry", "discern", "ken", "espied", "mark",
    "glimmer", "glimmering", "gleeful", "lustrous", "glisten",
    "radiant", "beaming", "effulgent", "fulgent", "refulgent", "splendid", "glorious",
    "ethereal", "ethereality", "etherealize", "etherealized", "celestial", "heavenly",
    "supernal", "celestial", "heavenly", "divine", "godly", "angelic", "ethereal",
    "ghostly", "spectral", "spectralize", "spectralized", "wraithlike", "phantasmal",
    "illusory", "illusory", "illusoriness", "unreal", "unrealness", "visionary",
    "spectral", "ghostly", "visionary", "hallucination", "hallucinatory", "hallucinate",
    "hallucinated", "mirage", "phantasmagoria", "phantasmagoric", "phantasmagorical",
    "grotesque", "macabre", "gruesome", "ghastly", "hideous",
    "menacing", "threatening", "foreboding", "portentous", "lurid",
    "black", "white", "red", "green", "blue", "gray", "brown", "yellow", "purple", 
    "orange", "pink", "turquoise", "navy", "silver", "gold", "beige", "cream", "maroon"
]

sound_words = [
    "hear", "listen", "sound", "resound", "echo", "reverberate", "ring", "boom",
    "crash", "bang", "clatter", "jingle", "rattle", "sizzle", "crackle", "pop",
    "whisper", "murmur", "rustle", "hum", "buzz", "drone", "roar", "scream", "shriek",
    "shout", "yell", "cry", "wail", "moan", "groan", "sigh", "sob", "sang", "sung",
    "twitter", "chirp", "sing", "croak", "growl", "snarl", "bark", "meow", "moo", "baa",
    "trumpet", "roar", "hoot", "coo", "cluck", "bleat", "neigh", "whine", "howl",
    "tingle", "jangle", "thrum", "thump", "thud", "clink", "clank", "scrape", "grate",
    "screech", "shriek", "squeak", "squawk", "babble", "gabble", "chatter", "prattle",
    "sound", "noise", "tone", "note", "pitch", "volume", "harmony", "melody", "radio",
    "rhythm", "discord", "cacophony", "silence", "echo", "reverberation", "frequency"
    "rustle", "hum", "buzz", "drone", "roar", "scream", "shriek", "shout",
    "clang", "hiss", "chirp", "trill", "screeching", "twang", "strum", "thump", "thud", "clink", "clank",
    "loud", "soft", "high-pitched", "low-pitched", "deafening", "shrill", "mellow", "melodic",
    "harmonic", "discordant", "rhythmic", "silent", "echoing", "reverberating", "whispering",
    "murmuring", "rustling", "humming", "buzzing", "droning", "roaring", "screaming", "shrieking",
    "shouting", "crying", "wailing", "moaning", "groaning", "sighing", "sobbing",
    "hark", "harkening", "hearken", "harker", "harkest", "harkened", "harkens",
    "harkeneth", "harkeningly", "harkener", "harkeners", "minstrel", "minstrelsy",
    "minstrel's", "minstrels", "bard", "ballad", "balladeer", "ballading", "lute",
    "lyre", "harp", "dulcimer", "recital", "recitative", "recitatively", "recitative's",
    "recitatives", "chant", "chanting", "chantingly", "chanter", "chantress",
    "chaunt", "chaunting", "chauntingly", "chaunter", "chauntress", "madrigal", "madrigalian",
    "madrigalist", "madrigalists", "madrigal's", "madrigals", "lay", "layman", "laymen",
    "lay's", "lays", "ditty", "ditties", "strain", "strains", "knell", "knell's", "knells",
    "toll", "tolling", "tolls", "tollingly", "tolling's"
]

smell_words = [
    "smell", "sniff", "scent", "inhale", "whiff", "reek", "stink", "perfume", "fragrance",
    "waft", "emanate", "permeate", "pungent", "acrid", "cloying", "fetid", "putrid",
    "sniffle", "breathe", "savour", "detect", "discern", "identify",
    "notice", "odor", "aroma", "stench", "fumes", "bouquet", "pall", "pungency", "acridity", 
    "cloyingness", "fetidness", "putridity", "essence", "hint", "trace", "nuance", "aura",
    "fragrant", "aromatic", "sweet-smelling", "foul-smelling", "musky", "earthy", "floral", "fruity",
    "heady", "invigorating", "refreshing", "unpleasant", "offensive", "overpowering",
    "subtle", "delicate", "distinctive", "heady", "intoxicating", "elicit", "evoke", "conjure",
    "bring to mind", "redolent", "evocative", "nostalgic", "distillation", "redolence", "miasma",
    "nosegay", "pomander", "potpourri", "incense", "frankincense",
    "myrrh", "balsam", "unguent", "ointment", "elixir", "potion", "vial", "phial", "flask",
    "olfactory", "olfaction", "apothecary", "attar", "musk", "civet", "galbanum",
    "asafoetida", "castoreum", "ambergris", "perfumed", "aromatic", "sweet-smelling", "sachet",
    "sniffing", "inhaling", "exhaling", "pungentness", "acridness", "sweetness", "sourness",
    "bitterness", "rankness", "perfumer", "perfumery"
]

taste_words = [
    "taste", "lick", "savour", "relish", "sample", "sip", "chew", "suck", "chomp",
    "savor", "perceive", "tingle", "pucker", "astringe",
    "flavor", "flavour", "palate", "gustation",
    "aftertaste", "tang", "zest", "bite", "kick", "hint", "nuance", "essence",
    "sweet", "sour", "salty", "bitter", "umami",
    "delicious", "yummy", "scrumptious", "luscious", "mouthwatering", "appetizing",
    "tantalizing", "delightful", "pleasing", "bland", "insipid", "unappetizing",
    "astringent",
    "rich", "creamy", "buttery", "nutty", "fruity", "floral", "spicy", "peppery",
    "tangy", "tart", "zesty", "meaty", "gamey", "fishy", "eggy", "metallic",
    "ambrosia", "nectar", "elixir", "potion", "viand", "victual", "provender",
    "regale", "savoury", "savory", "palatable", "palate", "nectarean", "nectareous",
    "luscious", "succulent", "toothsome", "gustatory", "gustation"
]

touch_words = [
    "touch", "feel", "grasp", "grip", "hold", "stroke", "caress", "pat", "rub", "pinch",
    "squeezing", "stroking", "caressing", "grasping", "clutching", "prodding", "poking",
    "gently", "roughly", "lightly", "heavily", "firmly", "delicately", "clumsily",
    "brush", "skim", "graze", "scratch", "tickle", "prick", "sting", "throb", "ache",
    "touch", "feel", "texture", "slippery", "smooth", "rough", "soft", "hard", "wet", "dry", 
    "hot", "cold", "pressure", "vibration", "bumpy", "clammy", "greasy", "sticky", "prickly",
    "tingling", "throbbing", "aching", "gentle", "rough", "light", "heavy", "firm",
    "delicate", "clumsy", "exquisite", "sensuous", "tactile", "tangible",
    "caress", "fondle", "haptic", "tactual", "palpate", "palpation", "embrace", "clasp",
    "clutch", "grasp", "tender", "gentle", "delicate", "caressing", "fondling",
    "coarse", "rough", "harsh", "abrasive", "prickling", "itching", "tingling", "throbbing",
    "itchy", "sharp", "dull", "numb",
]

for x in range(1087):

    # Initialize sentence lists.  Sentences with sensory terms will be put into lists.  Sentences can be in multiple lists.
    vision_sentences = []
    sound_sentences = []
    smell_sentences = []
    taste_sentences = []
    touch_sentences = []
    vision_sound_sentences = []
    vision_smell_sentences = []
    vision_taste_sentences = []
    vision_touch_sentences = []
    sound_smell_sentences = []
    sound_taste_sentences = []
    sound_touch_sentences = []
    smell_taste_sentences = []
    smell_touch_sentences = []
    taste_touch_sentences = []

    # SQL query to get book name
    query = """
            SELECT bookname
            FROM books
            WHERE book_id = """ + str(x)
    
    cursor.execute(query)
    for entry in cursor.fetchall():
        bookname = entry[0]

    # SQL query to get text from a book
    query = """
            SELECT text
            FROM text_files natural join book_file
            WHERE book_file.book_id = """ + str(x)
    
    cursor.execute(query)

    # Iterate through all entries belonging to this book id
    for entry in cursor.fetchall():
        text_content = entry[0]

        sentences = re.split(r"[.!\n,]+", text_content)

        # Process and analyze sentences
        for sentence in sentences:
            # Split the sentence into lowercase words
            words = sentence.lower().split()
            # Check for sensory words in each sentence
            vision = any(word in vision_words for word in words)
            sound = any(word in sound_words for word in words)
            smell = any(word in smell_words for word in words)
            taste = any(word in taste_words for word in words)
            touch = any(word in touch_words for word in words)

            # Sort sentence into appropriate lists
            if vision:
                vision_sentences.append(sentence.strip())
            if sound:
                sound_sentences.append(sentence.strip())
            if smell:
                smell_sentences.append(sentence.strip())
            if taste:
                taste_sentences.append(sentence.strip())
            if touch:
                touch_sentences.append(sentence.strip())

            if vision and sound:
                vision_sound_sentences.append(sentence.strip())
            if vision and smell:
                vision_smell_sentences.append(sentence.strip())
            if vision and taste:
                vision_taste_sentences.append(sentence.strip())
            if vision and touch:
                vision_touch_sentences.append(sentence.strip())
            if sound and smell:
                sound_smell_sentences.append(sentence.strip())
            if sound and taste:
                sound_taste_sentences.append(sentence.strip())
            if sound and touch:
                sound_touch_sentences.append(sentence.strip())
            if smell and taste:
                smell_taste_sentences.append(sentence.strip())
            if smell and touch:
                smell_touch_sentences.append(sentence.strip())
            if taste and touch:
                taste_touch_sentences.append(sentence.strip())

        '''print("Vision sentences:\n")
        for sentence in vision_sentences:
            print(sentence)
        print("\nSound sentences:\n")
        for sentence in sound_sentences:
            print(sentence)
        print("\nSmell sentences:\n")
        for sentence in smell_sentences:
            print(sentence)
        print("\nTaste sentences:\n")
        for sentence in taste_sentences:
            print(sentence)
        print("\nTouch sentences:\n")
        for sentence in touch_sentences:
            print(sentence)

        print("\nVision/Sound sentences:\n")
        for sentence in vision_sound_sentences:
            print(sentence)
        print("\nVision/Smell sentences:\n")
        for sentence in vision_smell_sentences:
            print(sentence)
        print("\nVision/Taste sentences:\n")
        for sentence in vision_taste_sentences:
            print(sentence)
        print("\nVision/Touch sentences:\n")
        for sentence in vision_touch_sentences:
            print(sentence)
        print("\nSound/Smell sentences:\n")
        for sentence in sound_smell_sentences:
            print(sentence)
        print("\nSound/Taste sentences:\n")
        for sentence in sound_taste_sentences:
            print(sentence)
        print("\nSound/Touch sentences:\n")
        for sentence in sound_touch_sentences:
            print(sentence)
        print("\nSmell/Taste sentences:\n")
        for sentence in smell_taste_sentences:
            print(sentence)
        print("\nSmell/Touch sentences:\n")
        for sentence in smell_touch_sentences:
            print(sentence)
        print("\nTaste/Touch sentences:\n")
        for sentence in taste_touch_sentences:
            print(sentence)'''
        
    print(x)

    totals.append([x, bookname, len(vision_sentences), len(sound_sentences), len(smell_sentences), len(taste_sentences), len(touch_sentences),
                    len(vision_sound_sentences), len(vision_smell_sentences), len(vision_taste_sentences), len(vision_touch_sentences),
                    len(sound_smell_sentences), len(sound_taste_sentences), len(sound_touch_sentences), len(smell_touch_sentences),
                    len(smell_taste_sentences), len(taste_touch_sentences)])
        
    print("length")
    print(len(totals))
    
    
# Define the SQL statement with placeholders for each attribute
sql = """INSERT INTO synesthesia (book_index, book_name, vision, sound, smell, taste, touch, vision_sound, vision_smell, vision_taste,
        vision_touch, sound_smell, sound_taste, sound_touch, smell_taste, smell_touch, taste_touch) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

for x in range(len(totals)):
    cursor.execute(sql, totals[x])

print(totals)

conn.commit()
cursor.close()
conn.close()