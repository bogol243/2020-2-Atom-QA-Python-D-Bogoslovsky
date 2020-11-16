APP_HOST = '127.0.0.1'
APP_PORT = 8080

APP_HOST_2 = '127.0.0.1'
APP_PORT_2 = 8082

MOCK_HOST = '127.0.0.1'
MOCK_PORT = 8081

MOCK_HOST_2 = '127.0.0.1'
MOCK_PORT_2 = 8083

CAUSE_500 = "000,111111"

APP_UP_MOCK_DOWN = ('127.0.0.1',9081,'127.0.0.1:9082')

ABSENT_ID = "-1"
ABSENT_TITLE = "n9e6he36teh61o38tnekl"

MOCK_DATA = {
    "data": {
        "123yn1k75m7lm1l": {
            "data": {
                "1": {
                    "title": "First text of first user",
                    "text": "some sample text"
                },
                "2": {
                    "title": "Second text of first user",
                    "text": "Other example data"
                }
            },
            "last_id": 2
        },
        "lrm8lm3l4322l219": {
            "data": {
                "1": {
                    "title": "First text of second user",
                    "text": "some sample text of other user"
                },
                "2": {
                    "title": "Second text of second user",
                    "text": "Other example data of other user"
                }
            },
            "last_id": 2
        }
    },
    "tokens": {
        "(123,123456)": "123yn1k75m7lm1l",  # normal
        "(321,654321)": "lrm8lm3l4322l219", # normal
        CAUSE_500: "ioe328ronh983e45"  # for causing 500
    }
}