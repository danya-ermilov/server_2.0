import { useState, useEffect } from "react";
import { me } from "../api/endpoints";
import { logout as doLogout } from "../utils/auth";
export default function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const fetchMe = async () => {
    setLoading(true);
    try {
      const { data } = await me();
      setUser(data);
    } catch (e) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    fetchMe();
  }, []);
  const logout = () => {
    doLogout();
    setUser(null);
  };
  return { user, loading, refresh: fetchMe, logout, setUser };
}
