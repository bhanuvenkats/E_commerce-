export default function AuthLayout({ children }) {
    return (
      <>
        {/* ===== CINEMATIC BACKGROUND ===== */}
        <div className="fixed inset-0 -z-10 bg-black">
          <div className="absolute inset-0 bg-gradient-to-br from-[#1a1f4d] via-black to-[#4b1235]"></div>
          <div className="absolute -top-40 -left-40 w-[700px] h-[700px] bg-indigo-500/25 rounded-full blur-3xl"></div>
          <div className="absolute top-1/3 -right-40 w-[600px] h-[600px] bg-pink-500/25 rounded-full blur-3xl"></div>
        </div>
  
        {/* Page content */}
        <main className="min-h-screen flex items-center justify-center px-6">
          {children}
        </main>
      </>
    );
  }