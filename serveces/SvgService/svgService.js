import path from 'path';
import { fileURLToPath } from 'url';

class SvgService {
    async getSvgFromLocaly() {
            const __filename = fileURLToPath(import.meta.url);
            const __dirname = path.dirname(__filename);

            const filePath = path.join(__dirname, '..', '..', 'svg_output', 'result.svg');
            return filePath;
    }
};

export default SvgService;