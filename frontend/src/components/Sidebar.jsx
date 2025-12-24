import { NavLink } from "react-router-dom";

const links = [
  { name: "Dashboard", path: "/dashboard" },
  { name: "Products", path: "/dashboard/products" },
  { name: "Categories", path: "/dashboard/categories" },
  { name: "Profile", path: "/dashboard/profile" }
];

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-gray-900 text-white p-6">
      <h2 className="text-xl font-bold mb-8">Siri Admin</h2>

      <nav className="space-y-4">
        {links.map(link => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              isActive
                ? "block px-4 py-2 bg-gray-700 rounded"
                : "block px-4 py-2 hover:bg-gray-800 rounded"
            }
          >
            {link.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}