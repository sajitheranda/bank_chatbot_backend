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


