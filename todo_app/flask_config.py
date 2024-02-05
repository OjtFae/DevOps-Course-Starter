import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')
        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
        self.TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
        #self.TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')
        if not self.TRELLO_API_KEY:
            raise ValueError("No TRELLO_API_KEY set . Did you follow the setup instructions?")
        if not self.TRELLO_API_TOKEN:
            raise ValueError("No TRELLO_API_TOKEN set . Did you follow the setup instructions?")
        if not self.TRELLO_BOARD_ID:
            raise ValueError("No TRELLO_BOARD_ID set . Did you follow the setup instructions?")
