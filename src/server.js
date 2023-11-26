const express = require("express");
const cors = require("cors");
const multer = require("multer");
const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());

const storage = multer.diskStorage({
  destination: process.cwd().concat("\\uploads"),
  filename: function (req, file, callback) {
    callback(null, file.originalname);
  },
});

const uploads = multer({ storage: storage });
app.post("/uploads/", uploads.array("files", 50), function (req, res) {
  console.log(req.files);
  res.send("Uploaded File!");
});

app.get("/process/", (req, res) => {
  const python = require("child_process").execFile(
    process.cwd().concat("\\doc_parser.exe")
  );

  /* const python = require("child_process").spawn("python", [
    process.cwd().concat("\\src\\scripts\\doc_parser.py"),
  ]); */

  python.stdout.pipe(res);
});

app.get("/check/", (req, res) => {
  res.send(process.cwd());
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
