# Gmail Form Data Extractor

This script extracts structured form data from emails in your Gmail account and saves it to a CSV file.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have a Google account with Gmail enabled.
* You have Python 3.6 or later installed on your local machine.
* You have pip installed for managing Python packages.

## Setup

1. Clone this repository or download the `form_data_extractor.py` script to your local machine.

2. Install the required Python packages:
   ```
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

3. Set up Google Cloud Project and enable Gmail API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Gmail API for your project.
   - Create credentials (OAuth client ID) for a Desktop application.
   - Download the client configuration file.

4. Rename the downloaded client configuration file to `client_secret.json` and place it in the same directory as `form_data_extractor.py`.

## Configuration

1. Open `form_data_extractor.py` in a text editor.

2. Modify the `query` parameter in the `main()` function to match the subject of the emails you want to extract. By default, it's set to:
   ```python
   query="subject:'Email Extractor Test'"
   ```

3. Adjust the `fields` list in the `extract_form_data()` function to match the form fields in your emails:
   ```python
   fields = ['Name', 'Email', 'Mobile', 'Address']
   ```

## Usage

1. Open a terminal or command prompt.

2. Navigate to the directory containing `form_data_extractor.py` and `client_secret.json`.

3. Run the script:
   ```
   python form_data_extractor.py
   ```

4. On the first run, the script will open a web browser for you to authenticate with your Google account. Grant the necessary permissions.

5. The script will create a `token.pickle` file to store your credentials for future runs.

6. After execution, you'll find a new file named `form_data.csv` in the same directory, containing the extracted form data.

## Customization

- To change the search criteria, modify the `query` parameter in the `main()` function.
- To adjust the output format or add more fields, modify the `extract_form_data()` function and update the `fieldnames` list in the `main()` function.

## Security Notes

- The `token.pickle` file contains your Google API credentials. Keep it secure and do not share it.
- Do not share your `client_secret.json` file or commit it to version control.

## Troubleshooting

- If you encounter authentication issues, delete the `token.pickle` file and run the script again.
- Ensure that you have the correct permissions set in your Google Cloud Project.

## Disclaimer

This script accesses your Gmail account. Use it responsibly and ensure you have the necessary rights to access and process the email content.
# gmail-content-extractor
