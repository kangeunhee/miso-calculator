import type { Metadata } from 'next';
import '.globals.css';

export const metadata Metadata = {
  title '전국 로또 명당 지도  1등 당첨 배출 판매점 모음',
  description '전국 로또 1등 당첨 횟수가 많은 최고의 명당 판매점 위치와 당첨 이력을 카카오 지도로 한눈에 확인하세요.',
  keywords ['로또명당', '로또1등', '로또판매점', '로또지도', '로또당첨지역'],
  openGraph {
    title '전국 로또 명당 지도',
    description '1등 당첨 배출 횟수 상위 로또 판매점 위치 안내',
    type 'website',
  },
};

export default function RootLayout({
  children,
} {
  children React.ReactNode;
}) {
  return (
    html lang=ko
      body className=antialiased m-0 p-0{children}body
    html
  );
}