import React from "react";

function ResultDisplay({ result }) {
    // Ensure `result` contains valid data
    if (!result) {
        return <p>No analysis data available.</p>;
    }

    // Ensure `metrics` and `issues` exist
    const metrics = result.metrics || [];
    const issues = result.issues || [];

    return (
        <div>
            <h2>Analysis Result</h2>
            <p><strong>Overall Score:</strong> {result.overall_score}</p>

            <h3>Metrics Breakdown:</h3>
            <ul>
                {metrics.length > 0 ? (
                    metrics.map((metric, index) => (
                        <li key={index}><strong>{metric.name}:</strong> {metric.score}</li>
                    ))
                ) : (
                    <li>No metrics available.</li>
                )}
            </ul>

            <h3>Issues Found:</h3>
            <ul>
                {issues.length > 0 ? (
                    issues.map((issue, index) => (
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

