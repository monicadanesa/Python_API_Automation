# Python_API_Automation_Test
API Automation Testing using python, pytest and allure.

Introduction
------------
Sample code API automation testing using Python 3.7, Pytest and also Allure Report.

Usage
-----
  * Clone code from master branch [Source Code](https://github.com/monicadanesa/Python_API_Automation.git).
  * Make sure python 3 is available by checking with  `python --version`.
  * Make sure the position already on repository local and Install all of dependecy by typing `pip install -r requirements.txt` on terminal.
 * Make sure pytest is instaled by checking with `pytest --version`.
 * Install allure for reporting result by typing `brew install allure`.
 * Please check allure document and make sure is running well [Allure](https://docs.qameta.io/allure/).
 * Pointing terminal on the testing folder.
 * Type `pytest --alluredir=allure_report testing.py` on terminal(allure_report is folder to save reports result).
 * Check report result typing `allure serve allure_report` and it will generate and start web server for reporting .
 * Put url on your browser.

Sample Report
-----
<img width="1677" alt="Screen Shot 2019-08-13 at 21 08 05" src="https://user-images.githubusercontent.com/23183123/62948442-89122c80-be0e-11e9-85be-dca27bf04395.png">

