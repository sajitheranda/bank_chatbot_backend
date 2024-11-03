# Bank Chatbot Backend using Rasa (Sinhala and English)

This project is a backend for a bank chatbot developed using [Rasa](https://rasa.com/), supporting interactions in both Sinhala and English. The chatbot assists users with various banking services, including checking account balances, applying for loans, and accessing transaction details.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Key Files and Configuration](#key-files-and-configuration)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [License](#license)

## Features
- **Bilingual Support**: Communicates in both Sinhala and English.
- **Banking Services**:
  - Check account balances.
  - View recent transactions.
  - Apply for different types of loans.
  - Apply for credit or debit cards.
- **User Input Validation**: Forms for securely collecting user details like account numbers and passwords.
- **Predefined Responses**: Intents for greeting, affirmation, denial, and mood expressions.
- **Custom Actions**: Logic for handling forms and user input to provide a seamless conversation flow.

## Project Structure

- **root/**
  - **data/**
    - `nlu.yml`: Training data for NLU in Sinhala and English
    - `stories.yml`: Stories for training conversation paths
  - `domain.yml`: Domain configuration file with intents, entities, and responses
  - `actions.py`: Custom action implementations
  - `rules.yml`: Rules for handling common user interactions
  - `config.yml`: Pipeline and policy configurations
  - `endpoints.yml`: Configurations for action server endpoints
  - `credentials.yml`: Credentials for external integrations



## Key Files and Configuration

### `nlu.yml`
Contains training examples for various intents in both Sinhala and English:
  - ```yaml
    - intent: greet
      examples: |
        - hey
        - hello
        - hi
        - ආයුබෝවන්
        - හෙලෝ
    
    - intent: account_balance
      examples: |
        - How can I check my account balance?
        - mata account balance eka balanaa one.


### `rules.yml`
Defines how the bot should respond to certain intents and manage active forms:
  - ```yaml
    - rule: Activate balance form
      steps:
      - intent: account_balance
      - action: account_balance_form
      - active_loop: account_balance_form

### `stories.yml`
Contains user stories that help train the conversation model:
  - ```yaml
    - story: account balance form
    steps:
    - intent: account_balance
    - action: account_balance_form
    - active_loop: account_balance_form
    - slot_was_set:
      - requested_slot: username
    - active_loop: null
    - action: get_account_balance

### `actions.py`
Implements custom actions for handling logic beyond predefined responses:
 - ```python
    from rasa_sdk import Action, Tracker
    from rasa_sdk.executor import CollectingDispatcher
    
    class GetAccountBalance(Action):
        def name(self):
            return "get_account_balance"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(text="Your current account balance is Rs. 50,000.")
        return []

## Installation and Setup
1. Clone the repository:
  - ``` bash
    git clone https://github.com/sajitheranda/bank_chatbot_backend.git
    cd bank_chatbot_backend

2. Set up a virtual environment:
  - ``` bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
3. Install dependencies:
  - ``` bash
    pip install rasa
    pip install rasa-sdk

4. Train the Rasa model:
 - ``` bash
    rasa train

5. Run the Rasa server:
- ``` bash
  rasa run --cors "*" --enable-api

6. Run the action server:
- ``` bash
  rasa run actions


    
## Usage

- **Start the bot**: Use a frontend integration or API call to communicate with the Rasa server.
- **Interacting with the bot**: The bot supports user inputs in both Sinhala and English, facilitating seamless bilingual conversations.

## Technologies Used

- **Rasa Open Source**: Natural Language Understanding (NLU) and dialogue management.
- **Python**: For building custom actions and logic.
- **YAML**: Configuration and training data format.

