# CITS3200 Cheating Detection Project

The application serves as a document analysis tool. When a student submits an assignment in the form of a Microsoft Word Document that was actually written by someone else, various aspects of the document's metadata potentially provide clues that may help substantiate an allegation of cheating. It is often the case that when students obtain an essay or similar written by another person they lightly edit the document, for example, adding their name and institution. At times, it is possible that document Properties are wiped or provide insufficient data to conclude how the work was written. However, forensic techniques exist that can dig deeper into documents when they are unzipped as XML files. See: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7324152. There are various clues in that can be drawn from the XML file that indicate potential cheating as outlines here https://doi.org/10.1007/s10805-019-09358-w and here https://doi.org/10.1007/978-3-031-12680-2_12

The application is a desktop program into which an MS Word document can be dropped or uploaded. It would then do the work of converting the file to a zip format, unzipping the file to its XML constituent parts, and analysing the relevant constituent parts to provide evidence to assess in cases of suspected cheating such as counts of revision identifiers, ratio of edited to words, versions of Word used, languages used in the document. In short, the tool would unzip and automate the analysis of cheating-relevant information in word documents.

The application is proposed by our client as a tool to assist with academic integrity.

Contact: Guy Curtis
Phone: 0864883356
Email: guy.curtis@uwa.edu.au
Preferred contact: Email
Location: UWA
IP Exploitation Model: Creative Commons (open source) http://creativecommons.org.au/

### Project setup

1. Install NodeJS
2. Run `npm install` to install required packages

### Compiles and hot-reloads for development

`npm run serve` (Browser)  
`npm run electron:serve` (Desktop)

### Compiles and minifies for production

`npm run build` (Creates production folder for server)  
`npm run electron:build` (Creates executable file)

### Lints and fixes files

`npm run lint`

### Running Python scripts

1. Export python file into executable using `pyinstaller ./src/scripts/doc_parser.py --onefile`
2. A dist/doc_parser.exe file will be created.
3. Place executable file into the dist_electron/win-unpacked folder after running `npm run electron:build`.

### Tech Stack

Front-end

- VueJS
- Tailwind CSS

Back-end

- ExpressJS
- Python
