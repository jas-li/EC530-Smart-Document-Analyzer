# EC530-Smart-Document-Analyzer

## Overview
https://github.com/jas-li/EC530-Smart-Document-Analyzer/assets/90875953/c5b60420-e3b4-41cc-9816-d77df349314e

## Authentication Endpoints

### Register
- **Method:** POST
- **Endpoint:** `/register`
- **Description:** Registers a new user in the system.
- **Parameters:** None (expects user data in request body)
- **Response:** Standard message indicating success or failure.

### Login
- **Method:** POST
- **Endpoint:** `/login`
- **Description:** Authenticates a user and establishes a session.
- **Parameters:** `username` and `password` in JSON body.
- **Response:** Token upon successful authentication; error message otherwise.

## File Handling Endpoints

### Upload File
- **Method:** POST
- **Endpoint:** `/upload`
- **Description:** Allows authenticated users to upload files.
- **Authentication Required:** Yes
- **Parameters:** File data in multipart/form data format.
- **Response:** Success or error message, including any server-side validation issues.

### Delete File
- **Method:** POST
- **Endpoint:** `/delete_file`
- **Description:** Allows authenticated users to delete their uploaded files.
- **Authentication Required:** Yes
- **Parameters:** `filename` in request args.
- **Response:** Success or error message.

### Get User Files
- **Method:** GET
- **Endpoint:** `/get_files`
- **Description:** Retrieves a list of files uploaded by the authenticated user.
- **Authentication Required:** Yes
- **Parameters:** None.
- **Response:** List of files or an error message.

## Document and Content Processing Endpoints

### Convert Document to Text
- **Method:** GET
- **Endpoint:** `/doc_to_text`
- **Description:** Converts an uploaded document to text for the authenticated user.
- **Authentication Required:** Yes
- **Parameters:** `filename` in request args.
- **Response:** Extracted text or an error message.

### Extract Content from URL
- **Method:** POST
- **Endpoint:** `/extract_from_url`
- **Description:** Extracts content from the specified URL.
- **Parameters:** JSON object containing `url`.
- **Response:** Extracted content or error message.

## NLP Analysis Endpoints

### Extract Keywords
- **Method:** POST
- **Endpoint:** `/text_keyword`
- **Description:** Extracts keywords from the provided text.
- **Parameters:** JSON object containing `text`.
- **Response:** List of keywords or error message.

### Generate Text Summary
- **Method:** POST
- **Endpoint:** `/text_summary`
- **Description:** Summarizes the provided text.
- **Parameters:** JSON object containing `text`.
- **Response:** Summary of text or error message.

### Analyze Text Sentiment
- **Method:** POST
- **Endpoint:** `/text_sentiment`
- **Description:** Analyzes the sentiment of the provided text.
- **Parameters:** JSON object containing `text`.
- **Response:** Sentiment analysis result or error message.

## External Content Search Endpoints

### Search Content Links
- **Method:** GET
- **Endpoint:** `/content_links`
- **Description:** Retrieves links from Wikipedia and NYTimes based on a keyword.
- **Parameters:** `keyword` in request args.
- **Response:** Links from Wikipedia and NYTimes or an error message.

### Get Word Definitions
- **Method:** GET
- **Endpoint:** `/keyword_def`
- **Description:** Retrieves definitions for a specified word.
- **Parameters:** `word` in request args.
- **Response:** Definitions or an error message.

## Running the Application

Host the Flask application with `python app.py`.
