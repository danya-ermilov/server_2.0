import React, { useEffect, useState } from "react";
import { getCart, deleteFromCart, clearCart } from "../api/endpoints";
export default function Cart() {
  const [cart, setCart] = useState(null);
  useEffect(() => {
    fetch();
  }, []);
  const fetch = async () => {
    const { data } = await getCart();
    setCart(data.cart);
  };
  const remove = async (id) => {
    await deleteFromCart({ item_id: id });
    fetch();
  };
  const clearAll = async () => {
    await clearCart();
    fetch();
  };
  if (!cart) return <div>Loading..</div>;
  return (
    <div className="bg-white p-4 rounded">
      <h2 className="text-xl">Cart</h2>
      <ul>
        {cart.items?.map((i) => (
          <li key={i.id} className="flex justify-between border-b py-2">
            <div>{i.title}</div>
            <div className="flex gap-2">
              <button onClick={() => remove(i.id)} className="textred-500">
                Remove
              </button>
            </div>
          </li>
        ))}
      </ul>
      <div className="mt-4">
        <button
          onClick={clearAll}
          className="px-3 py-1 bg-red-600 text-white rounded"
        >
          Clear cart
        </button>
      </div>
    </div>
  );
}
