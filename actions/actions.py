# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import List, Dict, Text, Any
from rasa_sdk import FormValidationAction, Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os

class WelcomeUser(Action):
    """Sends a welcome message to the user"""

    def name(self) -> Text:
        return "welcome_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        welcome_message = f"Welcome {username}!"
        # dispatcher.utter_message(welcome_message)
        GetAccountTransactions()
        return []

class GetAccountBalance(FormValidationAction):
    """Collects user information to provide account balance details"""

    def name(self):
        return "get_account_balance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")
        
        try:
            # Make a request to the authentication service to verify the password
            auth_url = f"https://backend-5glg.onrender.com/{username}/{password}"  # Replace with your actual URL
            response = requests.get(auth_url)

            if response.status_code == 200 and response.json().get("status") == "success":
                # Password is correct
                # Continue with fetching account transactions
                account_number = tracker.get_slot("account_number")
                    # You can use the account_number to fetch actual account balance from your backend/database
                account_balance = fetch_account_balance(username, account_number)  # Implement this function
                if account_balance:
                    dispatcher.utter_message(f"Your account balance is {account_balance}")
                else:
                    dispatcher.utter_message("Account number not found")
            else:
                # Password is incorrect
                dispatcher.utter_message("Invalid username or password. Please try again.")
        except Exception as e:
            dispatcher.utter_message(f"Error while working,send agian message")
        return []

class GetAccountTransactions(Action):
    """Collects user information to provide account transaction details"""

    def name(self) -> Text:
        return "get_account_transactions"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")
        
        try:
            # Make a request to the authentication service to verify the password
            auth_url = f"https://backend-5glg.onrender.com/{username}/{password}"  # Replace with your actual URL
            response = requests.get(auth_url)

            if response.status_code == 200 and response.json().get("status") == "success":
                # Password is correct
                # Continue with fetching account transactions
                account_number = tracker.get_slot("account_number")
                # You can use the account_number to fetch actual account transactions from your backend/database
                transactions = fetch_account_transactions(username, account_number)  # Implement this function
                if transactions:
                    response_message = "\n".join(transactions)
                    dispatcher.utter_message(f"Here are your account transactions:\n{response_message}")
                else:
                    dispatcher.utter_message("Account number not found.")
            else:
                # Password is incorrect
                dispatcher.utter_message("Invalid username or password. Please try again.")
        except Exception as e:
            dispatcher.utter_message(f"Error while working,send agian message")

        return []

class GetResponseAction(Action):
    def name(self) -> Text:
        return "get_response"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Get the question from the user utterance
        try:
            question = tracker.latest_message["text"]

            # Send the question to the Flask app and get the response
            response = requests.post(
                "http://e1ec-35-194-41-212.ngrok-free.app/", json={"question": question}
            ).json()

            dispatcher.utter_message(str(response)[12:-2])
        except Exception as e:
            dispatcher.utter_message(f"Mesaage is not received yet.")

        return []

# Implement the fetch_account_balance function as per your database/backend logic
def fetch_account_balance(username, account_number):
    # Implement the logic to fetch account balance from your database/backend
    # Replace this with your actual implementation
    url = f"https://backend-5glg.onrender.com/{username}/account"
    response = requests.get(url)
    data = response.json()

    if account_number in data:
        return str(data[account_number]["balance"])
    else:
        return None

# Implement the fetch_account_transactions function as per your database/backend logic
def fetch_account_transactions(username, account_number):
    # Implement the logic to fetch account transactions from your database/backend
    # Replace this with your actual implementation
    try:
        url = f"https://backend-5glg.onrender.com/{username}/account"
        response = requests.get(url)
        data = response.json()

        if account_number in data and "transaction" in data[account_number]:
            transactions = data[account_number]["transaction"]["3332"]
            transaction_details = [
                f"Amount: {str(transactions['amount'])}, "
                f"Description: {transactions['transaction_description']}, "
                f"Timestamp: {transactions['transaction_timestamp']}"
                # for transaction in transactions.values()
            ]
            return transaction_details
    except Exception as e:
        return []

from rasa_sdk.events import AllSlotsReset

class ActionResetAllSlots(Action):

    def name(self):
        return "reset_all_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Logout.")
        return [AllSlotsReset()]


class SaveLoanApplication(Action):
    """Save user loan form"""

    def name(self) -> Text:
        return "save_loan_application"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")
        account_number= tracker.get_slot("account_number")
        loan_type = tracker.get_slot("loan_type")
        loan_amount = tracker.get_slot("loan_amount")
        loan_duration= tracker.get_slot("loan_duration")
        telephone_number= tracker.get_slot("telephone_number")
        email= tracker.get_slot("email")
        loan_reason= tracker.get_slot("loan_reason")
        
        
        # dispatcher.utter_message(f'''username = {username}
        #                              password = {password}
        #                              loan_type = {loan_type}
        #                              loan_amount = {loan_amount}
        #                              loan_duration = {loan_duration}
        #                              telephone_number = {telephone_number}
        #                              email = {email}
        #                              loan_reason = {loan_reason}
        #                            ''')
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Combine the current directory with the JSON key file's name
        credentials_file = os.path.join(current_directory, "rasachat1-firebase-admin.json")

        try:
            # Initialize Firebase Admin SDK with the relative path to the JSON key file
            cred = credentials.Certificate(credentials_file)
            firebase_admin.initialize_app(cred)

            # Access the Firestore database
            db = firestore.client()

            # Rest of your code to save data to Firebase
            loan_apply_ref = db.collection("Loan_apply")

            # Create a document with the data
            new_loan_doc_ref = loan_apply_ref.add({
                "username": username,
                "password": password,
                "loan_type": loan_type,
                "loan_amount": loan_amount,
                "loan_duration": loan_duration,
                "telephone_number": telephone_number,
                "email": email,
                "loan_reason": loan_reason
            })
            db.close()
            firebase_admin.delete_app(firebase_admin.get_app())
            dispatcher.utter_message("Data saved,you wiil inform about loan later by an email")
            # dispatcher.utter_message("Data saved to Firebase.")
        except Exception as e:
            dispatcher.utter_message(f"Error while working,send agian message")
            # dispatcher.utter_message(f"Error: {str(e)}")

        
        
        return []


class SaveCardApplication(Action):
    """Save user card form"""

    def name(self) -> Text:
        return "save_card_application"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")
        card_type = tracker.get_slot("card_type")
        card_amount = tracker.get_slot("card_amount")
        telephone_number= tracker.get_slot("telephone_number")
        email= tracker.get_slot("email")
        
        
        # dispatcher.utter_message(f'''username = {username}
        #                              password = {password}
        #                              card_type = {card_type}
        #                              card_amount = {card_amount}
        #                              telephone_number = {telephone_number}
        #                              email = {email}
        #                            ''')
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Combine the current directory with the JSON key file's name
        credentials_file = os.path.join(current_directory, "rasachat1-firebase-admin.json")

        try:
            # Initialize Firebase Admin SDK with the relative path to the JSON key file
            cred = credentials.Certificate(credentials_file)
            firebase_admin.initialize_app(cred)

            # Access the Firestore database
            db = firestore.client()

            # Rest of your code to save data to Firebase
            loan_apply_ref = db.collection("Card_apply")

            # Create a document with the data
            new_loan_doc_ref = loan_apply_ref.add({
                "username": username,
                "password": password,
                "card_type": card_type,
                "card_amount": card_amount,
                "telephone_number": telephone_number,
                "email": email
            })
            db.close()
            firebase_admin.delete_app(firebase_admin.get_app())
            dispatcher.utter_message("Data saved,you wiil inform about card issuing later by an email")
            # dispatcher.utter_message("Data saved to Firebase.")
        except Exception as e:
            dispatcher.utter_message(f"Error: {str(e)}")

        
        
        dispatcher.utter_message("Data saves.you wiil inform about card isuue later by an email")
        return []



