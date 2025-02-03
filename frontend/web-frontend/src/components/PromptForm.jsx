import React, { useState } from 'react';

const PromptForm = ({ model, modelRunning, formSubmitted }) => {
    const [file, setFile] = useState(null);
    const [imageBase64, setImageBase64] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = () => {
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImageBase64(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        modelRunning.value = true;
        setFormSubmitted(true);

        const formData = new FormData(event.target);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        if (imageBase64) {
            data["image"] = imageBase64;
        } 
        formSubmitted.value = data;
    };

    return (
        <form onSubmit={handleSubmit}>
            {
                model.inputType.includes('text') && <input type="text" name="prompt" />
            }
            {
                model.inputType.includes('image') && <div>
                    <input type="file" accept="image/*" onChange={handleFileChange} />
                    <button onClick={handleUpload}>Upload</button>
                </div>
            }
            <button type="submit">Prompt</button>
        </form>
    );
};

export default PromptForm;