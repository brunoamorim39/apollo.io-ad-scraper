# Ad Copy Scraper for Alex Moriarty Marketing

#### What it does

This tool is designed to interface with various existing applications in order to source information regarding advertisements that various companies have and/or are currently running. The main interfaces of this tool are the following applications:

* apollo.io pre-defined lists

* Google ads transparency center

The control flow of this tool is designed as follows:

1. Collect information regarding businesses of interest via the apollo.io API. The list is pre-defined to keep results relevant and narrow.

2. Using the business information that was collected, create a Selenium webdriver session and search for ad creatives that each of the businesses have ran and/or are currently running.

3. Collect the creatives that are displayed in the form of images and save them to a CSV file

4. When the information collection is complete, email the CSV file to the client.