# Observations and actions with intention of improvements


## Design Choice


* Abstract Factory Pattern - The abstract factory pattern is also called factory of factories. This design pattern comes under the creational design pattern category. It provides one of the best ways to create an object. It includes an interface, which is responsible for creating objects related to Factory.

## Before refactoring


* There was no README for the python project code. It could be helpful to have some understanding of the project and what we are trying to achieve.


* The structure of the project files like putting the .py files in a right folder (named well) or package could be better for code readability purposes.


* Upgraded requirements.txt packages to up-to-date versions like importlib-resources==5.12.0 and Shapely==2.0.1.


* Call to `__init__` of super class was missed in line 12, 96, 126, 143 and 303 in csv_reports.py. Fixed it by adding super class call using `super().__init__`.


* Expected type 'bytes', got 'str' instead in line 22 in csv_reports.py. Fixed it by changing the return type to str.


* Made methods static in line 15 & 18 in csv_reports.py.


## After refactoring


* Refactored the code to have different python files for the different report formatter classes in report_formatter package.


* There is a warning in line 63 in main.py which says 'ReportFormatter' object is not callable, but then it is how we instantiate your class inheriting abstract class which then help us to use multiple implementations of the `generate` method.