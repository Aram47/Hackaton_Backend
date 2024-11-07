import fs from 'fs';
import path from 'path';
import { Readable } from "stream";
import { fileURLToPath } from 'url';
// import fetch from 'node-fetch'; 

function base64ToBlob(base64, contentType = 'image/png') {
    // Remove the Data URI scheme prefix if present (e.g., "data:image/png;base64,")
    const base64Data = base64.split(',')[1];
    
    // Decode the base64 string
    const binaryString = atob(base64Data);
    
    // Create an array of 8-bit unsigned integers
    const length = binaryString.length;
    const byteArray = new Uint8Array(length);
    for (let i = 0; i < length; i++) {
        byteArray[i] = binaryString.charCodeAt(i);
    }
    
    // Create a Blob from the byte array
    return new Blob([byteArray], { type: contentType });
}


class RemoveBgService {
    async fetchToPicsartApiForRemoveBg(req) {
        //console.log(req.body.img);
        const formData = new FormData();
        formData.append('output_type', 'cutout');
        formData.append('bg_blur', '0');
        formData.append('scale', 'fit');
        formData.append('auto_center', 'false');
        formData.append('stroke_size', '0');
        formData.append('stroke_color', 'FFFFFF');
        formData.append('stroke_opacity', '100');
        formData.append('shadow', 'disabled');
        formData.append('shadow_opacity', '20');
        formData.append('shadow_blur', '50');
        formData.append('format', 'PNG');
        // formData.append('image', req.body.img);
        formData.append('image', base64ToBlob(req.body.img));

        const url = process.env.REMOVE_BACKGROUND_API;
        const options = {
            method: 'POST',
            headers: {
            accept: 'application/json',
                'X-Picsart-API-Key': process.env.PICSART_TOKEN
            },
            body: formData
        };
        
        try {
            let response = await fetch(url, options);
            response = await response.json();
            response = await fetch(response.data.url);

            const blob = await response.blob(); // Get the response as a buffer


            const __filename = fileURLToPath(import.meta.url);
            const __dirname = path.dirname(__filename);
            // Construct the path to save the file
            const savePath = path.join(__dirname, '..', '..', 'imgs', 'result.png'); // Adjust 'output' to your folder name

            // Convert the Blob to an ArrayBuffer
            const arrayBuffer = await blob.arrayBuffer();
        
            // Convert the ArrayBuffer to a Buffer
            const buffer = Buffer.from(arrayBuffer);
            // Save the buffer to the file
            fs.writeFile(savePath, buffer, (err) => {
                if (err) {
                    console.error('Error saving the file:', err);
                } else {
                    console.log('File saved successfully at', savePath);
                }
            });
        } catch (err) {
            console.error('Error:', err);
        }

    }
};

export default RemoveBgService;