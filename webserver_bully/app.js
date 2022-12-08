const express = require("express");
const app = express();

var port = 8081;

app.listen(port, () => {
    console.log("Server is running on port " + port);
});

app.use(express.static("public"));

