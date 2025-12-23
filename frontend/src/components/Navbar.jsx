import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Shadow on scroll
  useEffect(() => {
    const onScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const isLoggedIn = false; // temp

  return (
    <header
      className={`sticky top-0 z-50 bg-white transition-shadow ${
        scrolled ? "shadow-md" : ""
      }`}
    >
      <nav className="max-w-7xl mx-auto px-8 py-6 flex items-center justify-between">
        
        {/* Logo */}
        <Link
          to="/"
          className="text-3xl font-extrabold tracking-tight"
        >
          siri<span className="text-gray-400">Store</span>
        </Link>

        {/* Nav Links */}
        <div className="hidden md:flex items-center gap-10 text-lg font-medium">
          <Link to="/" className="hover:text-gray-500 transition">
            Home
          </Link>
          <Link to="/shop" className="hover:text-gray-500 transition">
            Shop
          </Link>
          <Link to="/categories" className="hover:text-gray-500 transition">
            Categories
          </Link>
          <Link to="/contact" className="hover:text-gray-500 transition">
            Contact
          </Link>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-8 relative" ref={dropdownRef}>
          
          {/* Cart */}
          <button className="relative text-2xl">
            🛒
            <span className="absolute -top-2 -right-2 text-xs bg-black text-white rounded-full px-1.5">
              2
            </span>
          </button>

          {/* Profile */}
          <button
            onClick={() => setOpen(!open)}
            className="w-11 h-11 rounded-full bg-gray-100 flex items-center justify-center text-xl hover:bg-gray-200 transition"
          >
            👤
          </button>

          {/* Dropdown */}
          {open && (
            <div className="absolute right-0 top-14 w-48 bg-white border rounded-2xl shadow-xl overflow-hidden">
              {isLoggedIn ? (
                <>
                  <Link
                    to="/profile"
                    className="block px-5 py-3 text-base hover:bg-gray-100"
                  >
                    My Profile
                  </Link>
                  <Link
                    to="/orders"
                    className="block px-5 py-3 text-base hover:bg-gray-100"
                  >
                    Orders
                  </Link>
                  <button className="w-full text-left px-5 py-3 text-base hover:bg-gray-100">
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="block px-5 py-3 text-base hover:bg-gray-100"
                  >
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="block px-5 py-3 text-base hover:bg-gray-100"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          )}
        </div>
      </nav>
    </header>
  );
}