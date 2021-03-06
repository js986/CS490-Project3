import os
import sys
import unittest  
import unittest.mock as mock  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app
from app import socketio, app, emit_all_recipes

TEST_ID = 738270100
TEST_RECIPE_ID = 738270101
DIFFICULTY = "easy"
TEST_RECIPE = {
    "user": TEST_ID,
    "images": ["https://spoonacular.com/recipeImages/657178-556x370.jpg"],
    "title": "Protein Packed Carrot Muffins",
    "readyInMinutes": 45,
    "difficulty": DIFFICULTY,
    "servings": 6,
    "description": "A description",
    "tags": ["gluten free", "dinner"],
    "ingredients": [{"name": "Spice Rub", "amount": 1.0, "unit": "tbsp"}],
    "instructions": [{"number": 1, "step": "Preheat oven to 350 f."}],
}

TEST_USER = {"name": "Mr.Tester", "imageURL": "image", "email": "tester@tester.com"}
TEST_ADD_USER = {
    "id": TEST_ID,
    "name": "Mr.Tester",
    "profile_pic": "image",
    "email": "tester@tester.com",
    "shared_recipes": [],
    "shopping_list": ["potato"],
    "saved_recipes": [],
}
TEST_ADD_RECIPE = {
    "id": TEST_RECIPE_ID,
    "user_id": TEST_ID,
    "title": "Protein Packed Carrot Muffins",
    "description": "A description",
    "difficulty": DIFFICULTY,
    "instructions": [{"number": 1, "step": "Preheat oven to 350 f."}],
    "ready_in_minutes": 45,
    "servings": 6,
    "images": ["https://spoonacular.com/recipeImages/657178-556x370.jpg"],
    "ingredients": [{"name": "Spice Rub", "amount": 1.0, "unit": "tbsp"}],
}

TEST_ADD_TAG = {"name": "tag"}

class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_on_new_google_user(self):
        with mock.patch("app.emit_all_recipes"):
            with mock.patch("db_queries.get_user", mocked_get_user):
                with mock.patch("db_queries.add_user"):
                    with mock.patch("db_queries.get_shopping_list", mocked_get_shopping_list):
                        client = socketio.test_client(app)
                        client.emit('new google user', {'test':"test"})
                        received = client.get_received()
                        self.assertEqual(TEST_ADD_USER["name"], received[-1]["args"][0]["username"])
                        client.disconnect()
                        
    def test_on_old_google_user(self):
        with mock.patch("app.emit_all_recipes"):
            client = socketio.test_client(app)
            client.emit('old google user', {})
            received = client.get_received()
            self.assertEqual('logout', received[-1]["args"][0]["logout"])
            client.disconnect()
        
    def test_on_connect(self):
        with mock.patch("app.emit_all_recipes"):
            socketio_test_client = socketio.test_client(app)
            assert socketio_test_client.is_connected()
            received = socketio_test_client.get_received()
            self.assertEqual('Connected', received[-1]["args"][0]["test"])
            socketio_test_client.disconnect()

    def test_on_disconnect(self):
        with mock.patch("app.emit_all_recipes"):
            client1 = socketio.test_client(app)
            client1.disconnect()
            assert not client1.is_connected()
    
    def test_on_recipe_page(self):
        with mock.patch("app.emit_all_recipes"):
            with mock.patch("db_queries.get_user", mocked_get_user):
                with mock.patch("db_queries.get_recipe", mocked_get_recipe):
                    client = socketio.test_client(app)
                    client.emit('recipe page', {'id':1})
                    received = client.get_received()
                    self.assertEqual(TEST_RECIPE["title"], received[-1]["args"][0]["recipe"]["title"])
                    client.disconnect
                    
        
#         pass
#     def test_on_new_search(self):
#         pass
    def test_on_new_user_page(self):
        with mock.patch("app.emit_all_recipes"):
            with mock.patch("db_queries.get_user", mocked_get_user):
                client = socketio.test_client(app)
                client.emit('user page', {'user_id':TEST_ID})
                received = client.get_received()
                self.assertEqual(TEST_ADD_USER["name"], received[-1]["args"][0]["user"]['name'])
                client.disconnect()
        
#     def test_add_to_cart(self):
#         pass
    def test_on_new_zip(self):
        with mock.patch("app.emit_all_recipes"):
            client = socketio.test_client(app)
            client.emit('new zipcode query', {'zip':"12345"})
            received = client.get_received()
            print(received)
            self.assertEqual("12345", received[-1]["args"][0])
            client.disconnect()
#     def test_cart_page(self):
#         pass
#     def test_content_page(self):
#         pass
#     def test_new_recipe(self):
#         pass
#     def test_emit_recipe(self):
#         pass
#     def test_emit_all_recipes(self):
#         pass

# def mocked_emit_all_recipes(channel):
#     pass
#     socketio.emit(
#         MESSAGES_RECEIVED_CHANNEL,
#         {
#             "allMessages": [
#                 MockedMessage("text", "test.png", "test@test.com", "test-message")
#             ]
#         },
#     )
# def mocked_add_user(user_dict):
#     pass 

def mocked_get_shopping_list(user_id):
    return TEST_ADD_USER['shopping_list']

def mocked_get_user(user_id):
    return TEST_ADD_USER

def mocked_get_recipe(recipe_id):
    return TEST_RECIPE
if __name__ == "__main__":
    unittest.main()
        