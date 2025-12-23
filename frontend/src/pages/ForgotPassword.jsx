import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { requestPasswordReset } from "../api/auth";
import Toast from "../components/Toast";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [showToast, setShowToast] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await requestPasswordReset({ email });
      setShowToast(true);

      setTimeout(() => {
        navigate("/reset-password", { state: { email } });
      }, 900);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to send OTP");
    }
  };

  return (
    <section className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md bg-white p-8 rounded-2xl shadow-md">
        <h2 className="text-2xl font-bold text-center mb-6">
          Forgot Password
        </h2>

        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            required
            placeholder="Enter your registered email"
            className="w-full px-4 py-3 border rounded-xl"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <button className="w-full py-3 bg-black text-white rounded-xl">
            Send OTP
          </button>
        </form>
      </div>

      <Toast
        show={showToast}
        message="OTP sent to your registered phone number."
        onClose={() => setShowToast(false)}
      />
    </section>
  );
}