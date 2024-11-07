import express from 'express';
import RemoveBgService from '../../serveces/removeBackgroundService/removeBgServices.js';

const removeBgRouter = new express.Router();
const removeBgService = new RemoveBgService();

removeBgRouter.post('/', async (req, res) => {
    await removeBgService.fetchToPicsartApiForRemoveBg(req);
    res.status(201).send("Ok");
});

export default removeBgRouter;