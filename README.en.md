# Huazhong University of Science and Technology Badminton Court Booking Script

## Project Introduction
This project is used to automatically book badminton courts at Huazhong University of Science and Technology.

## Usage
1. Install dependencies:

   Linux users(using Ubuntu as an example) can run the following command directly. 

   ```sudo apt update```

   ```sudo apt install tesseract-ocr```

   ```pip install -r requirements.txt```

   Windows users should follow the [Note](#note) first, then execute the following command:

   ```pip install -r requirements.txt```

2. Modify the ```info.toml``` configuration file.
3. Run the script:

   ```python main.py```

## Note
1. Click  [Tesseract](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe) to install.
2. Add the Tesseract path to the environment variables. 

## Principle of filling in court.json (using Guanggu Sports Center, main badminton court as an example)
1. Open the URL in your browser: https://pecg.hust.edu.cn/cggl/front/syqk?cdbh=45

2. `cdbh` refers to the field mentioned in the link above (`cdbh`: chang di bian hao, which means "court number" in Chinese).

3. Right-click and select "View Page Source".

4. Press `ctrl+f` and search for the "pian" field to discover the principle.