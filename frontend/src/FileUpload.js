import React, { useState } from 'react';
import axios from 'axios';
import ResultDisplay from "./ResultDisplay";


function FileUpload() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    
    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append("file", file);
        
        const response = await axios.post("http://127.0.0.1:8000/analyze-code", formData);
        setResult(response.data);
    };
    
    return (
        <div>
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <button onClick={handleSubmit}>Analyze</button>
            {result && <ResultDisplay result={result} />}
        </div>
    );
}
export default FileUpload;