import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import removeBgRouter from './controller/removeBackground/removeBackgroundController.js';
import svgRouter from './controller/SvgController/svgController.js';


dotenv.config();

const PORT = process.env.PORT || 5000;
const app = express();

app.use(cors());
app.use(express.json());
app.use('/removeBg', removeBgRouter);
app.use('/svg', svgRouter);


app.listen(PORT, async () => {
    console.log(`Server listen on PORT: ${PORT}`);
});
