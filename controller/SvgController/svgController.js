import express from 'express';
import SvgService from '../../serveces/SvgService/svgService.js';

const svgRouter = new express.Router();
const svgService = new SvgService();

svgRouter.get('/', async (req, res) => {
    res.sendFile(await svgService.getSvgFromLocaly(), (err) => {
        if (err) {
            res.status(500).send('Error sending the file');
        }
    });
});

export default svgRouter;