import { useEffect, useState } from "react";
import { User, Mail, Phone, Save } from "lucide-react";
import api from "../api/axios";

export default function Profile() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: ""
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    api.get("/users/me")
      .then(res => {
        setForm({
          first_name: res.data.first_name || "",
          last_name: res.data.last_name || "",
          email: res.data.email || "",
          phone: res.data.phone || ""
        });
      })
      .finally(() => setLoading(false));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage("");

    try {
      await api.put("/users/me", form);
      setMessage("Profile updated successfully ✅");
    } catch {
      setMessage("Failed to update profile ❌");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p className="text-gray-500">Loading profile...</p>;
  }

  return (
    <div className="w-full min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-semibold mb-8">My Profile</h1>

        <form
          onSubmit={handleSubmit}
          className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white p-8 rounded-xl shadow"
        >
          {/* First Name */}
          <div>
            <label className="text-sm text-gray-500 mb-1 block">First Name</label>
            <div className="flex items-center border rounded px-3 py-2 gap-2">
              <User size={18} className="text-gray-400" />
              <input
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
                className="w-full outline-none"
                placeholder="First name"
              />
            </div>
          </div>

          {/* Last Name */}
          <div>
            <label className="text-sm text-gray-500 mb-1 block">Last Name</label>
            <div className="flex items-center border rounded px-3 py-2 gap-2">
              <User size={18} className="text-gray-400" />
              <input
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
                className="w-full outline-none"
                placeholder="Last name"
              />
            </div>
          </div>

          {/* Email */}
          <div>
            <label className="text-sm text-gray-500 mb-1 block">Email</label>
            <div className="flex items-center border rounded px-3 py-2 gap-2 bg-gray-100">
              <Mail size={18} className="text-gray-400" />
              <input
                name="email"
                value={form.email}
                disabled
                className="w-full bg-transparent outline-none text-gray-500 cursor-not-allowed"
              />
            </div>
          </div>

          {/* Phone */}
          <div>
            <label className="text-sm text-gray-500 mb-1 block">Phone</label>
            <div className="flex items-center border rounded px-3 py-2 gap-2">
              <Phone size={18} className="text-gray-400" />
              <input
                name="phone"
                value={form.phone}
                onChange={handleChange}
                className="w-full outline-none"
                placeholder="+91XXXXXXXXXX"
              />
            </div>
          </div>

          {/* Save Button */}
          <div className="md:col-span-2 flex items-center justify-between mt-4">
            <button
              type="submit"
              disabled={saving}
              className="flex items-center gap-2 bg-black text-white px-6 py-2 rounded-lg hover:opacity-90 transition disabled:opacity-50"
            >
              <Save size={18} />
              {saving ? "Saving..." : "Save Changes"}
            </button>

            {message && (
              <p className="text-sm text-gray-600">{message}</p>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}