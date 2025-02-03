import axios from 'axios';

const MULTIMODAL_MODELS = ["moondream"]
const OLLAMA_HOST = "http://127.0.0.1:11434"
const PYTHON_HOST = "http://127.0.0.1:8000"

export const fetchData = async () => {
    try {
        const [ollamaModels, pythonModels] = await Promise.all([
            axios.get(`${OLLAMA_HOST}/api/tags/`),
            axios.get(`${PYTHON_HOST}/list-models/`)
        ]);

        return [
            ...ollamaModels.data.models.map(model => {
                return {
                    id: model.name,
                    name: model.name,
                    type: 'ollama',
                    inputType: MULTIMODAL_MODELS.includes(model.name) ? ["image", "text"] : ["text"],
                    outputType: "textStream",
                    api: `${OLLAMA_HOST}/api/generate/`
                };
            }),
            ...pythonModels.data.models.map(model => {
                return {
                    ...model,
                    api: `${PYTHON_HOST}/${model.endpoint}`
                }
            })
        ];
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};