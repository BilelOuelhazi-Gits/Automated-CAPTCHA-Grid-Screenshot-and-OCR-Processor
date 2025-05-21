# Automated-CAPTCHA-Grid-Screenshot-and-OCR-Processor
This project automates the process of capturing and analyzing CAPTCHA grids from the BLS Tunisia Visa website using Selenium, Pillow (PIL), and Tesseract OCR.

The script:

Navigates to the webpage using Selenium.

Captures a full-page screenshot after interacting with the form.

Crops out a top instruction line and a 3×3 CAPTCHA grid.

Further crops and processes each grid cell using image enhancement techniques like contrast adjustment and adaptive thresholding.

Runs OCR using Tesseract to extract potential text or digits from each segment.

Key Features:

Automated interaction with dynamic web content (Selenium)

Advanced image preprocessing for better OCR results

Grid segmentation logic for CAPTCHA-style layouts

Logs extracted text from each segment

Designed to be adaptable for similar CAPTCHA recognition tasks

Note: This project is for educational and research purposes only. It is not intended for unauthorized automation of services that prohibit it.
![310](https://github.com/user-attachments/assets/5d5d8d36-c1c7-438a-933c-ad8bd5061745)
