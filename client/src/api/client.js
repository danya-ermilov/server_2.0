import axios from "axios";
import { API_BASE } from "./config";
const client = axios.create({ baseURL: API_BASE });
client.interceptors.request.use((cfg) => {
  const token = localStorage.getItem("access_token");
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});
export default client;
