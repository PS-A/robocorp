# Robocorp Practice
Repo for Robocorp Developer Certification training (Levels 1–3).  
This is hands-on automation practice using Robocorp’s tools, Control Room, and Python.

## About
Practicing Robocorp automation by completing the official certification levels.  
Focus on browser automation, data handling, PDF/report generation, and running robots both locally and in Control Room.

## Level 1 - Getting Started
Basic setup and first automation:
- Installed extensions and initialized the repo.
- Launched browser and logged in.
- Downloaded Excel file and read data.
- Filled form based on Excel input.
- Generated PDF from HTML.
- Uploaded to Control Room, ran successfully, and scheduled the process.

## Level 2 - Robot Build from Specs
Independent robot build according to given requirements:
- Opened robot order website and handled modal dialogs.
- Pulled orders from Control Room asset (orders.csv).
- Looped through orders, filling the form automatically.
- Captured screenshots of receipts.
- Created PDFs and embedded screenshots.
- Archived all receipts into a ZIP.
- Designed to run out-of-the-box both locally and in Control Room.

### Running Notes
In Control Room:
- Create an asset named orders.csv with required headers.
- Artifacts (PDFs, screenshots, archive) are collected from output/.

Locally:
- Create assets.json with reference to orders.csv.

## Disclaimers
- Training/learning code based on Robocorp certification material.
- Not production code, but written with clean repo structure and best practices (env handling, no secrets committed).

## License
This project is licensed under the MIT License.  
MIT was chosen because it’s simple, permissive, and widely adopted in open-source.  
It allows anyone to use, modify, and share the code freely, while keeping attribution and liability disclaimers clear.