const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello, Express.js!');
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
