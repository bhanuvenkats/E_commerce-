import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { verifyPasswordReset } from "../api/auth";
import Toast from "../components/Toast";

export default function ResetPassword() {
  const { state } = useLocation();
  const email = state?.email;

  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [showToast, setShowToast] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await verifyPasswordReset({
        email,
        otp,
        new_password: newPassword,
        confirm_password: confirmPassword,
      });

      setShowToast(true);

      setTimeout(() => {
        navigate("/login");
      }, 1000);
    } catch (err) {
      setError(err.response?.data?.detail || "Reset failed");
    }
  };

  return (
    <section className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md bg-white p-8 rounded-2xl shadow-md">
        <h2 className="text-2xl font-bold text-center mb-6">
          Reset Password
        </h2>

        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            placeholder="OTP"
            className="w-full px-4 py-3 border rounded-xl"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
          />

          <input
            type="password"
            placeholder="New password"
            className="w-full px-4 py-3 border rounded-xl"
            onChange={(e) => setNewPassword(e.target.value)}
          />

          <input
            type="password"
            placeholder="Confirm password"
            className="w-full px-4 py-3 border rounded-xl"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />

          <button className="w-full py-3 bg-black text-white rounded-xl">
            Reset Password
          </button>
        </form>
      </div>

      <Toast
        show={showToast}
        message="Password reset successfully. Please login."
        onClose={() => setShowToast(false)}
      />
    </section>
  );
}