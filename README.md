Restaurant Food Chat Bot using Dialogflow, FastAPI, and MySQL
-------------------------------------------------------------

### Overview

This project aims to create a restaurant food chatbot using Google Dialogflow for natural language processing, Python FastAPI for backend development, and MySQL for database management. The chatbot allows users to interact in natural language to inquire about the restaurant's menu, place orders, make reservations, and get recommendations.

### Features

1.  Natural Language Processing: Utilizes Google Dialogflow for understanding user queries and generating appropriate responses.
2.  Menu Inquiry: Users can ask about the restaurant's menu, including dishes, prices, and ingredients.
3.  Order Placement: Allows users to place orders directly through the chatbot interface.
4.  Reservation Handling: Supports reservation requests, including date, time, number of guests, and special preferences.
5.  Recommendations: Provides personalized food recommendations based on user preferences and past orders.
6.  Database Integration: Uses MySQL to store and manage restaurant data, including menus, orders, reservations, and user information.
7.  FastAPI Backend: Implements a FastAPI backend to handle incoming requests from Dialogflow, process logic, and interact with the database.
8.  RESTful API: Exposes RESTful endpoints for various functionalities, making it easy to integrate with different clients.

### Technologies Used

-   Google Dialogflow
-   Python FastAPI
-   MySQL
-   Dialogflow SDK for Python
-   SQLAlchemy (for database ORM)
-   Docker (optional, for containerization)

### Installation and Setup

1.  Clone the Repository

    bashCopy code

    `git clone https://github.com/your-username/restaurant-chatbot.git
    cd restaurant-chatbot`

2.  Install Dependencies

    bashCopy code

    `pip install -r requirements.txt`

3.  Database Configuration

    -   Create a MySQL database and update the database credentials in `config.py`.
4.  Dialogflow Configuration

    -   Create a Dialogflow agent and configure intents, entities, and fulfillment webhook.
    -   Update the Dialogflow credentials in `config.py`.
5.  Run the Application

    bashCopy code

    `uvicorn main:app --reload`

6.  Access the API

    -   API documentation and endpoints will be available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc).

### Usage

1.  Chatbot Interaction

    -   Access the chatbot through the configured messaging platform (e.g., website widget, Telegram, etc.).
    -   Start conversing with the chatbot by asking questions, placing orders, making reservations, etc.
2.  API Integration

    -   Integrate the RESTful API endpoints with frontend applications or other services to extend functionality and provide a seamless user experience.
