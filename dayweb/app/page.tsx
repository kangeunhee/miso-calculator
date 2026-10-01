import LottoMap from '@/components/LottoMap';
import Script from 'next/script';

export default function HomePage() {
  const adsenseClientId = process.env.NEXT_PUBLIC_ADSENSE_CLIENT_ID;

  return (
    <main className="w-full h-screen overflow-hidden relative">
      {/* 구글 애드센스 자동 광고 스크립트 (발급 후 사용) */}
      {adsenseClientId && (
        <Script
          async
          src={`https://pagead2.googlesyndication.com/pagead/js/adsensewrapper.js?client=${adsenseClientId}`}
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />
      )}

      {/* 로또 지도 메인 화면 */}
      <LottoMap />
    </main>
  );
}