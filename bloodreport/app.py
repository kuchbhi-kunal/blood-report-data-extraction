import flask
from flask import Flask , render_template , send_file , request , session, redirect, url_for
import os
import logging
import pdfplumber
import re

# Create a 'logs' folder if it doesn't exist
log_folder = 'logs'
os.makedirs(log_folder, exist_ok=True)

# Configure logging to save log files in the 'logs' folder
log_file_path = os.path.join(log_folder, 'app.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')


class Investigation:
  def __init__(self, name, value, ref_range, unit):
      self.name = name
      self.value = value
      self.ref_range = ref_range
      self.unit = unit
      self.tag = self._calculate_tag() 
      
  def _calculate_tag(self):
    ref_min, ref_max = map(float, self.ref_range.split("-"))
    value = float(self.value)

    if value < ref_min:
        return "low"
    elif value > ref_max:
        return "high"
    else:
        return "moderate"
    
 # call the function to set the tag
def extract_data(filepath):

  # code to  q PDF and extract data
  investigations = []

  # add extracted investigations to the list
  return investigations

def parse_text(text):
  logging.warning(f"raw text: {text}")
  # Identify format type:
  # Format 1: "Investigation (Abbr) Value Unit Ref Range"
  # regex = (r"^.*?(\w+(?:\s+\w+)?(?:\s+\w+)?)\s+(\d+(?:\.\d+)?)\s+((?:\d+\.\d+|\d+)-(\d+\.\d+|\d+))\s*(\S+)(?:\s+\S+(?:\s+\S+)*)?$")
  # if re.match(r"^\w+\s+\(\w+\)\s+(\d+\.\d+)\s+(.+?)\s+(\d+-\d+)$", text):
  #   logging.info(f"matched: {text}")
  #   match = re.match(r"^(\w+)\s+\(\w+\)\s+(\d+\.\d+)\s+(.+?)\s+(\d+-\d+)$", text)
  #   return Investigation(match.group(1), match.group(2), match.group(3), match.group(4))

  # # Format 1: "Investigation Value Ref Range Unit"
  match = re.match(r"^.*?(\w+(?:\s+\w+)?(?:\s+\w+)?)\s+(\d+(?:\.\d+)?)\s+((?:\d+\.\d+|\d+)-(\d+\.\d+|\d+))\s*(\S+)(?:\s+\S+(?:\s+\S+)*)?$", text)
  if re.match(r"^.*?(\w+(?:\s+\w+)?(?:\s+\w+)?)\s+(\d+(?:\.\d+)?)\s+((?:\d+\.\d+|\d+)-(\d+\.\d+|\d+))\s*(\S+)(?:\s+\S+(?:\s+\S+)*)?$", text):
    logging.info(f"matched2: {text}")
    logging.info(f"match: {match.group(1)} {match.group(2)} {match.group(3)} {match.group(4)} {match.group(5)} {match.groups()}")
    return Investigation(match.group(1), match.group(2), match.group(3), match.group(5))
  
  # match2 = re.match(r"^.*?(\w+(?:\s+\w+)?)\s+(\d+(?:\.\d+)?)\s+(\S+)\s+(\d+(?:-\d+)?)\s+(\S+)(?:\s+\S+(?:\s+\S+)*)?$", text)
  # if re.match2(r"^.*?(\w+(?:\s+\w+)?)\s+(\d+(?:\.\d+)?)\s+(\S+)\s+(\d+(?:-\d+)?)\s+(\S+)(?:\s+\S+(?:\s+\S+)*)?$", text):
  #   logging.info(f"matched second format: {text}")
  #   logging.info(f"match: {match2.group(1)} {match2.group(2)} {match2.group(3)} {match2.group(4)} {match2.group(5)} {match2.groups()}")
  #   return Investigation(match2.group(1), match2.group(2), match2.group(4), match2.group(3))
  
  # elif re.match(r"^(\w+(?:\s+\w+)?)\s+(\d+(?:\.\d+)?)\s+(\S+)\s+(\d+-\d+)$", text):
  #   logging.info(f"matched2: {text}")
  #   match = re.match(r"^(\w+(?:\s+\w+)?)\s+(\d+(?:\.\d+)?)\s+(\S+)\s+(\d+-\d+)$", text)
  #   logging.info(f"match: {match.group(1)} {match.group(2)} {match.group(3)} {match.group(4)} {match.group(5)} {match.groups()}")
  #   return Investigation(match.group(1), match.group(2), match.group(3), match.group(5))
  
  

  
  else:
    # Log or raise error for unrecognized format
        logging.warning(f"Unrecognized format: {text}")
        return None


def extract_data(filepath):
  # Open PDF with pdfplumber
  with pdfplumber.open(filepath) as pdf:
    investigations = []
    # Loop through pages and extract text per line
    for page in pdf.pages:
      for line in page.extract_text().splitlines():
        # Clean and parse each line
        text = line.strip()
        investigation = parse_text(text)
        if investigation:
          investigations.append(investigation)
    return investigations

def pred(filepath):
    investigations = extract_data(filepath)
    # for investigation in investigations:
    #     print(f"Name: {investigation.name}, Value: {investigation.value}, Unit: {investigation.unit}, Ref Range: {investigation.ref_range}")
    return investigations

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/results', methods=['POST','GET'])
def res():
    if request.method == 'GET':
       return render_template('index.html')
    if request.method == 'POST':
        file = request.files['filename'] # fet input
        filename = file.filename      
        print("@@ Input posted = ", filename)

        file_path = os.path.join('static/upload', filename)
        print("file_path", file_path)
        file.save(file_path)

        extractions = pred(filepath=file_path)

        return render_template("index.html",investigations=extractions, tags=True)

if __name__ == "__main__":
    app.run(debug = True) 
