import React, { useRef } from "react";
import Webcam from "react-webcam";

function Camera({ webcamRef }) {
  return (
    <div style={{ marginBottom: "20px" }}>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={260}
        height={220}
        style={{
          borderRadius: "20px",
          border: "2px solid #00E5FF",
          boxShadow: "0 0 20px #00E5FF",
        }}
      />
    </div>
  );
}

export default Camera;