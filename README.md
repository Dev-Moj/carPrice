# Car Pricing System

## Overview
This project is a car pricing system that utilizes data from APIs and web scraping to gather information about cars, stores the data in a MongoDB database, and employs machine learning to calculate the price of cars based on the input data.

## Components
1. **Data Scraping**: The project uses the `CarDataScraper` class to scrape car data from the Divar API and web pages. The data includes details such as title, token, price, and other relevant information.

2. **MongoDB Database**: The scraped data is stored in a MongoDB database named `carPricedb` with a collection named `cars`. The `pymongo` library is used to interact with the database.

3. **Web Scraping**: The `BeautifulSoup` library is employed to extract specific details from the HTML content of car posts on the Divar website.

4. **Data Preprocessing**: The extracted data is processed and converted to a suitable format for storage in the MongoDB database.

5. **Machine Learning (Not Implemented)**: The project mentions the use of machine learning to calculate the price of cars based on the input data. However, the machine learning part is not implemented in the provided code.

## Usage
1. **Dependencies Installation**:
   - Install the required Python libraries using the following command:
     ```
     pip install -r requirement.txt
     ```

2. **MongoDB Setup**:
   - Make sure MongoDB is installed and running on your local machine.
   - Update the MongoDB connection string in the code (`mongodb://localhost:27017/`) if needed.

3. **Run the Code**:
   - Execute the provided Python script to scrape car data and store it in the MongoDB database.
     ```
     python car_pricing_system.py
     ```

4. **Machine Learning (To be Implemented)**:
   - Implement machine learning algorithms to calculate the price of cars based on the stored data.

## Notes
- The project currently scrapes data from the Divar API and website, storing it in a MongoDB database. However, the machine learning component for calculating car prices is yet to be implemented.

- Make sure to handle exceptions appropriately, especially during web scraping, to ensure the robustness of the program.

- The project could be expanded by implementing machine learning models for predicting car prices based on the gathered data.

Feel free to contribute to the project by adding new features, improving existing functionality, or implementing machine learning algorithms for price prediction. Happy coding!