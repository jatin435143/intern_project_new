import React from "react";
import FileUpload from "./FileUpload";

function App() {
    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            minHeight: "100vh",
            background: "linear-gradient(135deg, #1E3C72, #2A5298)", // Blue gradient
            color: "white",
            fontFamily: "Arial, sans-serif",
            textAlign: "center",
            padding: "20px",
        }}>
            {/* Glassmorphism Heading */}
            <h1 style={{
                backgroundColor: "rgba(255, 255, 255, 0.2)",
                padding: "15px 30px",
                borderRadius: "10px",
                boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.2)",
                backdropFilter: "blur(10px)",
                fontSize: "32px",
                fontWeight: "bold",
                width: "fit-content",
                textTransform: "uppercase",
                letterSpacing: "1px",
            }}>
                Code Quality Analyzer
            </h1>

            {/* Upload Box */}
            <FileUpload />

            {/* Footer */}
            <footer style={{
                marginTop: "20px",
                fontSize: "14px",
                opacity: "0.7",
            }}>
                Built with 💙 by <strong>JATIN SHARMA</strong>
            </footer>
        </div>
    );
}

export default App;
