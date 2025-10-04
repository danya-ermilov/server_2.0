import React, { useEffect, useState } from "react";
import { getAllUsers, adminDeleteUser } from "../api/endpoints";
export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch();
  }, []);
  const fetch = async () => {
    const { data } = await getAllUsers();
    setUsers(data);
  };
  const del = async (username) => {
    await adminDeleteUser(username);
    fetch();
  };
  return (
    <div className="bg-white p-4 rounded">
      <h2 className="text-xl">Users</h2>
      <ul>
        {users.map((u) => (
          <li key={u.username} className="flex justify-between py-2 borderb">
            <div>
              {u.username} ({u.email})
            </div>

            <div>
              <button onClick={() => del(u.username)} className="textred-500">
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
