# Vivent Ticket Generator

**Note:** This project is only supported on **Windows OS** due to dependencies on Windows-specific Chrome binaries and rendering tools.

The **Vivent Ticket Generator** is a Python-based application designed to generate personalized event tickets for participants, upload them to a cloud storage service (Sirv), and update the database with the ticket links. This tool is ideal for managing event participants and automating the ticket generation process.

---

## Features

- **Dynamic Ticket Generation**: Generates personalized tickets with participant details and QR codes.
- **Cloud Upload**: Uploads tickets to Sirv cloud storage for easy access.
- **Database Integration**: Updates the database with the public URLs of the uploaded tickets.
- **Customizable Templates**: Supports HTML-based ticket templates for branding and customization.

---

## Prerequisites

**Important:** This project is only supported on **Windows OS**. Ensure you are running the project on a Windows machine.

Before running the project, ensure you have the following installed:

- Supported chrome binaries ([in here we use v131.0.6778.0](https://drive.google.com/drive/folders/1NkBMQMXUH4MYmXoTGKL73heSGs9G37qo?usp=sharing))
- Python 3.9 or higher
- PostgreSQL database
- Google Chrome (for `html2image` rendering)
- A Sirv account with API credentials

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PinsaraPerera/Vivent-ticket-generator.git
   cd Vivent-ticket-generator
   ```

2. **Set Up a Virtual Environment**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:Create a `.env` file in the root directory and add the following:
    ```bash
    DB_HOST=your_database_host
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_NAME=your_database_name
    CLIENT_ID=your_sirv_client_id
    CLIENT_SECRET=your_sirv_client_secret
    ```

5. **Set Up the Database**:Ensure your PostgreSQL database is running and the required tables (`participants`, `events`, etc.) are created.

6. **Unzip the downloaded chrome binaries in to the project root**: [Download from here ⬇️](https://drive.google.com/drive/folders/1NkBMQMXUH4MYmXoTGKL73heSGs9G37qo?usp=sharing)

## Usage

1. **Generate and Upload Tickets**: Run the generator.py script to process participants, generate tickets, upload them to Sirv, and update the database:
    ```bash
    python -m generator.generator
    ```

2. **Customize Ticket Templates**: Modify the template_1 variable in generator.py to customize the ticket design.

3. **Debugging**: Logs are generated for each step of the process. Check the logs for detailed information about errors or successful operations.

## Project Structure

    Vivent-ticket-generator/
    │
    |── chrome-win/            # chrome.exe with binaries(v131)
    ├── db/
    │   ├── config.py          # Database and environment configuration
    │   ├── db.py              # Database session management
    │   ├── participant_model.py  # SQLAlchemy model for participants
    │
    ├── generator/
    │   ├── generator.py       # Main script for ticket generation and upload
    │   ├── upload_tickets.py  # Handles file uploads to Sirv
    │
    ├── assets/
    │   ├── fosslogo.png       # Logo used in ticket templates
    │
    ├── tickets/               # Directory where generated tickets are saved
    │
    ├── .env                   # Environment variables 


## Example Workflow

1. **Add Participants**: Ensure participants are added to the database with their details (e.g., firstName, lastName, eventId).

2. **Run the Script**: Execute the generator.py script to process participants for a specific event.

Example Output

![Sample Ticket](./tickets/b16bf10d-c1d7-4267-b33a-2b6c8de3704f.png)

3. **Access Tickets**: Tickets are uploaded to Sirv and can be accessed via the public URLs stored in the database.

## Troubleshooting

- Database Errors: Ensure the database connection details in the .env file are correct and the database is running.

- Sirv Upload Issues: Verify the CLIENT_ID and CLIENT_SECRET in the .env file are correct and have the necessary permissions.

- HTML to Image Issues: Ensure Google Chrome is installed and the path to the executable is correctly set in Html2Image.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments ❤️

- SQLAlchemy for ORM support.
- html2image for rendering HTML to images.
- Sirv for cloud storage and API support.
- QRCode for generating QR codes.

## Compatibility

This project is designed to work only on **Windows OS** due to the use of Windows-specific Chrome binaries (v131.0.6778.0) for rendering HTML to images.

## Contact

For questions or support, please contact [me](https://pawanperera.com/).

