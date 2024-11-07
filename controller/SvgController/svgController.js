import express from 'express';
import SvgService from '../../serveces/SvgService/svgService.js';

const svgRouter = new express.Router();
const svgService = new SvgService();

svgRouter.get('/', async (req, res) => {
    await svgService.getSvgFromLocaly();
    res.status(200).send("Ok");
});