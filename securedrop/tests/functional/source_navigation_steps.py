import tempfile
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class SourceNavigationSteps():

    def _source_visits_source_homepage(self):
        self.driver.get(self.source_location)

        self.assertEqual("SecureDrop | Protecting Journalists and Sources", self.driver.title)

    def _source_chooses_to_submit_documents(self):
        if self.driver.find_element(By.ID,'submit-documents-button').is_displayed():
            element_to_hover_over = self.driver.find_element_by_id('submit-documents-button')
            hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
            hover.perform()

        self.wait_for(
             lambda: self.driver.find_element(By.ID,
                     'submit-documents-button-hover').is_displayed()
        )
        submit_button = self.driver.find_element_by_id('submit-documents-button-hover')
        submit_button.click()

        codename = self.driver.find_element_by_css_selector('#codename')

        self.assertTrue(len(codename.text) > 0)
        self.source_name = codename.text

    def _source_continues_to_submit_page(self):
        element_to_hover_over = self.driver.find_element_by_id('continue-button')
        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()

        self.wait_for(
             lambda: self.driver.find_element(By.ID,
                     'continue-button-hover').is_displayed()
        )
        continue_button = self.driver.find_element_by_id('continue-button-hover')
        continue_button.click()

        headline = self.driver.find_element_by_class_name('headline')
        self.assertEqual('Submit documents and messages', headline.text)

    def _source_submits_a_file(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(self.secret_message)
            file.seek(0)

            filename = file.name
            filebasename = filename.split('/')[-1]

            file_upload_box = self.driver.find_element_by_css_selector('[name=fh]')
            file_upload_box.send_keys(filename)

            element_to_hover_over = self.driver.find_element_by_id('submit-doc-button')
            hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
            hover.perform()

            self.wait_for(
                 lambda: self.driver.find_element(By.ID,
                         'submit-doc-button-hover').is_displayed()
            )

            submit_button = self.driver.find_element_by_id('submit-doc-button-hover')
            submit_button.click()

            notification = self.driver.find_element_by_css_selector('p.notification')
            expected_notification = 'Thanks for submitting something to SecureDrop! Please check back later for replies.'
            self.assertIn(expected_notification, notification.text)

    def _source_submits_a_message(self):
        text_box = self.driver.find_element_by_css_selector('[name=msg]')

        text_box.send_keys(self.secret_message)  # send_keys = type into text box

        element_to_hover_over = self.driver.find_element_by_id('submit-doc-button')
        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()

        self.wait_for(
             lambda: self.driver.find_element(By.ID,
                     'submit-doc-button-hover').is_displayed()
        )

        submit_button = self.driver.find_element_by_id('submit-doc-button-hover')
        submit_button.click()

        notification = self.driver.find_element_by_css_selector(
            'p.notification')
        self.assertIn('Thanks for submitting something to SecureDrop!'
                      ' Please check back later for replies.',
                      notification.text)

    def _source_logs_out(self):
        logout_button = self.driver.find_element_by_id('logout').click()
        notification = self.driver.find_element_by_css_selector('p.error')
        self.assertIn('Thank you for logging out!', notification.text)
