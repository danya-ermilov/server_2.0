import React, { useState } from "react";
import { register } from "../api/endpoints";
import { useNavigate } from "react-router-dom";
export default function Register() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [msg, setMsg] = useState("");
  const nav = useNavigate();
  const submit = async (e) => {
    e.preventDefault();
    try {
      await register(form);
      setMsg("Registered! Please login.");
      nav("/login");
    } catch (e) {
      setMsg("Registration failed");
    }
  };
  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded">
      <h2 className="text-xl mb-4">Register</h2>
      <form onSubmit={submit} className="flex flex-col gap-3">
        <input
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          placeholder="username"
          className="border p-2"
        />
        <input
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          placeholder="email"
          className="border p-2"
        />
        <input
          type="password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          placeholder="password"
          className="border p-2"
        />
        <button className="bg-green-600 text-white p-2 rounded">
          Register
        </button>
        {msg && <div className="text-sm">{msg}</div>}
      </form>
    </div>
  );
}
