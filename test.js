const express = require('express')
const app = express()
var bodyParser = require('body-parser')

// parse application/json
app.use(bodyParser.json())

app.get('/', function (req, res) {
  res.send('Hello World!')
})

app.post('/degats', function (req, res) {
  console.log("test", req.body)
  res.send('Hello World!')
})

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})
