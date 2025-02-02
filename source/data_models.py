BOOK_TABLE_FIELDS = {
    "ISBN": {
        "type": "VARCHAR",
        "length": 16,
        "index": True,
    },
    "Book_Title": {
        "type": "VARCHAR",
        "length": 200,
        "index": True,
    },
    "Book_Author": {
        "type": "VARCHAR",
        "length": 256,
        "index": True,
    },
    "Year_Of_Publication": {
        "type": "VARCHAR",
        "length": 24,
        "index": True,
    },
    "Publisher": {
        "type": "VARCHAR",
        "length": 146,
        "index": True,
    },
    "Image_URL_S": {
        "type": "VARCHAR",
        "length": 64,
        "index": False,
    },
    "Image_URL_M": {
        "type": "VARCHAR",
        "length": 64,
        "index": False,
    },
    "Image_URL_L": {
        "type": "VARCHAR",
        "length": 64,
        "index": False,
    },
}
