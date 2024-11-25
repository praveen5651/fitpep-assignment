import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestFitpeoPage(unittest.TestCase):
    def setUp(self):
        print("SetUp: \n"
              "1. Set up chrome driver path\n"
              "2. Navigate to fitpeo page\n"
              "3. Maximize the window")
        self.service = Service("C:\\Users\\LENOVO\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)
        self.actions = ActionChains(self.driver)
        self.driver.get("https://www.fitpeo.com/")
        self.driver.maximize_window()

    def test_navigate_to_revenue_calculate(self):
        # Navigate to revenue calculator URL
        print("\nTest Steps: \n"
              "1. Navigate to revenue calculator and validate revenue calculator page loaded \n"
              "2. Scroll down to slider bar and set to 820 value\n"
              "3. Validate slider value is updated to 820\n"
              "4. Change slider value 560 with number field and validate\n"
              "5. Set back to 820 value forther steps\n"
              "6. CPT-99091, CPT-99453, CPT-99454, CPT-99474 click respective values check boxes\n"
              "7. Validate Total Recurring Reimbursement for all Patients Per Month at top ")
        revenue_calculator = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/revenue-calculator"]')))
        revenue_calculator.click()
        time.sleep(5)
        self.assertTrue(self.driver.current_url == "https://www.fitpeo.com/revenue-calculator",
                        "The Revenue calculator should be launched")

        # Scroll down to slider bar
        self.actions.scroll_by_amount(0,500).release().perform()

        # Changing Slider value to 820
        slider_bar = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "MuiSlider-thumb MuiSlider-thumbSizeMedium")]')))
        self.actions.click_and_hold(slider_bar).move_by_offset(93, 0).release().perform()
        slider_value = self.driver.find_element(By.XPATH, '//input[@type="range"]')
        current_val = int(slider_value.get_attribute('aria-valuenow'))
        target = 820
        if current_val!=target:
            val = int(target-current_val)
            for i in range(val):
                self.actions.send_keys(Keys.ARROW_RIGHT).perform()

        # Wait for 5 Sec for checking 820 value is updated
        time.sleep(5)
        self.assertEqual(int(slider_value.get_attribute('aria-valuenow')), target, "Slider value is not set to 820")

        # Change slider value to 560 with entering number in field
        input_field = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="number"]')))

        def change_slider_value_with_input_field(number):
            input_field.send_keys(Keys.CONTROL + 'a')
            input_field.send_keys(Keys.DELETE)
            input_field.send_keys(number)

        change_slider_value_with_input_field('560')

        # Validate Slider value
        input_field_value = int(input_field.get_attribute('value'))
        slider_value = int(slider_value.get_attribute('aria-valuenow'))

        # Validate slider value and input field value is same or not
        time.sleep(5)
        self.assertEqual(input_field_value, slider_value, 'input field value 560 is not equal to slider value')

        # change slider value back to 820
        change_slider_value_with_input_field(820)

        # "CPT-99091", "CPT-99453", "CPT-99454", "CPT-99474" click respective check boxes to validate Total Recurring Reimbursement for all Patients Per Month
        time.sleep(5)
        target_cpt_codes = []
        expected_value = ["CPT-99091", "CPT-99453", "CPT-99454", "CPT-99474"]
        code_element = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//p[@class="MuiTypography-root MuiTypography-body1 inter css-1s3unkt"]')))

        for code in code_element:
            target_cpt_codes.append(code.text)
        indices = [target_cpt_codes.index(value) + 1 for value in expected_value if value in target_cpt_codes]

        for index in indices:
            checkbox = self.driver.find_element(By.XPATH, f'(//input[@type="checkbox"])[{index}]')
            if not checkbox.is_selected():
                checkbox.click()
                time.sleep(0.5)

        Validate_total_recurring_Reimbursement = self.driver.find_elements(By.XPATH, '//p[@class="MuiTypography-root MuiTypography-body2 inter css-1xroguk"]')
        values_new = []
        for val in Validate_total_recurring_Reimbursement:
            values_new.append(val.text)

        data_dict = {item.split(':')[0].strip(): item.split(':')[1].strip() for item in values_new}

        actual_total_recurring_Reimbursement = '$110700'
        self.assertEqual(data_dict['Total Recurring Reimbursement for all Patients Per Month'], actual_total_recurring_Reimbursement, "recurring values are not equal")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
