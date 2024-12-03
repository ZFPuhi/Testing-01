/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
      return [
        {
          source: "/api/:path*", // Proxy all /api/* requests
          destination: "http://localhost:8080/:path*", // Redirect to validator
        },
      ];
    },
  };
  
  export default nextConfig;
  