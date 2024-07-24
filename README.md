# Excel Generator from URL

This Flask web application allows users to generate an Excel file from a specified URL. The application fetches data from the provided URL, processes it, and generates an Excel file for download. During the process, users can monitor the progress and see logs in real-time. The application includes a cute tiger logo and a button to copy the default URL for the Guangxi government website.

## Features

- Copy default URL for Guangxi government website with a single click.
- Monitor the progress of data fetching and Excel generation.
- Download the generated Excel file upon completion.

## Prerequisites

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/excel-generator.git
    cd excel-generator
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Save the provided tiger logo image as `tiger_logo.png` in the `static` directory.

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://localhost:5001`.

3. You will see the following interface:

    ![Main Interface](static/screenshot.png)

4. Click the "Copy" button to copy the default URL for the Guangxi government website to your clipboard.

5. Paste the copied URL into the input field, or enter another URL if desired.

6. Click the "Generate and Download Excel" button.

7. You will be redirected to a progress page where you can monitor the data fetching and Excel generation process.

8. Once the process is complete, the Excel file will be automatically downloaded.

## Project Structure

```
your_project_folder/
│
├── app.py
├── gxzf.py
├── requirements.txt
├── static/
│   └── tiger_logo.png
│   └── screenshot.png
└── templates/
    ├── index.html
    └── progress.html
```

## Files

- `app.py`: The main Flask application file.
- `gxzf.py`: The script responsible for fetching data and generating the Excel file.
- `requirements.txt`: A list of required Python packages.
- `static/`: Directory containing static files such as images and stylesheets.
- `templates/`: Directory containing HTML templates for the web application.

## Screenshots

![Main Interface](static/tiger.jpg)

