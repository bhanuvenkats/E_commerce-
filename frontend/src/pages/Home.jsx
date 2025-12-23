import {
  Truck,
  ShieldCheck,
  RotateCcw,
  Star,
  Shirt,
  ShoppingBag,
  Laptop,
  Watch,
  Flame,
  Sparkles
} from "lucide-react";

export default function Home() {
    return (
      <>
        {/* ===== GLOBAL PAGE BACKGROUND ===== */}
        <div className="fixed inset-0 -z-10 bg-black">
          <div className="absolute inset-0 bg-gradient-to-br from-[#1a1f4d] via-black to-[#4b1235]"></div>
          <div className="absolute -top-40 -left-40 w-[700px] h-[700px] bg-indigo-500/25 rounded-full blur-3xl"></div>
          <div className="absolute top-1/3 -right-40 w-[600px] h-[600px] bg-pink-500/25 rounded-full blur-3xl"></div>
        </div>
        {/* ================= HERO SECTION ================= */}
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-transparent">
          
  
          {/* Content */}
          <div className="relative z-10 max-w-4xl px-6 text-center translate-y-6">
            <span className="inline-block mb-4 rounded-full border border-white/20 px-4 py-1 text-xl text-white/80">
              New Arrivals 2025
            </span>
  
            <h1 className="text-6xl md:text-8xl font-semibold tracking-tight text-white leading-tight">
              Shop smarter.
              <br />
              <span className="text-white/60">Live better.</span>
            </h1>
  
            <p className="mt-8 text-xl md:text-2xl text-white/70 max-w-3xl mx-auto">
              Discover premium products crafted for quality, performance, and
              everyday comfort.
            </p>
  
            <div className="mt-12 flex justify-center gap-6">
              <button className="px-10 py-4 rounded-full bg-white text-black font-medium hover:bg-white/90 transition text-lg">
                Shop Now
              </button>
  
              <button className="px-10 py-4 rounded-full border border-white/30 text-white hover:bg-white/10 transition text-lg">
                View Categories
              </button>
            </div>

            {/* Trust Signals */}
            <div className="mt-24 max-w-5xl mx-auto grid grid-cols-2 sm:grid-cols-4 gap-10 text-white/70 text-sm">
              <div className="group flex flex-col items-center text-center gap-2 transition">
                <Truck className="w-7 h-7 text-white/80 group-hover:text-white group-hover:-translate-y-1 transition" />
                <p className="font-medium text-white">Free Shipping</p>
                <p className="text-white/60">On orders over ₹999</p>
              </div>
              <div className="group flex flex-col items-center text-center gap-2 transition">
                <ShieldCheck className="w-7 h-7 text-white/80 group-hover:text-white group-hover:-translate-y-1 transition" />
                <p className="font-medium text-white">Secure Payments</p>
                <p className="text-white/60">100% protected</p>
              </div>
              <div className="group flex flex-col items-center text-center gap-2 transition">
                <RotateCcw className="w-7 h-7 text-white/80 group-hover:text-white group-hover:-translate-y-1 transition" />
                <p className="font-medium text-white">Easy Returns</p>
                <p className="text-white/60">7-day policy</p>
              </div>
              <div className="group flex flex-col items-center text-center gap-2 transition">
                <Star className="w-7 h-7 text-white/80 group-hover:text-white group-hover:-translate-y-1 transition" />
                <p className="font-medium text-white">4.8 Rating</p>
                <p className="text-white/60">10k+ customers</p>
              </div>
            </div>
          </div>
        </section>
  
        {/* ================= CATEGORIES SECTION ================= */}
        <section className="relative pt-0 pb-20 overflow-hidden bg-transparent">


          <div className="relative z-10 max-w-6xl mx-auto px-6 text-center">
            <h2 className="text-5xl md:text-7xl font-semibold tracking-tight mb-16 text-white">
              Shop by Category
            </h2>
  
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-12 mt-8">
              {[
                { name: "Men", icon: Shirt },
                { name: "Women", icon: ShoppingBag },
                { name: "Electronics", icon: Laptop },
                { name: "Accessories", icon: Watch },
              ].map((cat) => (
                <div
                  key={cat.name}
                  className="group relative h-52 rounded-3xl bg-white/10 backdrop-blur-lg border border-white/20 p-10 cursor-pointer overflow-hidden transition hover:scale-[1.04] hover:bg-white/15 hover:shadow-2xl"
                >
                  <h3 className="text-xl font-medium text-white flex items-center justify-center gap-3">
                    <cat.icon className="w-8 h-8 text-white/80 group-hover:text-white transition" />
                    {cat.name}
                  </h3>
  
                  <p className="mt-3 text-sm text-white/60 text-center">
                    Explore Collection
                  </p>
  
                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition"></div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ================= FEATURED PRODUCTS ================= */}
        <section className="relative py-20">
          <div className="max-w-7xl mx-auto px-6">
            <div className="flex justify-between items-end mb-12">
              <h2 className="text-3xl font-semibold text-white">
                Featured Products
              </h2>
              <a href="/shop" className="text-sm text-white/60 underline">
                View all
              </a>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
              {[1,2,3,4].map((i) => (
                <div
                  key={i}
                  className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-4 hover:scale-[1.03] transition"
                >
                  <div className="relative h-48 bg-black/30 rounded-xl mb-4 overflow-hidden">
                    {i === 1 && (
                      <span className="absolute top-3 left-3 flex items-center gap-1 text-xs bg-emerald-500 text-black px-2 py-1 rounded-full">
                        <Sparkles className="w-3 h-3" /> New
                      </span>
                    )}
                    {i === 2 && (
                      <span className="absolute top-3 left-3 flex items-center gap-1 text-xs bg-rose-500 text-white px-2 py-1 rounded-full">
                        <Flame className="w-3 h-3" /> Hot
                      </span>
                    )}
                  </div>
                  <h3 className="text-white font-medium">
                    Premium Product
                  </h3>
                  <p className="text-white/60 text-sm">
                    ₹1,499
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ================= WHY SIRISTORE ================= */}
        <section className="relative py-20">
          <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-12 text-white">
            <div>
              <h3 className="text-xl font-semibold mb-2 flex items-center gap-2">
                🧵 Curated Quality
              </h3>
              <p className="text-white/60">
                Every product is handpicked for durability, design, and comfort.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-2 flex items-center gap-2">
                🧠 Built for Everyday
              </h3>
              <p className="text-white/60">
                Designed to fit seamlessly into your lifestyle.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-2 flex items-center gap-2">
                ❤️ Trusted by Thousands
              </h3>
              <p className="text-white/60">
                Loved by customers across India.
              </p>
            </div>
          </div>
        </section>
  
        {/* ================= FOOTER ================= */}
        <footer className="relative bg-neutral-900 py-10 text-neutral-200">
          <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
          <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            
            {/* Brand */}
            <div>
              <h4 className="text-white font-semibold text-lg mb-2">
                siriStore
              </h4>
              <p className="text-xs text-neutral-400 leading-relaxed">
                Premium products designed for everyday excellence.
              </p>
            </div>
  
            {/* Links */}
            <div className="flex justify-center gap-5 text-xs text-neutral-300">
              <a href="#" className="hover:text-white underline underline-offset-4 transition">Privacy</a>
              <a href="#" className="hover:text-white underline underline-offset-4 transition">Terms</a>
              <a href="#" className="hover:text-white underline underline-offset-4 transition">Support</a>
            </div>
  
            {/* Copyright */}
            <div className="text-xs text-center md:text-right text-neutral-500">
              © {new Date().getFullYear()} siriStore. All rights reserved.
            </div>
          </div>
        </footer>
      </>
    );
  }