import React, { useEffect } from 'react';
import axios from 'axios';

const PromptRunner = ({form, model, isRunning, lastResult}) => {

    const [resultText, setResultText] = useState()

    function mapRequestData() {
        if (form.type === 'ollama') {
            return {
                ...form,
                model: model.name
            }
        } else {
            return form
        }

    }

    useEffect(() => {
        const response = axios.post(model.api, mapRequestData());
        for await (const chunk of response.body) {
            mapResponseData
        }

    }, []);

    return (
        <div>
            <p>Placeholder paragraph</p>
        </div>
    );
};

export default PromptRunner;