import React from "react";
import useAuth from "../hooks/useAuth";
export default function Profile() {
  const { user } = useAuth();
  if (!user) return <div>No user</div>;
  return (
    <div className="bg-white p-6 rounded">
      <h2 className="text-xl">Profile — {user.username}</h2>
      <pre className="mt-4">{JSON.stringify(user, null, 2)}</pre>
    </div>
  );
}
