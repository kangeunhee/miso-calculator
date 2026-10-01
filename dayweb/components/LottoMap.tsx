'use client';

import { useEffect, useRef } from 'react';
import { lottoStores } from '../data/lottoStores';

declare global {
  interface Window {
    kakao: any;
  }
}

export default function LottoMap() {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const kakaoKey = process.env.NEXT_PUBLIC_KAKAO_MAP_KEY;
    if (!kakaoKey) {
      console.error('카카오 맵 API 키가 설정되지 않았습니다.');
      return;
    }

    const script = document.createElement('script');
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${kakaoKey}&autoload=false`;
    script.async = true;
    document.head.appendChild(script);

    script.onload = () => {
      window.kakao.maps.load(() => {
        if (!mapRef.current) return;

        // 지도 기본 중심 좌표 (서울 시청 근처)
        const options = {
          center: new window.kakao.maps.LatLng(36.5, 127.8), // 대한민국 전체 시야
          level: 12,
        };

        const map = new window.kakao.maps.Map(mapRef.current, options);

        // 명당 마커 생성 및 이벤트 등록
        LOTTO_STORES.forEach((store: LottoStore) => {
          const markerPosition = new window.kakao.maps.LatLng(store.lat, store.lng);

          const marker = new window.kakao.maps.Marker({
            position: markerPosition,
            title: store.name,
          });

          marker.setMap(map);

          // 인포윈도우 (클릭 시 표시될 내용)
          const content = `
            <div style="padding:10px; font-size:12px; width:200px; color:#333;">
              <strong style="font-size:14px; color:#d97706;">🎯 ${store.name}</strong><br/>
              <span style="color:#ef4444; font-weight:bold;">1등 당첨: ${store.firstWinCount}회</span><br/>
              <span style="font-size:11px; color:#666;">${store.address}</span>
            </div>
          `;

          const infowindow = new window.kakao.maps.InfoWindow({
            content: content,
            removable: true,
          });

          window.kakao.maps.event.addListener(marker, 'click', () => {
            infowindow.open(map, marker);
          });
        });
      });
    };

    return () => {
      document.head.removeChild(script);
    };
  }, []);

  return (
    <div className="relative w-full h-screen">
      {/* 상단 헤더 & 정보 패널 */}
      <div className="absolute top-4 left-4 z-10 bg-white/90 backdrop-blur-md p-4 rounded-xl shadow-lg border border-gray-100 max-w-xs">
        <h1 className="text-xl font-extrabold text-gray-900 flex items-center gap-1.5">
          <span>🎯</span> 전국 로또 명당 지도
        </h1>
        <p className="text-xs text-gray-500 mt-1">
          1등 당첨 배출 횟수 상위 명당을 한눈에 확인하세요.
        </p>
      </div>

      {/* 지도 영역 */}
      <div ref={mapRef} className="w-full h-full" />
    </div>
  );
}