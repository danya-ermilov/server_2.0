import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getProduct,
  addToCart,
  getComments,
  createComment,
} from "../api/endpoints";
export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");
  useEffect(() => {
    fetch();
  }, [id]);
  const fetch = async () => {
    const { data } = await getProduct(id);
    setProduct(data);
    const c = await getComments(id);
    setComments(c.data);
  };
  const add = async () => {
    await addToCart({ item_id: id });
    alert("added");
  };
  const postComment = async () => {
    await createComment(id, text);
    setText("");
    fetch();
  };
  if (!product) return <div>Loading...</div>;
  return (
    <div className="bg-white p-6 rounded">
      <h2 className="text-2xl">{product.title || product.name}</h2>
      <p className="my-4">{product.description}</p>
      <div className="flex gap-2">
        <button
          onClick={add}
          className="px-3 py-1 bg-blue-600 text-white rounded"
        >
          Add to cart
        </button>
      </div>
      <section className="mt-6">
        <h3 className="font-bold">Comments</h3>
        <div className="mt-2">
          {comments.map((c, i) => (
            <div key={i} className="border p-2 mb-2 rounded">
              {c.text}
            </div>
          ))}
        </div>
        <div className="mt-2 flex gap-2">
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="border p-2 flex-1"
            placeholder="Write comment"
          />
          <button
            onClick={postComment}
            className="px-3 bg-green-600 textwhite rounded"
          >
            Post
          </button>
        </div>
      </section>
    </div>
  );
}
