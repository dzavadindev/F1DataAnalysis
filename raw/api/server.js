const jsonServer = require('json-server')
const server = jsonServer.create()
const router = jsonServer.router('api.json')
const middlewares = jsonServer.defaults({readOnly: true})
const db = require('./api.json')

server.use(middlewares)

server.get('/drivers/', (req, res) => {
  res.jsonp(db.drivers.map(x => x.id))
})

server.get('/teams/', (req, res) => {
  res.jsonp(db.teams.map(x => x.id))
})

server.use(router)
server.listen(3000, () => {
  console.log('JSON server is running on http://localhost:3000')
})

