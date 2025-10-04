import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/endpoints";
import { saveToken } from "../utils/auth";
export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [err, setErr] = useState("");
  const nav = useNavigate();
  const submit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await login(form);
      saveToken(data.access_token);
      nav("/");
    } catch (e) {
      setErr("Login failed");
    }
  };
  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded">
      <h2 className="text-xl mb-4">Login</h2>
      <form onSubmit={submit} className="flex flex-col gap-3">
        <input
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          placeholder="username"
          className="border p-2"
        />
        <input
          type="password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          placeholder="password"
          className="border p-2"
        />
        <button className="bg-blue-600 text-white p-2 rounded">Login</button>
        {err && <div className="text-red-500">{err}</div>}
      </form>
    </div>
  );
}
