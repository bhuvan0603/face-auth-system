import "./App.css";
import { useRef, useState } from "react";
import Camera from "./components/Camera";
import API from "./api";

function App() {
  const webcamRef = useRef(null);

  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  // Capture image from webcam
  const captureImage = async () => {
    const imageSrc = webcamRef.current.getScreenshot();

    const blob = await fetch(imageSrc).then((res) => res.blob());

    return blob;
  };

  // Register
  const handleRegister = async () => {
    if (!name) {
      alert("Enter username");
      return;
    }

    try {
      const blob = await captureImage();

      const formData = new FormData();
      formData.append("file", blob, "face.jpg");

      const res = await API.post(
        `/face/register?name=${name}`,
        formData
      );

      setMessage(res.data.message);
      alert("Registration Successful");
    } catch (err) {
      alert(
        err.response?.data?.detail || "Registration Failed"
      );
    }
  };

  // Login
  const handleLogin = async () => {
    try {
      const blob = await captureImage();

      const formData = new FormData();
      formData.append("file", blob, "face.jpg");

      const res = await API.post(
        "/face/login",
        formData
      );

      localStorage.setItem(
        "token",
        res.data.access_token
      );

      alert("Login Successful");

      const protectedData = await API.get("/protected", {
        headers: {
          Authorization:
            "Bearer " + res.data.access_token,
        },
      });

      setMessage(protectedData.data.message);
    } catch (err) {
      alert(
        err.response?.data?.detail || "Login Failed"
      );
    }
  };

  return (
    <div className="app">
      <div className="background"></div>

      <div className="glass-card">
        <h1>🤖 AI Face Authentication</h1>

        <p>Secure • Fast • Contactless Authentication</p>

        <Camera webcamRef={webcamRef} />

        <input
          type="text"
          placeholder="Enter Username"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <div className="buttons">
          <button
            className="register"
            onClick={handleRegister}
          >
            Register
          </button>

          <button
            className="login"
            onClick={handleLogin}
          >
            Login
          </button>
        </div>

        <h3 style={{ marginTop: 20 }}>
          {message}
        </h3>
      </div>
    </div>
  );
}

export default App;