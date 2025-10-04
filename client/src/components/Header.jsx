import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { logout as doLogout } from "../utils/auth";
export default function Header({ user }) {
  const nav = useNavigate();
  const logout = () => {
    doLogout();
    nav("/login");
  };
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto p-4 flex justify-between itemscenter">
        <div className="flex items-center gap-4">
          <Link to="/" className="font-bold text-lg">
            MyApp
          </Link>
          <Link to="/products" className="text-sm">
            Products
          </Link>
          <Link to="/cart" className="text-sm">
            Cart
          </Link>
        </div>
        <div>
          {user ? (
            <div className="flex items-center gap-3">
              <Link to="/profile" className="text-sm">
                {user.username}
              </Link>
              {user.is_admin && (
                <Link to="/admin/users" className="textsm">
                  Admin
                </Link>
              )}
              <button onClick={logout} className="px-3 py-1 rounded bggray-100">
                Logout
              </button>
            </div>
          ) : (
            <div className="flex gap-2">
              <Link to="/login" className="text-sm">
                Login
              </Link>
              <Link to="/register" className="text-sm">
                Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
