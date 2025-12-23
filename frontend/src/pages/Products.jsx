import { useEffect, useState } from "react";
import api from "../api/api";

const Products = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    api.get("/product")
      .then((res) => setProducts(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Products</h2>
      {products.map((p) => (
        <div key={p.id}>
          <h4>{p.name}</h4>
          <p>{p.price}</p>
        </div>
      ))}
    </div>
  );
};

export default Products;