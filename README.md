# Flask Weather Chatbot

This is a simple weather chatbot implemented using Flask. It utilizes the geopy library to retrieve weather information based on user queries.

## Prerequisites

Make sure you have the required packages installed. The requirements.txt file can be provided soon. For now, you need to install the following packages manually:

- Flask
- geopy

You can install them using pip:

## Step 1: Set Up the Environment

[Optional]: Create a virtual environment to keep the project dependencies isolated.

## Step 2: Run the Python File

Run the following command in your terminal:

# python3 app.py (on Mac)

or probably

# python app.py (on Windows)

This will start the Flask server and make the chatbot available.

## Step 3: Make the Local Server Online using Ngrok

Assuming you have Ngrok installed, follow these steps:

1. Run Ngrok in your terminal:

Replace `[port]` with the port number used by your Flask server (example 5000).

2. Ngrok will generate a forwarding URL for you. Use this URL to make your local server accessible from the internet.

## Step 4: Import the Exported Agent into Diagramflow CX

1.  Log in to your Diagramflow CX account.

2. Create a new project or open an existing one.

3. Import the `.blob` file.

Wait for the import process to complete. Once finished, you will have the WeatherBot agent available in Diagramflow CX.

## Step 5: Connect to Diagramflow CX Webhook

In the Diagramflow CX configuration, update the webhook URL to the corresponding Ngrok URL you obtained in Step 3. This ensures that the chatbot can receive and respond to user queries.

That's it! Your Flask weather chatbot is now set up and connected to Diagramflow CX.

Feel free to test or customize the chatbot's behavior and add more functionality as needed.