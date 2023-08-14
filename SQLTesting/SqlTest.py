from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column,
    ForeignKey,
    insert
)
import json

engine = create_engine("sqlite:///:memory:", future=True)
metadata_obj = MetaData()

artist = Table(
    "top_artists",
    metadata_obj,
    Column("name", String, primary_key=True),
    Column("streams", Integer),
    Column("daily", Integer),
    
)

songs = Table(
    "top_songs",
    metadata_obj,
    Column("artist", String, primary_key=True),
    Column("track", String, ForeignKey("top_artists.name")),
    Column("streams", Integer)
)

metadata_obj.create_all(engine)

from sqlalchemy import insert

artist_rows = [
    {"name": "Drake", "streams": 82772, "daily": 46},
    {"name": "Bad Bunny", "streams": 65547, "daily": 53},
    {"name": "Taylor Swift", "streams": 53714, "daily": 96},
    {"name": "The Weeknd", "streams": 51735, "daily": 47},
    {"name": "Ed Sherran", "streams": 47149, "daily": 19},
]

songs_rows = [
    {"artist": "The Weeknd", "track": "Blinding Lights", "streams": 3712},
    {"artist": "Ed Sherran", "track": "Shape of You", "streams": 3568},
    {"artist": "Lewis Capalidi", "track": "Someone You Loved", "streams": 2894},
    {"artist": "Post Malone", "track": "Blinding Lights", "streams": 2818},
    {"artist": "Drake", "track": "Blinding Lights", "streams": 2719},
    
]

for artist_row in artist_rows:
    stmt = insert(artist).values(**artist_row)
    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        connection.commit()
        
for songs_row in songs_rows:
    stmt = insert(songs).values(**songs_row)
    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        connection.commit()

print("Metadata tables:", metadata_obj.tables.keys())

# Get the metadata as a dictionary
metadata_dict = {}
for table in metadata_obj.sorted_tables:
    table_info = {}
    table_info['columns'] = {column.name: str(column.type) for column in table.columns}
    primary_keys = [column.name for column in table.columns if column.primary_key]
    if primary_keys:
        table_info['primary_keys'] = primary_keys

    foreign_keys = {}
    for column in table.columns:
        if isinstance(column.type, ForeignKey):
            foreign_keys[column.name] = column.type.column.table.name
    if foreign_keys:
        table_info['foreign_keys'] = foreign_keys

    metadata_dict[table.name] = table_info

# Convert the metadata dictionary to a JSON string
metadata_json = json.dumps(metadata_dict, indent=2)

# Output the metadata JSON
print(metadata_json)
    
# Import to OpenAI
import openai
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

messages = [{"role": "system", "content": f"""You are a SQL developer that will take in metadata {metadata_json} to answer the questions a user may have regarding the table.
             """},
             {"role": "user", "content": "What is the highest streamed song and how many daily streams does the artist have?"}]

response = openai.ChatCompletion.create(
    messages=messages,
    model='gpt-3.5-turbo',
    max_tokens = 160
    )

print(response)
