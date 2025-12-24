import { NavLink, Outlet, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Package,
  Layers,
  User,
  UserCircle,
  LogOut
} from "lucide-react";

const navItems = [
  { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { name: "Products", path: "/dashboard/products", icon: Package },
  { name: "Categories", path: "/dashboard/categories", icon: Layers },
  { name: "Profile", path: "/dashboard/profile", icon: User },
];

export default function DashboardLayout() {
  const navigate = useNavigate();

  const firstName = (() => {
    try {
      const user = JSON.parse(localStorage.getItem("user"));
      return user?.first_name || "User";
    } catch {
      return "User";
    }
  })();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      
      {/* Sidebar */}
      <aside className="w-64 bg-gradient-to-b from-indigo-900 via-indigo-800 to-slate-900 text-white flex flex-col shadow-xl">
        <div className="p-6 text-xl font-semibold tracking-wide border-b border-white/10">
          SIRI Admin
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(({ name, path, icon: Icon }) => (
            <NavLink
              key={name}
              to={path}
              end={path === "/dashboard"}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200
                 ${
                   isActive
                     ? "bg-white/20 text-white shadow-md scale-[1.02]"
                     : "text-indigo-200 hover:bg-white/10 hover:text-white"
                 }`
              }
            >
              <Icon size={20} />
              <span className="text-sm font-medium">{name}</span>
            </NavLink>
          ))}
        </nav>

        {/* User & Logout */}
        <div className="p-4 border-t border-white/10 space-y-3">
          <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-white/10">
            <UserCircle className="w-8 h-8 text-indigo-200" />
            <div className="leading-tight">
              <p className="text-xs text-indigo-200">Signed in as</p>
              <p className="text-sm font-medium text-white">{firstName}</p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg
                       bg-red-500/10 text-red-300 hover:bg-red-500/20 hover:text-red-200
                       transition-all duration-200 active:scale-95"
          >
            <LogOut className="w-5 h-5" />
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  );
}