import React from "react";

function ResultDisplay({ result }) {
    if (!result) {
        return null; // Don't render anything if no result is available
    }

    return (
        <div style={{
            backgroundColor: "rgba(255, 255, 255, 0.3)",
            padding: "20px",
            borderRadius: "10px",
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.2)",
            backdropFilter: "blur(10px)",
            marginTop: "20px",
            textAlign: "left",
            color: "white",
            width: "350px",
            maxWidth: "90%",
            overflowWrap: "break-word",
        }}>
            <h3>Analysis Result</h3>
            <p><strong>Overall Score:</strong> {result.overall_score}</p>

            <h4>Metrics Breakdown:</h4>
            <ul style={{ 
                paddingLeft: "20px",  // Adjusts dot positioning
                margin: "0",
                listStylePosition: "inside" // Moves the bullet close to text
            }}>
                {result.metrics && result.metrics.length > 0 ? (
                    result.metrics.map((metric, index) => (
                        <li key={index}><strong>{metric.name}:</strong> {metric.score}</li>
                    ))
                ) : (
                    <li>No metrics available.</li>
                )}
            </ul>

            <h4>Issues Found:</h4>
            <ul style={{ 
                paddingLeft: "20px", 
                margin: "0",
                listStylePosition: "inside"  // Moves the bullet close to text
            }}>
                {result.issues && result.issues.length > 0 ? (
                    result.issues.map((issue, index) => (
                        <li key={index}>{issue}</li>
                    ))
                ) : (
                    <li>No issues detected.</li>
                )}
            </ul>
        </div>
    );
}

export default ResultDisplay;

