const express = require("express");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

const PRODUCTS = [
  { id: 1, name: "Laptop",     price: 999.99, owner_id: 1 },
  { id: 2, name: "Mouse",      price:  29.99, owner_id: 1 },
  { id: 3, name: "Keyboard",   price:  79.99, owner_id: 2 },
  { id: 4, name: "Monitor",    price: 349.99, owner_id: 3 },
  { id: 5, name: "Headphones", price: 149.99, owner_id: 2 },
];

app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "products" });
});

app.get("/products", (req, res) => {
  const { owner_id } = req.query;
  if (owner_id) {
    const id = parseInt(owner_id, 10);
    return res.json(PRODUCTS.filter((p) => p.owner_id === id));
  }
  res.json(PRODUCTS);
});

app.get("/products/:id", (req, res) => {
  const product = PRODUCTS.find((p) => p.id === parseInt(req.params.id, 10));
  if (!product) {
    return res.status(404).json({ error: "Product not found" });
  }
  res.json(product);
});

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Products service listening on port ${PORT}`);
  });
}

module.exports = app;
