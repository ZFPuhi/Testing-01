"use client";

import React, { useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";

const HomePage = () => {
  const [file, setFile] = useState(null);
  const [validationResult, setValidationResult] = useState(null);
  const [error, setError] = useState("");

  const { getRootProps, getInputProps } = useDropzone({
    accept: ".xml", // Only accept .xml files
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
        setValidationResult(null);
        setError("");
      }
    },
  });

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload an XML file.");
      return;
    }
  
    // Create a new FileReader to read the file as text
    const reader = new FileReader();
  
    // Set up the FileReader to handle the file load event
    reader.onload = async () => {
      const xmlContent = reader.result;
  
      try {
        console.log("Uploading XML file:", file.name);
  
        // Send POST request directly to the validator daemon with raw XML content
        const response = await axios.post("http://localhost:8080/", xmlContent, {
          headers: {
            "Content-Type": "application/xml", // Set content type to application/xml
          },
        });
  
        console.log("Response from validator:", response.data);
        setValidationResult(response.data); // Set validation result to display
        setError(""); // Clear any previous errors
      } catch (err) {
        console.error("Validation error:", err.response?.data || err.message);
        setError(err.response?.data || "Validation failed. Please check the file and try again.");
      }
    };
    reader.readAsText(file);
  };
  
  

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-50">
      <div className="w-full max-w-md p-6 bg-white rounded shadow-md">
        <h1 className="text-2xl font-bold text-center mb-6">XRechnung Validator</h1>

        <div
          {...getRootProps()}
          className="border-2 border-dashed border-gray-400 p-6 text-center cursor-pointer hover:border-blue-500"
        >
          <input {...getInputProps()} />
          {file ? (
            <p className="text-sm text-gray-600">{file.name}</p>
          ) : (
            <p className="text-sm text-gray-600">Drag & drop an XML file here, or click to browse</p>
          )}
        </div>

        <button
          onClick={handleUpload}
          className="mt-6 w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Validate File
        </button>

        {error && <p className="mt-4 text-red-500">{error}</p>}

        {validationResult && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold">Validation Result:</h2>
            <pre className="mt-2 p-2 bg-gray-100 border rounded text-sm overflow-auto">
              {JSON.stringify(validationResult, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </main>
  );
};

export default HomePage;
