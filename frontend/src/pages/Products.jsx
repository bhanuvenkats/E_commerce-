import { useEffect, useState } from "react";
import api from "../api/axios";
import { Package } from "lucide-react";

export default function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    api
      .get("/product")
      .then((res) => setProducts(res.data))
      .catch((err) => console.error("Failed to load products", err));
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <Package className="w-6 h-6 text-indigo-600" />
          <h1 className="text-2xl font-semibold">Products</h1>
        </div>
        <p className="text-gray-600">Manage your products here.</p>
      </div>

      {/* Product List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.length === 0 ? (
          <p className="text-gray-500">No products found.</p>
        ) : (
          products.map((p) => (
            <div
              key={p.id}
              className="rounded-lg border bg-white p-4 hover:shadow-sm transition"
            >
              <h4 className="font-medium text-lg">{p.name}</h4>
              <p className="text-sm text-gray-600 mt-1">
                ₹{p.price}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}