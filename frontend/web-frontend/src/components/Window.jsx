import React, { useState, useEffect } from 'react';
import { fetchData } from '../lib.js';

export const Window = () => {
    const [data, setData] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);

    useEffect(() => {
        fetchData().then(data => setData(data));
    }, []);

    const handleSelectChange = (event) => {
        const selectedItem = data.find(item => item.id === event.target.value);
        setSelectedItem(selectedItem);
    };

    return (
        <div>
            <select onChange={handleSelectChange}>
                <option value="">Select an item</option>
                {data.map(item => (
                    <option key={item.id} value={item.id}>
                        {item.name}
                    </option>
                ))}
            </select>
            {selectedItem && (
                <div>
                    <h2>{selectedItem.name}</h2>
                </div>
            )}
        </div>
    );
};