import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Products from "./pages/Products";
import ProductDetail from "./pages/ProductDetail";
import Cart from "./pages/Cart";
import Profile from "./pages/Profile";
import AdminUsers from "./pages/AdminUsers";
import Header from "./components/Header";
import useAuth from "./hooks/useAuth";
export default function App() {
  const { user, loading } = useAuth();
  if (loading) return <div className="p-6">Loading...</div>;
  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} />
      <main className="container mx-auto p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/products" element={<Products />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/cart" element={<Cart />} />
          <Route
            path="/profile"
            element={user ? <Profile /> : <Navigate to="/login" replace />}
          />
          <Route
            path="/admin/users"
            element={
              user?.is_admin ? <AdminUsers /> : <Navigate to="/" replace />
            }
          />
        </Routes>
      </main>
    </div>
  );
}
