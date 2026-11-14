const request = require("supertest");
const app = require("../app");

describe("GET /health", () => {
  it("returns ok status", async () => {
    const res = await request(app).get("/health");
    expect(res.statusCode).toBe(200);
    expect(res.body).toEqual({ status: "ok", service: "products" });
  });
});

describe("GET /products", () => {
  it("lists all products", async () => {
    const res = await request(app).get("/products");
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveLength(5);
  });

  it("filters by owner_id", async () => {
    const res = await request(app).get("/products?owner_id=1");
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveLength(2);
    expect(res.body.every((p) => p.owner_id === 1)).toBe(true);
  });

  it("returns empty array for unknown owner", async () => {
    const res = await request(app).get("/products?owner_id=99");
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveLength(0);
  });
});

describe("GET /products/:id", () => {
  it("returns a single product", async () => {
    const res = await request(app).get("/products/1");
    expect(res.statusCode).toBe(200);
    expect(res.body.name).toBe("Laptop");
  });

  it("returns 404 for missing product", async () => {
    const res = await request(app).get("/products/999");
    expect(res.statusCode).toBe(404);
    expect(res.body).toHaveProperty("error");
  });
});
