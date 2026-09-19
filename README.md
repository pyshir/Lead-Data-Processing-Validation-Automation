# Lead Data Processing & Validation Automation

## Author: Jahid (Whatsapp: 8801309495010)

A Python-based data processing automation project designed to extract, validate, clean, normalize, and organize messy customer lead data.

This project simulates a realistic small-to-medium freelance data-processing/automation task where customer information comes in inconsistent formats and needs to be converted into structured, validated records.

---

## Project Overview

The input data contains **20 customer leads** with intentionally inconsistent formats.

The program processes the raw data and:

* Extracts structured information using Regex
* Validates important fields
* Detects invalid and missing data
* Normalizes email, phone, date, and amount data
* Converts supported currencies to BDT
* Detects duplicate leads
* Groups duplicate records
* Removes duplicate leads from the clean dataset
* Generates separate output and summary reports

---

## Technologies Used

* **Python 3**
* `re` — Regular Expressions
* `datetime` — Date validation and normalization
* File Handling
* Object-Oriented Programming
* Lists, Dictionaries, Loops and Functions
* Exception Handling with `try/except`

No external Python libraries are required.

---

## Project Structure

```text
lead-data-processing/
│
├── main.py
├── data.txt
├── clean_leads.txt
├── invalid_leads.txt
├── duplicate_leads.txt
├── summary_report.txt
└── README.md
```

### Input

`data.txt`

Contains the original messy lead data.

### Python Program

`main.py`

Processes and validates the input data.

### Generated Reports

#### `clean_leads.txt`

Contains valid leads after removing duplicates.

#### `invalid_leads.txt`

Contains leads that failed one or more validation rules.

#### `duplicate_leads.txt`

Contains duplicate groups and shows which fields were used to identify the duplicates.

#### `summary_report.txt`

Contains the overall processing summary, including:

* Total leads
* Valid leads
* Invalid leads
* Duplicate leads
* Validation errors
* Missing data
* Leads with websites
* Leads with notes

---

## Data Processing Flow

```text
Raw Lead Data
      │
      ▼
Extract Individual Leads
      │
      ▼
Regex-based Field Extraction
      │
      ▼
Field Validation
      │
      ├── Valid ───────► Structured Data
      │
      └── Invalid ─────► Invalid Data Report
                             
Structured Valid Data
      │
      ▼
Duplicate Detection
      │
      ├── Duplicate Leads
      │
      └── Unique Leads
              │
              ▼
       Clean Valid Dataset
              │
              ▼
          Reports
```

---

## Validation & Normalization

### Lead ID

Extracts the lead number from records such as:

```text
LEAD #001
```

---

### Name

Supports different field labels such as:

```text
Customer:
Name:
CUSTOMER NAME:
```

Names are normalized by removing unnecessary whitespace and applying basic capitalization.

---

### Email

Supports different labels such as:

```text
Email:
Email =>
contact:
```

Email addresses are normalized to lowercase.

The project also detects malformed email addresses.

Examples from the dataset include:

```text
sarah.ahmed @ yahoo.com
lina.das@@gmail.com
```

These are treated as invalid.

---

### Phone

Supports:

```text
Phone:
Mobile:
```

The phone validation handles:

* Different phone formats
* Country codes
* Spaces
* Hyphens
* Parentheses
* Digit-length validation
* Repeated-digit validation
* Malformed parentheses
* Invalid separator patterns

After validation, non-digit characters are removed for normalization.

---

### Date

The project supports multiple date formats, including:

```text
12/08/2026
16-08-2026
2026-08-19
Aug 15, 2026
19 Aug 2026
September 1, 2026
```

Dates are validated using Python's `datetime.strptime()` and normalized into:

```text
DD/MM/YYYY
```

Invalid dates such as:

```text
32/08/2026
```

are detected.

---

### Amount & Currency

The project processes different amount formats such as:

```text
Tk 12,500
Tk12500
BDT 7,500
$250
USD 1,250.50
GBP 500
EUR 1.200,50
9500 taka
```

Supported currencies are converted into BDT using the conversion values defined in the project.

---

### Product ID

Supports product identifiers such as:

```text
A-102
B-205
C-301
D-410
```

---

### Address

Supports different labels:

```text
Address:
location:
```

Missing or unavailable addresses are detected.

---

### Optional Fields

The project also extracts optional:

```text
Website:
Notes:
```

These fields are allowed to be absent.

---

## Duplicate Detection

Duplicate leads are identified using **email and phone**, rather than the customer's name.

This is intentional because the same customer can appear with slightly different name formats.

For example:

```text
Md. Rahim Uddin
Rahim Uddin
Md Rahim Uddin
```

can still represent the same lead when the email and phone match.

The project identifies duplicates using:

* Email + Phone
* Email
* Phone

### Duplicate Groups in the Dataset

The fixed dataset contains these duplicate groups:

```text
Group #1
PRIMARY: #002
DUPLICATE: #018
MATCHED BY: PHONE
```

```text
Group #2
PRIMARY: #001
DUPLICATE: #005, #014
MATCHED BY: EMAIL + PHONE
```

```text
Group #3
PRIMARY: #008
DUPLICATE: #009
MATCHED BY: EMAIL + PHONE
```

---

## Final Dataset Summary

The project processes a fixed dataset containing:

```text
Total Leads: 20
```

Final processing result:

```text
Valid Leads:      11
Invalid Leads:     5
Duplicate Leads:   4
```

### Validation Errors

```text
Invalid Emails:       2
Invalid Phones:       3
Invalid Dates:        1
Invalid Product IDs:  0
```

### Missing Data

```text
Missing Name:     1
Missing Email:    2
Missing Phone:    3
Missing Address:  1
Missing Website: 16
```

---

## Main Classes

### `StandardData`

Stores the structured information of each processed lead.

Main fields include:

```text
lead_no
name
email
phone
date
amount
currency
product_id
address
website
note
error
status
```

### `DataGenerate`

Responsible for:

* Reading raw data
* Extracting records
* Validation
* Separating valid and invalid data
* Duplicate detection
* Clean dataset generation
* Summary calculations

### `DataClean`

Responsible for removing `None` values when generating the invalid-data report.

---

## How to Run

Clone the repository:

```bash
git clone <your-repository-url>
```

Go into the project directory:

```bash
cd lead-data-processing
```

Run:

```bash
python3 main.py
```

The program will process `data.txt` and generate the report files.

---

## Learning Objectives

This project was built to practice practical Python automation skills rather than following a simple tutorial project.

The main concepts practiced were:

* Regular Expressions
* Data extraction
* Data validation
* Data normalization
* File handling
* Lists and dictionaries
* Loops and conditions
* Functions
* Object-Oriented Programming
* Exception handling
* Duplicate detection
* Report generation
* Handling messy real-world-style data

---

## Future Direction

This project is part of a broader Python learning path focused on:

```text
Python
   ↓
Automation
   ↓
APIs / requests
   ↓
AI Automation
```

The goal is to gradually move from basic Python scripting toward practical automation and AI-related projects.

---

## Author

**Jahid**

Built as a practical Python automation project while learning Python and Regex.
