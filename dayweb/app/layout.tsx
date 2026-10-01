import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '전국 로또 명당 지도 | 1등 당첨 배출 판매점 모음',
  description: '전국 로또 1등 당첨 횟수가 많은 최고의 명당 판매점 위치와 정보를 확인하세요.',
  keywords: ['로또명당', '로또1등', '로또판매점', '로또지도'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
