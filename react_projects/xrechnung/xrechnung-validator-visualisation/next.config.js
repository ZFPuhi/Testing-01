/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/validate", // Proxy endpoint
        destination: "http://localhost:8080/", // Validator daemon
      },
    ];
  },
};

module.exports = nextConfig;
