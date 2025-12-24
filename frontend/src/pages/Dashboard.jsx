import { useEffect, useState } from "react";
import axios from "../api/axios";
import { Package, Layers, Users } from "lucide-react";

export default function DashboardHome() {
  const [data, setData] = useState({
    total_products: 0,
    total_categories: 0,
    active_users: 0,
  });

  const user = (() => {
    try {
      return JSON.parse(localStorage.getItem("user"));
    } catch {
      return null;
    }
  })();

  useEffect(() => {
    axios.get("/dashboard/summary").then((res) => {
      setData(res.data);
    });
  }, []);

  return (
    <div className="space-y-10 max-w-7xl">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-semibold text-gray-900">
          Welcome back, {user?.first_name || "User"} 👋
        </h1>
        <p className="text-gray-500 mt-1">
          Here’s what’s happening in your store today
        </p>
      </div>

      {/* Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          title="Products"
          value={data.total_products}
          icon={Package}
          color="indigo"
        />
        <StatCard
          title="Categories"
          value={data.total_categories}
          icon={Layers}
          color="emerald"
        />
        <StatCard
          title="Users"
          value={data.active_users}
          icon={Users}
          color="amber"
        />
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, color }) {
  const colors = {
    indigo: "bg-indigo-100 text-indigo-700",
    emerald: "bg-emerald-100 text-emerald-700",
    amber: "bg-amber-100 text-amber-700",
  };

  return (
    <div
      className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100
                 hover:shadow-md hover:-translate-y-1 transition-all duration-200
                 flex items-center justify-between"
    >
      <div>
        <p className="text-sm text-gray-500 mb-1">{title}</p>
        <p className="text-3xl font-semibold text-gray-900">{value}</p>
      </div>

      <div
        className={`h-12 w-12 rounded-xl flex items-center justify-center ${colors[color]}`}
      >
        <Icon size={22} />
      </div>
    </div>
  );
}