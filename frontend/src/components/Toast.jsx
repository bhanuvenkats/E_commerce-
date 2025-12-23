import { useEffect } from "react";

export default function Toast({ message, show, onClose }) {
  useEffect(() => {
    if (show) {
      const timer = setTimeout(onClose, 2500);
      return () => clearTimeout(timer);
    }
  }, [show, onClose]);

  if (!show) return null;

  return (
    <div className="fixed top-6 right-6 z-50">
      <div
        className="
          flex items-center gap-3
          bg-black text-white
          px-5 py-4 rounded-2xl shadow-xl
          animate-toast
        "
      >
        <span className="text-xl">✅</span>
        <span className="text-sm font-medium">
          {message}
        </span>
      </div>
    </div>
  );
}