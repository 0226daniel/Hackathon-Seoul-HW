const mqtt = require('mqtt')
const client  = mqtt.connect('mqtt://ubuntu.kimjisub.kr')
 
client.on('connect', () => {
  console.log('connected')
  client.subscribe('presence', (err) => {
    if (!err) {
      client.publish('presence', 'Hello I\'m Backend Client')
    }
  })
})
 
client.on('message', (topic, message) => {
  // message is Buffer
  console.log(`${topic}: ${message.toString()}`)
  //client.end()
})
