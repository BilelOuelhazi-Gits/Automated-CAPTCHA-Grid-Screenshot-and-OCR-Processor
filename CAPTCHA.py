from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import time
import numpy as np

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_brightness(image):
    grayscale = image.convert('L')
    return np.mean(np.array(grayscale))

def get_contrast(image):
    grayscale = image.convert('L')
    pixel_values = np.array(grayscale)
    return np.std(pixel_values)

def adjust_contrast(image):
    avg_brightness = get_brightness(image)
    contrast_level = get_contrast(image)

    if avg_brightness < 100:
        contrast_factor = 2.5
    elif avg_brightness < 150:
        contrast_factor = 2.0
    elif avg_brightness < 180:
        contrast_factor = 1.5
    else:
        contrast_factor = 1.2

    enhancer = ImageEnhance.Contrast(image.convert('L'))
    enhanced_image = enhancer.enhance(contrast_factor)

    enhanced_image = enhanced_image.filter(ImageFilter.MedianFilter(size=3))

    return enhanced_image

def adaptive_threshold(image):
    pixel_values = np.array(image)
    mean_brightness = np.mean(pixel_values)

    threshold_value = mean_brightness * 0.9
    binary_image = image.point(lambda p: 255 if p > threshold_value else 0)

    return binary_image

def preprocess_image(image):
    enhanced = adjust_contrast(image)
    binary = adaptive_threshold(enhanced)
    return binary

def crop_inner_70(image):
    width, height = image.size
    margin_x = int(width * 0.15)
    margin_y = int(height * 0.15)

    cropped = image.crop((margin_x, margin_y, width - margin_x, height - margin_y))
    return cropped

try:
    url = "https://tunisia.blsspainglobal.com/Global/bls/doorstepform"
    driver.get(url)

    time.sleep(7)

    verify_button = driver.find_element(By.ID, "btnVerify")
    verify_button.click()

    print("Verify button clicked successfully.")

    time.sleep(6)

    full_screenshot = "captcha_screenshot.png"
    driver.save_screenshot(full_screenshot)
    print(f"Full screenshot saved as {full_screenshot}")

    image = Image.open(full_screenshot)
    width, height = image.size

    left1 = width * 0.25
    right1 = width * 0.75
    top1 = height * 0.25
    bottom1 = height * 0.30
    cropped_top_line = image.crop((left1, top1, right1, bottom1))
    cropped_top_line.save("captcha_top_line.png")
    print(f"Top line screenshot saved as 'captcha_top_line.png'")

    extracted_text_top_line = pytesseract.image_to_string(cropped_top_line)
    print("\n=== Extracted Text from Top Line ===")
    print(extracted_text_top_line)
    print("=============================\n")

    left2 = width * 0.32
    right2 = width * 0.66
    top2 = height * 0.30
    bottom2 = height * 0.68

    captcha_grid_image = image.crop((left2, top2, right2, bottom2))

    grid_width, grid_height = captcha_grid_image.size
    part_width = grid_width // 3
    part_height = grid_height // 3

    for row in range(3):
        for col in range(3):
            left = col * part_width
            top = row * part_height
            right = left + part_width
            bottom = top + part_height

            part_image = captcha_grid_image.crop((left, top, right, bottom))

            cropped_part = crop_inner_70(part_image)

            cropped_part.save(f"captcha_part_cropped_{row * 3 + col + 1}.png")
            print(f"Part {row * 3 + col + 1} cropped and saved as 'captcha_part_cropped_{row * 3 + col + 1}.png'")

            processed_image = preprocess_image(cropped_part)

            processed_image.save(f"captcha_part_processed_{row * 3 + col + 1}.png")
            print(f"Part {row * 3 + col + 1} preprocessed and saved as 'captcha_part_processed_{row * 3 + col + 1}.png'")

            extracted_number = pytesseract.image_to_string(processed_image, config='--psm 6')
            print(f"Extracted number from part {row * 3 + col + 1}: {extracted_number.strip()}")

    time.sleep(10)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
