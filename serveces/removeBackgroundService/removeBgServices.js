class RemoveBgService {
    async fetchToPicsartApiForRemoveBg(req) {
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
        formData.append('image', req.body.img);

        const url = process.env.REMOVE_BACKGROUND_API;
        const options = {
            method: 'POST',
            headers: {
            accept: 'application/json',
                'X-Picsart-API-Key': process.env.PICSART_TOKEN
            },
            body: formData
        };

        fetch(url, options)
        .then(res => res.json())
        .then(json => console.log(json))
        .catch(err => console.error(err));
    }
};

export default RemoveBgService;