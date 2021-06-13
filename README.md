# Cowin-Vaccine-Appointement-Finder
A web-interface made using Cowin API to search for vaccine appointement for a given pincode using Python, Flask, jQuery and AJAX.

To run please use python virutal venv
Steps:
1) Clone the repository
2) Create a virtual environment and activate the same. 
  ```
  python3 -m venv cowinapp && source cowinapp/bin/activate
  ```
  Here, a virutal env named "cowinapp" has been created and activated
  
3) Install libraries using requirement.txt
  ```
  pip install -r requirements.txt
  ```
4) set variable FLASK_APP as main.py and run the flask application
  ```
  export FLASK_APP=main.py
  flask run
  ```

