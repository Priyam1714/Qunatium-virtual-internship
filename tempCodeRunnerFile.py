import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.testing.application_runners import import_app
from dash.testing.base import SeleniumTestCase
import pytest

class TestDashApp(SeleniumTestCase):
    def setUp(self):
        self.driver = self.selenium.create_headless_browser()

    def tearDown(self):
        self.driver.quit()

    def app_url(self):
        return 'http://localhost:8050'

    def wait_for_element(self, selector):
        return self.wait.until(lambda driver: driver.find_element_by_css_selector(selector))

    def test_header_present(self):
        
        # Start the Dash app
        app = import_app('app')
        app.run_server(debug=True)

        # Open the app URL
        self.driver.get(self.app_url())

        # Wait for the header element
        header = self.wait_for_element('#header')

        # Assert that the header text is correct
        assert header.text == 'MORSEL SALES REPORT'

    def test_visualization_present(self):
        # Start the Dash app
        app = import_app('app')
        app.run_server(debug=True)

        # Open the app URL
        self.driver.get(self.app_url())

        # Wait for the visualization element
        visualization = self.wait_for_element('#visualization')

        # Assert that the visualization component is present
        assert visualization.tag_name == 'div'

    def test_region_picker_present(self):
        # Start the Dash app
        app = import_app('app')
        app.run_server(debug=True)

        # Open the app URL
        self.driver.get(self.app_url())

        # Wait for the region picker element
        region_picker = self.wait_for_element('#Region')

        # Assert that the region picker component is present
        assert region_picker.tag_name == 'div'

# Run the tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
