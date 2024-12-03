import React, { useEffect, useState } from "react";
import { parseStringPromise } from "xml2js"; // Import the XML parser

const ValidatorReport = ({ reportData }) => {
  const [parsedData, setParsedData] = useState(null);

  useEffect(() => {
    // Parse the XML string into a JavaScript object
    const parseXML = async () => {
      try {
        const result = await parseStringPromise(reportData);
        setParsedData(result);
      } catch (err) {
        console.error("Failed to parse XML:", err.message);
      }
    };

    if (reportData) {
      parseXML();
    }
  }, [reportData]);

  if (!parsedData) {
    return <p>Loading report...</p>;
  }

  return (
    <div className="validator-report">
      <h2 className="text-lg font-semibold">Validation Report</h2>
      <p><strong>Document Type:</strong> {parsedData?.document?.type || "Unknown"}</p>
      <p><strong>Timestamp:</strong> {parsedData?.document?.timestamp || "Unknown"}</p>
      <p><strong>Conformance:</strong> {parsedData?.document?.conformanceMessage || "N/A"}</p>
      <p><strong>Recommendation:</strong> {parsedData?.document?.recommendation || "N/A"}</p>

      {/* Render additional details */}
      <h3 className="text-md font-medium mt-4">Details:</h3>
      <ul className="mt-2 list-disc list-inside">
        {parsedData?.document?.details?.map((detail, index) => (
          <li key={index}>{detail.id}: {detail.value}</li>
        ))}
      </ul>
    </div>
  );
};

export default ValidatorReport;
