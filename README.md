# BizCard: Extracting Business Card Data with OCR
**linkedIn Video post: https://www.linkedin.com/feed/update/urn:li:activity:7185692821406810112/**
# Overview
BizCard is a Python-based project aimed at extracting information from business cards using Optical Character Recognition (OCR) technology. The extracted data is then organized and stored in a PostgreSQL database, allowing users to manage and retrieve information from various business cards.

# Technologies Used
- Python: Programming language used for development.
- EasyOCR: Python library for performing OCR on images.
- Streamlit: Open-source app framework used for building web interfaces.
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapper for interacting with databases.
- PostgreSQL: Relational database management system used for storing extracted data.
- Pandas: Python library for data manipulation and analysis.

# Workflow
- Home Page: Users can navigate through different sections of the application from the home page, including uploading business cards, modifying details, and viewing extracted data.

- Upload and Extract: Users upload images of business cards through the web interface. The EasyOCR library is then utilized to extract text from the uploaded images. Extracted information includes the cardholder's name, company name, designation, contact details, and address.

- Display Extracted Data: The extracted data is displayed on the web interface, allowing users to review and verify the information. Users can make any necessary modifications or corrections to the extracted details.

- Database Integration: Extracted data is stored in a PostgreSQL database using SQLAlchemy. Each entry in the database corresponds to a business card, with fields such as name, company name, designation, contact information, and address.

- Modify and Delete Data: Users have the option to modify or delete entries in the database. They can select specific entries to edit or remove, providing flexibility in managing stored information.

# Usage
- Clone the repository to your local machine.
- Install the required dependencies using pip install -r requirements.txt.
- Run the Streamlit web app using streamlit run app.py.
- Navigate through the different sections of the application to upload business cards, view extracted data, and manage database entries.
- Future Enhancements
- Implement authentication and user accounts for secure access to the application.
- Enhance OCR accuracy and robustness for improved extraction of text from business card images.
- Add support for additional languages and localization options.
- Integrate with external APIs for additional functionality, such as geocoding addresses or retrieving company information.

![biz2](https://github.com/Lavan1999/Project-3__BizCardDataExtracting/assets/152668558/2165e7d5-3128-45c3-afe4-f8c1253968cc)

![biz1](https://github.com/Lavan1999/Project-3__BizCardDataExtracting/assets/152668558/3d665add-1736-4db1-b38a-bfcedcb39f46)
