**Dog Breed Information Application**


**Description:**
This project is a Flask-based web application that retrieves and displays information about dog breeds using data from The Dog API.
Users can view breed characteristics, compare two breeds, and generate random dog images.


**How to Run the Application:**
1. Create and activate a virtual environment.


2. Install the following Python packages:
- Flask
- Flask_WTF
- WTForms
- Requests
- OS
- main_functions
3. Add a .env file containing the Dog API key (dog_key=your_key).


4. Run the Flask application with python app.py.


5. Open the application in a browser at http://127.0.0.1:5000.


**API Used and Its Purpose**

**The Dog API** is the primary data source for this web application.
It provides information about various dog breeds including weight, height, origin, temperament, and images.
This application uses the API to populate the dropdown selection with all available breeds, retrieve detailed breed information,
and provide a random image at the user's request.
This API integration allows real-time data access, providing structured data presentation within the web app.

**Features Implemented**

- **Dropdown Menus:** allows users to select dog breeds and compare their information.
- **Text Input:** allows users to input their favorite dog breed and display a corresponding message.
- **Radio Button:** allows users to opt in to displaying a random dog image.
- **Missing-Data Handling:** manages missing API fields by substituting placeholder text (e.g., “Unknown”).
- **Responsive User Interface:** designed with responsive to ensure readability across desktop and mobile devices.