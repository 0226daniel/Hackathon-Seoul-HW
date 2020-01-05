import express from 'express';
import helmet from 'helmet';
import Sequelize from 'sequelize';
import bodyParser from 'body-parser';
import cors from 'cors';

const sequelize = new Sequelize('shh', 'postgres', 'rodrm1211', {
  host: 'r.kdw.kr',
  dialect: 'postgres',
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000,
  },
  logging: false,
});

const DeviceTable = sequelize.define('devices', {
  device_id: {
    type: Sequelize.STRING,
    primaryKey: true,
  },
  lon: {
    type: Sequelize.FLOAT,
  },
  lat: {
    type: Sequelize.FLOAT
  }
}, {createdAt: 'created_at', updatedAt: 'updated_at'});

const RecordTable = sequelize.define('records', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  device_id: {
    type: Sequelize.STRING,
  },
}, {createdAt: 'created_at', updatedAt: 'updated_at'});

sequelize.sync({ alter: true });

const app = express();
app.use(helmet());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(cors({origin: ['http://localhost:8080']}))
app.get('/summary', (req, res) => {
  DeviceTable.findAll().then(data => {
    res.send(data);
  }).catch(err => {

  })
});
app.get('/', async (req, res) => {
  res.send(await DeviceTable.findAll({attributes: ['device_id', 'lon', 'lat', 'created_at', 'updated_at']}));
})
app.get('/events', async (req, res) => {
  res.send(await RecordTable.findAll({attributes: ['id', 'device_id', 'created_at']}));
});
app.delete('/:device_id', async (req, res) => {
  await DeviceTable.destroy({where: {device_id: req.params.device_id}});
  await RecordTable.destroy({where: {device_id: req.params.device_id}});
  res.send();
})
app.post('/:device_id', (req, res) => {
  const { device_id } = req.params;
  const { lon, lat } = req.body;
  console.log('init',device_id);
  DeviceTable.upsert({
    device_id,
    lon,
    lat
  }).then((data) => {
    res.send();
  }).catch((err) => {
    res.status(500).send(err);
  });
});
app.post('/:device_id/event', (req, res) => {
  const { device_id } = req.params;
  console.log('event',device_id);
  RecordTable.create({
    device_id,
  }).then((data) => {
    res.send();
  }).catch((err) => {
    res.status(500).send(err);
  });
});
app.listen(9999);