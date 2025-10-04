import React, { useEffect, useState } from "react";
import { listProducts, searchProducts } from "../api/endpoints";
import ProductCard from "../components/ProductCard";
export default function Products() {
  const [items, setItems] = useState([]);
  const [q, setQ] = useState("");
  useEffect(() => {
    fetch();
  }, []);
  const fetch = async () => {
    const { data } = await listProducts();
    setItems(data);
  };
  const doSearch = async (e) => {
    e.preventDefault();
    if (!q) return fetch();
    const { data } = await searchProducts(q);
    setItems(data);
  };
  return (
    <div>
      <form onSubmit={doSearch} className="mb-4 flex gap-2">
        <input
          className="border p-2 flex-1"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search"
        />
        <button className="px-3 bg-blue-500 text-white rounded">Search</button>
      </form>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {items.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}
