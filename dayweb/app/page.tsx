import LottoMap from '../components/LottoMap';
import Script from 'next/script';

export default function HomePage() {
  const adsenseClientId = process.env.NEXT_PUBLIC_ADSENSE_CLIENT_ID;

  return (
    <main className="w-full h-screen overflow-hidden relative">
      {/* 구글 애드센스 클라이언트 ID가 환경변수에 설정되어 있을 때만 스크립트 로드 */}
      {adsenseClientId && (
        <Script async crossOrigin="anonymous" src="{`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${adsenseClientId}`}" strategy="afterInteractive"/>
      )}

      {/* 로또 지도 메인 화면 */}
      <LottoMap/>
    </main>
  );
}
