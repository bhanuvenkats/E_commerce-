import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Mail, Lock, Eye, EyeOff, LogIn } from "lucide-react";
import { useAuth } from "../auth/AuthContext";
import Toast from "../components/Toast";
import AuthLayout from "../layouts/AuthLayout";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showToast, setShowToast] = useState(false);

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await login({ email: email.trim(), password });

      /**
       * ✅ FIX: Correctly extract token & profile from backend response
       */
      const { token, profile } = res.data;

      // ✅ Store token (explicit & safe)
      localStorage.setItem("token", token);
      localStorage.setItem("access_token", token);

      // ✅ Store full user profile (THIS FIXES SIDEBAR + DASHBOARD)
      localStorage.setItem(
        "user",
        JSON.stringify({
          user_id: profile.user_id,
          username: profile.username,
          first_name: profile.first_name,
          last_name: profile.last_name,
          email: profile.email,
          phone_number: profile.phone_number,
          role: profile.role,
        })
      );

      setShowToast(true);
      setTimeout(() => navigate("/dashboard"), 800);

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "Login failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="w-full max-w-lg bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-10 shadow-2xl text-white">

        <h2 className="text-4xl font-semibold mb-2">Welcome back</h2>
        <p className="text-white/60 mb-10">
          Sign in to continue to siriStore
        </p>

        {error && <p className="text-red-400 mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Email */}
          <div className="relative">
            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
            <input
              type="email"
              required
              placeholder="Email"
              className="auth-input text-lg py-4 pl-12"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-white/60 hover:text-white"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>

          <p className="text-sm text-right">
            <Link to="/forgot-password" className="underline text-white/70">
              Forgot password?
            </Link>
          </p>

          {/* Submit */}
          <button
            disabled={loading}
            className="w-full py-4 rounded-full bg-white text-black text-lg font-medium hover:bg-white/90 transition flex items-center justify-center gap-2"
          >
            {loading ? (
              <span className="w-6 h-6 border-2 border-black/30 border-t-black rounded-full animate-spin"></span>
            ) : (
              <>
                <LogIn size={18} />
                Login
              </>
            )}
          </button>
        </form>

        <p className="text-sm text-center mt-8 text-white/60">
          No account?{" "}
          <Link to="/signup" className="underline text-white">
            Sign up
          </Link>
        </p>

        <Toast
          show={showToast}
          message="Welcome back! Login successful."
          onClose={() => setShowToast(false)}
        />
      </div>
    </AuthLayout>
  );
}