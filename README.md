# Robocorp Practice
Repo for Robocorp Developer Certification training (Levels 1–3).  
This is hands-on automation practice using Robocorp’s tools, Control Room, and Python.

## About
Practicing Robocorp automation by completing the official certification levels.  
Focus on browser automation, data handling, PDF/report generation, and running robots both locally and in Control Room.

## Level 1 - Getting Started (guided setup)
Basic setup and first automation:
- Installed extensions and initialized the repo.
- Launched browser and logged in.
- Downloaded Excel file and read data.
- Filled form based on Excel input.
- Generated PDF from HTML.
- Uploaded to Control Room, ran successfully, and scheduled the process.

## Level 2 - Robot Build from Specs (independent build)
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

## Level 3 - Work Data Management (producer-consumer)
Guided work data management build with producer-consumer setup.
Steps included:
- Downloading JSON traffic data.
- Producing work items from JSON data.
- Creating a consumer step to process work items.
- Using Control Room to run the producer → consumer chain.
- Understanding best practices for scalable automation pipelines.

## Extras
This repo will also serve as a sandbox for personal robots beyond the certifications. Experiments, small automations, and side projects.

## Disclaimers
This repo is based on Robocorp certification exercises. While not production code, it follows good practices (clean repo structure, environment variables for secrets, no sensitive data committed).

## License
This project is licensed under the MIT License.  
MIT was chosen because it’s simple, permissive, and widely adopted in open-source.  
It allows anyone to use, modify, and share the code freely, while keeping attribution and liability disclaimers clear.