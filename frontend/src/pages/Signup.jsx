import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  User,
  Phone,
  UserPlus,
} from "lucide-react";
import { signupUser } from "../api/auth";
import Toast from "../components/Toast";
import AuthLayout from "../layouts/AuthLayout";

export default function Signup() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    username: "",
    password: "",
    phone_number: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showToast, setShowToast] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await signupUser(form);
      setShowToast(true);
      setTimeout(() => navigate("/login"), 900);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        err.response?.data?.detail ||
        "Signup failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="w-full max-w-lg bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-10 shadow-2xl text-white">

        <h2 className="text-4xl font-semibold mb-2">Create account</h2>
        <p className="text-white/60 mb-10">
          Join siriStore for a premium experience
        </p>

        {error && <p className="text-red-400 mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* First name */}
          <div className="relative">
            <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
            <input
              placeholder="First name"
              className="auth-input text-lg py-4 pl-12"
              onChange={(e) =>
                setForm({ ...form, first_name: e.target.value })
              }
            />
          </div>

          {/* Last name */}
          <div className="relative">
            <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
            <input
              placeholder="Last name"
              className="auth-input text-lg py-4 pl-12"
              onChange={(e) =>
                setForm({ ...form, last_name: e.target.value })
              }
            />
          </div>

          {/* Email */}
          <div className="relative">
            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
            <input
              type="email"
              required
              placeholder="Email"
              className="auth-input text-lg py-4 pl-12"
              onChange={(e) =>
                setForm({ ...form, email: e.target.value })
              }
            />
          </div>

          {/* Username */}
          <div className="relative">
            <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
            <input
              required
              placeholder="Username"
              className="auth-input text-lg py-4 pl-12"
              onChange={(e) =>
                setForm({ ...form, username: e.target.value })
              }
            />
          </div>

          {/* Password */}
          <div className="relative">
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
            <input
              type={showPassword ? "text" : "password"}
              required
              placeholder="Password"
              className="auth-input text-lg py-4 pl-12 pr-14"
              onChange={(e) =>
                setForm({ ...form, password: e.target.value })
              }
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-white/60 hover:text-white"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>

          {/* Phone */}
          <div className="relative">
            <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
            <input
              placeholder="Phone number (optional)"
              className="auth-input text-lg py-4 pl-12"
              onChange={(e) =>
                setForm({ ...form, phone_number: e.target.value })
              }
            />
          </div>

          {/* Submit */}
          <button
            disabled={loading}
            className="w-full py-4 rounded-full bg-white text-black text-lg font-medium hover:bg-white/90 transition flex items-center justify-center gap-2"
          >
            {loading ? (
              <span className="w-6 h-6 border-2 border-black/30 border-t-black rounded-full animate-spin"></span>
            ) : (
              <>
                <UserPlus size={18} />
                Sign Up
              </>
            )}
          </button>
        </form>

        <p className="text-sm text-center mt-8 text-white/60">
          Already have an account?{" "}
          <Link to="/login" className="underline text-white">
            Login
          </Link>
        </p>

        <Toast
          show={showToast}
          message="Account created successfully! Please login."
          onClose={() => setShowToast(false)}
        />
      </div>
    </AuthLayout>
  );
}