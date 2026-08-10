import axios from "axios";

const API = axios.create({
  baseURL: "https://face-auth-backend-bhuvan.onrender.com",
});

export default API;