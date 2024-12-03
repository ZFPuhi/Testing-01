"use client";

import React, { useState } from "react";
import ValidatorReport from "../components/ValidatorReport";

const HomePage = () => {
  const [file, setFile] = useState(null);
  const [validationResult, setValidationResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.name.endsWith(".xml")) {
      setFile(selectedFile);
      setValidationResult(null);
      setError("");
    } else {
      setError("Please upload a valid XML file.");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an XML file to upload.");
      return;
    }

    const reader = new FileReader();

    reader.onload = async () => {
      const xmlContent = reader.result;

      try {
        const response = await fetch("/api/validate", {
          method: "POST",
          headers: {
            "Content-Type": "application/xml",
          },
          body: xmlContent,
        });

        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }

        // Parse the response as plain text since it's XML
        const result = await response.text();

        // Pass the raw XML response to the validationResult state
        setValidationResult(result);
        setError("");
      } catch (err) {
        console.error("Validation error:", err.message);
        setError(err.message || "An error occurred while validating the file.");
      }
    };

    reader.readAsText(file);
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-50">
      <div className="w-full max-w-md p-6 bg-white rounded shadow-md">
        <h1 className="text-2xl font-bold text-center mb-6">XML Validator</h1>

        <div className="flex flex-col gap-4">
          <input
            type="file"
            accept=".xml"
            onChange={handleFileChange}
            className="file-input file-input-bordered w-full"
          />
          <button
            onClick={handleUpload}
            className="btn btn-primary w-full"
          >
            Validate File
          </button>
        </div>

        {error && <p className="text-red-500 mt-4">{error}</p>}

        {validationResult && (
          <div className="mt-6">
            {/* Pass the raw XML response to the ValidatorReport component */}
            <ValidatorReport reportData={validationResult} />
          </div>
        )}
      </div>
    </main>
  );
};

export default HomePage;
