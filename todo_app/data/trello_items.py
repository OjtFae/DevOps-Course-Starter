import requests
import os
import certifi
import ssl
from todo_app.flask_config import Config

class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list["name"])



def get_items(config: Config) -> list[Item]:
    """
    Fetches all cards from the trello board with id 'boardId and converts them to items.
    
    Args:
        config: User specific configuration parameters
    
    Returns:
        list: The list of saved items.
    """
    userKey= config["TRELLO_API_KEY"]
    userToken= config["TRELLO_API_TOKEN"]
    boardId= config["TRELLO_BOARD_ID"]
    
    get_cards_url = f"http://api.trello.com/1/boards/{boardId}/cards"
    query = {
    'key': userKey,
    'token': userToken
    }
    get_cards_response = requests.request(
    "GET",
    get_cards_url,
    params=query,
    verify=False)
    
    get_lists_url = f"https://api.trello.com/1/cards/{boardId}/list"
    get_lists_response = requests.request(
    "GET",
    get_lists_url,
    params=query,
    verify=False)
    
    if get_cards_response.status_code != 200:
        raise ValueError(f"Server responded {get_cards_response.status_code} instead of 200 OK") 
    #response.json() returns a list of dictionaries - one dictionary for each card
    #we can just get the id and name and create an "item" that we can easily display

    items = []
    for card in get_cards_response.json():
        cardId = card["id"]
        get_lists_url = f"https://api.trello.com/1/cards/{cardId}/list"
        get_lists_response = requests.request(
        "GET",
        get_lists_url,
        params=query,
        verify=False)
        items.append(Item.from_trello_card(card, get_lists_response.json()))
    return items


def add_item(config:Config, title:str):
    """
    Fetches the saved item with the specified ID.

    Args:
        config: User specific configuration parameters
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    userKey= config["TRELLO_API_KEY"]
    userToken= config["TRELLO_API_TOKEN"]
    listId= config["TRELLO_STD_LIST"]
    
    url = "https://api.trello.com/1/cards"
    query = {
    'idList': listId,
    'key': userKey,
    'token': userToken,
    'name': title
    }
    response = requests.request(
    "POST",
    url,
    params=query,
    verify=False)
    if response.status_code != 200:
        raise ValueError(f"Server responded {response.status_code} instead of 200 OK") 
    return response.json()["id"]

def update_item(config:Config, item_id:int, new_status:str):
    userKey= config["TRELLO_API_KEY"]
    userToken= config["TRELLO_API_TOKEN"]
    boardId= config["TRELLO_BOARD_ID"]
    
    get_lists_url = f"https://api.trello.com/1/boards/{boardId}/lists"
    get_lists_query = {
    'key': userKey,
    'token': userToken,
    }
    get_lists_response = requests.request(
    "GET",
    get_lists_url,
    params=get_lists_query,
    verify=False)
    
    list_id = None
    for trello_list in get_lists_response.json():
        if trello_list["name"] == new_status:
            list_id = trello_list["id"]
    
    update_url = f"https://api.trello.com/1/cards/{item_id}"
    update_query = {
    'idList': list_id,
    'key': userKey,
    'token': userToken,
    }
    update_response = requests.request(
    "PUT",
    update_url,
    params=update_query,
    verify=False)
    
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
    TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')    
    print(add_item(TRELLO_API_KEY, TRELLO_API_TOKEN, "65a6f69fe00dca50a85c4ca9", "new card 2"))
    print(get_items(TRELLO_API_KEY, TRELLO_API_TOKEN, "WyPfTVtS"))
    