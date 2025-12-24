import { useEffect, useState } from "react";
import api from "../api/axios";
import { Layers } from "lucide-react";

export default function Categories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/category/")
      .then((res) => setCategories(res.data))
      .catch((err) => console.error("Failed to load categories", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-gray-500">Loading categories...</p>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <Layers className="w-6 h-6 text-indigo-600" />
          <h1 className="text-2xl font-semibold">Categories</h1>
        </div>
        <p className="text-gray-600">Manage product categories here.</p>
      </div>

      {/* Categories List */}
      {categories.length === 0 ? (
        <p className="text-gray-500">No categories found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map((category) => (
            <div
              key={category.id}
              className="rounded-lg border bg-white p-4 hover:shadow-sm transition"
            >
              <p className="font-medium">{category.name}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}