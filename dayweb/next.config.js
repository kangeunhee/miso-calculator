/** @type {import('next').NextConfig} */
const nextConfig = {
  // React 엄격 모드 활성화 (권장)
  reactStrictMode: true,

  // 필요 시 외부 이미지(카카오 프로필 등) 도메인 허용 설정
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
};

module.exports = nextConfig;