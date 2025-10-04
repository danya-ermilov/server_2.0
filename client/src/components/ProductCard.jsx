import React from "react";
import { Link } from "react-router-dom";
export default function ProductCard({ product }) {
  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="font-bold">{product.title || product.name}</h3>
      <p className="text-sm">{product.description}</p>
      <div className="mt-3 flex justify-between items-center">
        <Link to={`/products/${product.id}`} className="text-blue-600">
          View
        </Link>
        <span className="text-sm">
          {product.price ? `${product.price} ₽` : ""}
        </span>
      </div>
    </div>
  );
}
