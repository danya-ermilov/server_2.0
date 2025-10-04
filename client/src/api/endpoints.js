import client from "./client";
export const register = (payload) => client.post("/register", payload);
export const login = (form) => client.post("/token", form);
export const me = () => client.get("/users/me");
export const getAllUsers = () => client.get("/users/getall");
export const getOneUser = (username) =>
  client.get(`/users/getone/${encodeURIComponent(username)}`);
export const getOneUserWithXp = (username) =>
  client.get(`/users/getone/${encodeURIComponent(username)}/xp`);
export const deleteUser = () => client.delete("/users/delete/");
export const updateUser = (payload) => client.put("/users/update/", payload);
export const setXpBulk = (payload) => client.post("/users/set_xp", payload);

// products
export const createProduct = (payload) => client.post("/products/", payload);
export const listProducts = (tag) =>
  client.get("/products/", { params: tag ? { tag } : {} });
export const searchProducts = (q) =>
  client.get("/products/search", {
    params: { query: q },
  });
export const getProduct = (id) => client.get(`/products/${id}`);
export const updateProduct = (id, payload) =>
  client.put(`/products/${id}`, payload);
export const deleteProduct = (id) => client.delete(`/products/${id}`);
export const getUsersByProduct = (id) => client.get(`/products/users/${id}`);

// cart
export const getCart = () => client.get("/cart/");
export const addToCart = (item_id) => client.post("/cart/add", { item_id });
export const clearCart = () => client.delete("/cart/");
export const deleteFromCart = (item_id) =>
  client.delete("/cart/delete", {
    data: { item_id },
  });

// admin
export const adminDeleteUser = (username) =>
  client.delete(`/admin/users/delete/${encodeURIComponent(username)}`);
export const adminUpdateUser = (username, payload) =>
  client.put(`/admin/users/update/${encodeURIComponent(username)}`, payload);
export const createTag = (name) =>
  client.post("/admin/tags/create", {
    name,
  });

// comments
export const createComment = (product_id, text) =>
  client.post(`/comments/products/${product_id}/comments`, { text });
export const getComments = (product_id) =>
  client.get(`/comments/products/${product_id}/comments`);

// tags
export const getTags = () => client.get("/tags/get");

// root
export const root = () => client.get("/");
